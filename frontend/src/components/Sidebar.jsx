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

  const primaryLinks = [
    ['dashboard', 'Dashboard', '/dashboard'],
    ['groups', 'Committees', '/committees'],
    ['event', 'Events', '/events'],
    ['person_search', 'Members', '/members'],
    ['how_to_reg', 'Visitors', '/visitors'],
    ['fact_check', 'Attendance', '/attendance'],
  ];
  const communicationLinks = [
    ['campaign', 'Announcements', '/announcements'],
    ['forum', 'Community', '/social'],
    ['folder', 'Documents', '/documents'],
    ['payments', 'Finance', '/finances'],
  ];

  const renderLink = ([icon, label, path]) => (
    <Link key={path} to={path} className={linkClass(path)} onClick={onNavigate}>
      <span className="material-symbols-outlined sidebar-link-icon" aria-hidden="true">{icon}</span>
      <span className="sidebar-link-label">{label}</span>
    </Link>
  );

  return (
    <aside className={`sidebar${isOpen ? ' sidebar-open' : ''}`}>
      <div className="sidebar-header">
        <img className="sidebar-logo" src="/images/church-emblem.png" alt="New Apostolic Church UNZA Congregation emblem" />
        <div className="sidebar-brand">
          <strong>New Apostolic Church</strong>
          <span>UNZA</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        <span className="sidebar-section-label">Workspace</span>
        {primaryLinks.map(renderLink)}
        <span className="sidebar-section-label">Communication</span>
        {communicationLinks.map(renderLink)}

        {(role === 'SUPER_USER' || role === 'ADMIN_USER') && <Link to="/reports" className={linkClass('/reports')} onClick={onNavigate}>
          <span className="material-symbols-outlined sidebar-link-icon" aria-hidden="true">bar_chart</span><span className="sidebar-link-label">Reports</span>
        </Link>}
        <Link to="/profile" className={linkClass('/profile')} onClick={onNavigate}>
          <span className="material-symbols-outlined sidebar-link-icon" aria-hidden="true">account_circle</span><span className="sidebar-link-label">My Profile</span>
        </Link>
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-footer-block">
          <span className="material-symbols-outlined" aria-hidden="true">location_on</span>
          <div><strong>UNZA Main Campus</strong><span>Great East Road, Lusaka</span></div>
        </div>
        <button type="button" className="sidebar-footer-link danger" onClick={handleLogout}><span className="material-symbols-outlined" aria-hidden="true">logout</span> Log out</button>
      </div>
    </aside>
  );
}