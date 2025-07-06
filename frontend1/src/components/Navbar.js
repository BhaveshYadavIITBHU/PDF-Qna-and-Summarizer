import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          📚 PDF Summarizer & Q&A
        </Link>
      </div>
    </nav>
  );
}

export default Navbar; 