import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { apiRequest } from '../api/client';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';
import EmptyState from '../components/EmptyState';

const isCommitteeMember = (committee, userId) => {
  if (!userId || !Array.isArray(committee?.memberships)) {
    return false;
  }

  return committee.memberships.some((membership) => Number(membership.user) === Number(userId) && membership.is_active);
};

export default function CommitteesPage() {
  const { user } = useAuth();
  const [committees, setCommittees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [busyAction, setBusyAction] = useState('');

  const loadCommittees = async () => {
    setLoading(true);
    setError('');

    try {
      const data = await apiRequest('/api/committees/');
      const normalized = Array.isArray(data) ? data : data?.results || [];
      setCommittees(normalized);
      setNotice('');
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
    setBusyAction(`${committee.id}-${action}`);
    setError('');
    setNotice('');

    try {
      const result = await apiRequest(`/api/committees/${committee.id}/${action}/`, {
        method: action === 'leave' ? 'DELETE' : 'POST',
      });
      setNotice(result.message || `Committee ${action} request complete.`);
      await loadCommittees();
    } catch (err) {
      setError(err.message || 'Unable to update committee membership.');
    } finally {
      setBusyAction('');
    }
  };

  if (loading) {
    return <Loading message="Loading committees..." />;
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>Committees</h1>
          <p>Review active congregation committees and your membership status.</p>
        </div>
      </div>

      {notice && <div className="success-message">{notice}</div>}
      {error && <ErrorMessage message={error} />}

      {!error && committees.length === 0 && (
        <EmptyState title="No committees available" description="Committee information will appear here once it is available." />
      )}

      {!error && committees.length > 0 && (
        <div className="list-grid">
          {committees.map((committee) => {
            const member = isCommitteeMember(committee, user?.id);
            const isBusy = busyAction === `${committee.id}-join` || busyAction === `${committee.id}-leave`;

            return (
              <article key={committee.id} className="card">
                <div className="card-meta">
                  <span className={`status-badge ${committee.is_active ? 'status-success' : 'status-neutral'}`}>
                    {committee.is_active ? 'Active' : 'Inactive'}
                  </span>
                  <span>{committee.total_members || 0} members</span>
                </div>

                <div>
                  <h2>{committee.name}</h2>
                  <p>{committee.description || 'No description available.'}</p>
                </div>

                <div style={{ display: 'grid', gap: '0.5rem', color: '#4d6a73', fontSize: '0.82rem' }}>
                  <div>
                    <strong>Schedule:</strong> {committee.meeting_schedule || 'Not specified'}
                  </div>
                  <div>
                    <strong>Purpose:</strong> {committee.purpose || 'No purpose listed.'}
                  </div>
                </div>

                <div className="card-action-row">
                  <button
                    type="button"
                    className="btn btn-primary"
                    disabled={isBusy || member}
                    onClick={() => updateMembership(committee, 'join')}
                  >
                    {member ? 'Joined' : 'Join'}
                  </button>
                  <button
                    type="button"
                    className="btn btn-secondary"
                    disabled={isBusy || !member}
                    onClick={() => updateMembership(committee, 'leave')}
                  >
                    Leave
                  </button>
                </div>
              </article>
            );
          })}
        </div>
      )}
    </div>
  );
}
