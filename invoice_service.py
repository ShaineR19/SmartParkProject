import os
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from tempfile import NamedTemporaryFile

import InvoiceGenerator.conf
import InvoiceGenerator.pdf
from InvoiceGenerator.api import Client, Creator, Invoice, Item, Provider
from InvoiceGenerator.pdf import SimpleInvoice

# Set language to English
os.environ["INVOICE_LANG"] = "en"

_orig_conf_gettext = getattr(InvoiceGenerator.conf, "_", lambda s: s)
_orig_pdf_gettext = getattr(InvoiceGenerator.pdf, "_", _orig_conf_gettext)

_HEADER_OVERRIDES = {
    "Price per one": "Price per hour",
    "Units": "Hours",
    "Date of exposure": "Date of issue",
}

def _custom_translate(text: str) -> str:
    translated = _orig_pdf_gettext(text)
    return _HEADER_OVERRIDES.get(text, _HEADER_OVERRIDES.get(translated, translated))

# Apply the custom translation to the PDF
InvoiceGenerator.conf._ = _custom_translate
InvoiceGenerator.pdf._ = _custom_translate


def generate_parking_invoice_pdf(
    transaction_id: int | str,
    license_plate: str,
    space_number: str,
    entry_time: datetime | str,
    exit_time: datetime | str,
    duration_hours: float,
    hourly_rate: float,
    payment_amount: float | None = None,
    currency: str = "$",
    currency_locale: str = "en_US.UTF-8",
    company_name: str = "Smart Park Systems",
    bank_account: str | None = None,
    generate_qr_code: bool = False,
) -> bytes:
    """Generate a parking invoice PDF as in-memory bytes using InvoiceGenerator."""
    # 1. Define Client, Provider, and Creator
    client = Client(
        f"Vehicle: {str(license_plate).upper()}",
        address=f"Space: {space_number}",
    )
    provider = Provider(
        company_name,
        bank_account=bank_account or "",
    )
    creator = Creator("Smart Park Services")

    # 2. Build Invoice
    invoice = Invoice(client, provider, creator)
    invoice.currency = currency
    invoice.currency_locale = currency_locale
    invoice.number = f"INV-{transaction_id}"

    # Handle dates
    if isinstance(exit_time, datetime):
        invoice.date = exit_time.date()
    elif isinstance(exit_time, date):
        invoice.date = exit_time
    else:
        try:
            invoice.date = datetime.fromisoformat(str(exit_time)).date()
        except Exception:
            invoice.date = date.today()

    # Format timestampsn
    entry_str = entry_time.strftime("%Y-%m-%d %H:%M") if isinstance(entry_time, datetime) else str(entry_time)
    exit_str = exit_time.strftime("%Y-%m-%d %H:%M") if isinstance(exit_time, datetime) else str(exit_time)
    item_desc = f"Parking Session ({entry_str} to {exit_str})"

    # 3. Add Item using Decimal. No ugly floats
    count_val = Decimal(str(round(duration_hours, 2)))
    price_val = Decimal(str(round(hourly_rate, 2)))

    invoice.add_item(Item(count_val, price_val, description=item_desc, tax=0))

    # 4. Generate PDF
    with NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
        temp_path = tmp_file.name

    try:
        pdf = SimpleInvoice(invoice)
        pdf.gen(temp_path, generate_qr_code=generate_qr_code)
        pdf_bytes = Path(temp_path).read_bytes()
    finally:
        temp_file_path = Path(temp_path)
        if temp_file_path.exists():
            temp_file_path.unlink()

    return pdf_bytes