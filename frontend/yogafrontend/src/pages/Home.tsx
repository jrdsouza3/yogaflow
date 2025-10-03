import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home: React.FC = () => {
  return (
    <div className="home">
      <section className="hero">
        <div className="hero-content">
          <h1 className="hero-title">
            Find Your Flow
            <span className="hero-subtitle">with YogaFlow</span>
          </h1>
          <p className="hero-description">
            Create personalized yoga sequences, track your practice, and discover your inner peace. 
            Whether you're a beginner or an experienced yogi, YogaFlow adapts to your journey.
          </p>
          <div className="hero-buttons">
            <Link to="/flow-generator" className="btn btn-primary">
              Start Your Flow
            </Link>
            <Link to="/signup" className="btn btn-secondary">
              Join Our Community
            </Link>
          </div>
        </div>
        <div className="hero-image">
          <div className="yoga-illustration">🧘‍♀️</div>
        </div>
      </section>

      <section className="features">
        <div className="container">
          <h2 className="section-title">Why Choose YogaFlow?</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🎯</div>
              <h3>Custom Routines</h3>
              <p>Create personalized yoga sequences tailored to your goals, experience level, and available time.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">⏰</div>
              <h3>Session Timer</h3>
              <p>Built-in timer for timed practices and meditation sessions to enhance your mindfulness journey.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📱</div>
              <h3>Responsive Design</h3>
              <p>Seamless experience across all devices - practice anywhere, anytime.</p>
            </div>
          </div>
        </div>
      </section>

      <section className="cta">
        <div className="container">
          <div className="cta-content">
            <h2>Ready to Begin Your Journey?</h2>
            <p>Join thousands of yogis who have transformed their practice with YogaFlow.</p>
            <Link to="/signup" className="btn btn-primary btn-large">
              Get Started Today
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
