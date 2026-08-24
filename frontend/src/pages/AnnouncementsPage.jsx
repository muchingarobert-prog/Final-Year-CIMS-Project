import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

export default function AnnouncementsPage() {
  const [announcements, setAnnouncements] = useState([]);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('cims_access_token');
    if (!token) {
      navigate('/login');
      return;
    }

    fetch(`${API_BASE}/api/announcements/`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(async (response) => {
        if (response.status === 401) {
          navigate('/login');
          return null;
        }
        if (!response.ok) throw new Error('Unable to load announcements.');
        return response.json();
      })
      .then((data) => setAnnouncements(Array.isArray(data) ? data : data?.results || []))
      .catch((requestError) => setError(requestError.message));
  }, [navigate]);

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Announcements</h1>
        <p>Keep up with congregation-wide messages and important updates.</p>
      </div>
      {error && <p className="error-message">{error}</p>}
      <div className="list-grid">
        {announcements.map((announcement) => (
          <article key={announcement.id} className="card">
            <h2>{announcement.title}</h2>
            <p>{announcement.content || announcement.message}</p>
          </article>
        ))}
      </div>
      {!error && announcements.length === 0 && <p>No announcements are available.</p>}
    </div>
  );
}
