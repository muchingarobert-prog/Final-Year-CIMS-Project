import { apiRequest, clearStoredTokens, persistTokens, getStoredTokens } from './client';

export const login = async ({ username, password }) => {
  const data = await apiRequest('/api/auth/login/', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  }, true);

  if (!data?.access) {
    throw new Error('No access token returned by the server.');
  }

  persistTokens({
    accessToken: data.access,
    refreshToken: data.refresh,
  });

  return data;
};

export const logout = async () => {
  const { refreshToken, accessToken } = getStoredTokens();

  if (refreshToken && accessToken) {
    try {
      await apiRequest(
        '/api/auth/logout/',
        {
          method: 'POST',
          body: JSON.stringify({ refresh: refreshToken }),
        },
        false,
      );
    } catch {
      // Ignore backend logout errors and clear local state.
    }
  }

  clearStoredTokens();
};

export const getCurrentUser = async () => {
  const data = await apiRequest('/api/auth/profile/');
  return data;
};
