import csv
import tempfile
from src.monitoring.pipeline import Pipeline


def make_csv(path, rows):
    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["product_id", "seller_id", "quantity", "price", "timestamp"])
        writer.writeheader()
        writer.writerows(rows)


def test_pipeline_validates_and_detects_anomalies(tmp_path):
    path = tmp_path / "test_products.csv"
    rows = [
        {"product_id": "p1", "seller_id": "s1", "quantity": "2", "price": "10.0", "timestamp": "2026-01-01T00:00:00Z"},
        {"product_id": "p2", "seller_id": "s2", "quantity": "3", "price": "20.0", "timestamp": "2026-01-01T01:00:00Z"},
        # outlier quantity
        {"product_id": "p3", "seller_id": "s2", "quantity": "1000", "price": "5.0", "timestamp": "2026-01-01T02:00:00Z"},
        # invalid record (missing seller_id)
        {"product_id": "p4", "seller_id": "", "quantity": "1", "price": "1.0", "timestamp": "2026-01-01T03:00:00Z"},
    ]
    make_csv(path, rows)

    pipeline = Pipeline()
    res = pipeline.run_from_csv(str(path))

    assert "valid" in res and "invalid" in res and "anomalies" in res
    assert len(res["invalid"]) == 1
    assert any(r["product_id"] == "p3" for r in res["anomalies"]) or len(res["anomalies"]) >= 1


def test_pipeline_uses_aws_client_metrics(tmp_path):
    # create a tiny CSV with one valid record
    path = tmp_path / "one.csv"
    rows = [{"product_id": "p1", "seller_id": "s1", "quantity": "1", "price": "10.0", "timestamp": "2026-01-01T00:00:00Z"}]
    make_csv(path, rows)

    metrics = []

    class DummyAWS:
        def put_metric(self, name, value):
            metrics.append((name, value))

    pipeline = Pipeline(aws_client=DummyAWS())
    res = pipeline.run_from_csv(str(path))
    # metrics include valid_count and invalid_count
    names = [m[0] for m in metrics]
    assert any("valid_count" in n for n in names)
    assert any("invalid_count" in n for n in names)
