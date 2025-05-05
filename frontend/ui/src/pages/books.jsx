import React, { useEffect, useState } from "react";

const Books = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortBy, setSortBy] = useState("title");
  const [newBook, setNewBook] = useState({
    title: "",
    author: "",
    quantity: 0,
    available: 0,
  });
  const [editMode, setEditMode] = useState(null);

  const fetchBooks = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/books/add");
      if (!response.ok) throw new Error("Network response was not ok");
      const data = await response.json();
      setBooks(data);
    } catch (error) {
      setError(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBooks();
  }, []);

  const handleInputChange = (e) => {
    setNewBook({ ...newBook, [e.target.name]: e.target.value });
  };

  const handleAddBook = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/books/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newBook),
      });
      if (response.ok) {
        setNewBook({ title: "", author: "", quantity: 0, available: 0 });
        fetchBooks();
      }
    } catch (error) {
      console.error("Add book failed", error);
    }
  };

  const handleDelete = async (id) => {
    await fetch(`http://127.0.0.1:5000/books/delete/${id}`, {
      method: "DELETE",
    });
    fetchBooks();
  };

  const handleEdit = (book) => {
    setEditMode(book.id);
    setNewBook({ ...book });
  };

  const handleUpdateBook = async () => {
    await fetch(`http://127.0.0.1:5000/books/update/${editMode}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newBook),
    });
    console.log("body", JSON.stringify(newBook));
    setEditMode(null);
    setNewBook({ title: "", author: "", quantity: 0, available: 0 });
    fetchBooks();
  };

  const filteredBooks = books.filter(
    (book) =>
      book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      book.author.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const sortedBooks = [...filteredBooks].sort((a, b) => {
    if (sortBy === "title") return a.title.localeCompare(b.title);
    if (sortBy === "author") return a.author.localeCompare(b.author);
    return 0;
  });

  return (
    <div>
      <h1>Books</h1>

      <input
        type="text"
        placeholder="Search by title"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
        <option value="title">Title</option>
        <option value="author">Author</option>
      </select>

      <h2>{editMode ? "Edit Book" : "Add Book"}</h2>
      <input
        name="title"
        placeholder="Title"
        value={newBook.title}
        onChange={handleInputChange}
      />
      <input
        name="author"
        placeholder="Author"
        value={newBook.author}
        onChange={handleInputChange}
      />
      <input
        name="quantity"
        placeholder="Quantity"
        type="number"
        value={newBook.quantity}
        onChange={handleInputChange}
      />
      <input
        name="available"
        placeholder="Available"
        type="number"
        value={newBook.available}
        onChange={handleInputChange}
      />
      <button onClick={editMode ? handleUpdateBook : handleAddBook}>
        {editMode ? "Update Book" : "Add Book"}
      </button>

      {loading && <p>Loading...</p>}
      {error && <p>Error: {error.message}</p>}

      {sortedBooks.map((book) => (
        <div
          key={book.id}
          style={{
            border: "1px solid #ccc",
            padding: "10px",
            margin: "10px 0",
          }}
        >
          <h3>{book.title}</h3>
          <p>Author: {book.author}</p>
          <p>Quantity: {book.quantity}</p>
          <p>Available: {book.available}</p>
          <button onClick={() => handleEdit(book)}>Edit</button>
          <button onClick={() => handleDelete(book.id)}>Delete</button>
        </div>
      ))}
    </div>
  );
};

export default Books;
