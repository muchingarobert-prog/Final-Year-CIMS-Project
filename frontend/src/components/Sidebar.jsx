import { Link, useLocation } from 'react-router-dom';

export default function Sidebar() {
  const location = useLocation();

  const menuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/events', label: 'Events', icon: '' },
    { path: '/committees', label: 'Committees', icon: '' },
    { path: '/members', label: 'Members', icon: '👥' },
    { path: '/attendance', label: 'Attendance', icon: '✅' },
    { path: '/announcements', label: 'Announcements', icon: '📢' },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <img src="/images/church-emblem.png" alt="UNZA CIMS" className="sidebar-logo" />
        <h2>UNZA CIMS</h2>
      </div>
      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`sidebar-link ${location.pathname === item.path ? 'active' : ''}`}
          >
            <span className="sidebar-icon">{item.icon}</span>
            <span className="sidebar-text">{item.label}</span>
          </Link>
        ))}
      </nav>
    </aside>
  );
}