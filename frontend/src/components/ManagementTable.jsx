export function getDisplayName(record) {
  return record?.full_name || [record?.first_name, record?.last_name].filter(Boolean).join(' ') || record?.username || 'Unnamed record';
}

export function formatDate(value, options = {}) {
  if (!value) return 'Not available';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleDateString(undefined, { dateStyle: 'medium', ...options });
}

export function formatDateTime(value) {
  if (!value) return 'Not scheduled';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' });
}

export function StatusBadge({ children, tone = 'neutral' }) {
  return <span className={`status-badge status-${tone}`}>{children}</span>;
}

export default function ManagementTable({ columns, rows, rowKey = 'id', emptyMessage = 'No records found.' }) {
  if (!rows.length) return <div className="table-empty">{emptyMessage}</div>;

  return (
    <div className="table-scroll">
      <table className="management-table">
        <thead>
          <tr>{columns.map((column) => <th key={column.key} scope="col">{column.label}</th>)}</tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={row[rowKey] || index}>
              {columns.map((column) => <td key={column.key}>{column.render ? column.render(row) : row[column.key] || '—'}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function PageToolbar({ search, onSearch, placeholder = 'Search records...', children }) {
  return (
    <div className="page-toolbar">
      <label className="search-field">
        <span aria-hidden="true">⌕</span>
        <input value={search} onChange={(event) => onSearch(event.target.value)} placeholder={placeholder} aria-label={placeholder} />
      </label>
      {children && <div className="toolbar-actions">{children}</div>}
    </div>
  );
}
