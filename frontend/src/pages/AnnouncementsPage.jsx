import { useEffect, useState } from 'react';
import { apiRequest } from '../api/client';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';
import EmptyState from '../components/EmptyState';

const formatDate = (value) => {
  if (!value) return 'Date not specified';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
};

export default function AnnouncementsPage() {
  const [announcements, setAnnouncements] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiRequest('/api/announcements/')
      .then((data) => setAnnouncements(Array.isArray(data) ? data : data?.results || []))
      .catch((requestError) => setError(requestError.message || 'Unable to load announcements.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Loading message="Loading announcements..." />;

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>Announcements</h1>
          <p>Keep up with congregation-wide updates and important activity.</p>
        </div>
      </div>

      {error && <ErrorMessage message={error} />}

      {!error && announcements.length === 0 && (
        <EmptyState title="No announcements available" description="There are no congregation announcements to show right now." />
      )}

      {!error && announcements.length > 0 && (
        <div className="data-list">
          {announcements.map((announcement) => (
            <article key={announcement.id} className="card">
              <div className="card-meta">
                <span className="status-badge status-info">{announcement.target_type === 'COMMITTEE' ? 'Committee' : 'Congregation'}</span>
                <time dateTime={announcement.created_at || announcement.posted_at}>{formatDate(announcement.created_at || announcement.posted_at)}</time>
              </div>
              <div>
                <h2>{announcement.title || 'Congregation announcement'}</h2>
                <p>{announcement.content || announcement.message || announcement.description || 'No announcement details were provided.'}</p>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
