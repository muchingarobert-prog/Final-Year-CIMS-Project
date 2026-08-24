import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '';
const AUTH_TOKEN_KEY = 'cims_access_token';

const EVENT_TYPE_COLORS = {
  SERVICE: '#4f46e5', // Indigo
  MEETING: '#0891b2', // Cyan
  YOUTH: '#ea580c',   // Orange
  SPECIAL: '#be185d', // Pink
};

const getStoredToken = () => localStorage.getItem(AUTH_TOKEN_KEY) || '';

export default function EventsPage() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const accessToken = getStoredToken();
    if (!accessToken) {
      navigate('/login');
      return;
    }
    loadEvents(accessToken);
  }, [navigate]);

  const loadEvents = async (token) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/api/events/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) {
        if (response.status === 401) navigate('/login');
        return;
      }
      const data = await response.json();
      setEvents(data);
    } catch (err) {
      console.error("Failed to load events", err);
    } finally {
      setLoading(false);
    }
  };

  const formatFullDate = (value) => {
    if (!value) return 'Date TBA';
    try {
      return new Date(value).toLocaleDateString('en-US', {
        month: 'long', day: 'numeric', year: 'numeric'
      });
    } catch { return value; }
  };

  const formatTime = (value) => {
    if (!value) return '';
    try {
      return new Date(value).toLocaleTimeString('en-US', {
        hour: '2-digit', minute: '2-digit'
      });
    } catch { return ''; }
  };

  if (loading) {
    return <div className="loading-container">Loading upcoming events...</div>;
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Upcoming Events</h1>
        <p>Discover the latest worship services, meetings, and youth programs across the congregation.</p>
      </div>

      {events.length > 0 ? (
        <div className="events-grid">
          {events.map((event) => {
            const typeColor = EVENT_TYPE_COLORS[event.event_type] || '#6b7280';
            return (
              <div key={event.id} className="event-card">
                <div className="event-card-header" style={{ backgroundColor: typeColor }}>
                  <span className="event-type-badge">{event.event_type.replace('_', ' ')}</span>
                  {event.recurrence !== 'NONE' && (
                    <span className="recurrence-badge">🔁 {event.recurrence}</span>
                  )}
                </div>
                
                <div className="event-card-body">
                  <h2 className="event-title">{event.title}</h2>
                  
                  <div className="event-details">
                    <div className="detail-row">
                      <span className="detail-icon">📅</span>
                      <div>
                        <strong>{event.weekday}, {formatFullDate(event.event_date)}</strong>
                        <p>{formatTime(event.event_date)}</p>
                      </div>
                    </div>
                    
                    <div className="detail-row">
                      <span className="detail-icon">📍</span>
                      <div>
                        <strong>Location</strong>
                        <p>{event.location || 'Main Sanctuary'}</p>
                      </div>
                    </div>

                    {event.max_attendees && (
                      <div className="detail-row">
                        <span className="detail-icon">👥</span>
                        <div className="attendee-info">
                          <strong>Attendance</strong>
                          <div className="progress-bar-container">
                            <div 
                              className="progress-bar-fill" 
                              style={{ width: `${(event.attendee_count / event.max_attendees) * 100}%` }}
                            ></div>
                          </div>
                          <p>{event.attendee_count} / {event.max_attendees} Registered ({event.available_slots} slots left)</p>
                        </div>
                      </div>
                    )}
                  </div>

                  {event.description && (
                    <p className="event-description">{event.description}</p>
                  )}

                  <button className="register-btn" style={{ backgroundColor: typeColor }}>
                    {event.registration_required ? 'Register Now' : 'View Details'}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="empty-state">
          <h3>No events found</h3>
          <p>Check back later for upcoming congregation events.</p>
        </div>
      )}
    </div>
  );
}