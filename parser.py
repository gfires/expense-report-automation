from dataclasses import dataclass
from typing import List
from openpyxl import load_workbook
from datetime import date, datetime
import requests
import tempfile
import os


# ----------------------------
# Data model
# ----------------------------

@dataclass
class ReportItem:
    description: str
    activity: str
    receipts: List[str]
    flyer: str


# ----------------------------
# Program number mapping
# ----------------------------

PROGRAM_MAP = {
    "Cab Retreat": "6100",
    "Cab Food/Prizes": "6653",
    "Laundry": "8206",
    "Initiative": "0200",
    "Storage Assistance": "0330",
    "Socioeconomic Inclusivity Fund": "1350",
    "RAs Budget": "6658",
    "Awards": "6333",
    "Spirit": "6137",
    "Sports": "2400",
    "Beer Bike": "6133",
    "Merch": "5080",
    "Community Service": "0331",
    "Permanent Improvements": "6531",
    "Staff Appreciation": "8601",
    "Associates": "6650",
    "Alumni": "6951",
    "Academic Mentors": "1110",
    "PAAs": "6655",
    "Diversity": "6600",
    "Senior Class": "6136",
    "Junior Class": "6601",
    "Sophomore Class": "6602",
    "Freshmen Class": "6134",
    "Off Campus": "6135",
    "Socials": "4600",
    "BGHS": "6603",
    "Chief Justice": "8202",
    "President": "6656",
    "STRIVE": "6604",
    "RHA": "8604",
    "BakerShake": "3150",
    "Baker Black Caucus": "6605",
    "O-Week": "6000",
}


# ----------------------------
# Helpers
# ----------------------------

def export_google_sheet_to_workbook(sheet_url: str):
    """
    Converts a public Google Sheet URL to an xlsx workbook via export.
    """
    spreadsheet_id = sheet_url.split("/d/")[1].split("/")[0]
    export_url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{spreadsheet_id}/export?format=xlsx"
    )

    response = requests.get(export_url)
    response.raise_for_status()

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    tmp.write(response.content)
    tmp.close()

    wb = load_workbook(tmp.name)
    os.unlink(tmp.name)
    return wb


def parse_mmddyyyy(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%m/%d/%Y")

def parse_receipts(cell_value) -> List[str]:
    if not cell_value:
        return []

    # Split on commas, strip whitespace, drop empties
    return [
        part.strip()
        for part in str(cell_value).split(",")
        if part.strip()
    ]

def extract_date(cell_value) -> date:
    if isinstance(cell_value, datetime):
        return cell_value.date()

    if isinstance(cell_value, date):
        return cell_value

    # Always ISO format: YYYY-MM-DD[ ...]
    return datetime.fromisoformat(str(cell_value).split(" ")[0]).date()


# ----------------------------
# Core parser
# ----------------------------

def parse_purchases(
    spreadsheet_link: str,
    cardholder_name: str,
    start_date: str
) -> List[ReportItem]:

    wb = export_google_sheet_to_workbook(spreadsheet_link)
    ws = wb["Purchases 2023-2024"]

    start_dt = datetime.strptime(start_date, "%m/%d/%Y").date()
    report_items: List[ReportItem] = []

    # Iterate bottom → top (skip header)
    for row in range(ws.max_row, 1, -1):
        A_timestamp = ws[f"A{row}"].value
        J_pcard = ws[f"J{row}"].value

        if not A_timestamp:
            continue

        # Timestamp is consistently formatted; extract date portion
        row_date = extract_date(A_timestamp)

        # Stop once we're before the start date
        if row_date < start_dt:
            break

        if J_pcard != cardholder_name:
            continue

        D_receipts = ws[f"D{row}"].value
        E_name = ws[f"E{row}"].value
        F_budget = ws[f"F{row}"].value
        G_endowment = ws[f"G{row}"].value
        L_flyer = ws[f"L{row}"].value
        M_items = ws[f"M{row}"].value
        N_event = ws[f"N{row}"].value

        description_parts = [
            str(E_name),
            "Baker College",
            row_date.strftime("%m/%d/%Y"),
            str(N_event),
            str(M_items),
            str(F_budget),
        ]

        if F_budget == "Other" and G_endowment:
            description_parts.append(str(G_endowment))

        description = " | ".join(description_parts)
        activity = PROGRAM_MAP.get(F_budget, "")


        report_items.append(
            ReportItem(
                description=description,
                activity=activity,
                receipts=parse_receipts(D_receipts),
                flyer=str(L_flyer) if L_flyer else "",
            )
        )

    return report_items

# ----------------------------
# Tests
# ----------------------------

def main():
    # Simple test
    SPREADSHEET_LINK = (
        "https://docs.google.com/spreadsheets/d/1DVerqZwwyPQY0aLVS2PI_5GItN-5f3uQex4JoJ_RLbE/edit?resourcekey=&gid=1857220607#gid=1857220607"
    )
    CARDHOLDER_NAME = "Gavin Firestone (Treasurer)"
    START_DATE = "11/01/2025"

    try:
        items = parse_purchases(
            SPREADSHEET_LINK,
            CARDHOLDER_NAME,
            START_DATE
        )

        print("EXPENSE REPORT ITEMS:")
        print(f"{'='*60}\n")

        for i, item in enumerate(items, 1):
            print(f"Item {i}:")
            print(f"  Description: {item.description}")
            print(f"  Activity: {item.activity}")
            print(f"  Receipts: {item.receipts}")
            print(f"  Flyer: {item.flyer}")
            print()

    except Exception as e:
        print(f"\n[ERROR] Failed to parse purchases: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
