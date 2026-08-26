import { useState } from 'react';
import DataPage, { asList } from '../components/DataPage';
import { apiRequest } from '../api/client';

export default function AttendancePage() {
  const [message, setMessage] = useState('');
  const checkIn = async (id) => { try { const result = await apiRequest(`/api/attendance/sessions/${id}/check_in/`, { method: 'POST' }); setMessage(result.message || 'Attendance recorded.'); } catch (e) { setMessage(e.message); } };
  return <DataPage title="Attendance" description="Review attendance sessions and check in to active services." endpoint="/api/attendance/sessions/" transform={asList} actions={message && <span className="success-message">{message}</span>} renderItem={(session) => <article className="card" key={session.id}><h2>{session.title}</h2><p>{session.service_type} · {new Date(session.session_date).toLocaleString()}</p><p>Present: {session.total_present} · Absent: {session.total_absent} · Rate: {session.attendance_rate}%</p>{session.is_active && <button className="btn btn-primary" onClick={() => checkIn(session.id)}>Check in</button>}</article>} />;
}
