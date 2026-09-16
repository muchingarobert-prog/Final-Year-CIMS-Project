import { useEffect, useState } from 'react';
import { apiRequest } from '../api/client';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';
import EmptyState from '../components/EmptyState';

const list = (value) => (Array.isArray(value) ? value : value?.results || []);

const formatDate = (value) => {
  if (!value) return 'No date';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString(undefined, { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
};

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const load = async () => {
    setLoading(true);
    try {
      const data = await apiRequest('/api/notifications/');
      setNotifications(list(data));
      setError('');
    } catch (e) {
      setError(e.message || 'Unable to load notifications.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const markAll = async () => {
    try {
      const result = await apiRequest('/api/notifications/mark_all_read/', { method: 'POST' });
      setMessage(result.message || 'All notifications marked as read.');
      load();
    } catch (e) {
      setMessage(e.message || 'Unable to mark notifications as read.');
    }
  };

  const markRead = async (id) => {
    try {
      await apiRequest(`/api/notifications/${id}/mark_read/`, { method: 'POST' });
      setMessage('Notification marked as read.');
      load();
    } catch (e) {
      setMessage(e.message || 'Unable to update this notification.');
    }
  };

  if (loading) return <Loading message="Loading notifications..." />;

  return (
    <div className="page-container">
      <div className="page-header page-header-actions">
        <div>
          <h1>Notifications</h1>
          <p>Monitor member updates, reminders, and congregation activity.</p>
        </div>
        <button className="btn btn-secondary" onClick={markAll}>Mark all read</button>
      </div>

      {message && <div className="success-message">{message}</div>}
      {error && <ErrorMessage message={error} />}

      {!error && notifications.length === 0 && (
        <EmptyState title="No notifications" description="You are all caught up." />
      )}

      {!error && notifications.length > 0 && (
        <div className="data-list">
          {notifications.map((item) => (
            <article className={`card ${item.is_read ? '' : 'unread'}`} key={item.id}>
              <div className="card-meta">
                <span className={`status-badge ${item.is_read ? 'status-neutral' : 'status-info'}`}>
                  {item.is_read ? 'Read' : 'Unread'}
                </span>
                <time dateTime={item.created_at}>{formatDate(item.created_at)}</time>
              </div>
              <div>
                <h2>{item.title || item.notification_type || 'Notification'}</h2>
                <p>{item.message || item.content || 'You have a new congregation update.'}</p>
              </div>
              {!item.is_read && (
                <div className="card-action-row">
                  <button className="btn btn-ghost" onClick={() => markRead(item.id)}>Mark read</button>
                </div>
              )}
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
