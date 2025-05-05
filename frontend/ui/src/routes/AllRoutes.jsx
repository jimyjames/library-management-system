import React from "react";
import { Route, Routes } from "react-router-dom";
import Books from "../pages/books.jsx";
import Members from "../pages/members.jsx";
import Transactions from "../pages/transactions.jsx";

const AllRoutes = () => {
  return (
    <Routes>
      <Route path="/books" element={<Books />} />
      <Route path="/members" element={<Members />} />
      <Route path="/transactions" element={<Transactions />} />
    </Routes>
  );
};

export default AllRoutes;
