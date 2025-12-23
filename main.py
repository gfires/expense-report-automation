from parser import parse_purchases
from reconcile import reconcile_expenses


def main():
    # ----------------------------
    # Configuration
    # ----------------------------
    SPREADSHEET_LINK = (
        "https://docs.google.com/spreadsheets/d/1DVerqZwwyPQY0aLVS2PI_5GItN-5f3uQex4JoJ_RLbE/edit?resourcekey=&gid=1857220607#gid=1857220607"
    )
    CARDHOLDER_NAME = "Gavin Firestone (Treasurer)"
    START_DATE = "11/01/2025"

    # Expected expenses text block
    # Format: MM/DD/YY - Vendor - $Price  OR  MM/DD/YY - $Price - Vendor
    EXPECTED_EXPENSES = """
    11/1/25 - Trader Joe's - $25.25
    11/3/25 - Target - $9.99
    11/9/25 - Target - $40.81
    11/13/25 - Academy Sports - $74.99
    11/15/25 - Target - $33.56
    11/16/25 - Cheesecake - $138.36
    11/16/25 - $214.20 - Burger Chan
    11/18/25 - Target - $17.82
    11/18/25 - HEB - $26.80
    11/19/25 - HEB - $55.98
    11/29/25 - HEB - $46.64
    11/30/25 - Custom Ink - $1,075.50
    """

    # ----------------------------
    # Parse spreadsheet
    # ----------------------------
    print("Parsing spreadsheet...")
    try:
        actual_items = parse_purchases(SPREADSHEET_LINK, CARDHOLDER_NAME, START_DATE)
        print(f"Found {len(actual_items)} actual expenses\n")
    except Exception as e:
        print(f"ERROR parsing spreadsheet: {e}")
        import traceback
        traceback.print_exc()
        return

    # ----------------------------
    # Reconcile expenses
    # ----------------------------
    print("Reconciling expenses...")
    results = reconcile_expenses(EXPECTED_EXPENSES, actual_items)

    # ----------------------------
    # Display results
    # ----------------------------
    print("\n" + "="*80)
    print("MATCHED EXPENSES")
    print("="*80)

    if results["matched"]:
        for i, (expected, actual) in enumerate(results["matched"], 1):
            print(f"\n[Match {i}]")
            print(f"  Expected: {expected.date} | {expected.vendor:30} | ${expected.price:>8.2f}")
            print(f"  Actual:")
            print(f"    Date:        {actual.date}")
            print(f"    Vendor:      {actual.vendor}")
            print(f"    Price:       ${actual.price:.2f}")
            print(f"    Description: {actual.description}")
            print(f"    Activity:    {actual.activity}")
            print(f"    Receipts:")
            if actual.receipts:
                for receipt in actual.receipts:
                    print(f"      - {receipt}")
            else:
                print(f"      (none)")
            print(f"    Flyer:       {actual.flyer}")
            if expected.vendor:
                from reconcile import vendor_similarity
                sim = vendor_similarity(expected.vendor, actual.vendor)
                print(f"  Vendor similarity: {sim:.2%}")
    else:
        print("\nNo matches found")

    print("\n" + "="*80)
    print("MISSING EXPECTED EXPENSES")
    print("="*80)

    if results["unmatched_expected"]:
        for i, expected in enumerate(results["unmatched_expected"], 1):
            print(f"\n[Missing {i}]")
            print(f"  Date:   {expected.date}")
            print(f"  Vendor: {expected.vendor}")
            print(f"  Price:  ${expected.price:.2f}")
    else:
        print("\nAll expected expenses matched!")

    print("\n" + "="*80)
    print("EXTRA ACTUAL EXPENSES")
    print("="*80)

    if results["unmatched_actual"]:
        for i, actual in enumerate(results["unmatched_actual"], 1):
            print(f"\n[Extra {i}]")
            print(f"  Date:        {actual.date}")
            print(f"  Vendor:      {actual.vendor}")
            print(f"  Price:       ${actual.price:.2f}")
            print(f"  Description: {actual.description}")
            print(f"  Activity:    {actual.activity}")
            print(f"  Receipts:")
            if actual.receipts:
                for receipt in actual.receipts:
                    print(f"    - {receipt}")
            else:
                print(f"    (none)")
            print(f"  Flyer:       {actual.flyer}")
    else:
        print("\nNo extra actual expenses")

    # ----------------------------
    # Summary
    # ----------------------------
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Matched:             {len(results['matched'])}")
    print(f"Unmatched expected:  {len(results['unmatched_expected'])}")
    print(f"Unmatched actual:    {len(results['unmatched_actual'])}")
    print()


if __name__ == "__main__":
    main()
