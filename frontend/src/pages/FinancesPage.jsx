import { useEffect, useState } from 'react';
import { apiRequest } from '../api/client';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';
import EmptyState from '../components/EmptyState';

const list = (value) => Array.isArray(value) ? value : value?.results || [];
const money = (value) => Number(value || 0).toLocaleString(undefined, { minimumFractionDigits: 2 });

export default function FinancesPage() {
  const [state, setState] = useState({ income: [], expenses: [], summary: null });
  const [loading, setLoading] = useState(true); const [error, setError] = useState('');
  useEffect(() => { Promise.all([apiRequest('/api/finances/income/'), apiRequest('/api/finances/expenses/'), apiRequest('/api/finances/income/summary/')]).then(([income, expenses, summary]) => setState({ income: list(income), expenses: list(expenses), summary })).catch((e) => setError(e.message)).finally(() => setLoading(false)); }, []);
  if (loading) return <Loading message="Loading finances..." />;
  return <div className="page-container"><div className="page-header"><h1>Finances</h1><p>Review recorded income and expense activity.</p></div>{error && <ErrorMessage message={error} />}<div className="summary-banner"><strong>Total income</strong><span>{money(state.summary?.total_income)}</span></div><section><h2>Income</h2>{state.income.length ? <div className="list-grid">{state.income.map((item) => <article className="card" key={item.id}><h3>{item.category_name || `Category #${item.category}`}</h3><p>{money(item.amount)} · {item.payment_method}</p><p>{item.notes || item.reference_number || 'No notes'}</p></article>)}</div> : <EmptyState title="No income records" />}</section><section><h2>Expenses</h2>{state.expenses.length ? <div className="list-grid">{state.expenses.map((item) => <article className="card" key={item.id}><h3>{item.title}</h3><p>{money(item.amount)} · {item.status}</p><p>{item.description || 'No description'}</p></article>)}</div> : <EmptyState title="No expense records" />}</section></div>;
}
