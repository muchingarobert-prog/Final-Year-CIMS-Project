import { useEffect, useState } from 'react';
import { apiRequest } from '../api/client';

export default function AnnouncementsPage() {
  const [announcements, setAnnouncements] = useState([]);
  const [error, setError] = useState('');
  useEffect(() => {
    apiRequest('/api/announcements/')
      .then((data) => setAnnouncements(Array.isArray(data) ? data : data?.results || []))
      .catch((requestError) => setError(requestError.message));
  }, []);

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
