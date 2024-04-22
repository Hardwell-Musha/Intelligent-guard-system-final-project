import React from 'react';
import { createRoot } from 'react-dom/client'; // Import createRoot from react-dom/client
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './login';
import Register from './Register';
import App from './App'; // Assuming App.js contains your main application component

const root = createRoot(document.getElementById('root')); // Create a root using createRoot

root.render(
  <Router>
    <Routes>
      <Route path="/login" element={<Login />} /> {/* Route for Login component */}
      <Route path="/register" element={<Register />} /> {/* Route for Register component */}
      <Route path="/" element={<App />} /> {/* Main route for App component (dashboard) */}
    </Routes>
  </Router>
);
