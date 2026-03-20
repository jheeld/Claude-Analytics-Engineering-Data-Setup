---
name: ml-case-notebook
description: Generate a machine learning analysis notebook using the project template.
---

# ml-case-notebook Skill

When starting a machine learning analysis:

## Step 0 — Dataset Context (REQUIRED)

Run the `dataset-context` skill on the provided dataset.

**Wait for all clarifying questions to be answered before proceeding. Do not generate the notebook until the dataset-context skill is complete and all questions are resolved.**

When context is provided, always write it directly as code and markdown cells into the notebook — do not just summarize in chat.

---

## Step 1 — Generate the Notebook

1. Load the template located at:
   `templates/ml_case_template.ipynb`

2. Create a new notebook in:
   `notebooks/analysis.ipynb`

3. Follow the template structure.

Notebook sections should include:

- Problem framing
- Data loading
- Data audit
- Exploratory data analysis
- Outlier detection (before any removal)
- Outlier removal
- Feature engineering
- Train/test split
- Baseline model
- Candidate models
- Model evaluation
- Error analysis
- Final recommendation

If data is provided, begin filling the sections starting with data loading and EDA.

---

## Step 2 — Generate SQL Queries File

Create a file at `notebooks/queries.sql` with the following basic queries adapted to the dataset's table name and columns:

```sql
-- 1. Row count
SELECT COUNT(*) AS total_rows FROM <table>;

-- 2. Class / target distribution
SELECT <target_col>, COUNT(*) AS count,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct
FROM <table>
GROUP BY <target_col>;

-- 3. Missing values per column
SELECT
  COUNT(*) AS total_rows,
  <col_nulls>
FROM <table>;

-- 4. Basic descriptive stats for numeric columns
SELECT
  MIN(<numeric_col>) AS min_val,
  MAX(<numeric_col>) AS max_val,
  AVG(<numeric_col>) AS mean_val,
  STDDEV(<numeric_col>) AS std_val
FROM <table>;

-- 5. Sample rows
SELECT * FROM <table> LIMIT 10;

-- 6. Target rate by a categorical or binned feature (adapt as needed)
SELECT <feature_col>, AVG(<target_col>) AS target_rate, COUNT(*) AS n
FROM <table>
GROUP BY <feature_col>
ORDER BY target_rate DESC;
```

Replace `<table>`, `<target_col>`, `<numeric_col>`, and `<feature_col>` with the actual names from the dataset context step.

## Outlier Detection Checks

Before removing any outliers, always add a detection step with the following checks:

1. **Histogram plot** — plot the distribution of the most correlated features for the target class to visually identify skew and extreme values.

2. **IQR summary table** — for each feature flagged as high-correlation, compute and display:
   - Q25, Q75, IQR
   - Lower bound: Q25 - 1.5 × IQR
   - Upper bound: Q75 + 1.5 × IQR
   - Outlier count and outlier values

3. **Print row count** before removal so the impact of removal is visible.

Apply these checks on the relevant subset (e.g. balanced sample or minority class) and on the features most correlated with the target variable.