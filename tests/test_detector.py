from anomaly.detector import AnomalyDetector


def test_detector_detects_large_outlier():
    det = AnomalyDetector()
    recs = [{"product_id":"a","quantity":1},{"product_id":"b","quantity":2},{"product_id":"c","quantity":1000}]
    anomalies = det.detect_quantity_anomalies(recs, threshold=2.5)
    assert any(r["product_id"] == "c" for r in anomalies)
