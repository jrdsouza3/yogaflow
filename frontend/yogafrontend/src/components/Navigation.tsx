import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navigation.css';

const Navigation: React.FC = () => {
  const location = useLocation();

  return (
    <nav className="navigation">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          🧘‍♀️ YogaFlow
        </Link>
        
        <div className="nav-menu">
          <Link 
            to="/" 
            className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
          >
            Home
          </Link>
          <Link 
            to="/flow-generator" 
            className={`nav-link ${location.pathname === '/flow-generator' ? 'active' : ''}`}
          >
            Flow Generator
          </Link>
          <Link 
            to="/login" 
            className={`nav-link ${location.pathname === '/login' ? 'active' : ''}`}
          >
            Login
          </Link>
          <Link 
            to="/signup" 
            className={`nav-link ${location.pathname === '/signup' ? 'active' : ''}`}
          >
            Sign Up
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
