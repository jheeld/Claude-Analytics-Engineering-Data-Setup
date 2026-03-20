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

## Step 2 — Generate SQL Queries (inline in notebook)

Do NOT create a separate .sql file. Instead, add a code cell in the notebook that generates and writes `notebooks/queries.sql` on the fly using the actual table name, column names, and target column resolved from the dataset context step.

The generated SQL must include:

1. Row count
2. Target distribution with percentages
3. Missing values per column (one line per column)
4. Descriptive stats for all numeric columns (min, max, mean, std, percentiles)
5. Sample rows
6. Target rate grouped by each categorical feature
7. Per-entity volume and target rate (if an entity/group column exists)
8. Volume over time (if a date column exists)

Use actual column names — do not use placeholders like `<table>` in the output file.

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