import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { apiRequest, clearStoredTokens, getStoredTokens, refreshAccessToken } from '../api/client';
import { getCurrentUser, login as loginRequest, logout as logoutRequest } from '../api/auth';

const AuthContext = createContext(null);
const SESSION_EXPIRED_EVENT = 'cims:session-expired';
const TOKENS_REFRESHED_EVENT = 'cims:tokens-refreshed';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [accessToken, setAccessToken] = useState(() => localStorage.getItem('cims_access_token'));
  const [refreshToken, setRefreshToken] = useState(() => localStorage.getItem('cims_refresh_token'));
  const [isLoading, setIsLoading] = useState(true);
  const [authError, setAuthError] = useState('');

  const clearSession = () => {
    clearStoredTokens();
    setAccessToken(null);
    setRefreshToken(null);
    setUser(null);
    setAuthError('');
  };

  const resolveUser = async (token = accessToken) => {
    if (!token) {
      setUser(null);
      return null;
    }

    const profile = await apiRequest('/api/auth/profile/');
    setUser(profile);
    return profile;
  };

  const refreshSession = async () => {
    const stored = getStoredTokens();

    if (!stored.refreshToken) {
      clearSession();
      return null;
    }

    const nextAccess = await refreshAccessToken(stored.refreshToken);
    setAccessToken(nextAccess);
    const nextTokens = getStoredTokens();
    setRefreshToken(nextTokens.refreshToken);
    return resolveUser(nextAccess);
  };

  useEffect(() => {
    const handleSessionExpired = () => {
      clearSession();
      setAuthError('Your session expired. Please log in again.');
    };
    const handleTokensRefreshed = () => {
      const stored = getStoredTokens();
      setAccessToken(stored.accessToken);
      setRefreshToken(stored.refreshToken);
    };

    window.addEventListener(SESSION_EXPIRED_EVENT, handleSessionExpired);
    window.addEventListener(TOKENS_REFRESHED_EVENT, handleTokensRefreshed);

    const restoreSession = async () => {
      setIsLoading(true);
      const stored = getStoredTokens();

      try {
        if (stored.accessToken) {
          setAccessToken(stored.accessToken);
          setRefreshToken(stored.refreshToken);
          await resolveUser(stored.accessToken);
        } else if (stored.refreshToken) {
          await refreshSession();
        } else {
          clearSession();
        }
      } catch (error) {
        if (error.status === 0 || error.status === 429 || error.status >= 500) {
          setAuthError(error.message || 'Unable to restore your session. Check your connection and try again.');
        } else {
          clearSession();
          setAuthError('Your session expired. Please log in again.');
        }
      } finally {
        setIsLoading(false);
      }
    };

    restoreSession();

    return () => {
      window.removeEventListener(SESSION_EXPIRED_EVENT, handleSessionExpired);
      window.removeEventListener(TOKENS_REFRESHED_EVENT, handleTokensRefreshed);
    };
  }, []);

  const login = async (credentials) => {
    setAuthError('');
    const data = await loginRequest(credentials);
    setAccessToken(data.access);
    setRefreshToken(data.refresh);

    const profile = await getCurrentUser();
    setUser(profile);
    setAuthError('');
    return profile;
  };

  const logout = async () => {
    try {
      await logoutRequest();
    } catch {
      // Fail closed to local cleanup.
    } finally {
      clearSession();
    }
  };

  const value = useMemo(
    () => ({
      user,
      accessToken,
      refreshToken,
      authError,
      isAuthenticated: Boolean(accessToken && user),
      isLoading,
      login,
      logout,
      refreshSession,
      setUser,
      setAccessToken,
    }),
    [user, accessToken, refreshToken, authError, isLoading],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
}
