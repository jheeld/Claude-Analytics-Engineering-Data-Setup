---
name: dataset-context
description: Analyze a CSV or JSON dataset, inspect columns and sample values, then ask the user for missing business context before interpreting features and suggesting preprocessing.
disable-model-invocation: false
---

When provided with a CSV, JSON, or dataframe, follow this workflow.

## Step 1: Inspect the dataset first

Before making assumptions, inspect the dataset and summarize:

- column names
- sample values
- likely data types
- possible identifier columns
- possible datetime columns
- possible target-like columns

If a dataframe is already available, first look at:

- `df.head()`
- `df.info()`
- missing value summary
- basic descriptive statistics where useful

If a CSV or JSON file path is provided, suggest loading it first if it has not already been loaded.

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