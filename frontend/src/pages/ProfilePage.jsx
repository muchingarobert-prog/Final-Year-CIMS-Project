import { useEffect, useState } from 'react';
import { apiRequest } from '../api/client';
import { useAuth } from '../context/AuthContext';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';

export default function ProfilePage() {
  const { user, setUser } = useAuth();
  const [form, setForm] = useState({});
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(!user);

  useEffect(() => {
    if (user) { setForm(user); return; }
    apiRequest('/api/auth/profile/').then((profile) => { setForm(profile); setUser(profile); }).catch((e) => setError(e.message)).finally(() => setLoading(false));
  }, [user, setUser]);

  const update = (event) => setForm({ ...form, [event.target.name]: event.target.value });
  const submit = async (event) => {
    event.preventDefault(); setStatus(''); setError('');
    try { const profile = await apiRequest('/api/auth/profile/', { method: 'PATCH', body: JSON.stringify(form) }); setForm(profile); setUser(profile); setStatus('Profile updated successfully.'); }
    catch (e) { setError(e.message || 'Unable to update profile.'); }
  };

  if (loading) return <Loading message="Loading your profile..." />;
  return <div className="page-container"><div className="page-header"><h1>My Profile</h1><p>Keep your congregation information up to date.</p></div><form className="form-panel" onSubmit={submit}>
    <div className="form-row"><label>First name<input name="first_name" value={form.first_name || ''} onChange={update} /></label><label>Last name<input name="last_name" value={form.last_name || ''} onChange={update} /></label></div>
    <div className="form-row"><label>Email<input type="email" name="email" value={form.email || ''} onChange={update} /></label><label>Phone<input name="phone_number" value={form.phone_number || ''} onChange={update} /></label></div>
    <div className="form-row"><label>Programme of study<input name="programme_of_study" value={form.programme_of_study || ''} onChange={update} /></label><label>Year of study<input type="number" name="year_of_study" value={form.year_of_study || ''} onChange={update} /></label></div>
    <label>Bio<textarea name="bio" value={form.bio || ''} onChange={update} rows="4" /></label>
    {error && <ErrorMessage message={error} />}{status && <ErrorMessage message={status} variant="success" />}<button className="btn btn-primary" type="submit">Save profile</button>
  </form></div>;
}
