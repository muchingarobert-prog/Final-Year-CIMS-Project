import { useEffect, useMemo, useState } from 'react';
import { apiRequest } from '../api/client';
import ErrorMessage from '../components/ErrorMessage';
import Loading from '../components/Loading';
import EmptyState from '../components/EmptyState';
import ManagementTable, { getDisplayName, PageToolbar, StatusBadge } from '../components/ManagementTable';

const initials = (member) => getDisplayName(member).split(' ').map((part) => part[0]).join('').slice(0, 2).toUpperCase();

export default function MembersPage() {
  const [members, setMembers] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedMemberId, setSelectedMemberId] = useState(null);

  useEffect(() => {
    let isMounted = true;

    const loadMembers = async () => {
      setLoading(true);
      setError('');

      try {
        const query = search.trim();
        const path = query ? `/api/users/search/?q=${encodeURIComponent(query)}` : '/api/users/member_directory/';
        const data = await apiRequest(path);
        const normalized = Array.isArray(data) ? data : data?.results || [];

        if (!isMounted) return;

        setMembers(normalized);
        if (!selectedMemberId && normalized.length) {
          setSelectedMemberId(normalized[0].id);
        }
      } catch (requestError) {
        if (isMounted) {
          setError(requestError.message || 'Unable to load members.');
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    loadMembers();
    return () => {
      isMounted = false;
    };
  }, [search]);

  const selectedMember = useMemo(
    () => members.find((member) => member.id === selectedMemberId) || members[0] || null,
    [members, selectedMemberId],
  );

  if (loading) {
    return <Loading message="Loading member directory..." />;
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>Member directory</h1>
          <p>Find congregation members and the contact information available to your account.</p>
        </div>
      </div>

      {error && <ErrorMessage message={error} />}

      {!error && (
        <>
          <PageToolbar
            search={search}
            onSearch={setSearch}
            placeholder="Search members by name, username, email or phone"
          />

          <div className="section-heading">
            <strong>{members.length}</strong> members
          </div>

          {members.length ? (
            <div style={{ display: 'grid', gridTemplateColumns: '1.7fr 1fr', gap: '1.5rem', alignItems: 'start' }}>
              <div>
                <ManagementTable
                  rows={members}
                  emptyMessage="No members match your search."
                  columns={[
                    {
                      key: 'name',
                      label: 'Member',
                      render: (member) => (
                        <button
                          type="button"
                          className="link-button"
                          onClick={() => setSelectedMemberId(member.id)}
                          style={{ display: 'flex', alignItems: 'center', background: 'transparent', padding: 0, border: 0, cursor: 'pointer' }}
                        >
                          <span className="avatar-sm">{initials(member)}</span>
                          <span className="table-primary">{getDisplayName(member)}</span>
                        </button>
                      ),
                    },
                    {
                      key: 'role',
                      label: 'Role',
                      render: (member) => (
                        <StatusBadge tone={member.role === 'MEMBER' ? 'neutral' : 'info'}>
                          {(member.role || 'MEMBER').replaceAll('_', ' ')}
                        </StatusBadge>
                      ),
                    },
                    {
                      key: 'username',
                      label: 'Username',
                      render: (member) => member.username || '—',
                    },
                    {
                      key: 'bio',
                      label: 'Summary',
                      render: (member) => member.bio || 'No profile summary available.',
                    },
                  ]}
                />
              </div>

              <div className="card" style={{ padding: '1.25rem' }}>
                {selectedMember ? (
                  <>
                    <div className="card-meta" style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                      <span className="avatar-lg" style={{ display: 'inline-grid', width: '52px', height: '52px', placeItems: 'center', borderRadius: '50%', background: '#ebf4f7', color: '#123f4a', fontSize: '1rem', fontWeight: 800 }}>{initials(selectedMember)}</span>
                      <div>
                        <h3 style={{ margin: 0 }}>{getDisplayName(selectedMember)}</h3>
                        <div>{(selectedMember.role || 'MEMBER').replaceAll('_', ' ')}</div>
                      </div>
                    </div>

                    <div style={{ display: 'grid', gap: '0.8rem' }}>
                      <div>
                        <strong>Username</strong>
                        <div>{selectedMember.username || '—'}</div>
                      </div>
                      <div>
                        <strong>Email</strong>
                        <div>{selectedMember.email || 'Not shared'}</div>
                      </div>
                      <div>
                        <strong>Phone</strong>
                        <div>{selectedMember.phone_number || 'Not shared'}</div>
                      </div>
                      <div>
                        <strong>Programme</strong>
                        <div>{selectedMember.programme_of_study || 'Not provided'}</div>
                      </div>
                      <div>
                        <strong>Profile</strong>
                        <div>{selectedMember.bio || 'No profile summary has been shared yet.'}</div>
                      </div>
                    </div>
                  </>
                ) : (
                  <EmptyState title="No member selected" description="Choose a member from the list to review their details." />
                )}
              </div>
            </div>
          ) : (
            <EmptyState title="No members found" description={search ? 'Try a different search term.' : 'The member directory is empty.'} />
          )}
        </>
      )}
    </div>
  );
}
