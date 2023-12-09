import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Login.jsx'; // Adjust the path as necessary

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        {/* Add other routes as needed */}
      </Routes>
    </Router>
  );
}

export default App;
