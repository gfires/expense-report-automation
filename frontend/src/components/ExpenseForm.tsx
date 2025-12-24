import { useState } from 'react';
import type { FormEvent } from 'react';
import { reconcileExpenses } from '../api';
import type { ReconcileResponse } from '../types';

interface ExpenseFormProps {
  onSuccess: (response: ReconcileResponse) => void;
  onError: (error: string) => void;
  onLoadingChange: (loading: boolean) => void;
}

export default function ExpenseForm({
  onSuccess,
  onError,
  onLoadingChange,
}: ExpenseFormProps) {
  const [cardholderName, setCardholderName] = useState('Gavin Firestone (Treasurer)');
  const [startDate, setStartDate] = useState('2025-11-01');
  const [expectedExpenses, setExpectedExpenses] = useState(
    '11/1/25 - Trader Joe\'s - $25.25\n11/3/25 - Target - $9.99'
  );

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    onLoadingChange(true);

    try {
      const response = await reconcileExpenses({
        cardholder_name: cardholderName,
        start_date: startDate,
        expected_expenses: expectedExpenses,
      });
      onSuccess(response);
    } catch (error) {
      if (error instanceof Error) {
        onError(error.message);
      } else {
        onError('An unexpected error occurred');
      }
    } finally {
      onLoadingChange(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="expense-form">
      <div className="form-group">
        <label htmlFor="cardholderName">Cardholder Name</label>
        <input
          id="cardholderName"
          type="text"
          value={cardholderName}
          onChange={(e) => setCardholderName(e.target.value)}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="startDate">Start Date</label>
        <input
          id="startDate"
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="expectedExpenses">Expected Expenses</label>
        <textarea
          id="expectedExpenses"
          value={expectedExpenses}
          onChange={(e) => setExpectedExpenses(e.target.value)}
          rows={10}
          placeholder="11/1/25 - Vendor - $25.00"
          required
        />
        <small>Format: MM/DD/YY - Vendor - $Price (one per line)</small>
      </div>

      <button type="submit" className="submit-button">
        Reconcile Expenses
      </button>
    </form>
  );
}
