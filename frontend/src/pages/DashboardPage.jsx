import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { apiRequest } from '../api/client';
import { useAuth } from '../context/AuthContext';
import EmptyState from '../components/EmptyState';
import ErrorMessage from '../components/ErrorMessage';
import Loading from '../components/Loading';

const asList = (value) => (Array.isArray(value) ? value : value?.results || value?.data || []);

const formatDate = (value, options) => {
  if (!value) return 'Date to be confirmed';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? 'Date to be confirmed' : new Intl.DateTimeFormat(undefined, options).format(date);
};

const formatEventDate = (value) => formatDate(value, { weekday: 'short', month: 'short', day: 'numeric' });
const formatEventTime = (value) => formatDate(value, { hour: 'numeric', minute: '2-digit' });
const formatNotificationDate = (value) => formatDate(value, { month: 'short', day: 'numeric' });

const sourceRequests = [
  ['summary', '/api/dashboard/'],
  ['events', '/api/events/upcoming/'],
  ['announcements', '/api/announcements/latest/'],
  ['notifications', '/api/notifications/'],
];

const initialData = { summary: null, events: [], announcements: [], notifications: [] };

function SummaryCard({ icon, label, value, description, tone = '' }) {
  return (
    <article className="dashboard-stat-card">
      <div className={`dashboard-stat-icon ${tone}`}>
        <span className="material-symbols-outlined" aria-hidden="true">{icon}</span>
      </div>
      <div>
        <p className="dashboard-stat-label">{label}</p>
        <strong className="dashboard-stat-value">{value ?? '—'}</strong>
        <span className="dashboard-stat-description">{description}</span>
      </div>
    </article>
  );
}

function SectionHeading({ icon, title, linkTo, linkLabel }) {
  return (
    <div className="dashboard-section-heading">
      <div className="dashboard-section-title">
        <span className="material-symbols-outlined" aria-hidden="true">{icon}</span>
        <h2>{title}</h2>
      </div>
      {linkTo && <Link className="dashboard-section-link" to={linkTo}>{linkLabel}</Link>}
    </div>
  );
}

