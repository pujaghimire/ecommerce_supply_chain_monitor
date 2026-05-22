from validation.validator import Validator


def test_validator_valid_record():
    v = Validator()
    rec = {"product_id":"p1","seller_id":"s1","quantity":2,"price":10.0,"timestamp":"2026-01-01T00:00:00Z"}
    ok, errs = v.validate_record(rec)
    assert ok
    assert errs == []


def test_validator_invalid_record():
    v = Validator()
    rec = {"product_id":"p1","quantity":-1,"price":0}
    ok, errs = v.validate_record(rec)
    assert not ok
    assert "missing:seller_id" in errs
    assert "quantity_negative" in errs or "price_non_positive" in errs
