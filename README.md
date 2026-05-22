# E-Commerce Supply Chain & Fulfillment Monitor

A lightweight Python demo for validating inventory movement events and detecting fulfillment anomalies in near-real-time.

## What it does

- Validates synthetic product movement records for required fields and data quality issues.
- Detects quantity anomalies using statistical outlier scoring.
- Includes AWS integration stubs for S3/DynamoDB/CloudWatch-style publishing.
- Provides a synthetic data generator to exercise the pipeline.

## Project structure

- `src/monitoring/pipeline.py` — pipeline orchestration and CSV ingestion
- `src/validation/validator.py` — record validation rules
- `src/anomaly/detector.py` — anomaly detection helpers
- `src/aws_utils/aws_client.py` — AWS client wrapper and fallback behavior
- `scripts/generate_synthetic_data.py` — synthetic product movement CSV generator
- `tests/` — pytest regression coverage
- `pyproject.toml` — dependency management

## Setup

Use `uv` to manage the virtual environment and install dependencies from `pyproject.toml`:

```bash
pip install --user uv
uv venv create .venv
source .venv/bin/activate
pip install -e .[dev]
```

Alternatively, create the venv manually:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Run the demo

Generate sample data and execute the monitor pipeline:

```bash
python scripts/generate_synthetic_data.py
python -m src.monitoring.pipeline --csv data/synthetic_products.csv
```

## Testing

Run the full suite with:

```bash
pytest -q
```

## Notes

- This project uses `pyproject.toml` for dependency management.
- AWS integration is represented with safe stub behavior when `boto3` is unavailable.
- The pipeline is designed to showcase validation, anomaly detection, and monitoring tooling.
