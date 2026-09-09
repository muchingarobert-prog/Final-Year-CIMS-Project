import { BrowserRouter as Router, Navigate, Route, Routes } from 'react-router-dom';
import './App.css';
import AppShell from './components/AppShell';
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
import ProtectedRoute from './components/ProtectedRoute';
import RoleRoute from './components/RoleRoute';

const adminRoles = ['SUPER_USER', 'ADMIN_USER'];
const highPrivilegeRoles = ['SUPER_USER', 'ADMIN_USER', 'HIGH_PRIVILEGE_USER'];

function AuthenticatedApp() {
  const { logout, isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <Loading message="Restoring your session..." />;
  }

  return (
    <div className={isAuthenticated ? undefined : 'public-area'}>
      <Routes>
        <Route path="/" element={<OverviewPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/dashboard" element={<ProtectedRoute><AppShell onLogout={logout}><DashboardPage /></AppShell></ProtectedRoute>} />
        <Route path="/events" element={<ProtectedRoute><AppShell onLogout={logout}><EventsPage /></AppShell></ProtectedRoute>} />
        <Route path="/committees" element={<ProtectedRoute><AppShell onLogout={logout}><CommitteesPage /></AppShell></ProtectedRoute>} />
        <Route path="/members" element={<ProtectedRoute><AppShell onLogout={logout}><MembersPage /></AppShell></ProtectedRoute>} />
        <Route path="/announcements" element={<ProtectedRoute><AppShell onLogout={logout}><AnnouncementsPage /></AppShell></ProtectedRoute>} />
        <Route path="/attendance" element={<ProtectedRoute><AppShell onLogout={logout}><AttendancePage /></AppShell></ProtectedRoute>} />
        <Route path="/notifications" element={<ProtectedRoute><AppShell onLogout={logout}><NotificationsPage /></AppShell></ProtectedRoute>} />
        <Route path="/documents" element={<ProtectedRoute><AppShell onLogout={logout}><DocumentsPage /></AppShell></ProtectedRoute>} />
        <Route path="/finances" element={<ProtectedRoute><AppShell onLogout={logout}><FinancesPage /></AppShell></ProtectedRoute>} />
        <Route path="/social" element={<ProtectedRoute><AppShell onLogout={logout}><SocialPage /></AppShell></ProtectedRoute>} />
        <Route path="/profile" element={<ProtectedRoute><AppShell onLogout={logout}><ProfilePage /></AppShell></ProtectedRoute>} />
        <Route path="/visitors" element={<RoleRoute allow={highPrivilegeRoles}><AppShell onLogout={logout}><VisitorsPage /></AppShell></RoleRoute>} />
        <Route path="/reports" element={<RoleRoute allow={adminRoles}><AppShell onLogout={logout}><ReportsPage /></AppShell></RoleRoute>} />
        <Route path="*" element={<Navigate to={isAuthenticated ? '/dashboard' : '/'} replace />} />
      </Routes>
    </div>
  );
}

function App() {
  return (
    <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <AuthProvider>
        <AuthenticatedApp />
      </AuthProvider>
    </Router>
  );
}

export default App;