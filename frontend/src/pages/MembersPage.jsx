import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

export default function MembersPage() {
  const [members, setMembers] = useState([]);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('cims_access_token');
    if (!token) {
      navigate('/login');
      return;
    }

    fetch(`${API_BASE}/api/users/member_directory/`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(async (response) => {
        if (response.status === 401) {
          navigate('/login');
          return null;
        }
        if (!response.ok) throw new Error('Unable to load members.');
        return response.json();
      })
      .then((data) => setMembers(Array.isArray(data) ? data : data?.results || []))
      .catch((requestError) => setError(requestError.message));
  }, [navigate]);

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Member Directory</h1>
        <p>Find congregation members and their available contact information.</p>
      </div>
      {error && <p className="error-message">{error}</p>}
      <div className="list-grid">
        {members.map((member) => (
          <article key={member.id} className="card">
            <h2>{member.first_name} {member.last_name}</h2>
            <p>{member.programme_of_study || 'Congregation member'}</p>
            <p>{member.email}</p>
          </article>
        ))}
      </div>
      {!error && members.length === 0 && <p>No members are available.</p>}
    </div>
  );
}
