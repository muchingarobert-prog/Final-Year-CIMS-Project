import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Topbar from './Topbar';

export default function AppShell({ children, onLogout }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="app-container">
      <Sidebar onLogout={onLogout} isOpen={sidebarOpen} onNavigate={() => setSidebarOpen(false)} />
      {sidebarOpen && <button type="button" className="sidebar-overlay" onClick={() => setSidebarOpen(false)} aria-label="Close navigation menu" />}
      <div className="main-area">
        <Topbar onMenuClick={() => setSidebarOpen(true)} />
        <main className="content-area">{children || <Outlet />}</main>
      </div>
    </div>
  );
}
