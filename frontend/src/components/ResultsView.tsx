import type { ReconcileResponse } from '../types';
import ExpenseTable from './ExpenseTable';

interface ResultsViewProps {
  results: ReconcileResponse;
}

export default function ResultsView({ results }: ResultsViewProps) {
  return (
    <div className="results-view">
      <section className="results-section">
        <h2>✅ Matched Expenses ({results.matched.length})</h2>
        {results.matched.length === 0 ? (
          <p className="empty-message">No matches found</p>
        ) : (
          results.matched.map((match, index) => (
            <div key={index} className="match-pair">
              <div className="expected">
                <h4>Expected</h4>
                <p className="inline-info">
                  <strong>Date:</strong> {match.expected.date} | <strong>Vendor:</strong> {match.expected.vendor} | <strong>Price:</strong> ${match.expected.price.toFixed(2)}
                </p>
              </div>
              <div className="actual">
                <h4>Actual</h4>
                <p className="inline-info">
                  <strong>Date:</strong> {match.actual.date} | <strong>Vendor:</strong> {match.actual.vendor} | <strong>Price:</strong> ${match.actual.price.toFixed(2)}
                </p>
                <p><strong>Activity:</strong> {match.actual.activity}</p>
                <p><strong>Description:</strong> {match.actual.description}</p>
                {(match.actual.receipts.length > 0 || match.actual.needsAffidavit) && (
                  <div>
                    <strong>Receipts:</strong>
                    <ul>
                      {match.actual.receipts.map((receipt, i) => (
                        <li key={i}>
                          <a href={receipt} target="_blank" rel="noopener noreferrer">
                            Receipt {i + 1}
                          </a>
                        </li>
                      ))}
                      {match.actual.needsAffidavit && (
                        <li>Affidavit</li>
                      )}
                    </ul>
                  </div>
                )}
                {match.actual.flyer && (
                  <p>
                    <strong>Flyer:</strong>{' '}
                    <a href={match.actual.flyer} target="_blank" rel="noopener noreferrer">
                      View Flyer
                    </a>
                  </p>
                )}
              </div>
            </div>
          ))
        )}
      </section>

      <section className="results-section">
        <h2>⚠️ Missing Expected Expenses ({results.unmatched_expected.length})</h2>
        {results.unmatched_expected.length === 0 ? (
          <p className="success-message">All expected expenses matched!</p>
        ) : (
          <ExpenseTable
            columns={[
              { key: 'date', label: 'Date' },
              { key: 'vendor', label: 'Vendor' },
              { key: 'price', label: 'Price', formatter: (val) => `$${(val as number).toFixed(2)}` },
            ]}
            data={results.unmatched_expected}
          />
        )}
      </section>

      <section className="results-section">
        <h2>➕ Extra Actual Expenses ({results.unmatched_actual.length})</h2>
        {results.unmatched_actual.length === 0 ? (
          <p className="success-message">No extra expenses found!</p>
        ) : (
          <ExpenseTable
            columns={[
              { key: 'date', label: 'Date' },
              { key: 'vendor', label: 'Vendor' },
              { key: 'price', label: 'Price', formatter: (val) => `$${(val as number).toFixed(2)}` },
              { key: 'activity', label: 'Activity' },
              { key: 'description', label: 'Description' },
            ]}
            data={results.unmatched_actual}
          />
        )}
      </section>
    </div>
  );
}
