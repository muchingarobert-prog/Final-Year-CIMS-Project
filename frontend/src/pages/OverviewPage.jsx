import { Link } from 'react-router-dom';

const featureCards = [
  {
    icon: 'groups',
    title: 'Members and roles',
    text: 'Keep member records organized, connected to committees, and easy for congregation leaders to manage.',
  },
  {
    icon: 'event',
    title: 'Events and attendance',
    text: 'Track church services, youth programs, and scheduled activities while monitoring participation efficiently.',
  },
  {
    icon: 'campaign',
    title: 'Announcements',
    text: 'Share updates and important congregation notices in one accessible communication channel.',
  },
  {
    icon: 'folder',
    title: 'Documents',
    text: 'Store and retrieve church documents, reports, and reference materials in a single workspace.',
  },
  {
    icon: 'account_balance',
    title: 'Finance overview',
    text: 'Monitor contributions, routine records, and operational information with clearer reporting structure.',
  },
  {
    icon: 'insights',
    title: 'Operational insight',
    text: 'Use the dashboard to keep an accurate view of active congregation activities, communications, and planning.',
  },
];

export default function OverviewPage() {
  return (
    <div className="landing-page">
      <header className="landing-header">
        <Link to="/" className="brand-lockup" aria-label="UNZA Congregation home">
          <img src="/images/church-emblem.png" alt="Church emblem" className="brand-crest" />
          <div className="brand-copy">
            <strong>New Apostolic Church</strong>
            <span>UNZA Congregation</span>
          </div>
        </Link>

        <nav className="landing-nav" aria-label="Main navigation">
          <Link to="/login" className="nav-chip">Member Login</Link>
          <Link to="/register" className="nav-chip nav-chip-primary">Register</Link>
        </nav>
      </header>

      <main>
        <section className="hero-section" id="overview">
          <div className="hero-content">
            <span className="eyebrow">Congregation information portal</span>
            <h1 className="hero-title">
              Professional church administration for <span className="highlight">UNZA</span>
            </h1>
            <p className="hero-subtitle">
              Keep the congregation connected through streamlined member records, event planning, committee coordination, and transparent communication.
            </p>

            <div className="hero-buttons">
              <Link to="/register" className="btn btn-primary btn-large">
                Create account
              </Link>
              <Link to="/login" className="btn btn-secondary btn-large">
                Member Login
              </Link>
            </div>

            <ul className="hero-points" aria-label="Key system benefits">
              <li><span className="material-symbols-outlined" aria-hidden="true">check_circle</span> Member and committee coordination</li>
              <li><span className="material-symbols-outlined" aria-hidden="true">check_circle</span> Real-time congregation updates</li>
              <li><span className="material-symbols-outlined" aria-hidden="true">check_circle</span> Secure access for leaders and members</li>
            </ul>
          </div>

          <div className="hero-visual" aria-label="Church administrative overview">
            <div className="hero-card hero-card-primary">
              <div className="hero-card-row">
                <span className="material-symbols-outlined" aria-hidden="true">church</span>
                <span>Institutional overview</span>
              </div>
              <h2>UNZA Congregation</h2>
              <p>Connecting people, planning activities, and maintaining a clear operational record.</p>
            </div>

            <div className="hero-mini-grid">
              <div className="mini-stat">
                <span className="material-symbols-outlined" aria-hidden="true">groups</span>
                <div>
                  <strong>Members</strong>
                  <small>Directory</small>
                </div>
              </div>
              <div className="mini-stat">
                <span className="material-symbols-outlined" aria-hidden="true">event_available</span>
                <div>
                  <strong>Events</strong>
                  <small>Scheduled</small>
                </div>
              </div>
              <div className="mini-stat">
                <span className="material-symbols-outlined" aria-hidden="true">notifications_active</span>
                <div>
                  <strong>Updates</strong>
                  <small>Announcements</small>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="features-section" aria-labelledby="platform-features-title">
          <div className="section-heading">
            <span className="eyebrow">Platform capabilities</span>
            <h2 id="platform-features-title">A cohesive system for church operations.</h2>
          </div>

          <div className="features-grid">
            {featureCards.map((feature) => (
              <article className="feature-card" key={feature.title}>
                <span className="feature-icon material-symbols-outlined" aria-hidden="true">{feature.icon}</span>
                <h3>{feature.title}</h3>
                <p>{feature.text}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="cta-section" aria-labelledby="member-access-title">
          <div className="cta-panel">
            <span className="eyebrow gold">Who this serves</span>
            <h2 id="member-access-title">Built for members, leaders, and administrators.</h2>
            <p>
              The system supports informed congregation management, clear communication, and secure access to the information people need most.
            </p>
            <div className="hero-buttons cta-buttons">
              <Link to="/login" className="btn btn-primary btn-large">Sign in</Link>
              <Link to="/register" className="btn btn-secondary btn-large">Create account</Link>
            </div>
          </div>
        </section>
      </main>

      <footer className="landing-footer">
        <p>© 2026 New Apostolic Church — UNZA Congregation</p>
      </footer>
    </div>
  );
}