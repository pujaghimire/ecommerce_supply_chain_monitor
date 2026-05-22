# Infra notes for E-Commerce Supply Chain & Fulfillment Monitor

This folder lists suggested AWS components (placeholders) for a production deployment:

- S3: Raw ingestion and archived CSV/Parquet files
- DynamoDB: Store validation status or lightweight metadata per product-event
- CloudWatch: Metrics and alarms for invalid records / anomaly counts
- Lambda: Serverless processors to run validation and anomaly detection in near-real-time
- EventBridge or Kinesis: Stream transport for transactional events

Add CloudFormation / CDK templates here when ready.
