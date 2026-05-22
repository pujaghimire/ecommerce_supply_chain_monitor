"""Anomaly detection helpers for numeric fields."""
from typing import List, Dict
import numpy as np
import statistics


class AnomalyDetector:
    def detect_quantity_anomalies(self, records: List[Dict], threshold: float = 3.0) -> List[Dict]:
        if not records:
            return []

        quantities = [int(r.get("quantity", 0)) for r in records]
        mean = statistics.mean(quantities)
        stdev = statistics.pstdev(quantities) if len(quantities) > 1 else 0

        anomalies = []
        for r, q in zip(records, quantities):
            score = 0.0
            if stdev > 0:
                score = abs((q - mean) / stdev)
            if score >= threshold:
                ar = r.copy()
                ar["anomaly_score"] = score
                anomalies.append(ar)

        # fallback: try isolation forest if sklearn is available for better detection
        if not anomalies:
            try:
                from sklearn.ensemble import IsolationForest
                X = np.array(quantities).reshape(-1, 1)
                iso = IsolationForest(random_state=1, contamination=0.01)
                pred = iso.fit_predict(X)
                for r, p in zip(records, pred):
                    if p == -1:
                        ar = r.copy()
                        ar["anomaly_method"] = "isolation_forest"
                        anomalies.append(ar)
            except Exception:
                pass

        return anomalies


def example():
    det = AnomalyDetector()
    recs = [{"product_id":"a","quantity":1},{"product_id":"b","quantity":2},{"product_id":"c","quantity":100}]
    print(det.detect_quantity_anomalies(recs))


if __name__ == "__main__":
    example()
