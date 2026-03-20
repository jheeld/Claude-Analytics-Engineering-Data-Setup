---
name: ml-problem-framing
description: Force structured problem framing before any ML modeling begins.
---

# ML Problem Framing Skill

Focuses purely on business and product context. Dataset inspection is handled by `dataset-context`. Do not repeat schema or EDA work here.

Show 10 random rows from the dataset first, then ask the following questions. Wait for answers before proceeding.

## 1. Objective
- What exactly are we predicting?
- What is the unit of prediction? (e.g. user, transaction, time-step, household)

## 2. Business Action
- What decision or action will this model trigger?
- Who consumes the model output and how?

## 3. Success Metrics
- Offline metric: precision, recall, F1, AUC, RMSE — pick the right one based on the problem
- Business metric: fewer missed payments, fewer false alerts, reduced churn, etc.
- What does "good enough" look like to ship?

## 4. Constraints
- Real-time vs batch inference?
- What data is available at prediction time vs what would leak the future?

## 5. Risks
- Class imbalance
- Bias across user segments (new vs old, low vs high activity)
- Cold start for new entities

## Behavior

Do NOT cover dataset inspection, column types, or EDA — that belongs in `dataset-context`.

Once all questions are answered, write the framing directly into the notebook as a markdown cell under "Problem Framing."
