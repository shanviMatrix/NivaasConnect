
import { useState } from 'react'
import './Maintenance.css'

function Maintenance({ onBack }) {
  const [message, setMessage] = useState('')

  const handlePayment = () => {
    setMessage('Payment gateway will be connected with the backend.')
  }

  return (
    <div className="maintenance-page">

      {/* Header */}
      <header className="maintenance-header">
        <div>
          <p className="maintenance-breadcrumb">
            NivaasConnect / Resident / Maintenance
          </p>
          <h1>Maintenance & Payments</h1>
          <p className="maintenance-subtitle">
            Manage your monthly society maintenance and payment records.
          </p>
        </div>

        <button className="maintenance-back" onClick={onBack}>
          ← Back to Dashboard
        </button>
      </header>

      {/* Summary */}
      <section className="maintenance-summary">

        <div className="maintenance-summary-card">
          <span>OUTSTANDING AMOUNT</span>
          <h2>₹2,500</h2>
          <small>November 2026 maintenance</small>
        </div>

        <div className="maintenance-summary-card">
          <span>NEXT DUE DATE</span>
          <h2>10 Nov 2026</h2>
          <small>Upcoming payment deadline</small>
        </div>

        <div className="maintenance-summary-card">
          <span>PAYMENT STATUS</span>
          <h2 className="maintenance-pending">Pending</h2>
          <small>Payment not yet received</small>
        </div>

      </section>

      {/* Current Bill */}
      <section className="maintenance-current-bill">

        <div className="maintenance-section-heading">
          <div>
            <span>CURRENT INVOICE</span>
            <h2>November 2026 Bill</h2>
          </div>

          <span className="maintenance-status">Payment Pending</span>
        </div>

        <div className="maintenance-bill-info">
          <div>
            <small>Invoice Number</small>
            <strong>NC-MNT-2026-011</strong>
          </div>

          <div>
            <small>Flat Number</small>
            <strong>A-204</strong>
          </div>

          <div>
            <small>Billing Period</small>
            <strong>November 2026</strong>
          </div>

          <div>
            <small>Due Date</small>
            <strong>10 November 2026</strong>
          </div>
        </div>

        <div className="maintenance-charge-heading">
          <h3>Bill Breakdown</h3>
          <span>Amount</span>
        </div>

        <div className="maintenance-charge-row">
          <span>Monthly Maintenance</span>
          <strong>₹2,000</strong>
        </div>

        <div className="maintenance-charge-row">
          <span>Common Area & Security</span>
          <strong>₹300</strong>
        </div>

        <div className="maintenance-charge-row">
          <span>Water & Utility Charges</span>
          <strong>₹200</strong>
        </div>

        <div className="maintenance-total">
          <strong>Total Amount Due</strong>
          <strong>₹2,500</strong>
        </div>

        <div className="maintenance-payment-action">
          <div>
            <small>Total Payable</small>
            <h2>₹2,500</h2>
          </div>

          <button onClick={handlePayment}>
            Proceed to Payment →
          </button>
        </div>

        {message && (
          <p className="maintenance-message">{message}</p>
        )}

      </section>

      {/* Payment History */}
      <section className="maintenance-history">

        <div className="maintenance-section-heading">
          <div>
            <span>TRANSACTION RECORDS</span>
            <h2>Payment History</h2>
          </div>
        </div>

        <div className="maintenance-table-wrapper">
          <table className="maintenance-table">
            <thead>
              <tr>
                <th>Invoice</th>
                <th>Month</th>
                <th>Amount</th>
                <th>Payment Date</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              <tr>
                <td>NC-MNT-2026-010</td>
                <td>October 2026</td>
                <td>₹2,500</td>
                <td>05 Oct 2026</td>
                <td>
                  <span className="paid-status">Paid</span>
                </td>
              </tr>

              <tr>
                <td>NC-MNT-2026-009</td>
                <td>September 2026</td>
                <td>₹2,500</td>
                <td>07 Sep 2026</td>
                <td>
                  <span className="paid-status">Paid</span>
                </td>
              </tr>

              <tr>
                <td>NC-MNT-2026-008</td>
                <td>August 2026</td>
                <td>₹2,400</td>
                <td>06 Aug 2026</td>
                <td>
                  <span className="paid-status">Paid</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

      </section>

      <footer className="maintenance-footer">
        © 2026 NivaasConnect. Community • Care • Together.
      </footer>

    </div>
  )
}

export default Maintenance
