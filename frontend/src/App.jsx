import { BrowserRouter as Router, Navigate, Route, Routes } from 'react-router-dom';
import './App.css';
import Sidebar from './components/Sidebar';
import Loading from './components/Loading';
import { AuthProvider, useAuth } from './context/AuthContext';
import OverviewPage from './pages/OverviewPage.jsx';
import LoginPage from './pages/LoginPage.jsx';
import RegisterPage from './pages/RegisterPage.jsx';
import DashboardPage from './pages/DashboardPage.jsx';
import CommitteesPage from './pages/CommitteesPage.jsx';
import EventsPage from './pages/EventsPage.jsx';
import MembersPage from './pages/MembersPage.jsx';
import AnnouncementsPage from './pages/AnnouncementsPage.jsx';
import ProfilePage from './pages/ProfilePage.jsx';
import AttendancePage from './pages/AttendancePage.jsx';
import NotificationsPage from './pages/NotificationsPage.jsx';
import DocumentsPage from './pages/DocumentsPage.jsx';
import VisitorsPage from './pages/VisitorsPage.jsx';
import FinancesPage from './pages/FinancesPage.jsx';
import ReportsPage from './pages/ReportsPage.jsx';
import SocialPage from './pages/SocialPage.jsx';

function AppShell() {
  const { logout, isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <Loading message="Restoring your session..." />;
  }

  if (!isAuthenticated) {
    return (
      <div className="public-area">
        <Routes>
          <Route path="/" element={<OverviewPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    );
  }

  return (
    <div className="app-container">
      <Sidebar onLogout={logout} />
      <div className="main-area">
        <main className="content-area">
          <Routes>
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/events" element={<EventsPage />} />
            <Route path="/committees" element={<CommitteesPage />} />
            <Route path="/members" element={<MembersPage />} />
            <Route path="/announcements" element={<AnnouncementsPage />} />
            <Route path="/attendance" element={<AttendancePage />} />
            <Route path="/notifications" element={<NotificationsPage />} />
            <Route path="/documents" element={<DocumentsPage />} />
            <Route path="/visitors" element={<VisitorsPage />} />
            <Route path="/finances" element={<FinancesPage />} />
            <Route path="/reports" element={<ReportsPage />} />
            <Route path="/social" element={<SocialPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <AuthProvider>
        <AppShell />
      </AuthProvider>
    </Router>
  );
}

export default App;