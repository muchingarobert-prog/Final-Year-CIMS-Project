import { useState } from 'react';
import { BrowserRouter as Router, Navigate, Route, Routes } from 'react-router-dom';
import './App.css';
import Sidebar from './components/Sidebar';
import OverviewPage from './pages/OverviewPage.jsx';
import LoginPage from './pages/LoginPage.jsx';
import RegisterPage from './pages/RegisterPage.jsx';
import DashboardPage from './pages/DashboardPage.jsx';
import CommitteesPage from './pages/CommitteesPage.jsx';
import EventsPage from './pages/EventsPage.jsx';
import MembersPage from './pages/MembersPage.jsx';
import AnnouncementsPage from './pages/AnnouncementsPage.jsx';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(() => Boolean(localStorage.getItem('cims_access_token')));

  return (
    <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <div className="app-container">
        {isLoggedIn ? (
          <>
            <Sidebar onLogout={() => setIsLoggedIn(false)} />
            <div className="main-area">
              <main className="content-area">
                <Routes>
                  <Route path="/dashboard" element={<DashboardPage />} />
                  <Route path="/events" element={<EventsPage />} />
                  <Route path="/committees" element={<CommitteesPage />} />
                  <Route path="/members" element={<MembersPage />} />
                  <Route path="/announcements" element={<AnnouncementsPage />} />
                  <Route path="*" element={<Navigate to="/dashboard" replace />} />
                </Routes>
              </main>
            </div>
          </>
        ) : (
          <div className="public-area">
            <Routes>
              <Route path="/" element={<OverviewPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </div>
        )}
      </div>
    </Router>
  );
}

export default App;