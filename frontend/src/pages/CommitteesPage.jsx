import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const API_BASE = 'http://127.0.0.1:8000';
const AUTH_TOKEN_KEY = 'cims_demo_access_token';

const getStoredToken = () => localStorage.getItem(AUTH_TOKEN_KEY) || '';

export default function CommitteesPage() {
  const [committees, setCommittees] = useState([]);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const accessToken = getStoredToken();
    if (!accessToken) {
      navigate('/login');
      return;
    }
    loadCommittees(accessToken);
  }, [navigate]);

  const loadCommittees = async (token) => {
    setMessage('Loading committees...');
    try {
      const response = await fetch(`${API_BASE}/api/committees/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        if (response.status === 401) {
          navigate('/login');
          return;
        }
        throw new Error(`${response.status}`);
      }
      const data = await response.json();
      setCommittees(data);
      setMessage(`Loaded ${data.length} committees.`);
    } catch (err) {
      setMessage(`Committee load failed: ${err.message}`);
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
            </div>
          ))}
        </div>
      ) : (
        <p>{message}</p>
      )}
    </div>
  );
}
