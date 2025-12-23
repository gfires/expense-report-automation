# Expense Report Automation

A Python script that parses Google Sheets expense data and returns formatted expense report items.

## Features

- Exports and parses Google Sheets containing expense/purchase data
- Filters expenses by cardholder name and date range
- Maps budget categories to program numbers
- Extracts receipts and flyer information
- Returns structured expense report items

## Requirements

- Python 3.7+
- See [requirements.txt](requirements.txt) for dependencies

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

The main function in [parser.py](parser.py) demonstrates basic usage:

```python
from parser import parse_purchases

SPREADSHEET_LINK = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
CARDHOLDER_NAME = "Your Name"
START_DATE = "09/01/2023"  # Format: MM/DD/YYYY

items = parse_purchases(
    SPREADSHEET_LINK,
    CARDHOLDER_NAME,
    START_DATE
)

for item in items:
    print(item)
```

### Parameters

- `spreadsheet_link`: Public Google Sheets URL
- `cardholder_name`: Name of the cardholder to filter for
- `start_date`: Start date in MM/DD/YYYY format (will include all purchases from this date forward)

### Output

Returns a list of `ReportItem` objects with:
- `description`: Formatted description including name, date, event, items, and budget
- `activity`: Mapped program number from budget category
- `receipts`: List of receipt URLs
- `flyer`: Flyer URL or information

## Running the Test

```bash
python parser.py
```

Note: The test requires access to the specific Google Sheet hardcoded in the `main()` function.

## Google Sheets Format

The script expects a sheet named "Purchases 2023-2024" with columns:
- Column A: Timestamp
- Column D: Receipts (comma-separated URLs)
- Column E: Name
- Column F: Budget category
- Column G: Endowment (for "Other" budget category)
- Column J: Cardholder name
- Column L: Flyer
- Column M: Items
- Column N: Event
