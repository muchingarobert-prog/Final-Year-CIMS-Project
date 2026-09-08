import { useEffect, useState } from 'react';
import { apiRequest } from '../api/client';
import ErrorMessage from '../components/ErrorMessage';
import Loading from '../components/Loading';
import EmptyState from '../components/EmptyState';
import ManagementTable, { getDisplayName, PageToolbar, StatusBadge } from '../components/ManagementTable';

const initials = (member) => getDisplayName(member).split(' ').map((part) => part[0]).join('').slice(0, 2).toUpperCase();

export default function MembersPage() {
  const [members, setMembers] = useState([]); const [search, setSearch] = useState(''); const [loading, setLoading] = useState(true); const [error, setError] = useState('');
  useEffect(() => { apiRequest('/api/users/member_directory/').then((data) => setMembers(Array.isArray(data) ? data : data?.results || [])).catch((requestError) => setError(requestError.message || 'Unable to load members.')).finally(() => setLoading(false)); }, []);
  const filtered = members.filter((member) => `${getDisplayName(member)} ${member.email || ''} ${member.phone_number || ''}`.toLowerCase().includes(search.toLowerCase()));
  if (loading) return <Loading message="Loading member directory..." />;
  return <div className="page-container"><div className="page-header"><h1>Member directory</h1><p>Find congregation members and the contact information available to your account.</p></div>{error && <ErrorMessage message={error} />}{!error && <><PageToolbar search={search} onSearch={setSearch} placeholder="Search members by name, email or phone" /><div className="section-heading"><strong>{filtered.length}</strong> members</div>{filtered.length ? <ManagementTable rows={filtered} emptyMessage="No members match your search." columns={[{ key: 'name', label: 'Member', render: (member) => <span><span className="avatar-sm">{initials(member)}</span><span className="table-primary">{getDisplayName(member)}</span></span> }, { key: 'contact', label: 'Contact', render: (member) => member.email || member.phone_number || 'No contact details' }, { key: 'programme', label: 'Programme', render: (member) => member.programme_of_study || '—' }, { key: 'committees', label: 'Committees', render: (member) => member.committee_count ?? '—' }, { key: 'role', label: 'Role', render: (member) => <StatusBadge tone={member.role === 'MEMBER' ? 'neutral' : 'info'}>{(member.role || 'MEMBER').replaceAll('_', ' ')}</StatusBadge> }]} /> : <EmptyState title="No members found" description={search ? 'Try a different search term.' : 'The member directory is empty.'} />}</>}</div>;
}
