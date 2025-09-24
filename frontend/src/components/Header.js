import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Header.css';

const Header = () => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <header className="header">
      <div className="header-container">
        <div className="header-brand">
          <h1>Data Ingestion System</h1>
        </div>
        <nav className="header-nav">
          <Link 
            to="/" 
            className={`nav-link ${isActive('/') ? 'active' : ''}`}
          >
            Dashboard
          </Link>
          <Link 
            to="/ingest" 
            className={`nav-link ${isActive('/ingest') ? 'active' : ''}`}
          >
            Ingest Data
          </Link>
          <Link 
            to="/view" 
            className={`nav-link ${isActive('/view') ? 'active' : ''}`}
          >
            View Data
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;
