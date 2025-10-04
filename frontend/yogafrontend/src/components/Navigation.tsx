import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Navigation.css';

const Navigation: React.FC = () => {
  const location = useLocation();
  const { user, isAuthenticated, logout } = useAuth();

  const handleLogout = () => {
    logout();
  };

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
          
          {isAuthenticated ? (
            <>
              <span className="nav-user">
                Welcome, {user?.first_name}!
              </span>
              <button 
                onClick={handleLogout}
                className="nav-link nav-logout"
              >
                Logout
              </button>
            </>
          ) : (
            <>
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
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
