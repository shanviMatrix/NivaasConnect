import './AdminDashboard.css'

function AdminDashboard({ onLogout }) {
  return (
    <div className="admin-dashboard">

      <aside className="admin-sidebar">
        <div className="admin-brand">
          <h2>NivaasConnect</h2>
          <p>ADMINISTRATION</p>
        </div>

        <nav className="admin-menu">
          <a href="#overview" className="active">▦ Dashboard</a>
          <a href="#residents">♙ Residents & Flats</a>
          <a href="#complaints">☷ Complaints</a>
          <a href="#visitors">♧ Visitor Records</a>
          <a href="#maintenance">₹ Maintenance & Payments</a>
          <a href="#notices">▤ Notices & Events</a>
          <a href="#reports">▥ Reports & Analytics</a>
        </nav>

        <button className="admin-logout" onClick={onLogout}>
          ↪ Logout
        </button>
      </aside>

      <main className="admin-main">

        <header className="admin-topbar">
          <div>
            <p className="admin-date">SOCIETY MANAGEMENT</p>
            <h2>Administration Overview</h2>
          </div>

          <div className="admin-profile">
            <div className="admin-avatar">A</div>
            <div>
              <strong>Society Admin</strong>
              <p>Administrator</p>
            </div>
          </div>
        </header>

        <section className="admin-welcome">
          <div>
            <p>ADMIN CONTROL PANEL</p>
            <h1>Good Evening, Administrator</h1>
            <span>Here's what's happening in your society today.</span>
          </div>
          <div className="admin-welcome-icon">⌂</div>
        </section>

        <section className="admin-stats">
          <div className="admin-stat-card">
            <span>Total Residents</span>
            <h2>248</h2>
            <p>Registered members</p>
          </div>

          <div className="admin-stat-card">
            <span>Total Flats</span>
            <h2>120</h2>
            <p>Across all blocks</p>
          </div>

          <div className="admin-stat-card">
            <span>Pending Complaints</span>
            <h2>08</h2>
            <p>Require attention</p>
          </div>

          <div className="admin-stat-card">
            <span>Visitors Inside</span>
            <h2>12</h2>
            <p>Currently in society</p>
          </div>
        </section>

        <section className="admin-content-grid">

          <div className="admin-panel">
            <div className="admin-panel-heading">
              <div>
                <h3>Recent Complaints</h3>
                <p>Latest resident requests</p>
              </div>
              <a href="#complaints">View all</a>
            </div>

            <div className="admin-table-wrap">
              <table className="admin-table">
                <thead>
                  <tr>
                    <th>Complaint</th>
                    <th>Flat</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Water leakage</td>
                    <td>A-204</td>
                    <td><span className="admin-status pending">Pending</span></td>
                  </tr>
                  <tr>
                    <td>Lift maintenance</td>
                    <td>B-103</td>
                    <td><span className="admin-status progress">In Progress</span></td>
                  </tr>
                  <tr>
                    <td>Street lighting</td>
                    <td>C-301</td>
                    <td><span className="admin-status resolved">Resolved</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div className="admin-panel admin-activity">
            <h3>Society Overview</h3>
            <p>Current management summary</p>

            <div className="admin-activity-item">
              <span className="activity-dot green"></span>
              <div>
                <strong>Maintenance Collection</strong>
                <p>₹2,40,000 collected this month</p>
              </div>
            </div>

            <div className="admin-activity-item">
              <span className="activity-dot amber"></span>
              <div>
                <strong>Pending Payments</strong>
                <p>18 residents have outstanding dues</p>
              </div>
            </div>

            <div className="admin-activity-item">
              <span className="activity-dot blue"></span>
              <div>
                <strong>Visitor Activity</strong>
                <p>36 visitor entries recorded today</p>
              </div>
            </div>
          </div>

        </section>

        <footer className="admin-footer">
          NivaasConnect · Community • Care • Together
        </footer>

      </main>
    </div>
  )
}

export default AdminDashboard