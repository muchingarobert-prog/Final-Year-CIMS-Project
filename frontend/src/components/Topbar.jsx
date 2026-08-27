import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const pageNames = {
  '/dashboard': 'Dashboard',
  '/members': 'Members',
  '/committees': 'Committees',
  '/events': 'Events',
  '/attendance': 'Attendance',
  '/announcements': 'Announcements',
  '/notifications': 'Notifications',
  '/documents': 'Documents',
  '/visitors': 'Visitors',
  '/finances': 'Finance',
  '/reports': 'Reports',
  '/social': 'Community',
  '/profile': 'My Profile',
};

function getInitials(user) {
  const name = `${user?.first_name || ''}${user?.last_name || ''}`.trim();
  return name ? name.split(/\s+/).map((part) => part[0]).join('').slice(0, 2).toUpperCase() : 'U';
}

function formatRole(role) {
  return role ? role.replaceAll('_', ' ').toLowerCase().replace(/\b\w/g, (letter) => letter.toUpperCase()) : 'Member';
}

export default function Topbar({ onMenuClick }) {
  const location = useLocation();
  const { user } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const pageName = pageNames[location.pathname] || 'Workspace';

  return (
    <header className="topbar">
      <div className="topbar-leading">
        <button type="button" className="icon-button mobile-menu-button" onClick={onMenuClick} aria-label="Open navigation menu">
          <span aria-hidden="true">☰</span>
        </button>
        <div className="page-context">
          <span className="breadcrumb">UNZA / Workspace</span>
          <h1>{pageName}</h1>
        </div>
      </div>
      <div className="topbar-actions">
        <Link to="/notifications" className="icon-button notification-button" aria-label="Open notifications">
          <span aria-hidden="true">♢</span>
        </Link>
        <div className="profile-menu-wrapper">
          <button type="button" className="profile-trigger" onClick={() => setMenuOpen((open) => !open)} aria-expanded={menuOpen} aria-haspopup="menu">
            <span className="avatar" aria-hidden="true">{getInitials(user)}</span>
            <span className="profile-summary"><strong>{user?.first_name || user?.username || 'Member'}</strong><small>{formatRole(user?.role)}</small></span>
            <span className="profile-chevron" aria-hidden="true">⌄</span>
          </button>
          {menuOpen && <div className="profile-menu" role="menu"><Link to="/profile" role="menuitem" onClick={() => setMenuOpen(false)}>View profile</Link><Link to="/notifications" role="menuitem" onClick={() => setMenuOpen(false)}>Notifications</Link></div>}
        </div>
      </div>
    </header>
  );
}
