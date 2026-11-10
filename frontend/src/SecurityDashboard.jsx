
import { useState } from 'react'
import './SecurityDashboard.css'

function SecurityDashboard({ onLogout }) {
  const [visitors, setVisitors] = useState([
    {
      id: 1,
      name: 'Rahul Sharma',
      flat: 'A-204',
      purpose: 'Personal Visit',
      entry: '09:30 AM',
      status: 'Inside'
    },
    {
      id: 2,
      name: 'Amit Kumar',
      flat: 'B-103',
      purpose: 'Delivery',
      entry: '10:15 AM',
      status: 'Inside'
    },
    {
      id: 3,
      name: 'Neha Verma',
      flat: 'C-301',
      purpose: 'Guest',
      entry: '08:45 AM',
      status: 'Exited'
    }
  ])

  const [name, setName] = useState('')
  const [flat, setFlat] = useState('')
  const [purpose, setPurpose] = useState('Personal Visit')
  const [message, setMessage] = useState('')

  const insideCount = visitors.filter(
    visitor => visitor.status === 'Inside'
  ).length

  const handleEntry = (e) => {
    e.preventDefault()

    if (!name.trim() || !flat.trim()) {
      setMessage('Please enter visitor name and flat number.')
      return
    }

    const newVisitor = {
      id: Date.now(),
      name: name.trim(),
      flat: flat.trim().toUpperCase(),
      purpose,
      entry: new Date().toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
      }),
      status: 'Inside'
    }

    setVisitors([newVisitor, ...visitors])
    setName('')
    setFlat('')
    setPurpose('Personal Visit')
    setMessage('Visitor entry registered successfully.')
  }

  const handleExit = (id) => {
    setVisitors(visitors.map(visitor =>
      visitor.id === id
        ? { ...visitor, status: 'Exited' }
        : visitor
    ))
  }

  return (
    <div className="security-dashboard">

      <aside className="security-sidebar">
        <div className="security-brand">
          <h2>NivaasConnect</h2>
          <p>SECURITY MANAGEMENT</p>
        </div>

        <nav className="security-menu">
          <a href="#security-overview" className="active">Dashboard</a>
          <a href="#visitor-entry">Visitor Entry</a>
          <a href="#current-visitors">Visitors Inside</a>
          <a href="#visitor-history">Visitor History</a>
        </nav>

        <button className="security-logout" onClick={onLogout}>
          Logout
        </button>
      </aside>

      <main className="security-main">

        <header className="security-topbar">
          <div>
            <p className="security-eyebrow">SECURITY CONTROL PANEL</p>
            <h1>Security Dashboard</h1>
          </div>

          <div className="security-profile">
            <div className="security-avatar">G</div>
            <div>
              <strong>Security Guard</strong>
              <p>Gate Management</p>
            </div>
          </div>
        </header>

        <section className="security-welcome" id="security-overview">
          <div>
            <span>GATE OPERATIONS</span>
            <h2>Welcome, Security Team</h2>
            <p>Manage visitor movement and maintain society security records.</p>
          </div>
          <div className="security-welcome-icon">⌂</div>
        </section>

        <section className="security-stats">
          <div className="security-stat-card">
            <span>Currently Inside</span>
            <h2>{insideCount}</h2>
            <p>Active visitor entries</p>
          </div>

          <div className="security-stat-card">
            <span>Total Records</span>
            <h2>{visitors.length}</h2>
            <p>Visitor records in this session</p>
          </div>

          <div className="security-stat-card">
            <span>Visitors Exited</span>
            <h2>{visitors.filter(v => v.status === 'Exited').length}</h2>
            <p>Completed visits</p>
          </div>
        </section>

        <section className="security-entry-panel" id="visitor-entry">
          <div className="security-section-heading">
            <div>
              <span>GATE REGISTER</span>
              <h2>Register New Visitor</h2>
            </div>
          </div>

          <form className="security-entry-form" onSubmit={handleEntry}>
            <div>
              <label>Visitor Name</label>
              <input
                type="text"
                placeholder="Enter visitor's full name"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

            <div>
              <label>Flat Number</label>
              <input
                type="text"
                placeholder="Example: A-204"
                value={flat}
                onChange={(e) => setFlat(e.target.value)}
              />
            </div>

            <div>
              <label>Purpose of Visit</label>
              <select
                value={purpose}
                onChange={(e) => setPurpose(e.target.value)}
              >
                <option>Personal Visit</option>
                <option>Delivery</option>
                <option>Maintenance Work</option>
                <option>Guest</option>
                <option>Other</option>
              </select>
            </div>

            <button type="submit">+ Register Entry</button>
          </form>

          {message && <p className="security-message">{message}</p>}
        </section>

        <section className="security-visitors-panel" id="current-visitors">
          <div className="security-section-heading">
            <div>
              <span>LIVE VISITOR REGISTER</span>
              <h2>Visitor Records</h2>
            </div>
            <span className="security-live-label">● Session Records</span>
          </div>

          <div className="security-table-wrap">
            <table className="security-table">
              <thead>
                <tr>
                  <th>Visitor Name</th>
                  <th>Flat</th>
                  <th>Purpose</th>
                  <th>Entry Time</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {visitors.map(visitor => (
                  <tr key={visitor.id}>
                    <td><strong>{visitor.name}</strong></td>
                    <td>{visitor.flat}</td>
                    <td>{visitor.purpose}</td>
                    <td>{visitor.entry}</td>
                    <td>
                      <span className={
                        visitor.status === 'Inside'
                          ? 'security-status-inside'
                          : 'security-status-exited'
                      }>
                        {visitor.status}
                      </span>
                    </td>
                    <td>
                      {visitor.status === 'Inside' ? (
                        <button
                          className="security-exit-btn"
                          onClick={() => handleExit(visitor.id)}
                        >
                          Mark Exit
                        </button>
                      ) : (
                        <span className="security-completed">Completed</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <footer className="security-footer" id="visitor-history">
          NivaasConnect · Security Management
        </footer>

      </main>
    </div>
  )
}

export default SecurityDashboard
