import { useEffect, useState } from 'react';
import { apiRequest } from '../api/client';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';
import EmptyState from '../components/EmptyState';

const list = (value) => (Array.isArray(value) ? value : value?.results || []);

const formatDate = (value) => {
  if (!value) return 'Date not set';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' });
};

export default function AttendancePage() {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const load = async () => {
    setLoading(true);
    try {
      const data = await apiRequest('/api/attendance/sessions/');
      setSessions(list(data));
      setError('');
    } catch (e) {
      setError(e.message || 'Unable to load attendance sessions.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const checkIn = async (id) => {
    try {
      const result = await apiRequest(`/api/attendance/sessions/${id}/check_in/`, { method: 'POST' });
      setMessage(result.message || 'Attendance recorded.');
      load();
    } catch (e) {
      setMessage(e.message || 'Attendance could not be recorded.');
    }
  };

  if (loading) return <Loading message="Loading attendance sessions..." />;

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>Attendance</h1>
          <p>Review active services and record member check-ins.</p>
        </div>
      </div>

      {message && <div className="success-message">{message}</div>}
      {error && <ErrorMessage message={error} />}

      {!error && sessions.length === 0 && (
        <EmptyState title="No attendance sessions" description="Check back later for the next congregation service." />
      )}

      {!error && sessions.length > 0 && (
        <div className="data-list">
          {sessions.map((session) => (
            <article className="card" key={session.id}>
              <div className="card-meta">
                <span className={`status-badge ${session.is_active ? 'status-success' : 'status-neutral'}`}>
                  {session.is_active ? 'Open' : 'Closed'}
                </span>
                <span>{session.service_type || 'Service'}</span>
              </div>

              <div>
                <h2>{session.title || 'Attendance session'}</h2>
                <p>{formatDate(session.session_date)}</p>
              </div>

              <div className="info-grid">
                <div className="info-item"><span>Present</span><strong>{session.total_present ?? 0}</strong></div>
                <div className="info-item"><span>Absent</span><strong>{session.total_absent ?? 0}</strong></div>
                <div className="info-item"><span>Rate</span><strong>{session.attendance_rate ?? 0}%</strong></div>
              </div>

              {session.is_active && (
                <div className="card-action-row">
                  <button className="btn btn-primary" onClick={() => checkIn(session.id)}>Check in</button>
                </div>
              )}
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
