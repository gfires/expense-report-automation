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
        <div className="header-content">
          <img src="/bakerlogo.png" alt="Baker Logo" className="header-logo" />
          <h1>Baker Expense Report Helper</h1>
          <img src="/bakerlogo.png" alt="Baker Logo" className="header-logo" />
        </div>
      </header>

      <main>
        {error && (
          <div className="error-banner">
            <strong>Error:</strong> {error}
            <button onClick={handleReset}>Try Again</button>
          </div>
        )}

        <ExpenseForm
          onSuccess={handleReconcile}
          onError={handleError}
          onLoadingChange={setLoading}
        />

        {loading && <div className="loading-spinner">Processing...</div>}

        {results && <ResultsView results={results} />}
      </main>
    </div>
  );
}

export default App;
