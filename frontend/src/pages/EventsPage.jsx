import { useEffect, useMemo, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { apiRequest } from '../api/client';

const EVENT_TYPE_COLORS = {
  SERVICE: '#4f46e5',
  MEETING: '#0891b2',
  YOUTH: '#ea580c',
  SPECIAL: '#be185d',
};

const EMPTY_FORM = {
  title: '',
  description: '',
  event_type: 'SERVICE',
  event_date: '',
  location: '',
  registration_required: false,
  max_attendees: '',
  recurrence: 'NONE',
  recurrence_day: '',
  recurrence_end_date: '',
  is_active: true,
};

const formatTypeLabel = (value) => (value || 'SERVICE').replace('_', ' ');

const toDateTimeInputValue = (value) => {
  if (!value) return '';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  const pad = (n) => String(n).padStart(2, '0');
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
};

const formatFullDate = (value) => {
  if (!value) return 'Date TBA';
  try {
    return new Date(value).toLocaleDateString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric',
    });
  } catch {
    return value;
  }
};

const formatTime = (value) => {
  if (!value) return 'Time TBA';
  try {
    return new Date(value).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch {
    return value;
  }
};

export default function EventsPage() {
  const { user } = useAuth();
  const isAdmin = ['SUPER_USER', 'ADMIN_USER'].includes(user?.role);

  const [events, setEvents] = useState([]);
  const [registeredEventIds, setRegisteredEventIds] = useState([]);
  const [selectedEventId, setSelectedEventId] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [eventTypeFilter, setEventTypeFilter] = useState('ALL');
  const [dateFilter, setDateFilter] = useState('upcoming');
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState('');
  const [error, setError] = useState('');
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [formMode, setFormMode] = useState('create');
  const [formData, setFormData] = useState(EMPTY_FORM);
  const [busyAction, setBusyAction] = useState('');

  useEffect(() => {
    if (!isFormOpen) return undefined;

    const bodyOverflow = document.body.style.overflow;
    const documentOverflow = document.documentElement.style.overflow;
    document.body.style.overflow = 'hidden';
    document.documentElement.style.overflow = 'hidden';

    return () => {
      document.body.style.overflow = bodyOverflow;
      document.documentElement.style.overflow = documentOverflow;
    };
  }, [isFormOpen]);

  const loadEvents = async () => {
    setLoading(true);
    setError('');

    try {
      const [eventData, registrationData] = await Promise.all([
        apiRequest('/api/events/'),
        apiRequest('/api/events/my_registrations/').catch(() => []),
      ]);

      const normalizedEvents = Array.isArray(eventData) ? eventData : eventData?.results || [];
      const normalizedRegistrations = Array.isArray(registrationData) ? registrationData : registrationData?.results || [];

      setEvents(normalizedEvents);
      setRegisteredEventIds(normalizedRegistrations.map((item) => Number(item.event)).filter(Boolean));

      if (!selectedEventId && normalizedEvents.length > 0) {
        setSelectedEventId(normalizedEvents[0].id);
      }
    } catch (err) {
      setError(err.message || 'Unable to load events right now.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEvents();
  }, []);

  const visibleEvents = useMemo(() => {
    const query = searchQuery.trim().toLowerCase();

    return events.filter((event) => {
      if (eventTypeFilter !== 'ALL' && event.event_type !== eventTypeFilter) {
        return false;
      }

      if (query) {
        const haystack = [event.title, event.description, event.location].join(' ').toLowerCase();
        if (!haystack.includes(query)) {
          return false;
        }
      }

      const eventDate = event.event_date ? new Date(event.event_date).getTime() : null;
      const now = Date.now();

      if (dateFilter === 'upcoming' && (!eventDate || eventDate < now)) {
        return false;
      }

      if (dateFilter === 'past' && (!eventDate || eventDate >= now)) {
        return false;
      }

      return true;
    });
  }, [events, searchQuery, eventTypeFilter, dateFilter]);

  useEffect(() => {
    if (!visibleEvents.length) {
      setSelectedEventId(null);
      return;
    }

    if (!visibleEvents.some((event) => event.id === selectedEventId)) {
      setSelectedEventId(visibleEvents[0].id);
    }
  }, [visibleEvents, selectedEventId]);

  const selectedEvent = visibleEvents.find((event) => event.id === selectedEventId) || visibleEvents[0] || null;

  const openCreateForm = () => {
    setFormMode('create');
    setFormData({ ...EMPTY_FORM, event_date: '' });
    setIsFormOpen(true);
    setNotice('');
    setError('');
  };

  const openEditForm = (event) => {
    setFormMode('edit');
    setFormData({
      title: event.title || '',
      description: event.description || '',
      event_type: event.event_type || 'SERVICE',
      event_date: toDateTimeInputValue(event.event_date),
      location: event.location || '',
      registration_required: Boolean(event.registration_required),
      max_attendees: event.max_attendees ?? '',
      recurrence: event.recurrence || 'NONE',
      recurrence_day: event.recurrence_day || '',
      recurrence_end_date: event.recurrence_end_date || '',
      is_active: event.is_active !== false,
    });
    setIsFormOpen(true);
    setNotice('');
    setError('');
  };

  const handleFormChange = (event) => {
    const { name, type, checked, value } = event.target;
    setFormData((current) => ({
      ...current,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!isAdmin) {
      setError('Only administrators can create or edit church events.');
      return;
    }

    try {
      setBusyAction('submit');
      setError('');

      const payload = {
        ...formData,
        max_attendees: formData.max_attendees === '' ? null : Number(formData.max_attendees),
        recurrence_day: formData.recurrence === 'WEEKLY' ? formData.recurrence_day : '',
        recurrence_end_date: formData.recurrence === 'NONE' ? '' : formData.recurrence_end_date,
      };

      if (!payload.title || !payload.event_date) {
        throw new Error('Title and event date/time are required.');
      }

      if (payload.recurrence === 'WEEKLY' && !payload.recurrence_day) {
        throw new Error('Please select the weekday for weekly recurring events.');
      }

      const endpoint = formMode === 'edit' ? `/api/events/${selectedEvent?.id}/` : '/api/events/';
      const method = formMode === 'edit' ? 'PUT' : 'POST';
      const result = await apiRequest(endpoint, {
        method,
        body: JSON.stringify(payload),
      });

      setNotice(formMode === 'edit' ? 'Event updated successfully.' : 'Event created successfully.');
      setIsFormOpen(false);
      setFormData(EMPTY_FORM);
      await loadEvents();
      if (result?.id) setSelectedEventId(result.id);
    } catch (err) {
      setError(err.message || 'The event could not be saved.');
    } finally {
      setBusyAction('');
    }
  };

  const toggleRegistration = async (eventItem) => {
    if (!eventItem) return;

    const isRegistered = registeredEventIds.includes(Number(eventItem.id));
    const action = isRegistered ? 'cancel_registration' : 'register';

    try {
      setBusyAction(`register-${eventItem.id}`);
      setError('');
      const result = await apiRequest(`/api/events/${eventItem.id}/${action}/`, { method: 'POST' });
      setNotice(result.message || (isRegistered ? 'Registration cancelled.' : 'Registration confirmed.'));
      await loadEvents();
    } catch (err) {
      setError(err.message || 'Unable to update your registration.');
    } finally {
      setBusyAction('');
    }
  };

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading-container">Loading upcoming events...</div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>Events</h1>
          <p>Stay connected with worship services, meetings, and church activities.</p>
        </div>
        {isAdmin && (
          <button type="button" className="btn btn-primary" onClick={openCreateForm}>
            + New Event
          </button>
        )}
      </div>

      {notice && <div className="success-message">{notice}</div>}
      {error && <div className="error-message">{error}</div>}

      <div className="page-toolbar">
        <div className="search-field" style={{ minWidth: 'min(100%, 360px)' }}>
          <span aria-hidden="true">⌕</span>
          <input
            type="search"
            value={searchQuery}
            onChange={(event) => setSearchQuery(event.target.value)}
            placeholder="Search by title, place, or description"
            aria-label="Search events"
          />
        </div>

        <div className="toolbar-actions">
          <select value={eventTypeFilter} onChange={(event) => setEventTypeFilter(event.target.value)} aria-label="Filter by event type">
            <option value="ALL">All types</option>
            <option value="SERVICE">Service</option>
            <option value="MEETING">Meeting</option>
            <option value="YOUTH">Youth program</option>
            <option value="SPECIAL">Special event</option>
          </select>
          <select value={dateFilter} onChange={(event) => setDateFilter(event.target.value)} aria-label="Filter by date range">
            <option value="upcoming">Upcoming</option>
            <option value="all">All events</option>
            <option value="past">Past events</option>
          </select>
        </div>
      </div>

      <div className="events-grid" style={{ gridTemplateColumns: '1.2fr 0.8fr' }}>
        <section>
          {visibleEvents.length === 0 ? (
            <div className="empty-state">
              <h3>No events match your filters</h3>
              <p>Try another keyword or date range.</p>
            </div>
          ) : (
            <div className="list-grid" style={{ gridTemplateColumns: '1fr' }}>
              {visibleEvents.map((event) => {
                const typeColor = EVENT_TYPE_COLORS[event.event_type] || '#6b7280';
                const isSelected = selectedEvent?.id === event.id;
                const isRegistered = registeredEventIds.includes(Number(event.id));

                return (
                  <article key={event.id} className={`card ${isSelected ? 'selected' : ''}`} style={{ borderColor: isSelected ? typeColor : undefined }}>
                    <div className="event-card-header" style={{ backgroundColor: typeColor }}>
                      <span>{formatTypeLabel(event.event_type)}</span>
                      {event.recurrence && event.recurrence !== 'NONE' && <span>🔁 {event.recurrence}</span>}
                    </div>

                    <div className="event-card-body" style={{ display: 'grid', gap: '1rem' }}>
                      <div className="event-body-top" style={{ display: 'flex', justifyContent: 'space-between', gap: '12px', alignItems: 'flex-start' }}>
                        <div>
                          <h3>{event.title}</h3>
                          <small>{event.weekday || 'Scheduled'} · {formatFullDate(event.event_date)}</small>
                        </div>
                        <span className={`status-badge ${event.is_active !== false ? 'status-success' : 'status-neutral'}`}>
                          {event.is_active !== false ? 'Active' : 'Inactive'}
                        </span>
                      </div>

                      <div className="info-grid">
                        <div className="info-item">
                          <span>Location</span>
                          <strong>{event.location || 'TBA'}</strong>
                        </div>
                        <div className="info-item">
                          <span>Time</span>
                          <strong>{formatTime(event.event_date)}</strong>
                        </div>
                      </div>

                      {event.max_attendees && (
                        <div>
                          <div className="progress-bar-container" style={{ height: '8px', borderRadius: '999px', overflow: 'hidden', background: '#e5e7eb', marginBottom: '6px' }}>
                            <div
                              style={{
                                width: `${Math.min(((event.attendee_count || 0) / event.max_attendees) * 100, 100)}%`,
                                height: '100%',
                                background: typeColor,
                              }}
                            />
                          </div>
                          <small>{event.attendee_count || 0} / {event.max_attendees} registered</small>
                        </div>
                      )}

                      <p>{event.description || 'No description provided.'}</p>

                      <div className="card-action-row">
                        <button type="button" className="btn btn-secondary" onClick={() => setSelectedEventId(event.id)}>
                          View details
                        </button>
                        {isAdmin && (
                          <button type="button" className="btn btn-ghost" onClick={() => openEditForm(event)}>
                            Edit
                          </button>
                        )}
                        {event.registration_required && (
                          <button
                            type="button"
                            className="btn btn-primary"
                            onClick={() => toggleRegistration(event)}
                            disabled={busyAction === `register-${event.id}`}
                          >
                            {busyAction === `register-${event.id}` ? 'Working...' : (isRegistered ? 'Cancel registration' : 'Register')}
                          </button>
                        )}
                      </div>
                    </div>
                  </article>
                );
              })}
            </div>
          )}
        </section>

        <aside>
          {selectedEvent ? (
            <div className="card event-detail-card" style={{ gap: '1rem' }}>
              <div className="event-card-header" style={{ backgroundColor: EVENT_TYPE_COLORS[selectedEvent.event_type] || '#6b7280', margin: '-24px -24px 0', padding: '16px 20px' }}>
                <span>{formatTypeLabel(selectedEvent.event_type)}</span>
                {selectedEvent.recurrence && selectedEvent.recurrence !== 'NONE' && <span>🔁 {selectedEvent.recurrence}</span>}
              </div>

              <h2>{selectedEvent.title}</h2>
              <p>{selectedEvent.description || 'No additional description provided.'}</p>

              <div className="info-grid">
                <div className="info-item">
                  <span>Date</span>
                  <strong>{formatFullDate(selectedEvent.event_date)}</strong>
                </div>
                <div className="info-item">
                  <span>Time</span>
                  <strong>{formatTime(selectedEvent.event_date)}</strong>
                </div>
                <div className="info-item">
                  <span>Location</span>
                  <strong>{selectedEvent.location || 'TBA'}</strong>
                </div>
                <div className="info-item">
                  <span>Attendance</span>
                  <strong>{selectedEvent.max_attendees ? `${selectedEvent.attendee_count || 0}/${selectedEvent.max_attendees}` : 'Open registration'}</strong>
                </div>
              </div>

              <div className="card-action-row">
                {selectedEvent.registration_required && (
                  <button type="button" className="btn btn-primary" onClick={() => toggleRegistration(selectedEvent)} disabled={busyAction === `register-${selectedEvent.id}`}>
                    {busyAction === `register-${selectedEvent.id}` ? 'Working...' : (registeredEventIds.includes(Number(selectedEvent.id)) ? 'Cancel registration' : 'Register now')}
                  </button>
                )}
                {isAdmin && (
                  <button type="button" className="btn btn-secondary" onClick={() => openEditForm(selectedEvent)}>
                    Edit event
                  </button>
                )}
              </div>
            </div>
          ) : (
            <div className="empty-state">
              <h3>No event selected</h3>
              <p>Select a church event to review its details.</p>
            </div>
          )}
        </aside>
      </div>

      {isFormOpen && (
        <div className="modal-backdrop event-modal-backdrop" role="dialog" aria-modal="true">
          <div className="modal-card event-modal-panel">
            <div className="modal-header event-modal-header">
              <h2 style={{ margin: 0 }}>{formMode === 'edit' ? 'Update event' : 'Create event'}</h2>
              <button type="button" className="icon-button" onClick={() => setIsFormOpen(false)} aria-label="Close event form">×</button>
            </div>

            <form onSubmit={handleSubmit} className="event-form event-modal-form">
              <div className="event-form-content">
                <div className="form-row">
                  <label>
                    Title
                    <input name="title" value={formData.title} onChange={handleFormChange} required />
                  </label>
                  <label>
                    Event type
                    <select name="event_type" value={formData.event_type} onChange={handleFormChange}>
                      <option value="SERVICE">Service</option>
                      <option value="MEETING">Meeting</option>
                      <option value="YOUTH">Youth program</option>
                      <option value="SPECIAL">Special event</option>
                    </select>
                  </label>
                </div>

                <label>
                  Description
                  <textarea name="description" value={formData.description} onChange={handleFormChange} rows="4" />
                </label>

                <div className="form-row">
                  <label>
                    Event date and time
                    <input type="datetime-local" name="event_date" value={formData.event_date} onChange={handleFormChange} required />
                  </label>
                  <label>
                    Location
                    <input name="location" value={formData.location} onChange={handleFormChange} placeholder="Main Sanctuary" />
                  </label>
                </div>

                <div className="form-row">
                  <label>
                    Recurrence
                    <select name="recurrence" value={formData.recurrence} onChange={handleFormChange}>
                      <option value="NONE">None</option>
                      <option value="DAILY">Daily</option>
                      <option value="WEEKLY">Weekly</option>
                      <option value="MONTHLY">Monthly</option>
                    </select>
                  </label>
                  <label>
                    Recurrence day
                    <select name="recurrence_day" value={formData.recurrence_day} onChange={handleFormChange} disabled={formData.recurrence !== 'WEEKLY'}>
                      <option value="">Select a weekday</option>
                      <option value="MONDAY">Monday</option>
                      <option value="TUESDAY">Tuesday</option>
                      <option value="WEDNESDAY">Wednesday</option>
                      <option value="THURSDAY">Thursday</option>
                      <option value="FRIDAY">Friday</option>
                      <option value="SATURDAY">Saturday</option>
                      <option value="SUNDAY">Sunday</option>
                    </select>
                  </label>
                </div>

                <div className="form-row">
                  <label style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    Registration required
                    <input type="checkbox" name="registration_required" checked={formData.registration_required} onChange={handleFormChange} />
                  </label>
                  <label>
                    Maximum attendees
                    <input type="number" min="1" name="max_attendees" value={formData.max_attendees} onChange={handleFormChange} placeholder="Optional" />
                  </label>
                </div>

                <div className="form-row">
                  <label>
                    Recurrence end date
                    <input type="date" name="recurrence_end_date" value={formData.recurrence_end_date} onChange={handleFormChange} disabled={formData.recurrence === 'NONE'} />
                  </label>
                  <label style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    Active
                    <input type="checkbox" name="is_active" checked={formData.is_active} onChange={handleFormChange} />
                  </label>
                </div>
              </div>

              <div className="modal-footer event-modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setIsFormOpen(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary" disabled={busyAction === 'submit'}>
                  {busyAction === 'submit' ? 'Saving...' : (formMode === 'edit' ? 'Save changes' : 'Create event')}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
