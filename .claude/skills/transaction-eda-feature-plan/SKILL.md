---
name: transaction-eda-feature-plan
description: Feature engineering plan for transaction or time-series datasets. EDA and schema inspection are handled by dataset-context — this skill focuses on what features to build and why.
---

# Transaction Feature Planning Skill

Dataset inspection and EDA are handled by `dataset-context`. This skill focuses purely on what features to engineer and why.

## Feature Engineering

### Time Features
- Rolling averages: 7-day, 30-day windows
- Time since last transaction
- Day of week, day of month, month of year
- Is weekend flag

### Entity-Level Features (per user / per household)
- Mean spend per entity
- Standard deviation per entity
- Z-score normalization per entity (critical for personalized behavior)
- Transaction frequency

### Behavioral Pattern Features
- Frequency of each category per entity
- Recurring payment detection (same amount, same interval)
- Ratio of current transaction to entity rolling mean

### Anomaly Signals
- Z-score deviation from entity rolling mean
- Unusual category for this entity
- Percentage change from prior period
- Spike relative to entity baseline

## Key Rule

**Normalize per entity, not globally.** What is normal for one entity may be anomalous for another. Global thresholds will produce high false positive rates.

Always start with simple, interpretable features before engineering complex ones.
