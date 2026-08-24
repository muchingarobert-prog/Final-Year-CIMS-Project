import { Link, useNavigate } from 'react-router-dom';

export default function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem('cims_access_token');

  const handleLogout = () => {
    localStorage.removeItem('cims_access_token');
    localStorage.removeItem('cims_refresh_token');
    navigate('/');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <img 
            src="/images/church-emblem.png" 
            alt="UNZA CIMS Logo" 
            className="logo-emblem"
          />
          <span className="logo-text">UNZA CIMS</span>
        </Link>
        
        <div className="navbar-menu">
          {token ? (
            <>
              <Link to="/dashboard" className="nav-link">Dashboard</Link>
              <Link to="/events" className="nav-link">Events</Link>
              <Link to="/committees" className="nav-link">Committees</Link>
              <Link to="/members" className="nav-link">Members</Link>
              <button onClick={handleLogout} className="nav-link logout-btn">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="nav-link">Login</Link>
              <Link to="/register" className="nav-link btn-primary">
                Get Started
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}