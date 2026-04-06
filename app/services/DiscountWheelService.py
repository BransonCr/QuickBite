import csv
import random
from datetime import date, timedelta
from pathlib import Path
from typing import List, Optional

from fastapi import HTTPException
from app.schemas.DiscountWheel import DiscountWheelRecord, SpinResult, WheelStatus

DATA_DIR = Path(__file__).parent.parent / "db"
WHEEL_CSV = DATA_DIR / "discount_wheel.csv"
USERS_CSV = DATA_DIR / "user.csv"

DISCOUNTS = [5, 7, 8, 10, 12, 15, 17, 20]


def _user_exists(user_id: str) -> bool:
    if not USERS_CSV.exists():
        return False
    with open(USERS_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["user_id"] == user_id:
                return True
    return False


def _load_all() -> List[DiscountWheelRecord]:
    records = []
    if WHEEL_CSV.exists():
        with open(WHEEL_CSV, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(DiscountWheelRecord.model_validate(row))
    return records


def _save_all(records: List[DiscountWheelRecord]):
    with open(WHEEL_CSV, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=list(DiscountWheelRecord.model_fields.keys())
        )
        writer.writeheader()
        for r in records:
            writer.writerow(r.model_dump())


def _find_record(user_id: str) -> Optional[DiscountWheelRecord]:
    for r in _load_all():
        if r.user_id == user_id:
            return r
    return None


class DiscountWheelService:

    def get_status(self, user_id: str) -> WheelStatus:
        if not _user_exists(user_id):
            raise HTTPException(status_code=404, detail="User not found")

        record = _find_record(user_id)

        if not record:
            return WheelStatus(can_spin=True, message="Spin the wheel to get a discount!")

        last = date.fromisoformat(record.last_spin_date)
        next_spin = last + timedelta(days=30)

        if date.today() >= next_spin:
            return WheelStatus(can_spin=True, message="Your monthly spin is ready!")

        return WheelStatus(
            can_spin=False,
            discount_percent=record.discount_percent,
            discount_code=record.discount_code,
            is_redeemed=record.is_redeemed,
            next_spin_date=next_spin.isoformat(),
            message=f"Next spin available on {next_spin.isoformat()}",
        )

    def spin(self, user_id: str) -> SpinResult:
        if not _user_exists(user_id):
            raise HTTPException(status_code=404, detail="User not found")

        record = _find_record(user_id)

        if record:
            last = date.fromisoformat(record.last_spin_date)
            next_spin = last + timedelta(days=30)
            if date.today() < next_spin:
                raise HTTPException(
                    status_code=429,
                    detail=f"Spin not available until {next_spin.isoformat()}",
                )

        discount = random.choice(DISCOUNTS)
        code = f"SPIN{discount}{user_id[:4].upper()}"

        new_record = DiscountWheelRecord(
            user_id=user_id,
            last_spin_date=date.today().isoformat(),
            discount_percent=discount,
            discount_code=code,
            is_redeemed=False,
        )

        records = [r for r in _load_all() if r.user_id != user_id]
        records.append(new_record)
        _save_all(records)

        return SpinResult(
            discount_percent=discount,
            discount_code=code,
            message=f"You won {discount}% off! Use code {code} at checkout.",
        )

    def redeem(self, user_id: str, code: str) -> dict:
        if not _user_exists(user_id):
            raise HTTPException(status_code=404, detail="User not found")

        records = _load_all()
        for r in records:
            if r.user_id == user_id and r.discount_code == code:
                if r.is_redeemed:
                    raise HTTPException(status_code=400, detail="Code already redeemed")
                r.is_redeemed = True
                _save_all(records)
                return {"message": f"Code {code} redeemed successfully!"}

        raise HTTPException(status_code=404, detail="Invalid code or user mismatch")