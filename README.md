# Expense Reconciliation Application

Full-stack web application for reconciling expected expenses against actual expenses from Google Sheets.

## Overview

This application helps you track and reconcile expected expenses with actual purchases. It:
- Parses actual expenses from a Google Sheets spreadsheet
- Matches them against expected expenses you provide
- Categorizes results into matched, missing expected, and extra actual expenses

## Architecture

- **Backend**: FastAPI (Python 3.13)
- **Frontend**: React 18 + TypeScript + Vite
- **Data Source**: Google Sheets (read-only access via export API)

## Prerequisites

- Python 3.13+
- Node.js 18+
- npm or yarn

## Installation

### 1. Install Backend Dependencies

```bash
pip install -r backend/requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 3. Install Root Dependencies (for development orchestration)

```bash
npm install
```

## Development

### Run Both Servers Simultaneously

```bash
npm run dev
```

This will start:
- **Backend** at http://localhost:8000
- **Frontend** at http://localhost:5173

Open http://localhost:5173 in your browser to use the application.

### Run Servers Separately

If you prefer to run them separately:

```bash
# Terminal 1: Backend
uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend && npm run dev
```

## API Documentation

Interactive API documentation is available at http://localhost:8000/docs when the backend is running.

### POST /reconcile

Reconcile expected expenses against actual expenses from Google Sheets.

**Request:**
```json
{
  "cardholder_name": "Gavin Firestone (Treasurer)",
  "start_date": "2025-11-01",
  "expected_expenses": "11/1/25 - Trader Joe's - $25.25\n11/3/25 - Target - $9.99"
}
```

**Response:**
```json
{
  "matched": [
    {
      "expected": {
        "date": "2025-11-01",
        "vendor": "Trader Joe's",
        "price": 25.25
      },
      "actual": {
        "date": "2025-11-01",
        "vendor": "Trader Joe's",
        "price": 25.25,
        "activity": "4600",
        "description": "...",
        "receipts": ["https://..."],
        "flyer": "..."
      }
    }
  ],
  "unmatched_expected": [...],
  "unmatched_actual": [...]
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

## Project Structure

```
.
├── backend/              # FastAPI backend
│   ├── api.py           # Main API with /reconcile endpoint
│   ├── models.py        # Pydantic schemas
│   └── requirements.txt # Backend dependencies
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── api.ts      # API client
│   │   ├── types.ts    # TypeScript types
│   │   └── App.tsx     # Main app
│   ├── vite.config.ts  # Vite configuration
│   └── package.json    # Frontend dependencies
├── models.py            # Core data models (existing)
├── parser.py            # Google Sheets parser (existing)
├── reconcile.py         # Reconciliation logic (existing)
└── package.json         # Root orchestration scripts
```

## Core Functionality

### 1. Parse Google Sheets
Extracts expense data for a specific cardholder from a hardcoded Google Sheets URL.

### 2. Match Expenses
Two-phase matching algorithm:
- **Phase 1**: Exact price match where `price == price AND actual_date >= expected_date`
- **Phase 2**: Fuzzy matching where `|price_diff| <= $1.00 AND actual_date >= expected_date AND vendor_similarity >= 75%`

### 3. Display Results
Three categories:
- **Matched expenses**: Expected + actual pairs
- **Unmatched expected expenses**: Missing from actual purchases
- **Unmatched actual expenses**: Extra purchases not in expected list

## Configuration

### Hardcoded Spreadsheet URL

The Google Sheets URL is hardcoded in [backend/api.py](backend/api.py:31):

```python
HARDCODED_SPREADSHEET = "https://docs.google.com/spreadsheets/d/1DVerqZwwyPQY0aLVS2PI_5GItN-5f3uQex4JoJ_RLbE/edit?resourcekey=&gid=1857220607#gid=1857220607"
```

To use a different spreadsheet, update this constant.

### Matching Parameters

Price tolerance and vendor similarity thresholds are set in [backend/api.py](backend/api.py:73-74):

```python
price_tolerance=1.00       # Max price difference: $1.00
similarity_threshold=0.75  # Min vendor similarity: 75%
```

## Usage Guide

1. **Enter Cardholder Name**: The name used to filter transactions in the spreadsheet
2. **Select Start Date**: Transactions from this date forward will be included
3. **Paste Expected Expenses**: One per line, format: `MM/DD/YY - Vendor - $Price`
4. **Click "Reconcile Expenses"**: The app will process and display results

### Expected Expenses Format

```
11/1/25 - Trader Joe's - $25.25
11/3/25 - Target - $9.99
11/5/25 - $15.00 - Amazon
```

Both `MM/DD/YY - Vendor - $Price` and `MM/DD/YY - $Price - Vendor` formats are supported.

## Troubleshooting

### Backend won't start
- Ensure Python dependencies are installed: `pip install -r backend/requirements.txt`
- Check that you're running from the project root directory
- Verify port 8000 is not already in use

### Frontend won't start
- Ensure frontend dependencies are installed: `cd frontend && npm install`
- Check that port 5173 is not already in use
- Clear Vite cache: `rm -rf frontend/.vite`

### Google Sheets access fails
- Verify the spreadsheet URL is correct and publicly accessible
- Check your internet connection
- Ensure the spreadsheet has the expected format and sheet name

### CORS errors
- Ensure both servers are running
- Verify Vite proxy is configured in [frontend/vite.config.ts](frontend/vite.config.ts)
- Check that backend CORS middleware allows `http://localhost:5173`

## License

MIT
