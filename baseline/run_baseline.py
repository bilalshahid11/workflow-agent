from playwright.sync_api import sync_playwright

BASE = "http://localhost:5001"
INVOICES = [
    {"customer": "Acme Corp", "invoice_number": "A-1001", "amount": 1200.50},
    {"customer": "Globex", "invoice_number": "G-2044", "amount": 87.00},
    {"customer": "Initech", "invoice_number": "I-3310", "amount": 4300.00},
    {"customer": "Umbrella Health", "invoice_number": "U-5521", "amount": 920.75},
    {"customer": "Wayne Logistics", "invoice_number": "W-7789", "amount": 15000.00},
]


def process(page, inv):
    page.goto(BASE)
    page.select_option("#customer", label=inv["customer"])
    page.fill("#invoice_number", inv["invoice_number"])
    page.fill("#amount", str(inv["amount"]))
    page.get_by_role("button", name="Submit").click()
    return page.locator("#confirmation").inner_text()


def main():
    ok, failed = 0, 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page()
        page.set_default_timeout(3000)  # fail fast
        for inv in INVOICES:
            try:
                conf = process(page, inv)
                print(f"OK   {inv['invoice_number']} -> {conf}")
                ok += 1
            except Exception as e:
                print(f"FAIL {inv['invoice_number']}: {str(e).splitlines()[0]}")
                failed += 1
        browser.close()
    print(f"\nSucceeded: {ok}/{ok + failed}")


if __name__ == "__main__":
    main()
