import { useState } from 'react'
import './App.css'
import Login from './Login'
import ResidentDashboard from './ResidentDashboard'
import AdminDashboard from './AdminDashboard'
import SecurityDashboard from './SecurityDashboard'

function App() {

  const [showLogin, setShowLogin] = useState(false)
const [showResidentDashboard, setShowResidentDashboard] = useState(false)
const [showAdminDashboard, setShowAdminDashboard] = useState(false)
const [showSecurityDashboard, setShowSecurityDashboard] = useState(false)
if (showAdminDashboard) {
  return (
    <AdminDashboard
      onLogout={() => {
        setShowAdminDashboard(false)
        setShowLogin(true)
      }}
    />
  )
}
if (showSecurityDashboard) {
  return (
    <SecurityDashboard
      onLogout={() => {
        setShowSecurityDashboard(false)
        setShowLogin(true)
      }}
    />
  )
}
if (showResidentDashboard) {
  return (
    <ResidentDashboard
      onLogout={() => {
        setShowResidentDashboard(false)
        setShowLogin(true)
      }}
    />
  )
}
if (showLogin) {
  return (
    <Login
  onBack={() => setShowLogin(false)}
  onLogin={(role) => {
  setShowLogin(false)

  if (role === 'Admin') {
    setShowAdminDashboard(true)
  } else if (role === 'Resident') {
    setShowResidentDashboard(true)
  } else if (role === 'Security Guard') {
    setShowSecurityDashboard(true)
  }
}}
/>
  )
}

  return (
    <div className="website">

      {/* Navigation Bar */}
      <nav className="navbar">
        <div className="logo">
          <span className="logo-icon">⌂</span>
          <div>
            <h2>NivaasConnect</h2>
            <p>Community • Care • Together</p>
          </div>
        </div>

        <div className="nav-links">
          <a href="#home">Home</a>
          <a href="#about">About Us</a>
          <a href="#features">Features</a>
          <a href="#contact">Contact</a>
        </div>

        <button
  className="login-btn"
  onClick={() => setShowLogin(true)}
>
  Login
</button>
      </nav>

      {/* Hero Section */}
      <section className="hero" id="home">
        <div className="hero-content">
          <span className="tagline">WELCOME TO YOUR COMMUNITY</span>

          <h1>
            A smarter, safer and more
            <span> connected neighbourhood.</span>
          </h1>

          <p>
            Manage your community with ease. Connect with neighbours,
            manage visitors, pay maintenance bills and stay updated
            with everything happening in your society.
          </p>

          <div className="hero-buttons">
            <button className="primary-btn">Explore Features →</button>
            <button className="secondary-btn">Learn More</button>
          </div>
        </div>

        <div className="hero-card">
          <div className="home-icon">🏡</div>
          <h2>Your Community, One Place.</h2>
          <p>Everything your neighbourhood needs, connected together.</p>

          <div className="mini-stats">
            <div>
              <strong>24/7</strong>
              <small>Security</small>
            </div>
            <div>
              <strong>Easy</strong>
              <small>Payments</small>
            </div>
            <div>
              <strong>Smart</strong>
              <small>Community</small>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features" id="features">
        <div className="section-heading">
          <span>OUR SERVICES</span>
          <h2>Everything your society needs</h2>
          <p>Simple solutions for a better community experience.</p>
        </div>

        <div className="feature-grid">
          <div className="feature-card">
            <div className="feature-icon">👥</div>
            <h3>Resident Management</h3>
            <p>Manage residents, flats and community information easily.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🛡️</div>
            <h3>Visitor Management</h3>
            <p>Keep track of visitor entries, exits and approvals.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">💳</div>
            <h3>Maintenance Payments</h3>
            <p>View monthly bills, pay dues and check payment history.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📝</div>
            <h3>Complaints</h3>
            <p>Raise complaints and track their resolution status.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📅</div>
            <h3>Facility Booking</h3>
            <p>Book community spaces and manage your reservations.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📢</div>
            <h3>Notices & Events</h3>
            <p>Stay informed about important updates and society events.</p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer id="contact">
        <h2>NivaasConnect</h2>
        <p>Community • Care • Together</p>
        <p>© 2026 NivaasConnect. All rights reserved.</p>
      </footer>

    </div>
  )
}

export default App
