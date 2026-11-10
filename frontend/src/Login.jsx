
import { useState } from 'react'
import './Login.css'

function Login({ onBack, onLogin }) {
  const [role, setRole] = useState('Resident')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [message, setMessage] = useState('')

  const handleLogin = (e) => {
    e.preventDefault()

    if (!email.trim() || !password.trim()) {
      setMessage('Please enter your email and password.')
      return
    }

  if (
  role === 'Admin' ||
  role === 'Resident' ||
  role === 'Security Guard'
) {
  onLogin(role)
}
  }

  return (
    <div className="login-page">

      <header className="login-header">
        <button className="brand" onClick={onBack}>
          <span className="brand-symbol">⌂</span>
          <span>
            <strong>NivaasConnect</strong>
            <small>Community • Care • Together</small>
          </span>
        </button>

        <button className="back-home" onClick={onBack}>
          ← Back to Home
        </button>
      </header>

      <main className="login-main">

        <section className="login-intro">
          <span className="login-label">YOUR COMMUNITY, CONNECTED</span>

          <h1>
            Welcome to a
            <span> better way </span>
            of living.
          </h1>

          <p>
            One platform to manage your neighbourhood,
            simplify everyday tasks and bring your
            community closer.
          </p>

          <div className="login-benefits">
            <div>
              <span>01</span>
              <p>Smart Community Management</p>
            </div>

            <div>
              <span>02</span>
              <p>Secure Visitor Management</p>
            </div>

            <div>
              <span>03</span>
              <p>Seamless Maintenance Payments</p>
            </div>
          </div>
        </section>

        <section className="login-form-section">
          <div className="login-form-card">

            <div className="form-heading">
              <span>ACCOUNT ACCESS</span>
              <h2>Sign in</h2>
              <p>Enter your credentials to continue.</p>
            </div>

            <form onSubmit={handleLogin}>

              <label htmlFor="role">Login as</label>

              <select
                id="role"
                value={role}
                onChange={(e) => setRole(e.target.value)}
              >
                <option value="Resident">Resident</option>
                <option value="Admin">Admin</option>
                <option value="Security Guard">Security Guard</option>
              </select>

              <label htmlFor="email">Email Address</label>

              <input
                id="email"
                type="email"
                placeholder="Enter your email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />

              <label htmlFor="password">Password</label>

              <div className="password-wrapper">
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />

                <button
                  type="button"
                  className="show-password"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? 'Hide' : 'Show'}
                </button>
              </div>

              <div className="forgot-password">
                <a href="#forgot-password">Forgot password?</a>
              </div>

              <button type="submit" className="sign-in-btn">
                Sign In <span>→</span>
              </button>

              {message && (
                <p className="login-message">{message}</p>
              )}

            </form>

            <div className="login-security">
              <span>●</span>
              Secure Community Access
            </div>

          </div>
        </section>

      </main>

      <footer className="login-footer">
        © 2026 NivaasConnect. All rights reserved.
      </footer>

    </div>
  )
}

export default Login
