import DataPage, { asList } from '../components/DataPage';
import { buildApiUrl } from '../api/client';

export default function DocumentsPage() {
  return <DataPage title="Documents" description="Access congregation documents available to your account." endpoint="/api/documents/recent/" transform={asList} renderItem={(document) => <article className="card" key={document.id}><h2>{document.title}</h2><p>{document.description || document.document_type}</p><p>Version {document.version} · {document.download_count} downloads</p>{document.file && <a className="btn btn-secondary" href={document.file.startsWith('http') ? document.file : buildApiUrl(document.file)} target="_blank" rel="noreferrer">Download</a>}</article>} />;
}
