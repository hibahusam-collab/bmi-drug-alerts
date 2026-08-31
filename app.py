"""BMI + Obesity-Class Drug Alerts - Gradio front end.

Educational tool only. Do not enter real patient-identifiable data.
"""

from dotenv import load_dotenv
import gradio as gr

from calculator import calculate_bmi, classify_bmi
from db import init_db, get_alerts, log_calculation

# Load environment config, then auto-initialize the database on startup.
load_dotenv()
init_db()


def run(weight_kg, height_cm):
    if weight_kg in (None, "") or height_cm in (None, ""):
        return "Please enter both weight and height."
    try:
        weight = float(weight_kg)
        height = float(height_cm)
        bmi = calculate_bmi(weight, height)
    except (TypeError, ValueError) as err:
        return f"Invalid input: {err}"

    category, class_key = classify_bmi(bmi)
    log_calculation(weight, height, bmi, category)

    lines = [f"## BMI: {bmi} kg/m^2", f"**Category:** {category}", ""]
    if class_key:
        alerts = get_alerts(class_key)
        if alerts:
            lines.append(f"### Obesity dosing alerts - {category}")
            for a in alerts:
                lines.append(f"- **{a['drug_name']}** - {a['alert']}")
    else:
        lines.append("_No obesity-class drug alerts for this BMI range._")

    lines.append("")
    lines.append(
        "_Educational tool only - verify against your local formulary, "
        "protocols, and clinical judgment._"
    )
    return "\n".join(lines)


with gr.Blocks(title="BMI + Obesity-Class Drug Alerts") as demo:
    gr.Markdown(
        "# BMI + Obesity-Class Drug Alerts\n"
        "Enter a weight and height to get the BMI, WHO category, and, for "
        "obesity classes, common weight-related dosing/monitoring prompts.\n\n"
        "**Do not enter real patient-identifiable data.**"
    )
    with gr.Row():
        weight = gr.Number(label="Weight (kg)", value=70)
        height = gr.Number(label="Height (cm)", value=170)
    calculate = gr.Button("Calculate", variant="primary")
    output = gr.Markdown()

    calculate.click(run, inputs=[weight, height], outputs=output)
    weight.submit(run, inputs=[weight, height], outputs=output)
    height.submit(run, inputs=[weight, height], outputs=output)


if __name__ == "__main__":
    demo.launch()
