"""Simple data validation rules for product records."""
from typing import Tuple, List, Dict


class Validator:
    REQUIRED_FIELDS = ["product_id", "seller_id", "quantity", "price", "timestamp"]

    def validate_record(self, record: Dict) -> Tuple[bool, List[str]]:
        errors = []
        for f in self.REQUIRED_FIELDS:
            if f not in record or record[f] in (None, ""):
                errors.append(f"missing:{f}")

        # type / value checks
        try:
            q = int(record.get("quantity", 0))
            if q < 0:
                errors.append("quantity_negative")
        except Exception:
            errors.append("quantity_not_int")

        try:
            p = float(record.get("price", 0.0))
            if p <= 0:
                errors.append("price_non_positive")
        except Exception:
            errors.append("price_not_float")

        # simple timestamp presence check (further parsing can be added)
        if not record.get("timestamp"):
            errors.append("timestamp_missing_or_invalid")

        return (len(errors) == 0), errors


def example():
    v = Validator()
    ok, errs = v.validate_record({"product_id":"p1","seller_id":"s1","quantity":2,"price":10.0,"timestamp":"2026-01-01T00:00:00Z"})
    print(ok, errs)


if __name__ == "__main__":
    example()