export default function DashboardPage() {
  const { user } = useAuth();
  const [data, setData] = useState(initialData);
  const [failedSources, setFailedSources] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;

    Promise.allSettled(sourceRequests.map(([, path]) => apiRequest(path)))
      .then((results) => {
        if (!active) return;

        const nextData = { ...initialData };
        const failures = [];

        results.forEach((result, index) => {
          const [key] = sourceRequests[index];
          if (result.status === 'fulfilled') {
            nextData[key] = key === 'summary' ? result.value : asList(result.value);
          } else {
            failures.push(key);
          }
        });

        setData(nextData);
        setFailedSources(failures);
        setLoading(false);
      });

    return () => { active = false; };
  }, []);

  if (loading) return <Loading message="Loading your dashboard..." />;

  const firstName = user?.first_name || user?.username || 'there';
  const summary = data.summary || {};
  const visibleAnnouncements = data.announcements.slice(0, 3);
  const visibleNotifications = data.notifications.slice(0, 4);
  const isAdmin = ['SUPER_USER', 'ADMIN_USER', 'HIGH_PRIVILEGE_USER'].includes(user?.role);

  return (
    <div className="page-container dashboard-page">
      {failedSources.length > 0 && <ErrorMessage message="Some dashboard information is temporarily unavailable. Available sections are still shown." />}

      <section className="dashboard-welcome">
        <div>
          <span className="dashboard-eyebrow">UNZA congregation</span>
          <h1>Welcome back, {firstName}</h1>
          <p>Keep an eye on the latest events, announcements, and congregation activity.</p>
        </div>
        <span className="material-symbols-outlined dashboard-welcome-icon" aria-hidden="true">church</span>
      </section>

      <section aria-labelledby="dashboard-summary-title">
        <div className="dashboard-section-heading dashboard-summary-heading">
          <div>
            <span className="dashboard-eyebrow">At a glance</span>
            <h2 id="dashboard-summary-title">Congregation overview</h2>
          </div>
        </div>
        <div className="dashboard-stat-grid">
          <SummaryCard icon="groups" label="Members" value={summary.members} description="Registered members" />
          <SummaryCard icon="event_upcoming" label="Upcoming events" value={summary.upcoming_events} description="Scheduled gatherings" tone="gold" />
          <SummaryCard icon="fact_check" label="Attendance sessions" value={summary.attendance_sessions} description="Recorded sessions" tone="soft" />
          <SummaryCard icon="notifications" label="Unread notifications" value={summary.unread_notifications} description="Needs your attention" tone="alert" />
        </div>
      </section>

      <div className="dashboard-content-grid">
        <section className="dashboard-panel" aria-labelledby="upcoming-events-title">
          <SectionHeading icon="event_upcoming" title="Upcoming events" linkTo="/events" linkLabel="View all" />
          {data.events.length === 0 ? (
            <EmptyState title="No upcoming events" description="New congregation events will appear here when scheduled." />
          ) : (
            <div className="dashboard-event-list">
              {data.events.slice(0, 5).map((event) => (
                <Link className="dashboard-event-row" to="/events" key={event.id}>
                  <div className="dashboard-date-block" aria-hidden="true">
                    <span>{formatDate(event.event_date, { month: 'short' })}</span>
                    <strong>{formatDate(event.event_date, { day: 'numeric' }).replace(/\D/g, '') || '—'}</strong>
                  </div>
                  <div className="dashboard-event-details">
                    <strong>{event.title || 'Congregation event'}</strong>
                    <span>{formatEventDate(event.event_date)} · {formatEventTime(event.event_date)}</span>
                    <small>{event.location || 'Location to be confirmed'}</small>
                  </div>
                  <span className="material-symbols-outlined dashboard-row-arrow" aria-hidden="true">chevron_right</span>
                </Link>
              ))}
            </div>
          )}
        </section>

        <section className="dashboard-panel" aria-labelledby="announcements-title">
          <SectionHeading icon="campaign" title="Announcements" linkTo="/announcements" linkLabel="View all" />
          {visibleAnnouncements.length === 0 ? (
            <EmptyState title="No announcements" description="There are no active announcements to show." />
          ) : (
            <div className="dashboard-announcement-list">
              {visibleAnnouncements.map((announcement) => (
                <article className="dashboard-announcement" key={announcement.id}>
                  <div className="dashboard-announcement-meta">
                    <span>{announcement.target_type === 'COMMITTEE' ? 'Committee' : 'Congregation'}</span>
                    <time dateTime={announcement.created_at}>{formatNotificationDate(announcement.created_at)}</time>
                  </div>
                  <h3>{announcement.title || 'Congregation announcement'}</h3>
                  {(announcement.content || announcement.description) && <p>{announcement.content || announcement.description}</p>}
                </article>
              ))}
            </div>
          )}
        </section>

        <section className="dashboard-panel" aria-labelledby="notifications-title">
          <SectionHeading icon="notifications" title="Recent notifications" linkTo="/notifications" linkLabel="View all" />
          {visibleNotifications.length === 0 ? (
            <EmptyState title="No notifications" description="You are all caught up." />
          ) : (
            <div className="dashboard-notification-list">
              {visibleNotifications.map((notification) => (
                <Link className={`dashboard-notification${notification.is_read ? '' : ' unread'}`} to="/notifications" key={notification.id}>
                  <span className="material-symbols-outlined" aria-hidden="true">{notification.is_read ? 'notifications_none' : 'notifications_active'}</span>
                  <div>
                    <strong>{notification.title || notification.notification_type || 'Notification'}</strong>
                    <p>{notification.message || notification.content || 'You have a new congregation update.'}</p>
                  </div>
                  <time dateTime={notification.created_at}>{formatNotificationDate(notification.created_at)}</time>
                </Link>
              ))}
            </div>
          )}
        </section>

        <section className="dashboard-panel dashboard-quick-actions" aria-labelledby="quick-actions-title">
          <SectionHeading icon="bolt" title="Quick actions" />
          <div className="dashboard-action-list">
            <Link to="/events"><span className="material-symbols-outlined" aria-hidden="true">calendar_add_on</span>Browse events</Link>
            <Link to="/members"><span className="material-symbols-outlined" aria-hidden="true">person_search</span>Member directory</Link>
            <Link to="/announcements"><span className="material-symbols-outlined" aria-hidden="true">campaign</span>Announcements</Link>
            {isAdmin && <Link to="/reports"><span className="material-symbols-outlined" aria-hidden="true">bar_chart</span>Reports</Link>}
          </div>
        </section>
      </div>
    </div>
  );
}
