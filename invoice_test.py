from datetime import datetime, timedelta
from pathlib import Path
<<<<<<< HEAD
from backend.invoice_service import generate_parking_invoice_pdf
=======
#from invoice_service import generate_parking_invoice_pdf
>>>>>>> 898f1fc (test for deploy)


def run_test():
    print("Running InvoiceGenerator service test...")

    # Test Data Stuff
    now = datetime.now()
    entry = now - timedelta(hours=2, minutes=45)
    exit_time = now

    test_payload = {
        "transaction_id": "SP-2026-0042",
        "license_plate": "7XYZ99",
        "bank_account": "9876543210",
        "space_number": "C12",
        "entry_time": entry,
        "exit_time": exit_time,
        "duration_hours": 2.75,
        "hourly_rate": 5.00,
        "company_name": "Smart Park Services LLC",
        "generate_qr_code": False,
    }

    print("Test Input Parameters:")
    for key, value in test_payload.items():
        print(f"  - {key}: {value}")

    # Generate in-memory
    pdf_bytes = generate_parking_invoice_pdf(**test_payload)

    # Verify 
    assert isinstance(pdf_bytes, bytes), "Output is not bytes!"
    assert len(pdf_bytes) > 0, "Generated PDF is empty!"
    assert pdf_bytes.startswith(b"%PDF-"), f"Invalid PDF header: {pdf_bytes[:10]}"

    # Save to disk
    output_file = Path("test_invoice_output.pdf")
    output_file.write_bytes(pdf_bytes)

    print(f"\nAssertion passed: Valid PDF generated ({len(pdf_bytes):,} bytes).")
    print(f"Sample PDF written to: {output_file.resolve()}")


if __name__ == "__main__":
    run_test()