
import { useState } from 'react'
import './ResidentDashboard.css'
import Maintenance from './Maintenance'
import Complaints from './Complaints'

function ResidentDashboard({ onLogout }) {
  const [showMaintenance, setShowMaintenance] = useState(false)
  const [showComplaints, setShowComplaints] = useState(false)

  if (showMaintenance) {
    return <Maintenance onBack={() => setShowMaintenance(false)} />
  }

  if (showComplaints) {
    return <Complaints onBack={() => setShowComplaints(false)} />
  }
  return (
    <div className="resident-dashboard">

      {/* Sidebar */}
      <aside className="resident-sidebar">
        <div className="resident-brand">
          <span className="resident-brand-icon">⌂</span>
          <div>
            <h2>NivaasConnect</h2>
            <p>COMMUNITY • CARE • TOGETHER</p>
          </div>
        </div>

        <div className="resident-profile">
          <div className="resident-avatar">R</div>
          <div>
            <strong>Resident</strong>
            <small>Community Member</small>
          </div>
        </div>

        <p className="sidebar-label">MAIN MENU</p>

        <nav className="resident-menu">
          <a href="#overview" className="active">▦ Dashboard</a>
          <a
  href="#maintenance"
  onClick={(e) => {
    e.preventDefault()
    setShowMaintenance(true)
  }}
>
  ₹ Maintenance
</a>
          <a href="#visitors">♙ Visitors</a>
          <a
  href="#complaints"
  onClick={(e) => {
    e.preventDefault()
    setShowComplaints(true)
  }}
>
  ☷ Complaints
</a>
          <a href="#facilities">▣ Facility Booking</a>
          <a href="#notices">◉ Notices & Events</a>
        </nav>

        <button className="resident-logout" onClick={onLogout}>
  ↪ Logout
</button>
      </aside>

      {/* Main Content */}
      <main className="resident-main" id="overview">

        <header className="resident-topbar">
          <div>
            <p className="resident-breadcrumb">NivaasConnect / Resident</p>
            <h1>Resident Dashboard</h1>
          </div>

          <div className="resident-top-profile">
            <div className="notification-icon">♧</div>
            <div className="resident-avatar small">R</div>
            <div>
              <strong>Resident</strong>
              <small>Community Member</small>
            </div>
          </div>
        </header>

        <section className="resident-welcome">
          <div>
            <span>THURSDAY, 05 NOVEMBER 2026</span>
            <h2>Welcome back, Resident!</h2>
            <p>Here's what's happening in your community today.</p>
          </div>
          <div className="welcome-decoration">⌂</div>
        </section>

        {/* Summary Cards */}
        <section className="resident-stats">
          <div className="resident-stat-card">
            <span className="stat-icon amber">₹</span>
            <p>Maintenance Due</p>
            <h2>₹2,500</h2>
            <small>Payment pending</small>
          </div>

          <div className="resident-stat-card">
            <span className="stat-icon green">♙</span>
            <p>Visitors Today</p>
            <h2>03</h2>
            <small>Expected entries</small>
          </div>

          <div className="resident-stat-card">
            <span className="stat-icon blue">☷</span>
            <p>My Complaints</p>
            <h2>02</h2>
            <small>1 currently in progress</small>
          </div>

          <div className="resident-stat-card">
            <span className="stat-icon red">▣</span>
            <p>Facility Bookings</p>
            <h2>01</h2>
            <small>Upcoming reservation</small>
          </div>
        </section>

        {/* Lower Sections */}
        <section className="resident-content-grid">

          <div className="resident-panel" id="maintenance">
            <div className="panel-heading">
              <div>
                <span>PAYMENTS</span>
                <h3>Maintenance Overview</h3>
              </div>
              <span className="status-pending">Pending</span>
            </div>

            <div className="payment-amount">₹2,500</div>
            <p className="panel-description">Monthly maintenance • November 2026</p>

            <div className="payment-details">
              <span>Due date</span>
              <strong>10 November 2026</strong>
            </div>

            <button className="resident-primary-btn">
              View Payment Details →
            </button>
          </div>

          <div className="resident-panel" id="notices">
            <div className="panel-heading">
              <div>
                <span>COMMUNITY UPDATES</span>
                <h3>Latest Notices</h3>
              </div>
              <a href="#notices">View all</a>
            </div>

            <div className="notice-item">
              <div className="notice-date">08<br />NOV</div>
              <div>
                <strong>Water Tank Cleaning</strong>
                <p>Scheduled maintenance from 10 AM.</p>
              </div>
            </div>

            <div className="notice-item">
              <div className="notice-date">12<br />NOV</div>
              <div>
                <strong>Community Meeting</strong>
                <p>Monthly residents' meeting in the clubhouse.</p>
              </div>
            </div>
          </div>

          <div className="resident-panel" id="complaints">
            <div className="panel-heading">
              <div>
                <span>SUPPORT</span>
                <h3>My Recent Complaints</h3>
              </div>
              <a href="#complaints">View all</a>
            </div>

            <div className="complaint-item">
              <div>
                <strong>Water leakage</strong>
                <p>Complaint #NC1024</p>
              </div>
              <span className="status-progress">In Progress</span>
            </div>

            <div className="complaint-item">
              <div>
                <strong>Lift maintenance</strong>
                <p>Complaint #NC1021</p>
              </div>
              <span className="status-resolved">Resolved</span>
            </div>
          </div>

          <div className="resident-panel" id="visitors">
            <div className="panel-heading">
              <div>
                <span>SECURITY</span>
                <h3>Visitor Information</h3>
              </div>
            </div>

            <div className="visitor-summary">
              <div>
                <h2>03</h2>
                <p>Expected today</p>
              </div>
              <div>
                <h2>02</h2>
                <p>Currently inside</p>
              </div>
            </div>
            <p className="panel-description">
              Keep track of visitor entries and approvals.
            </p>
          </div>

        </section>

        <footer className="resident-footer">
          © 2026 NivaasConnect. Community • Care • Together.
        </footer>

      </main>
    </div>
  )
}

export default ResidentDashboard
