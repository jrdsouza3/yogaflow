import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Navigation from './components/Navigation';
import Home from './pages/Home';
import Login from './pages/Login';
import SignUp from './pages/SignUp';
import FlowGenerator from './pages/FlowGenerator';
import StepThrough from './pages/StepThrough';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Navigation />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/flow-generator" element={<FlowGenerator />} />
            <Route path="/step-through" element={<StepThrough />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
