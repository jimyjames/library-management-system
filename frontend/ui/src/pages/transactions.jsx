import React, { useEffect, useState } from "react";

const Transactions = () => {
  const [transactions, setTransactions] = useState([]);
  const [members, setMembers] = useState([]);
  const [books, setBooks] = useState([]);
  const [formData, setFormData] = useState({
    member_id: "",
    book_id: "",
    expected_at: "",
  });
  const [editId, setEditId] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchTransactions = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/lending/add");
      const data = await res.json();
      setTransactions(data);
    } catch (err) {
      console.error("Failed to fetch transactions", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchBooksAndMembers = async () => {
    try {
      const [booksRes, membersRes] = await Promise.all([
        fetch("http://127.0.0.1:5000/books/add"),
        fetch("http://127.0.0.1:5000/members/add"),
      ]);
      const booksData = await booksRes.json();
      const membersData = await membersRes.json();
      setBooks(booksData);
      setMembers(membersData);
    } catch (err) {
      console.error("Failed to fetch books or members", err);
    }
  };

  useEffect(() => {
    fetchTransactions();
    fetchBooksAndMembers();
  }, []);

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const url = editId
      ? `http://localhost:5000/lending/${editId}`
      : `http://localhost:5000/lending/add`;
    const method = editId ? "PUT" : "POST";

    try {
      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const result = await res.json();
      if (!res.ok) {
        alert("Error: " + (result.error || JSON.stringify(result)));
      } else {
        fetchTransactions();
        setFormData({ member_id: "", book_id: "", expected_at: "" });
        setEditId(null);
      }
    } catch (err) {
      console.error("Error submitting form", err);
    }
  };

  const handleEdit = (txn) => {
    setFormData({
      member_id: txn.member_id,
      book_id: txn.book_id,
      expected_at: txn.expected_at?.split("T")[0] || "",
    });
    setEditId(txn.id);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this transaction?"))
      return;
    try {
      await fetch(`http://localhost:5000/lending/${id}`, { method: "DELETE" });
      fetchTransactions();
    } catch (err) {
      console.error("Delete error:", err);
    }
  };

  const getMemberName = (id) => {
    const member = members.find((m) => m.id === id);
    return member
      ? `${member.first_name} ${member.middle_name || ""} ${
          member.last_name
        }`.trim()
      : id;
  };

  const getBookTitle = (id) => {
    const book = books.find((b) => b.id === id);
    return book ? book.title : id;
  };

  return (
    <div>
      <h1>Transactions</h1>
      <form onSubmit={handleSubmit}>
        <select
          name="member_id"
          value={formData.member_id}
          onChange={handleChange}
          required
        >
          <option value="">Select Member</option>
          {members.map((member) => (
            <option key={member.id} value={member.id}>
              {`${member.first_name} ${member.middle_name || ""} ${
                member.last_name
              }`}
            </option>
          ))}
        </select>

        <select
          name="book_id"
          value={formData.book_id}
          onChange={handleChange}
          required
        >
          <option value="">Select Book</option>
          {books.map((book) => (
            <option key={book.id} value={book.id}>
              {book.title}
            </option>
          ))}
        </select>

        <input
          type="date"
          name="expected_at"
          value={formData.expected_at}
          onChange={handleChange}
          required
        />
        <button type="submit">{editId ? "Update" : "Add"} Transaction</button>
      </form>

      <h2>All Lending Records</h2>
      {loading ? (
        <p>Loading transactions...</p>
      ) : (
        <table border="1">
          <thead>
            <tr>
              <th>ID</th>
              <th>Member</th>
              <th>Book</th>
              <th>Issued At</th>
              <th>Expected At</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((txn) => (
              <tr key={txn.id}>
                <td>{txn.id}</td>
                <td>{getMemberName(txn.member_id)}</td>
                <td>{getBookTitle(txn.book_id)}</td>
                <td>{new Date(txn.issued_at).toLocaleDateString()}</td>
                <td>{new Date(txn.expected_at).toLocaleDateString()}</td>
                <td>{txn.status}</td>

                <td>
                  <button onClick={() => handleEdit(txn)}>Edit</button>
                  <button onClick={() => handleDelete(txn.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default Transactions;
