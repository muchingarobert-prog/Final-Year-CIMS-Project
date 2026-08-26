import { useEffect, useState } from 'react';
import { apiRequest } from '../api/client';

export default function MembersPage() {
  const [members, setMembers] = useState([]);
  const [error, setError] = useState('');
  useEffect(() => {
    apiRequest('/api/users/member_directory/')
      .then((data) => setMembers(Array.isArray(data) ? data : data?.results || []))
      .catch((requestError) => setError(requestError.message));
  }, []);

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
