import { useEffect, useState } from 'react';
import { apiRequest } from '../api/client';
import Loading from './Loading';
import ErrorMessage from './ErrorMessage';
import EmptyState from './EmptyState';

export function asList(data) {
  return Array.isArray(data) ? data : data?.results || [];
}

export default function DataPage({ title, description, endpoint, renderItem, emptyTitle = 'No records found', transform = asList, actions }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      setData(transform(await apiRequest(endpoint)));
    } catch (requestError) {
      setError(requestError.message || 'Unable to load this section.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [endpoint]);

  return (
    <div className="page-container">
      <div className="page-header page-header-actions">
        <div><h1>{title}</h1>{description && <p>{description}</p>}</div>
        {actions}
      </div>
      {loading && <Loading message={`Loading ${title.toLowerCase()}...`} />}
      {!loading && error && <ErrorMessage message={error} />}
      {!loading && !error && data.length === 0 && <EmptyState title={emptyTitle} />}
      {!loading && !error && data.length > 0 && <div className="list-grid">{data.map(renderItem)}</div>}
    </div>
  );
}
