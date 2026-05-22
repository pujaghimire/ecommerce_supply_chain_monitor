"""Pipeline orchestrator for the E-Commerce Supply Chain & Fulfillment Monitor

This module ties together ingestion (from CSV for demo), validation, anomaly
detection, and optional AWS publishing (S3/DynamoDB via aws_utils).
"""
from pathlib import Path
import csv
import json
from typing import List, Dict

from validation.validator import Validator
from anomaly.detector import AnomalyDetector
from aws_utils.aws_client import AWSClient


class Pipeline:
    def __init__(self, aws_client: AWSClient = None):
        self.validator = Validator()
        self.detector = AnomalyDetector()
        self.aws = aws_client

    def run_from_csv(self, csv_path: str) -> Dict[str, List]:
        csv_path = Path(csv_path)
        if not csv_path.exists():
            raise FileNotFoundError(f"{csv_path} does not exist")

        records = []
        with csv_path.open("r", newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                # simple normalization
                row["quantity"] = int(row.get("quantity", 0))
                row["price"] = float(row.get("price", 0.0))
                records.append(row)

        valid = []
        invalid = []
        for r in records:
            ok, errors = self.validator.validate_record(r)
            if ok:
                valid.append(r)
            else:
                r["validation_errors"] = errors
                invalid.append(r)

        # detect anomalies on numeric fields (example: quantity)
        anomalies = self.detector.detect_quantity_anomalies(valid)

        result = {"valid": valid, "invalid": invalid, "anomalies": anomalies}

        # Optionally publish metrics or records to AWS
        if self.aws:
            try:
                # publish counts to CloudWatch or DynamoDB (placeholder)
                self.aws.put_metric("monitor.valid_count", len(valid))
                self.aws.put_metric("monitor.invalid_count", len(invalid))
                if anomalies:
                    self.aws.put_metric("monitor.anomaly_count", len(anomalies))
            except Exception:
                pass

        return result


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="data/synthetic_products.csv")
    args = parser.parse_args()

    pipeline = Pipeline()
    res = pipeline.run_from_csv(args.csv)
    print(json.dumps({
        "valid": len(res["valid"]),
        "invalid": len(res["invalid"]),
        "anomalies": len(res["anomalies"])}, indent=2))


if __name__ == "__main__":
    main()
