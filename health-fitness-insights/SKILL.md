---
name: health-fitness-insights
description: Parse exported health and wearable data (Apple Health XML, CSV, Garmin/Fitbit) into meal, workout, sleep, and trend insights dashboards. Use when the user asks to analyze Apple Health or fitness exports, build a personal health dashboard, or correlate sleep, steps, and nutrition logs.
allowed-tools: client
---
# Health & Fitness Insights

Transform exported wearable and nutrition data (Apple Health `export.xml`, CSV logs, Garmin/Fitbit exports) into clean local trend analyses, meal/workout summaries, and interactive dashboards.

## When to Use

- The user exports Apple Health, Garmin, Fitbit, or nutrition/workout CSV data and wants patterns or visualizations.
- The user wants to build a local personal fitness/meal insights dashboard.
- The user asks to correlate sleep, resting heart rate, step counts, workouts, and calorie/macro logs.

## Steps

### 1. Inspect the Export Format Locally

Check file size and structure before loading into memory (`export.xml` from Apple Health can be hundreds of MB):

```bash
ls -lh /path/to/health_export*
```

For large XML files, use streaming parsing (`xml.etree.ElementTree.iterparse` in Python) filtered to the requested date range and record types (`StepCount`, `ActiveEnergyBurned`, `SleepAnalysis`, `RestingHeartRate`, `BodyMass`, `Workout`).

### 2. Clean and Aggregate Metrics

- Normalize timezones, deduplicate overlapping wearable/phone sources (prefer watch over phone for steps/HR when both exist), and compute 7-day / 30-day rolling averages.
- Summarize adherence, workout frequency, sleep consistency, and macro/calorie trends if meal logs are provided.

### 3. Build Dashboard and Actionable Observations

- Generate a local HTML/Chart.js dashboard or clean Markdown report highlighting objective trends and correlations.
- Frame meal and fitness suggestions as general wellness options aligned with the user's stated goals, and include a clear note that this is informational—not medical advice.

## Scripts

`scripts/health_summary.py` streams Apple Health `export.xml` and writes `daily.csv` (steps with a 7-day average, active energy, resting heart rate, sleep hours) and `summary.md`. It uses one source per metric, so an iPhone and Apple Watch are not added together. Sleep counts only "Asleep" stages.

```bash
python3 scripts/health_summary.py ./export.xml ./out --since 2026-01-01
```

## Gotchas

- **Not medical advice**: Never diagnose conditions or prescribe medical diets/treatments; advise consulting a qualified healthcare professional for medical concerns.
- **Privacy first**: Health exports are sensitive personal data; process everything locally and never upload raw health files to external APIs.
- **Duplicate Apple Health sources**: Summing raw `StepCount` records without filtering by `sourceName` often double-counts iPhone + Apple Watch steps.
