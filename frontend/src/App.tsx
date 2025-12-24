import { useState } from 'react';
import ExpenseForm from './components/ExpenseForm';
import ResultsView from './components/ResultsView';
import type { ReconcileResponse } from './types';
import './styles/App.css';

function App() {
  const [results, setResults] = useState<ReconcileResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleReconcile = (response: ReconcileResponse) => {
    setResults(response);
    setError(null);
  };

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
    setResults(null);
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
  };

  return (
    <div className="app">
      <header>
        <h1>Expense Reconciliation</h1>
      </header>

      <main>
        {error && (
          <div className="error-banner">
            <strong>Error:</strong> {error}
            <button onClick={handleReset}>Try Again</button>
          </div>
        )}

        {!results && !error && (
          <ExpenseForm
            onSuccess={handleReconcile}
            onError={handleError}
            onLoadingChange={setLoading}
          />
        )}

        {results && (
          <>
            <button onClick={handleReset} className="back-button">
              New Reconciliation
            </button>
            <ResultsView results={results} />
          </>
        )}

        {loading && <div className="loading-spinner">Processing...</div>}
      </main>
    </div>
  );
}

export default App;
