import { useEffect, useState } from 'react';
import { apiRequest } from '../api/client';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';

const reports = [['Overview', '/api/reports/'], ['Attendance', '/api/reports/attendance/'], ['Committees', '/api/reports/committees/'], ['Events', '/api/reports/events/'], ['Members', '/api/reports/members/'], ['Finances', '/api/reports/finances/']];
export default function ReportsPage() {
  const [data, setData] = useState({}); const [error, setError] = useState(''); const [loading, setLoading] = useState(true);
  useEffect(() => { Promise.all(reports.map(([, endpoint]) => apiRequest(endpoint))).then((values) => setData(Object.fromEntries(reports.map(([name], index) => [name, values[index]])))).catch((e) => setError(e.message)).finally(() => setLoading(false)); }, []);
  if (loading) return <Loading message="Loading reports..." />;
  return <div className="page-container"><div className="page-header"><h1>Reports</h1><p>Operational summaries from the congregation management system.</p></div>{error && <ErrorMessage message={error} />}{!error && <div className="report-grid">{reports.map(([name]) => <article className="card" key={name}><h2>{name}</h2>{Object.entries(data[name] || {}).map(([key, value]) => <p key={key}><strong>{key.replaceAll('_', ' ')}:</strong> {typeof value === 'object' ? JSON.stringify(value) : String(value)}</p>)}</article>)}</div>}</div>;
}
