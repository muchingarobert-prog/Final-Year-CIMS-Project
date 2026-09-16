import { useEffect, useState } from 'react';
import { apiRequest } from '../api/client';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';
import EmptyState from '../components/EmptyState';

export default function CommitteesPage() {
  const [committees, setCommittees] = useState([]);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadCommittees = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await apiRequest('/api/committees/');
      setCommittees(Array.isArray(data) ? data : data?.results || []);
      setMessage('');
    } catch (err) {
      setError(err.message || 'Unable to load committees.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCommittees();
  }, []);

  const updateMembership = async (committee, action) => {
    try {
      const result = await apiRequest(`/api/committees/${committee.id}/${action}/`, { method: action === 'leave' ? 'DELETE' : 'POST' });
      setMessage(result.message || `Committee ${action} request complete.`);
      loadCommittees();
    } catch (error) {
      setMessage(error.message || 'Unable to update committee membership.');
    }
  };

  if (loading) return <Loading message="Loading committees..." />;

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>Committees</h1>
          <p>Review active congregation committees and your membership status.</p>
        </div>
      </div>

      {message && <div className="success-message">{message}</div>}
      {error && <ErrorMessage message={error} />}

      {!error && committees.length === 0 && (
        <EmptyState title="No committees available" description="Committee information will appear here once it is available." />
      )}

      {!error && committees.length > 0 && (
        <div className="list-grid">
          {committees.map((committee) => (
            <article key={committee.id} className="card">
              <div className="card-meta">
                <span className={`status-badge ${committee.is_active ? 'status-success' : 'status-neutral'}`}>
                  {committee.is_active ? 'Active' : 'Inactive'}
                </span>
                <span>{committee.membership_count || 0} members</span>
              </div>
              <div>
                <h2>{committee.name}</h2>
                <p>{committee.description || 'No description available.'}</p>
              </div>
              <div className="card-action-row">
                <button className="btn btn-primary" onClick={() => updateMembership(committee, 'join')}>Join</button>
                <button className="btn btn-secondary" onClick={() => updateMembership(committee, 'leave')}>Leave</button>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
