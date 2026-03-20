---
name: leakage-checker
description: Check for data leakage before training any model, especially on time-series or transaction data.
---

# Data Leakage Checker

Before training ANY model, run through these checks.

## Core Checks

1. **Time-based leakage**
   - Is the train/test split time-based?
   - Are any rolling or aggregate features computed on the full dataset instead of past-only data?
   - Does the test set bleed into feature computation?

2. **Label leakage**
   - Are any features derived directly or indirectly from the label?
   - Do any column values only exist after the outcome is known?

3. **Future data leakage**
   - Are we using information that would not be available at prediction time?
   - Example: using the final month's average to predict mid-month behavior

4. **Aggregate leakage**
   - Global means/stds computed before splitting will leak test distribution into training features
   - Always fit scalers and aggregators on training data only, then transform test data

## Red Flags

- Suspiciously high accuracy or AUC early in the process
- Features that are perfectly correlated with the target
- Aggregate features that include future rows

## Action

If leakage is suspected, stop and fix before proceeding.

Document what leakage was found and how it was resolved in the notebook.
