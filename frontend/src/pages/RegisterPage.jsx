import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { apiRequest } from '../api/client';

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    gender: 'M',
    date_of_birth: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      await apiRequest('/api/auth/register/', {
        method: 'POST',
        body: JSON.stringify(formData),
      }, true);

      setSuccess('Registration successful! Redirecting to login...');
      setTimeout(() => {
        navigate('/login');
      }, 1500);
    } catch (err) {
      const message = err?.data?.detail || err?.data?.non_field_errors || err?.message || 'Registration failed. Please review the form and try again.';
      setError(Array.isArray(message) ? message.join(', ') : message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-shell auth-shell-wide">
        <aside className="auth-visual">
          <div className="auth-brand">
            <img src="/images/church-emblem.png" alt="Church emblem" className="auth-brand-mark" />
            <div>
              <p className="eyebrow auth-eyebrow">New Apostolic Church</p>
              <h2>UNZA Congregation</h2>
            </div>
          </div>

          <div className="auth-side-card">
            <span className="material-symbols-outlined" aria-hidden="true">person_add</span>
            <h3>Join the congregation</h3>
            <p>Create your account to access your member profile, events, and church updates.</p>
          </div>

          <ul className="auth-list" aria-label="Registration benefits">
            <li><span className="material-symbols-outlined" aria-hidden="true">check</span> Create your member profile</li>
            <li><span className="material-symbols-outlined" aria-hidden="true">check</span> Stay informed of events and announcements</li>
            <li><span className="material-symbols-outlined" aria-hidden="true">check</span> Access your congregation workspace</li>
          </ul>
        </aside>

        <section className="auth-panel" aria-labelledby="register-title">
          <div className="auth-header">
            <span className="eyebrow">Create account</span>
            <h1 id="register-title">Register</h1>
            <p>Set up your profile to access the UNZA congregation system.</p>
          </div>

          <form onSubmit={handleSubmit} className="auth-form">
            <div className="field-grid">
              <div className="field-group">
                <label htmlFor="username">Username *</label>
                <div className="input-wrap">
                  <span className="material-symbols-outlined" aria-hidden="true">person</span>
                  <input
                    type="text"
                    id="username"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                    placeholder="Choose a username"
                  />
                </div>
              </div>

              <div className="field-group">
                <label htmlFor="email">Email *</label>
                <div className="input-wrap">
                  <span className="material-symbols-outlined" aria-hidden="true">alternate_email</span>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    placeholder="you@example.com"
                  />
                </div>
              </div>
            </div>

            <div className="field-group">
              <label htmlFor="password">Password *</label>
              <div className="input-wrap">
                <span className="material-symbols-outlined" aria-hidden="true">lock</span>
                <input
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                  placeholder="Create a strong password"
                  minLength="8"
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

            <div className="field-grid">
              <div className="field-group">
                <label htmlFor="first_name">First name *</label>
                <div className="input-wrap">
                  <span className="material-symbols-outlined" aria-hidden="true">badge</span>
                  <input
                    type="text"
                    id="first_name"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleChange}
                    required
                    placeholder="First name"
                  />
                </div>
              </div>

              <div className="field-group">
                <label htmlFor="last_name">Last name *</label>
                <div className="input-wrap">
                  <span className="material-symbols-outlined" aria-hidden="true">badge</span>
                  <input
                    type="text"
                    id="last_name"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleChange}
                    required
                    placeholder="Last name"
                  />
                </div>
              </div>
            </div>

            <div className="field-grid">
              <div className="field-group">
                <label htmlFor="date_of_birth">Date of birth *</label>
                <div className="input-wrap input-wrap-date">
                  <span className="material-symbols-outlined" aria-hidden="true">calendar_month</span>
                  <input
                    type="date"
                    id="date_of_birth"
                    name="date_of_birth"
                    value={formData.date_of_birth}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>

              <div className="field-group">
                <label htmlFor="gender">Gender *</label>
                <div className="input-wrap">
                  <span className="material-symbols-outlined" aria-hidden="true">wc</span>
                  <select
                    id="gender"
                    name="gender"
                    value={formData.gender}
                    onChange={handleChange}
                    required
                  >
                    <option value="M">Male</option>
                    <option value="F">Female</option>
                  </select>
                </div>
              </div>
            </div>

            {error && <div className="error-message">{error}</div>}
            {success && <div className="success-message auth-success">{success}</div>}

            <button type="submit" className="btn btn-primary btn-large" disabled={loading}>
              {loading ? 'Creating account...' : 'Register'}
            </button>
          </form>

          <p className="auth-footer">
            Already have an account? <Link to="/login">Sign in</Link>
          </p>
        </section>
      </div>
    </div>
  );
}