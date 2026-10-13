const ACCESS_TOKEN_KEY = 'cims_access_token';
const REFRESH_TOKEN_KEY = 'cims_refresh_token';
const SESSION_EXPIRED_EVENT = 'cims:session-expired';
const TOKENS_REFRESHED_EVENT = 'cims:tokens-refreshed';

let refreshPromise = null;

const getApiBase = () => {
  if (import.meta.env.DEV) return window.location.origin;

  const envBase = import.meta.env.VITE_API_BASE_URL || '';
  if (envBase) return envBase.replace(/\/$/, '');
  return window.location.origin;
};

export const buildApiUrl = (path) => {
  const normalized = path.startsWith('/') ? path : `/${path}`;
  const base = getApiBase();
  return `${base}${normalized}`;
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

const expireStoredSession = () => {
  clearStoredTokens();
  window.dispatchEvent(new Event(SESSION_EXPIRED_EVENT));
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

const extractErrorMessage = (data, fallback) => {
  if (data == null) return fallback;
  if (typeof data === 'string') return data;
  if (Array.isArray(data)) {
    return data.map((entry) => extractErrorMessage(entry, fallback)).filter(Boolean).join(', ');
  }
  if (typeof data === 'object') {
    const direct = data.detail || data.message || data.error || data.non_field_errors;
    if (direct) {
      if (Array.isArray(direct)) return direct.join(', ');
      if (typeof direct === 'object') return Object.values(direct).flat().join(', ');
      return String(direct);
    }
    return Object.values(data).flatMap((value) => Array.isArray(value) ? value : [value]).filter(Boolean).join(', ');
  }
  return fallback;
};

const handleResponse = async (response) => {
  const data = await parseJsonIfPresent(response);

  if (!response.ok) {
    throw new ApiError(extractErrorMessage(data, `Request failed with status ${response.status}`), response.status, data);
  }

  return data;
};

const fetchApi = async (url, options) => {
  try {
    return await fetch(url, options);
  } catch {
    throw new ApiError('Unable to reach the API. Check that Django is running and the API base URL is configured correctly.', 0);
  }
};

const requestRefreshedAccessToken = async (refreshToken) => {
  const response = await fetchApi(buildApiUrl('/api/auth/token/refresh/'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify({ refresh: refreshToken }),
  });

  const data = await parseJsonIfPresent(response);

  if (!response.ok) {
    throw new ApiError(extractErrorMessage(data, 'Session expired'), response.status, data);
  }

  if (!data?.access) {
    throw new ApiError('Refresh token did not return a valid access token', 401, data);
  }

  localStorage.setItem(ACCESS_TOKEN_KEY, data.access);
  if (data.refresh) {
    localStorage.setItem(REFRESH_TOKEN_KEY, data.refresh);
  }
  window.dispatchEvent(new Event(TOKENS_REFRESHED_EVENT));

  return data.access;
};

export const refreshAccessToken = (refreshToken) => {
  if (!refreshPromise) {
    refreshPromise = requestRefreshedAccessToken(refreshToken).finally(() => {
      refreshPromise = null;
    });
  }

  return refreshPromise;
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

  let response = await fetchApi(buildApiUrl(path), requestInit);

  if (response.status === 401 && !skipAuth && !_retry && (accessToken || refreshToken)) {
    if (!refreshToken) {
      expireStoredSession();
      throw new ApiError('Your session expired. Please log in again.', 401);
    }

    try {
      const latestTokens = getStoredTokens();
      const nextAccessToken = latestTokens.accessToken && latestTokens.accessToken !== accessToken
        ? latestTokens.accessToken
        : await refreshAccessToken(latestTokens.refreshToken || refreshToken);
      headers.set('Authorization', `Bearer ${nextAccessToken}`);
      response = await fetchApi(buildApiUrl(path), {
        ...requestInit,
        headers,
      });
    } catch (error) {
      if (![400, 401, 403].includes(error.status)) throw error;
      expireStoredSession();
      throw new ApiError('Your session expired. Please log in again.', 401, error.data);
    }

    if (response.status === 401) {
      expireStoredSession();
      throw new ApiError('Your session expired. Please log in again.', 401);
    }
  }

  return handleResponse(response);
};