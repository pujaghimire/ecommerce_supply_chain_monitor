# E-Commerce Supply Chain & Fulfillment Monitor (Demo)

This repository demonstrates a near-real-time pipeline to validate inventory movement
records and detect anomalies. It's a lightweight demo using Python and simple
modules; AWS helpers are included as stubs for integration.

Getting started:

1. Create a virtualenv and install dependencies (using `uv` to manage venv):

```bash
# install uv globally (one-time)
pip install --user uv

# create and activate a venv named .venv (uv manages venvs)
uv venv create .venv
source .venv/bin/activate

# install project dependencies from pyproject.toml (dev extras included)
pip install -e .[dev]
```

If you prefer not to use `uv`, you can still create a venv with:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

2. Generate synthetic data and run the pipeline:

```bash
python scripts/generate_synthetic_data.py
python -m src.monitoring.pipeline --csv data/synthetic_products.csv
```

3. Run tests:

```bash
pytest -q
```

Files of interest:
- [src/monitoring/pipeline.py](src/monitoring/pipeline.py)
- [src/validation/validator.py](src/validation/validator.py)
- [src/anomaly/detector.py](src/anomaly/detector.py)
- [src/aws_utils/aws_client.py](src/aws_utils/aws_client.py)
