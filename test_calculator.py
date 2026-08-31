"""Basic tests for the BMI logic. Run: python test_calculator.py"""

from calculator import calculate_bmi, classify_bmi


def test_bmi_value():
    assert calculate_bmi(70, 175) == 22.9
    assert calculate_bmi(100, 170) == 34.6


def test_categories():
    assert classify_bmi(17.0) == ("Underweight", None)
    assert classify_bmi(22.9) == ("Normal weight", None)
    assert classify_bmi(27.0) == ("Overweight", None)
    assert classify_bmi(32.0) == ("Obesity Class I", "Class I")
    assert classify_bmi(37.0) == ("Obesity Class II", "Class II")
    assert classify_bmi(41.5) == ("Obesity Class III", "Class III")


def test_invalid_input():
    for bad in [(0, 170), (70, 0), (-5, 170)]:
        try:
            calculate_bmi(*bad)
        except ValueError:
            continue
        raise AssertionError(f"Expected ValueError for {bad}")


if __name__ == "__main__":
    test_bmi_value()
    test_categories()
    test_invalid_input()
    print("All tests passed.")
