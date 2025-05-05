import React, { useEffect, useState } from "react";

const Members = () => {
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortBy, setSortBy] = useState("name");
  const [form, setForm] = useState({
    first_name: "",
    middle_name: "",
    last_name: "",
    email: "",
    phone: "",
    gender: "Other",
  });
  const [isEditing, setIsEditing] = useState(false);
  const [editingId, setEditingId] = useState(null);

  const API_BASE = "http://127.0.0.1:5000/members";

  useEffect(() => {
    fetchMembers();
  }, []);

  const fetchMembers = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/add`);
      const data = await response.json();
      setMembers(data);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  const getFullName = (member) =>
    `${member.first_name || ""} ${member.middle_name || ""} ${
      member.last_name || ""
    }`.trim();

  const filteredMembers = members.filter((member) =>
    getFullName(member).toLowerCase().includes(searchTerm.toLowerCase())
  );

  const sortedMembers = [...filteredMembers].sort((a, b) => {
    if (sortBy === "name") return getFullName(a).localeCompare(getFullName(b));
    if (sortBy === "email") return a.email.localeCompare(b.email);
    if (sortBy === "phone") return a.phone.localeCompare(b.phone);
    return 0;
  });

  const handleSearch = (e) => setSearchTerm(e.target.value);
  const handleSort = (e) => setSortBy(e.target.value);
  const handleInputChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleEdit = (member) => {
    setForm(member);
    setIsEditing(true);
    setEditingId(member.id);
  };

  const handleDelete = async (id) => {
    try {
      await fetch(`${API_BASE}/delete/${id}`, { method: "DELETE" });
      setMembers(members.filter((m) => m.id !== id));
    } catch (err) {
      alert("Failed to delete");
    }
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    const method = isEditing ? "PUT" : "POST";
    const url = isEditing
      ? `${API_BASE}/update/${editingId}`
      : `${API_BASE}/add`;

    try {
      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      if (!response.ok) {
        const data = await response.json();
        console.log("Error:", data);
        console.log("Response:", response);
        alert(data.error || "Validation error");
        return;
      }

      setForm({
        first_name: "",
        middle_name: "",
        last_name: "",
        email: "",
        phone: "",
        gender: "Other",
      });
      setIsEditing(false);
      setEditingId(null);
      fetchMembers();
    } catch (err) {
      alert("Failed to submit");
    }
  };

  return (
    <div>
      <h1>Library Members</h1>

      {/* Search & Sort */}
      <input
        type="text"
        placeholder="Search by name"
        value={searchTerm}
        onChange={handleSearch}
      />
      <select value={sortBy} onChange={handleSort}>
        <option value="name">Name</option>
        <option value="email">Email</option>
        <option value="phone">Phone</option>
      </select>

      {/* Member Form */}
      <h2>{isEditing ? "Edit Member" : "Add Member"}</h2>
      <form onSubmit={handleFormSubmit}>
        <input
          name="first_name"
          placeholder="First Name"
          value={form.first_name}
          onChange={handleInputChange}
          required
        />
        <input
          name="middle_name"
          placeholder="Middle Name"
          value={form.middle_name}
          onChange={handleInputChange}
        />
        <input
          name="last_name"
          placeholder="Last Name"
          value={form.last_name}
          onChange={handleInputChange}
        />
        <input
          name="email"
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={handleInputChange}
          required
        />
        <input
          name="phone"
          placeholder="Phone"
          value={form.phone}
          onChange={handleInputChange}
          required
        />
        <select name="gender" value={form.gender} onChange={handleInputChange}>
          <option>Male</option>
          <option>Female</option>
          <option>Other</option>
        </select>
        <button type="submit">{isEditing ? "Update" : "Add"} Member</button>
      </form>

      {/* List of Members */}
      <h2>Member List</h2>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>Error: {error.message}</p>
      ) : (
        <ul>
          {sortedMembers.map((member) => (
            <li key={member.id}>
              {getFullName(member)} - {member.email} - {member.phone}
              <button onClick={() => handleEdit(member)}>Edit</button>
              <button onClick={() => handleDelete(member.id)}>Delete</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Members;
