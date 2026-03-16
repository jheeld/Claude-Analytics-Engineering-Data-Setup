# Claude Project Guidelines

This repository contains machine learning case analysis workflows.

## Templates

Reusable templates exist in the `templates/` directory.

Key templates:

- templates/ml_case_template.ipynb → standard ML case notebook structure

Before writing new analysis code, check the templates directory for reusable patterns.

## ML Workflow

When solving a machine learning problem:

1. Start from `templates/ml_case_template.ipynb`.
2. Follow the notebook structure sequentially.
3. Inspect the dataset before modeling.
4. Perform exploratory data analysis before feature engineering.
5. Start with a simple baseline model.
6. Compare at least two candidate models.
7. Evaluate models with appropriate metrics.
8. Conclude with a business-focused recommendation.

## Coding Style

- Use pandas for tabular inspection.
- Use sklearn pipelines for preprocessing and modeling.
- Prefer readable and production-oriented Python.
- Include concise explanations for each modeling step.

## Goal

Produce clear, structured machine learning analyses suitable for real-world decision making.