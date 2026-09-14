import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Sidebar({ onLogout, isOpen = false, onNavigate = () => {} }) {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const role = user?.role || 'MEMBER';

  const handleLogout = async () => {
    try {
      await (onLogout || logout)?.();
    } finally {
      navigate('/login');
    }
  };

  const isActive = (path) => location.pathname === path || location.pathname.startsWith(`${path}/`);
  const linkClass = (path) => `sidebar-link${isActive(path) ? ' active' : ''}`;

  return (
    <aside className={`sidebar${isOpen ? ' sidebar-open' : ''}`}>
      <div className="sidebar-header">
        <img className="sidebar-logo" src="/images/church-emblem.png" alt="New Apostolic Church UNZA Congregation emblem" />
        <div className="sidebar-brand">
          <strong>UNZA Hub</strong>
          <span>Congregation Management</span>
        </div>
      </div>

      <div className="sidebar-term-chip">
        <span className="material-symbols-outlined">church</span>
        <div>
          <strong>Academic Term '24</strong>
          <span>Season: Ordinary Time</span>
        </div>
        <span className="sidebar-term-dot" />
      </div>

      <span className="sidebar-section-label">Main Navigation</span>

      <nav className="sidebar-nav">
        <Link to="/dashboard" className={linkClass('/dashboard')} onClick={onNavigate}>
          <div className="sidebar-link-inner"><span className="material-symbols-outlined">home</span><span className="sidebar-link-label">Dashboard</span></div>
        </Link>
        <Link to="/committees" className={linkClass('/committees')} onClick={onNavigate}>
          <div className="sidebar-link-inner"><span className="material-symbols-outlined">groups</span><span className="sidebar-link-label">Committees</span></div>
          <span className="sidebar-link-badge">9</span>
        </Link>
        <Link to="/events" className={linkClass('/events')} onClick={onNavigate}>
          <div className="sidebar-link-inner"><span className="material-symbols-outlined">calendar_month</span><span className="sidebar-link-label">Events &amp; Calendar</span></div>
          <span className="sidebar-link-badge badge-secondary">Upcoming</span>
        </Link>
        <Link to="/social" className={linkClass('/social')} onClick={onNavigate}>
          <div className="sidebar-link-inner"><span className="material-symbols-outlined">forum</span><span className="sidebar-link-label">Social Feed</span></div>
        </Link>
        <Link to="/announcements" className={linkClass('/announcements')} onClick={onNavigate}>
          <div className="sidebar-link-inner"><span className="material-symbols-outlined">notifications</span><span className="sidebar-link-label">Announcements</span></div>
          <span className="sidebar-link-badge badge-announcement">3 New</span>
        </Link>
        <Link to="/members" className={linkClass('/members')} onClick={onNavigate}>
          <div className="sidebar-link-inner"><span className="material-symbols-outlined">person_search</span><span className="sidebar-link-label">Member Directory</span></div>
        </Link>
        <Link to="/attendance" className={linkClass('/attendance')} onClick={onNavigate}>
          <div className="sidebar-link-inner"><span className="material-symbols-outlined">fact_check</span><span className="sidebar-link-label">Attendance</span></div>
        </Link>
        <Link to="/visitors" className={linkClass('/visitors')} onClick={onNavigate}>
          <div className="sidebar-link-inner"><span className="material-symbols-outlined">how_to_reg</span><span className="sidebar-link-label">Visitors</span></div>
        </Link>
        <Link to="/documents" className={linkClass('/documents')} onClick={onNavigate}>
          <div className="sidebar-link-inner"><span className="material-symbols-outlined">folder</span><span className="sidebar-link-label">Documents</span></div>
        </Link>

        <div className="sidebar-divider" />

        {(role === 'SUPER_USER' || role === 'ADMIN_USER') && <Link to="/reports" className={linkClass('/reports')} onClick={onNavigate}>
          <div className="sidebar-link-inner"><span className="material-symbols-outlined">bar_chart</span><span className="sidebar-link-label">Reports</span></div>
        </Link>}
        {role === 'SUPER_USER' && <Link to="/audit" className={linkClass('/audit')} onClick={onNavigate}>
          <div className="sidebar-link-inner"><span className="material-symbols-outlined">admin_panel_settings</span><span className="sidebar-link-label">Audit</span></div>
          <span className="sidebar-link-badge badge-admin">Admin</span>
        </Link>}
        <Link to="/profile" className={linkClass('/profile')} onClick={onNavigate}>
          <div className="sidebar-link-inner"><span className="material-symbols-outlined">account_circle</span><span className="sidebar-link-label">My Profile</span></div>
        </Link>
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-footer-block">
          <span className="material-symbols-outlined">location_on</span>
          <div><strong>UNZA Main Campus</strong><span>Great East Road, Lusaka</span></div>
        </div>
        <div className="sidebar-footer-row">
          <Link to="/settings" className="sidebar-footer-link" onClick={onNavigate}><span className="material-symbols-outlined">help</span> Help &amp; Support</Link>
          <button type="button" className="sidebar-footer-link danger" onClick={handleLogout}><span className="material-symbols-outlined">logout</span> Log Out</button>
        </div>
      </div>
    </aside>
  );
}