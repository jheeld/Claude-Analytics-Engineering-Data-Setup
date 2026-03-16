# Claude Analytics Engineering Setup

An analytics engineering workspace powered by [Claude Code](https://claude.ai/claude-code) — designed to accelerate data modeling, SQL development, pipeline debugging, and insight generation using AI-assisted workflows.

---

## Overview

This repo is a template and reference setup for analytics engineers who want to use Claude as an active collaborator in their data work. It pairs modern analytics engineering tooling (dbt, SQL, Python) with Claude Code's agentic capabilities to speed up repetitive tasks, improve code quality, and surface insights faster.

**Claude handles:**
- Generating and reviewing dbt models, tests, and documentation
- Explaining complex SQL queries and data lineage
- Suggesting data quality checks and schema validation logic
- Drafting and iterating on analytical queries from natural language prompts
- Debugging pipeline failures and data anomalies

**You stay in control of:**
- Data source connections and credentials
- Model promotion and deployment decisions
- Final review of all generated SQL and logic

---

## Stack

| Layer | Tool |
|---|---|
| AI Assistant | Claude Code (claude-sonnet-4-6 / claude-opus-4-6) |
| Transformation | dbt Core or dbt Cloud |
| Warehouse | DuckDB (local) / Snowflake / BigQuery (configurable) |
| Orchestration | Airflow / dbt Cloud / Dagster |
| Version Control | Git |
| Language | SQL, Python, YAML |
| Visualization | Matplotlib, Seaborn |
| Machine Learning | scikit-learn |

---

## Getting Started

### Prerequisites

- [Claude Code CLI](https://claude.ai/claude-code) installed and authenticated
- Python 3.9+
- dbt Core installed (`pip install dbt-core dbt-<adapter>`)
- Access to a supported data warehouse

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-org>/Claude-Analytics-Engineering-Data-Setup.git
   cd Claude-Analytics-Engineering-Data-Setup
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure your dbt profile in `~/.dbt/profiles.yml` or use environment variables.

4. Launch Claude Code in this directory:

   ```bash
   claude
   ```

---

## Data Pipeline Steps

This project follows a structured analytics pipeline. Each step leverages Claude Code as an active collaborator.

---

### Step 1: Ingest CSV or JSON Data

Load raw data from local files or APIs into DuckDB using Python or SQL.

```python
# Claude can generate ingestion scripts like:
import duckdb
conn = duckdb.connect("analytics.duckdb")
conn.execute("CREATE TABLE raw_sales AS SELECT * FROM read_csv_auto('data/sales.csv')")
conn.execute("CREATE TABLE raw_events AS SELECT * FROM read_json_auto('data/events.json')")
```

**Claude prompt:**
```
> Ingest sales.csv and events.json into DuckDB. Infer schema automatically and load into raw tables.
```

---

### Step 2: Data Quality Checks

Run automated checks for nulls, duplicates, type mismatches, and value range violations before any transformation.

```python
# Claude can generate quality check queries like:
conn.execute("""
    SELECT
        COUNT(*) AS total_rows,
        COUNT(order_id) AS non_null_order_ids,
        COUNT(DISTINCT order_id) AS unique_orders,
        MIN(order_date) AS earliest_date,
        MAX(order_date) AS latest_date
    FROM raw_sales
""")
```

**Claude prompt:**
```
> Run data quality checks on raw_sales: check for nulls, duplicate IDs, out-of-range prices, and invalid dates.
```

---

### Step 3: Build Basic Data Models (DuckDB)

Transform raw data into clean, business-ready models following staging → intermediate → mart layers.

```sql
-- Claude can generate models like:
CREATE OR REPLACE VIEW stg_sales AS
SELECT
    order_id,
    customer_id,
    product,
    category,
    quantity,
    unit_price,
    quantity * unit_price AS revenue,
    CAST(order_date AS DATE) AS order_date,
    region,
    status
FROM raw_sales
WHERE status != 'returned';
```

**Claude prompt:**
```
> Build a staging model for raw_sales that cleans types, calculates revenue, and filters out returned orders.
```

---

### Step 4: Exploratory Data Analysis (EDA) + Summarization

Compute summary statistics, group-level aggregations, and trend breakdowns directly in DuckDB or pandas.

```python
# Claude can generate EDA queries like:
summary = conn.execute("""
    SELECT
        category,
        region,
        COUNT(*) AS orders,
        SUM(revenue) AS total_revenue,
        AVG(revenue) AS avg_order_value,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY revenue) AS median_revenue
    FROM stg_sales
    GROUP BY ALL
    ORDER BY total_revenue DESC
""").df()
```

**Claude prompt:**
```
> Summarize revenue by category and region. Include order count, total, average, and median order value.
```

---

### Step 5: Python Visualizations

Generate charts using Matplotlib and Seaborn to visualize distributions, trends, and comparisons.

```python
# Claude can generate visualization code like:
import matplotlib.pyplot as plt
import seaborn as sns

# Revenue by category
sns.barplot(data=summary, x="category", y="total_revenue")
plt.title("Total Revenue by Category")
plt.tight_layout()
plt.savefig("outputs/revenue_by_category.png")

# Monthly revenue trend
monthly = conn.execute("""
    SELECT DATE_TRUNC('month', order_date) AS month, SUM(revenue) AS revenue
    FROM stg_sales GROUP BY 1 ORDER BY 1
""").df()
sns.lineplot(data=monthly, x="month", y="revenue")
plt.title("Monthly Revenue Trend")
```

**Claude prompt:**
```
> Create a bar chart of revenue by category, a line chart of monthly revenue trend, and a heatmap of region vs category performance.
```

---

### Step 6: Basic Machine Learning

Train simple predictive models using scikit-learn — e.g., predicting order value, classifying churn risk, or clustering customers.

```python
# Claude can generate ML pipelines like:
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

df = conn.execute("SELECT * FROM stg_sales").df()
X = df[["quantity", "category_encoded", "region_encoded"]]
y = df["revenue"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestRegressor()
model.fit(X_train, y_train)
print("MAE:", mean_absolute_error(y_test, model.predict(X_test)))
```

**Claude prompt:**
```
> Train a Random Forest model to predict order revenue. Encode categoricals, split train/test, fit the model, and report MAE and feature importances.
```

---

## Claude Skills & Functionality Used in This Project

| Skill / Feature | What It Does |
|---|---|
| **Code generation** | Writes ingestion scripts, SQL models, EDA queries, chart code, and ML pipelines from natural language |
| **Data quality review** | Suggests null checks, uniqueness constraints, and accepted value ranges based on schema |
| **DuckDB SQL** | Generates and optimizes DuckDB-flavored SQL including `read_csv_auto`, `PERCENTILE_CONT`, `DATE_TRUNC` |
| **MotherDuck MCP** | Runs queries directly against MotherDuck cloud DuckDB from within Claude Code |
| **Visualization generation** | Produces Matplotlib/Seaborn chart code from chart type descriptions |
| **ML pipeline scaffolding** | Scaffolds end-to-end sklearn pipelines with preprocessing, train/test split, and evaluation |
| **Exploratory analysis** | Interprets query results and surfaces trends, anomalies, and recommendations in plain English |
| **Memory** | Remembers project conventions, schema decisions, and past modeling choices across sessions |
| **CLAUDE.md** | Loads project-specific instructions (naming conventions, warehouse dialect, known issues) at session start |

---

## Claude Code Workflows

### Generate a dbt Model

```
> Create a dbt model that calculates 7-day rolling revenue by customer segment from the orders table
```

Claude will generate the SQL model, suggest appropriate materializations, and add column-level documentation.

### Review and Improve SQL

```
> Review this query for performance issues and suggest optimizations
```

Paste or reference a query and Claude will analyze it for inefficient joins, missing filters, or warehouse-specific improvements.

### Write dbt Tests

```
> Add dbt tests for the fct_orders model — cover nulls, uniqueness, referential integrity, and accepted value ranges
```

### Debug a Failed Pipeline Run

```
> Here is the error log from my dbt run. What caused this and how do I fix it?
```

Paste the error output and Claude will diagnose the root cause and walk you through a fix.

### Generate Documentation

```
> Write dbt documentation for all models in the marts/finance/ directory
```

Claude will read existing model files and generate `schema.yml` entries with descriptions for models and columns.

---

## Project Structure

```
Claude-Analytics-Engineering-Data-Setup/
├── CLAUDE.md                  # Claude Code project instructions and conventions
├── README.md
├── models/
│   ├── staging/               # Source-aligned staging models
│   ├── intermediate/          # Reusable building blocks
│   └── marts/                 # Business-facing final models
│       ├── finance/
│       ├── marketing/
│       └── product/
├── tests/                     # Custom dbt tests and data quality checks
├── macros/                    # Reusable SQL macros
├── seeds/                     # Static reference data
├── analyses/                  # Ad hoc analytical queries
├── docs/                      # Supplemental documentation
└── scripts/                   # Python utilities and automation scripts
```

---

## CLAUDE.md

The `CLAUDE.md` file in the root of this repo is read automatically by Claude Code at the start of every session. It contains:

- Project-specific conventions (naming standards, model layers, grain definitions)
- Warehouse dialect and performance guidelines
- Approved patterns for common transformations
- Known data quality issues or caveats Claude should be aware of

Edit `CLAUDE.md` to give Claude context specific to your environment so it generates accurate, consistent code from the start.

---

## Best Practices

- **Review all generated SQL** before running it in production environments. Claude is a collaborator, not an auto-approver.
- **Keep CLAUDE.md updated** with your team's conventions so Claude stays aligned as the project evolves.
- **Use Git** to track all AI-generated changes the same way you would human-written code.
- **Start with staging models** when onboarding Claude to a new source — establish the grain and field definitions early.
- **Iterate conversationally** — ask Claude to refine, explain, or test its own output rather than accepting the first result.

---

## Contributing

1. Create a feature branch
2. Make changes with Claude Code or manually
3. Run `dbt compile` and `dbt test` before opening a PR
4. Request review

---

## License

MIT
