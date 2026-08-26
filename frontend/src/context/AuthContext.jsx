import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { apiRequest, clearStoredTokens, getStoredTokens, refreshAccessToken } from '../api/client';
import { getCurrentUser, login as loginRequest, logout as logoutRequest } from '../api/auth';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [accessToken, setAccessToken] = useState(() => localStorage.getItem('cims_access_token'));
  const [refreshToken, setRefreshToken] = useState(() => localStorage.getItem('cims_refresh_token'));
  const [isLoading, setIsLoading] = useState(true);

  const clearSession = () => {
    clearStoredTokens();
    setAccessToken(null);
    setRefreshToken(null);
    setUser(null);
  };

  const resolveUser = async (token = accessToken) => {
    if (!token) {
      setUser(null);
      return null;
    }

    try {
      const profile = await apiRequest('/api/auth/profile/');
      setUser(profile);
      return profile;
    } catch {
      return null;
    }
  };

  const refreshSession = async () => {
    const stored = getStoredTokens();

    if (!stored.refreshToken) {
      clearSession();
      return null;
    }

    try {
      const nextAccess = await refreshAccessToken(stored.refreshToken);
      setAccessToken(nextAccess);
      const profile = await resolveUser(nextAccess);
      return profile;
    } catch {
      clearSession();
      return null;
    }
  };

  useEffect(() => {
    const restoreSession = async () => {
      setIsLoading(true);

      const stored = getStoredTokens();

      if (stored.accessToken) {
        setAccessToken(stored.accessToken);
        try {
          const profile = await resolveUser(stored.accessToken);
          if (!profile) {
            await refreshSession();
          }
        } catch {
          clearSession();
        }
      } else if (stored.refreshToken) {
        await refreshSession();
      } else {
        clearSession();
      }

      setIsLoading(false);
    };

    restoreSession();
  }, []);

  const login = async (credentials) => {
    const data = await loginRequest(credentials);
    setAccessToken(data.access);
    setRefreshToken(data.refresh);

    const profile = await getCurrentUser();
    setUser(profile);
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
      isAuthenticated: Boolean(accessToken && user),
      isLoading,
      login,
      logout,
      refreshSession,
      setUser,
      setAccessToken,
    }),
    [user, accessToken, refreshToken, isLoading],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
}
