import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiRequest } from '../api/client';

export default function CommitteesPage() {
  const [committees, setCommittees] = useState([]);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    loadCommittees();
  }, [navigate]);

  const loadCommittees = async () => {
    setMessage('Loading committees...');
    try {
      const data = await apiRequest('/api/committees/');
      setCommittees(Array.isArray(data) ? data : data?.results || []);
      setMessage(`Loaded ${data.length} committees.`);
    } catch (err) {
      setMessage(`Committee load failed: ${err.message}`);
    }
  };

  const updateMembership = async (committee, action) => {
    try {
      const result = await apiRequest(`/api/committees/${committee.id}/${action}/`, { method: action === 'leave' ? 'DELETE' : 'POST' });
      setMessage(result.message || `Committee ${action} request complete.`);
    } catch (error) {
      setMessage(error.message);
    }
  };

  return (
    <div>
      <div className="button-row">
        <button onClick={() => navigate('/dashboard')}>Back</button>
      </div>
      <h2>Committees</h2>
      {committees.length > 0 ? (
        <div className="list-grid">
          {committees.map((committee) => (
            <div key={committee.id} className="card">
              <h3>{committee.name}</h3>
              <p>{committee.description || 'No description available.'}</p>
              <p>Status: {committee.is_active ? 'Active' : 'Inactive'}</p>
              <div className="button-row"><button className="btn btn-primary" onClick={() => updateMembership(committee, 'join')}>Join</button><button className="btn btn-secondary" onClick={() => updateMembership(committee, 'leave')}>Leave</button></div>
            </div>
          ))}
        </div>
      ) : (
        <p>{message}</p>
      )}
    </div>
  );
}
