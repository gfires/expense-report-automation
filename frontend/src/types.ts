export interface ReconcileRequest {
  cardholder_name: string;
  start_date: string;
  expected_expenses: string;
}

export interface ExpectedExpense {
  date: string;
  vendor: string;
  price: number;
}

export interface ReportItem {
  description: string;
  activity: string;
  date: string;
  price: number;
  vendor: string;
  receipts: string[];
  flyer: string;
}

export interface MatchedPair {
  expected: ExpectedExpense;
  actual: ReportItem;
}

export interface ReconcileResponse {
  matched: MatchedPair[];
  unmatched_expected: ExpectedExpense[];
  unmatched_actual: ReportItem[];
}

export type ApiError = {
  detail: string;
}
