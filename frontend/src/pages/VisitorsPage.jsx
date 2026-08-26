import DataPage, { asList } from '../components/DataPage';

export default function VisitorsPage() {
  return <DataPage title="Visitors" description="Track visitor follow-up and congregation welcome activity." endpoint="/api/visitors/" transform={asList} renderItem={(visitor) => <article className="card" key={visitor.id}><h2>{visitor.first_name} {visitor.last_name}</h2><p>{visitor.visit_date} · {visitor.gender === 'M' ? 'Male' : 'Female'}</p><p>{visitor.phone_number || visitor.email || 'No contact details'}</p><strong>{visitor.follow_up_status}</strong>{visitor.notes && <p>{visitor.notes}</p>}</article>} />;
}
