---
title: BMI Obesity-Class Drug Alerts
emoji: 💊
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 6.26.0
app_file: app.py
pinned: false
license: mit
---

# BMI + Obesity-Class Drug Alerts

A small clinical lookup tool built with **Gradio + SQLite**. It computes BMI,
maps it to the WHO category, and for obesity classes returns common
weight-related dosing / monitoring prompts held in a seeded SQLite reference
table.

> **Educational tool only.** It is not a formulary and not a substitute for
> clinical judgment. **Do not enter real patient-identifiable data.**

## Features

- BMI calculation and WHO classification (`calculator.py`)
- SQLite data layer with an **auto-init** pattern and **parameterized
  queries** (`db.py`)
- Seeded reference table of obesity-class dosing alerts (higher classes
  inherit lower-class alerts)
- Anonymous calculation log (anthropometrics only, no identifiers)

## Project structure

```
app.py              Gradio UI
calculator.py       BMI + classification logic
db.py               SQLite auto-init, seed data, queries
test_calculator.py  Basic tests (python test_calculator.py)
requirements.txt
.env.example        Copy to .env
.gitignore
```

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # Windows: copy .env.example .env
python app.py
```

Then open the local URL Gradio prints (default http://127.0.0.1:7860).

Run the tests with:

```bash
python test_calculator.py
```

## Configuration

| Variable  | Default      | Purpose                         |
|-----------|--------------|---------------------------------|
| `DB_PATH` | `bmi_app.db` | Location of the SQLite database |

No secrets are stored in the code. `DB_PATH` is read from the environment.

## Data & privacy

The app stores only weight, height, BMI, and category with a timestamp - no
names, IDs, or other identifiers. On Hugging Face Spaces this database is
ephemeral and resets on restart. In any real clinical setting the calculation
log would need to be disabled or moved behind hospital access controls.

## License

MIT
