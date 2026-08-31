"""BMI calculation and obesity classification.

Pure functions with no I/O so they are easy to unit-test.
"""


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Return BMI (kg/m^2) rounded to 1 decimal place.

    Raises ValueError on non-positive input.
    """
    if weight_kg <= 0 or height_cm <= 0:
        raise ValueError("Weight and height must be positive numbers.")
    height_m = height_cm / 100.0
    return round(weight_kg / (height_m ** 2), 1)


def classify_bmi(bmi: float):
    """Map a BMI value to (category_label, obesity_class_key).

    obesity_class_key is None below Class I; otherwise it is the key
    used to look up drug alerts in the database.
    """
    if bmi < 18.5:
        return ("Underweight", None)
    if bmi < 25.0:
        return ("Normal weight", None)
    if bmi < 30.0:
        return ("Overweight", None)
    if bmi < 35.0:
        return ("Obesity Class I", "Class I")
    if bmi < 40.0:
        return ("Obesity Class II", "Class II")
    return ("Obesity Class III", "Class III")
