import { useState } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { login, authError } = useAuth();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login({ username: username.trim(), password });
      navigate(location.state?.from || '/dashboard', { replace: true });
    } catch (err) {
      const message = err?.data?.detail || err?.response?.data?.detail || err?.message || 'Unable to sign in. Please verify your credentials and the backend connection.';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-shell">
        <aside className="auth-visual">
          <div className="auth-brand">
            <img src="/images/church-emblem.png" alt="Church emblem" className="auth-brand-mark" />
            <div>
              <p className="eyebrow auth-eyebrow">New Apostolic Church</p>
              <h2>UNZA Congregation</h2>
            </div>
          </div>

          <div className="auth-side-card">
            <span className="material-symbols-outlined" aria-hidden="true">shield_person</span>
            <h3>Member access</h3>
            <p>Sign in to manage attendance, announcements, events, and key congregation information.</p>
          </div>

          <ul className="auth-list" aria-label="System benefits">
            <li><span className="material-symbols-outlined" aria-hidden="true">check</span> Secure member portal</li>
            <li><span className="material-symbols-outlined" aria-hidden="true">check</span> Event and attendance updates</li>
            <li><span className="material-symbols-outlined" aria-hidden="true">check</span> Committee communication</li>
          </ul>
        </aside>

        <section className="auth-panel" aria-labelledby="login-title">
          <div className="auth-header">
            <span className="eyebrow">Welcome back</span>
            <h1 id="login-title">Sign in</h1>
            <p>Access your congregation workspace securely.</p>
          </div>

          <form onSubmit={handleLogin} className="auth-form">
            <div className="field-group">
              <label htmlFor="username">Username</label>
              <div className="input-wrap">
                <span className="material-symbols-outlined" aria-hidden="true">person</span>
                <input
                  type="text"
                  id="username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                  placeholder="Enter your username"
                  autoComplete="username"
                />
              </div>
            </div>

            <div className="field-group">
              <label htmlFor="password">Password</label>
              <div className="input-wrap">
                <span className="material-symbols-outlined" aria-hidden="true">lock</span>
                <input
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  placeholder="Enter your password"
                  autoComplete="current-password"
                />
                <button
                  type="button"
                  className="pass-toggle"
                  onClick={() => setShowPassword((value) => !value)}
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                >
                  <span className="material-symbols-outlined" aria-hidden="true">{showPassword ? 'visibility_off' : 'visibility'}</span>
                </button>
              </div>
            </div>

            <div className="auth-utility">
              <label className="checkbox-row">
                <input type="checkbox" />
                <span>Remember me</span>
              </label>
              <Link to="/register">Need an account?</Link>
            </div>

            {(error || authError) && <div className="error-message">{error || authError}</div>}

            <button type="submit" className="btn btn-primary btn-large" disabled={loading}>
              {loading ? 'Logging in...' : 'Sign in'}
            </button>
          </form>
        </section>
      </div>
    </div>
  );
}