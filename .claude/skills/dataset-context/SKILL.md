---
name: dataset-context
description: Analyze a CSV or JSON dataset, inspect columns and sample values, then ask the user for missing business context before interpreting features and suggesting preprocessing.
disable-model-invocation: false
---

When provided with a CSV, JSON, or dataframe, follow this workflow.

## Pre-Step: Multiple Files Check

If more than one file is provided (CSV, JSON, or any combination):

**Stop and ask before doing anything else:**

1. What does each file represent? (e.g. transactions, users, products)
2. How should the files be joined? (join key, join type: inner/left/right)
3. Is there a primary file that drives the unit of analysis?
4. Are there any known data quality issues across files (e.g. missing keys, duplicates)?

Do NOT inspect, describe, or run any context steps until all join questions are answered and the files have been merged into a single working dataframe.

## Step 1: Inspect the dataset first

Before making assumptions, always output the following in a clean, readable format — whether called standalone or from the `ml-case-notebook` orchestrator:

1. **10 random rows** — `df.sample(10)` displayed as a formatted table
2. **Descriptive statistics** — `df.describe()` rounded to 2 decimal places
3. **Schema summary** — column name, dtype, non-null count, missing count per column
4. **Categorical value counts** — for every column with dtype `object` or low-cardinality int, print `value_counts()` with percentages
5. **Outlier summary** — for every numeric column, compute IQR bounds and print count of values below lower and above upper bound

Format all outputs with clear section headers (e.g. `=== RANDOM SAMPLE ===`, `=== DESCRIPTIVE STATS ===`, `=== CATEGORICAL VALUES ===`, `=== OUTLIERS ===`).

Then summarize:

- possible identifier columns
- possible datetime columns
- possible target-like columns

If a CSV or JSON file path is provided, load it first before inspecting.

## Step 2: Ask the user for missing context

Before interpreting the schema deeply, ask concise clarifying questions.

Ask:

1. What does each row represent?  
   Examples: customer, transaction, device event, account, order, shipment

2. What is the prediction target, if any?  
   If there is no target yet, ask what decision they are trying to support.

3. Are there identifiers that should not be used as features?  
   Examples: customer_id, order_id, session_id, email

4. Are there timestamps or event dates that determine ordering?  
   Ask whether this should be treated as a time-based problem.

5. What business decision or outcome is this model meant to support?

Pause and wait for the user's response before continuing if this context is missing.

## Step 3: Interpret the columns using both the dataset and user context

For each column, infer:

- likely meaning
- feature type
- whether it may be useful for modeling
- whether it may be risky

Classify columns into one of these categories:

- identifier
- target
- numeric feature
- categorical feature
- datetime feature
- boolean feature
- text feature
- unknown / ambiguous

## Step 4: Flag modeling risks

Check for:

- identifier columns that should likely be excluded
- target leakage
- post-outcome fields
- timestamp columns that require time-aware splitting
- high-cardinality categorical variables
- columns with excessive missingness
- suspicious aggregate fields that may leak future information
- duplicated rows or near-duplicate columns if obvious from inspection

## Step 5: Produce a structured schema/context report

Return a table with these columns:

| column | inferred meaning | feature type | include/exclude | notes | feature engineering ideas |

Also include short sections for:

### Possible target
- the most likely target column(s), if any

### Recommended exclusions
- columns that should likely not be used as features

### Recommended preprocessing
- missing value handling
- categorical encoding
- scaling needs
- datetime extraction ideas
- text handling, if relevant

### Recommended validation strategy
Choose and justify one:
- random split
- stratified split
- group split
- time-based split

## Step 6: Suggest next-step modeling direction

Based on the dataset and user context, recommend:

- likely ML task type
- 1 baseline model
- 1–2 stronger candidate models
- the most appropriate evaluation metrics

## Behavior guidelines

- Do not overconfidently guess business meaning when the dataset is ambiguous.
- Ask for context first when needed.
- Prefer concise, structured outputs.
- Be explicit about uncertainty.
- If the dataset appears unsuitable for modeling until more context is provided, say so clearly.