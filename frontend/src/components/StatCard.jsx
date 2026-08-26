export default function StatCard({ icon, label, value, accent = 'blue' }) {
  return (
    <div className={`stat-card stat-card-${accent}`}>
      <div className="stat-icon">{icon}</div>
      <div className="stat-info">
        <div className="stat-number">{value ?? 0}</div>
        <div className="stat-label">{label}</div>
      </div>
    </div>
  );
}
