import { Link } from 'react-router-dom';

export default function OverviewPage() {
  return (
    <div className="landing-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            <span className="highlight">UNZA Congregation</span><br />
            Management System
          </h1>
          <p className="hero-subtitle">
            Connecting members, organizing committees, and managing church activities<br />
            for the New Apostolic Church UNZA Congregation
          </p>
          <div className="hero-buttons">
            <Link to="/register" className="btn btn-primary btn-large">
              Join the Congregation
            </Link>
            <Link to="/login" className="btn btn-secondary btn-large">
              Member Login
            </Link>
          </div>
        </div>
        <div className="hero-image">
          <img 
            src="/images/church-emblem.png" 
            alt="Church Emblem" 
            className="hero-emblem"
          />
        </div>
      </section>

      {/* What This System Does */}
      <section className="features-section">
        <h2 className="section-title">What This System Does</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">👥</div>
            <h3>Member Directory</h3>
            <p>Keep track of all congregation members, their contact details, spiritual milestones (baptism, sealing), and committee memberships.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📅</div>
            <h3>Events & Programs</h3>
            <p>View upcoming church services, youth programs, committee meetings, and special events. Register for events that require attendance tracking.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🎯</div>
            <h3>Committee Management</h3>
            <p>Nine active committees (Catering, Music, Organizing, Finance, DRAPO, Communication, Testify, Flowering, Secretarial) with role assignments and meeting schedules.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">✅</div>
            <h3>Attendance Records</h3>
            <p>Track attendance for Sunday services, midweek meetings, and special programs. Monitor member participation and engagement.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📢</div>
            <h3>Announcements</h3>
            <p>Stay updated with church announcements, event reminders, and important notifications sent directly to your account.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">💬</div>
            <h3>Community Fellowship</h3>
            <p>Share testimonies, submit prayer requests, post announcements, and engage with fellow members in a safe, church-focused space.</p>
          </div>
        </div>
      </section>

      {/* Who Can Use It */}
      <section className="cta-section">
        <h2>Who Can Use This System?</h2>
        <div style={{ maxWidth: '800px', margin: '0 auto 2rem', textAlign: 'center' }}>
          <p style={{ marginBottom: '1rem', fontSize: '1.1rem' }}>
            <strong>Members:</strong> View events, update your profile, join committees, and stay connected with the congregation.
          </p>
          <p style={{ marginBottom: '1rem', fontSize: '1.1rem' }}>
            <strong>Committee Leaders:</strong> Manage your committee members, schedule meetings, and coordinate activities.
          </p>
          <p style={{ marginBottom: '1rem', fontSize: '1.1rem' }}>
            <strong>Administrators:</strong> Oversee all church operations, manage user roles, generate reports, and maintain church records.
          </p>
        </div>
        <Link to="/register" className="btn btn-primary btn-large">
          Create Your Account
        </Link>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <p>&copy; 2026 UNZA CIMS - New Apostolic Church UNZA Congregation</p>
        <p style={{ marginTop: '0.5rem', fontSize: '0.9rem', opacity: 0.8 }}>
          Built for the University of Zambia Congregation
        </p>
      </footer>
    </div>
  );
}