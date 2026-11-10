import { useState } from 'react'
import './Complaints.css'

function Complaints({ onBack }) {
  const [category, setCategory] = useState('Maintenance')
  const [description, setDescription] = useState('')
  const [complaints, setComplaints] = useState([
    {
      id: 'CMP-1024',
      title: 'Water leakage in kitchen',
      category: 'Plumbing',
      date: '02 Nov 2026',
      status: 'In Progress'
    },
    {
      id: 'CMP-1018',
      title: 'Lift not working properly',
      category: 'Electrical',
      date: '28 Oct 2026',
      status: 'Resolved'
    }
  ])

  const handleSubmit = (e) => {
    e.preventDefault()

    if (!description.trim()) return

    const newComplaint = {
      id: `CMP-${Date.now().toString().slice(-5)}`,
      title: description.trim(),
      category,
      date: new Date().toLocaleDateString('en-IN', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
      }),
      status: 'Pending'
    }

    setComplaints([newComplaint, ...complaints])
    setDescription('')
  }

  return (
    <div className="complaints-page">
      <header className="complaints-header">
        <div>
          <p className="complaints-eyebrow">RESIDENT SERVICES</p>
          <h1>Complaints & Requests</h1>
          <p>Raise an issue and track its resolution.</p>
        </div>
        <button className="complaints-back" onClick={onBack}>
          ← Back to Dashboard
        </button>
      </header>

      <section className="complaints-summary">
        <div className="complaint-stat">
          <span>Total Complaints</span>
          <strong>{complaints.length}</strong>
        </div>
        <div className="complaint-stat">
          <span>Pending</span>
          <strong>{complaints.filter(c => c.status === 'Pending').length}</strong>
        </div>
        <div className="complaint-stat">
          <span>In Progress</span>
          <strong>{complaints.filter(c => c.status === 'In Progress').length}</strong>
        </div>
        <div className="complaint-stat">
          <span>Resolved</span>
          <strong>{complaints.filter(c => c.status === 'Resolved').length}</strong>
        </div>
      </section>

      <div className="complaints-content">
        <section className="complaint-form-card">
          <h2>Raise a New Complaint</h2>
          <p>Provide details so the management team can assist you.</p>

          <form onSubmit={handleSubmit}>
            <label>Complaint Category</label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
            >
              <option>Maintenance</option>
              <option>Plumbing</option>
              <option>Electrical</option>
              <option>Security</option>
              <option>Cleanliness</option>
              <option>Other</option>
            </select>

            <label>Describe Your Issue</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe the issue and its location..."
              rows="5"
              required
            />

            <button type="submit" className="complaint-submit">
              Submit Complaint →
            </button>
          </form>
        </section>

        <section className="complaint-list-card">
          <div className="complaint-list-heading">
            <div>
              <h2>My Complaints</h2>
              <p>Track your submitted requests.</p>
            </div>
            <span>{complaints.length} Records</span>
          </div>

          <div className="complaint-list">
            {complaints.map((complaint) => (
              <article className="complaint-item" key={complaint.id}>
                <div className="complaint-item-top">
                  <span className="complaint-id">{complaint.id}</span>
                  <span className={`complaint-status ${complaint.status.toLowerCase().replace(' ', '-')}`}>
                    {complaint.status}
                  </span>
                </div>
                <h3>{complaint.title}</h3>
                <div className="complaint-meta">
                  <span>{complaint.category}</span>
                  <span>{complaint.date}</span>
                </div>
              </article>
            ))}
          </div>
        </section>
      </div>
    </div>
  )
}

export default Complaints