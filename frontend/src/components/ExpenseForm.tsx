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
  const [cardholderName, setCardholderName] = useState('');
  const [startDate, setStartDate] = useState('');
  const [expectedExpenses, setExpectedExpenses] = useState('');

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
      <div className="form-columns">
        <div className="form-column-left">
          <div className="form-group">
            <label htmlFor="cardholderName">Cardholder Name</label>
            <select
              id="cardholderName"
              value={cardholderName}
              onChange={(e) => setCardholderName(e.target.value)}
              required
            >
              <option value="">Select Cardholder</option>
              <option value="Shammas Ahmed (Treasurer)">Shammas Ahmed (Treasurer)</option>
              <option value="Gavin Firestone (Treasurer)">Gavin Firestone (Treasurer)</option>
              <option value="Alex Rubio (President)">Alex Rubio (President)</option>
              <option value="Sami Johnson (IVP)">Sami Johnson (IVP)</option>
              <option value="Tori Xiao (EVP)">Tori Xiao (EVP)</option>
              <option value="Eman Fayyaz (CVP)">Eman Fayyaz (CVP)</option>
            </select>
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
        </div>

        <div className="form-column-right">
          <div className="form-group">
            <label htmlFor="expectedExpenses">Expected Expenses (paste from Kristen's email)</label>
            <textarea
              id="expectedExpenses"
              value={expectedExpenses}
              onChange={(e) => setExpectedExpenses(e.target.value)}
              rows={10}
              placeholder="Ex. 11/1/25 - Target - $25.00"
              required
            />
            <small>Format: MM/DD/YY - Vendor - $Price (one per line)</small>
          </div>
        </div>
      </div>

      <div className="form-button-container">
        <button type="submit" className="submit-button">
          Reconcile Expenses
        </button>
      </div>
    </form>
  );
}
