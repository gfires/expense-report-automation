from typing import List, Tuple
from datetime import datetime
from difflib import SequenceMatcher
from models import ExpectedExpense, ReportItem


# ----------------------------
# Expected expense parser
# ----------------------------

def parse_expected_expenses(text: str) -> List[ExpectedExpense]:
    """
    Parse text block with expected expenses.

    Supports two formats per line:
      11/16/25 - Cheesecake - $138.36
      11/16/25 - $214.20 - Burger Chan

    Returns list of ExpectedExpense objects.
    """
    expenses = []

    for line in text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue

        parts = [p.strip() for p in line.split("-")]
        if len(parts) != 3:
            continue

        date_str, part1, part2 = parts

        # Parse date (MM/DD/YY format)
        try:
            expense_date = datetime.strptime(date_str.strip(), "%m/%d/%y").date()
        except ValueError:
            continue

        # Determine which part is price and which is vendor
        # Price starts with $ sign
        if part1.startswith("$"):
            price_str = part1
            vendor = part2
        else:
            vendor = part1
            price_str = part2

        # Parse price
        try:
            price = float(price_str.replace("$", "").replace(",", "").strip())
        except ValueError:
            continue

        expenses.append(ExpectedExpense(
            date=expense_date,
            vendor=vendor,
            price=price
        ))

    return expenses


# ----------------------------
# Vendor similarity
# ----------------------------

def vendor_similarity(vendor1: str, vendor2: str) -> float:
    """
    Calculate similarity between two vendor names using difflib.SequenceMatcher.
    Returns a value between 0.0 and 1.0.
    """
    if not vendor1 or not vendor2:
        return 0.0

    # Normalize for comparison (lowercase, strip whitespace)
    v1 = vendor1.lower().strip()
    v2 = vendor2.lower().strip()

    return SequenceMatcher(None, v1, v2).ratio()


# ----------------------------
# Reconciliation logic
# ----------------------------

def reconcile_expenses(
    expected_text: str,
    actual_items: List[ReportItem],
    price_tolerance: float = 1.00,
    similarity_threshold: float = 0.75
) -> dict:
    """
    Match expected expenses against actual parsed expenses.

    Matching rules (one-to-one):
    1. Exact match: prices equal AND parsed_date >= expected_date
    2. Fuzzy match: |price_diff| <= tolerance AND parsed_date >= expected_date
                     AND vendor similarity >= threshold

    Returns:
    {
        "matched": [(ExpectedExpense, ReportItem), ...],
        "unmatched_expected": [ExpectedExpense, ...],
        "unmatched_actual": [ReportItem, ...]
    }
    """
    expected_expenses = parse_expected_expenses(expected_text)

    matched_pairs: List[Tuple[ExpectedExpense, ReportItem]] = []
    matched_expected_indices = set()
    matched_actual_indices = set()

    # Phase 1: Exact price matches
    for exp_idx, expected in enumerate(expected_expenses):
        if exp_idx in matched_expected_indices:
            continue

        for act_idx, actual in enumerate(actual_items):
            if act_idx in matched_actual_indices:
                continue

            # Check exact price match and date constraint
            if (expected.price == actual.price and
                actual.date >= expected.date):

                matched_pairs.append((expected, actual))
                matched_expected_indices.add(exp_idx)
                matched_actual_indices.add(act_idx)
                break

    # Phase 2: Fuzzy matches (price tolerance + vendor similarity)
    for exp_idx, expected in enumerate(expected_expenses):
        if exp_idx in matched_expected_indices:
            continue

        for act_idx, actual in enumerate(actual_items):
            if act_idx in matched_actual_indices:
                continue

            # Check price tolerance
            price_diff = abs(expected.price - actual.price)
            if price_diff > price_tolerance:
                continue

            # Check date constraint
            if actual.date < expected.date:
                continue

            # Check vendor similarity
            similarity = vendor_similarity(expected.vendor, actual.vendor)
            if similarity < similarity_threshold:
                continue

            matched_pairs.append((expected, actual))
            matched_expected_indices.add(exp_idx)
            matched_actual_indices.add(act_idx)
            break

    # Collect unmatched items
    unmatched_expected = [
        exp for idx, exp in enumerate(expected_expenses)
        if idx not in matched_expected_indices
    ]

    unmatched_actual = [
        act for idx, act in enumerate(actual_items)
        if idx not in matched_actual_indices
    ]

    return {
        "matched": matched_pairs,
        "unmatched_expected": unmatched_expected,
        "unmatched_actual": unmatched_actual
    }
