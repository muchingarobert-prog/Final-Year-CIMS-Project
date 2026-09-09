import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { hasAnyRole } from '../utils/permissions';
import Loading from './Loading';

export default function RoleRoute({ children, allow = [] }) {
  const { user, isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) return <Loading message="Checking access..." />;
  if (!isAuthenticated) return <Navigate to="/login" replace state={{ from: `${location.pathname}${location.search}` }} />;
  if (!hasAnyRole(user?.role, allow)) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}
