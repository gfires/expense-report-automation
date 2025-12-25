from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from datetime import datetime
import os

# Register cursive font
FONT_PATH = os.path.join(os.path.dirname(__file__), "templates", "fonts", "AguafinaScript-Regular.ttf")
if os.path.exists(FONT_PATH):
    pdfmetrics.registerFont(TTFont('AguafinaScript', FONT_PATH))
    SIGNATURE_FONT = 'AguafinaScript'
else:
    SIGNATURE_FONT = 'Helvetica-Oblique'  # Fallback

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "blank_affidavit.pdf")

def parse_cardholder_name(full_name: str) -> str:
    """Extract first two words from cardholder name.
    Example: 'Gavin Firestone (Treasurer)' -> 'Gavin Firestone'
    """
    words = full_name.strip().split()
    return ' '.join(words[:2]) if len(words) >= 2 else full_name

def generate_affidavit(
    vendor: str,
    price: float,
    date: str,  # Expected date (YYYY-MM-DD from backend)
    cardholder_name: str
) -> BytesIO:
    """
    Generate a filled affidavit PDF.

    Args:
        vendor: Vendor name from expected expense
        price: Price from expected expense
        date: Date from expected expense (ISO format YYYY-MM-DD)
        cardholder_name: Full cardholder name with role

    Returns:
        BytesIO object containing the filled PDF
    """
    # Read template PDF
    template_pdf = PdfReader(TEMPLATE_PATH)
    output_pdf = PdfWriter()

    # Create overlay with text
    overlay = BytesIO()
    c = canvas.Canvas(overlay, pagesize=letter)

    # Format data
    parsed_name = parse_cardholder_name(cardholder_name)
    expense_date = datetime.fromisoformat(date).strftime("%m/%d/%Y")
    receipt_details = f"{vendor}, ${price:.2f}, {expense_date}"
    today_date = datetime.now().strftime("%m/%d/%Y")

    # Coordinate mapping (estimated, may need adjustment)
    # "COPIES ARE NOT AVAILABLE" section (bottom half)

    # Receipt details line (first blank line under "Print receipt detail(s)...")
    c.setFont("Helvetica", 14)
    c.drawString(40, 260, receipt_details)

    # Signature line
    c.setFont(SIGNATURE_FONT, 16)
    c.drawString(40, 145, parsed_name)

    # Date field (to the right of signature)
    c.setFont("Helvetica", 14)
    c.drawString(320, 145, today_date)

    c.save()

    # Merge overlay with template
    overlay.seek(0)
    overlay_pdf = PdfReader(overlay)

    page = template_pdf.pages[0]
    page.merge_page(overlay_pdf.pages[0])
    output_pdf.add_page(page)

    # Write to BytesIO
    output = BytesIO()
    output_pdf.write(output)
    output.seek(0)

    return output
