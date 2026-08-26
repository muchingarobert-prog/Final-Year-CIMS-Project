import { useState } from 'react';
import DataPage, { asList } from '../components/DataPage';
import { apiRequest } from '../api/client';

export default function NotificationsPage() {
  const [message, setMessage] = useState('');
  const markAll = async () => { try { const result = await apiRequest('/api/notifications/mark_all_read/', { method: 'POST' }); setMessage(result.message || 'All notifications marked as read.'); } catch (e) { setMessage(e.message); } };
  const markRead = async (id) => { try { await apiRequest(`/api/notifications/${id}/mark_read/`, { method: 'POST' }); setMessage('Notification marked as read.'); } catch (e) { setMessage(e.message); } };
  return <DataPage title="Notifications" description="Read congregation updates and reminders." endpoint="/api/notifications/" transform={asList} actions={<button className="btn btn-secondary" onClick={markAll}>Mark all read</button>} renderItem={(item) => <article className={`card ${item.is_read ? '' : 'unread'}`} key={item.id}><h2>{item.title}</h2><p>{item.message}</p><small>{item.created_at ? new Date(item.created_at).toLocaleString() : ''}</small>{!item.is_read && <button className="btn btn-ghost" onClick={() => markRead(item.id)}>Mark read</button>}</article>} />;
}
