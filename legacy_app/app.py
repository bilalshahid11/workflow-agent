import os, random, time
from flask import Flask, render_template, request

app = Flask(__name__)
CUSTOMERS = ["Acme Corp", "Globex", "Initech", "Umbrella Health", "Wayne Logistics"]


def ui():
    """UI 'drift' mode: set DRIFT=1 to simulate the vendor changing the site."""
    drift = os.getenv("DRIFT") == "1"
    return {
        "submit_label": "Save and Continue" if drift else "Submit",
        "ids": {
            "customer": "cust_sel" if drift else "customer",
            "invoice": "ref_no" if drift else "invoice_number",
            "amount": "amt" if drift else "amount",
        },
        "conf_id": "conf_no" if drift else "confirmation",
    }


@app.get("/")
def form():
    time.sleep(random.uniform(0.3, 1.0))  # legacy systems are slow
    return render_template("form.html", customers=CUSTOMERS, **ui())


@app.post("/submit")
def submit():
    time.sleep(random.uniform(0.3, 1.0))
    confirmation = f"CONF-{random.randint(100000, 999999)}"
    return render_template(
        "confirm.html",
        confirmation=confirmation,
        customer=request.form["customer"],
        invoice=request.form["invoice_number"],
        **ui(),
    )


if __name__ == "__main__":
    app.run(port=5001)  # 5000 is taken by AirPlay on newer Macs
