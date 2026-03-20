import csv 
from pathlib import Path
from typing import List, Dict, Any

from app.schemas.Payment import Payment
DATA_DIR = Path(__file__).parent.parent/"db"

PAYMENT_CSV = DATA_DIR/"payment.csv"


def load_all() ->list[Payment]:
    payments = []
    with open (PAYMENT_CSV,"r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            payments.append(Payment.model_validate(row))
    return payments


def save_all(payments: List[Payment]) ->None:
    with open (PAYMENT_CSV,"w") as f:
        writer = csv.DictWriter(f,fieldnames=list(Payment.model_fields.keys()))
        writer.writeheader()
        for payment in payments:
            writer.writerow(payment.model_dump())