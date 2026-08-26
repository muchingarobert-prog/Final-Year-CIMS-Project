const ACCESS_TOKEN_KEY = 'cims_access_token';
const REFRESH_TOKEN_KEY = 'cims_refresh_token';

const getApiBase = () => {
  const envBase = import.meta.env.VITE_API_BASE_URL || '';
  return envBase.replace(/\/$/, '');
};

export const buildApiUrl = (path) => {
  const normalized = path.startsWith('/') ? path : `/${path}`;
  const base = getApiBase();
  return base ? `${base}${normalized}` : normalized;
};

export const getStoredTokens = () => ({
  accessToken: localStorage.getItem(ACCESS_TOKEN_KEY),
  refreshToken: localStorage.getItem(REFRESH_TOKEN_KEY),
});

export const persistTokens = ({ accessToken, refreshToken }) => {
  if (accessToken) localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  if (refreshToken) localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
};

export const clearStoredTokens = () => {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
};

export class ApiError extends Error {
  constructor(message, status, data = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
  }
}

const parseJsonIfPresent = async (response) => {
  const text = await response.text();
  if (!text) return null;

  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
};

const handleResponse = async (response) => {
  const data = await parseJsonIfPresent(response);

  if (!response.ok) {
    const errorMessage =
      data?.detail ||
      data?.message ||
      data?.error ||
      `Request failed with status ${response.status}`;

    throw new ApiError(errorMessage, response.status, data);
  }

  return data;
};

export const refreshAccessToken = async (refreshToken) => {
  const response = await fetch(buildApiUrl('/api/auth/token/refresh/'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify({ refresh: refreshToken }),
  });

  const data = await parseJsonIfPresent(response);

  if (!response.ok) {
    throw new ApiError(data?.detail || 'Session expired', response.status, data);
  }

  if (!data?.access) {
    throw new ApiError('Refresh token did not return a valid access token', 401, data);
  }

  localStorage.setItem(ACCESS_TOKEN_KEY, data.access);
  if (data.refresh) {
    localStorage.setItem(REFRESH_TOKEN_KEY, data.refresh);
  }

  return data.access;
};

export const apiRequest = async (path, options = {}, skipAuth = false) => {
  const { accessToken, refreshToken } = getStoredTokens();
  const headers = new Headers(options.headers || {});

  if (!skipAuth && accessToken) {
    headers.set('Authorization', `Bearer ${accessToken}`);
  }

  if (!(options.body instanceof FormData) && !headers.has('Content-Type') && options.body !== undefined) {
    headers.set('Content-Type', 'application/json');
  }

  const { _retry, ...fetchOptions } = options;
  const requestInit = {
    ...fetchOptions,
    headers,
  };

  let response = await fetch(buildApiUrl(path), requestInit);

  if (response.status === 401 && !skipAuth && !_retry && refreshToken) {
    try {
      const nextAccessToken = await refreshAccessToken(refreshToken);
      headers.set('Authorization', `Bearer ${nextAccessToken}`);
      response = await fetch(buildApiUrl(path), {
        ...requestInit,
        headers,
      });
    } catch {
      clearStoredTokens();
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
      throw new ApiError('Your session expired. Please log in again.', 401);
    }
  }

  return handleResponse(response);
};
