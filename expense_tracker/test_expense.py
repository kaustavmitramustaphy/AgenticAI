from datetime import date
import unittest

from expense import CSV_FIELD_NAMES, Expense, VALIDATION_COMPONENT, sample_expense


# Prints the expected and actual values so each test can be manually verified.
def print_manual_check(test_name, explanation, expected, actual):
    print(f"\n{test_name}")
    print(f"Explanation: {explanation}")
    print(f"Expected: {expected}")
    print(f"Actual:   {actual}")


class TestExpenseModel(unittest.TestCase):
    # Tests that a new Expense stores each field exactly as provided.
    def test_expense_stores_expected_fields(self):
        expense = Expense(
            amount=10.0,
            category="Food",
            description="Sandwich",
            date=date(2026, 1, 15),
        )

        expected = {
            "amount": 10.0,
            "category": "Food",
            "description": "Sandwich",
            "date": date(2026, 1, 15),
        }
        actual = {
            "amount": expense.amount,
            "category": expense.category,
            "description": expense.description,
            "date": expense.date,
        }
        print_manual_check(
            "test_expense_stores_expected_fields",
            "A new Expense should keep the same values used to create it.",
            expected,
            actual,
        )

        self.assertEqual(expense.amount, 10.0)
        self.assertEqual(expense.category, "Food")
        self.assertEqual(expense.description, "Sandwich")
        self.assertEqual(expense.date, date(2026, 1, 15))

    # Tests that the sample expense uses easy-to-verify expected values.
    def test_sample_expense_has_expected_values(self):
        expected = {
            "amount": 12.5,
            "category": "Food",
            "description": "Lunch",
            "date": date(2026, 5, 13),
        }
        actual = {
            "amount": sample_expense.amount,
            "category": sample_expense.category,
            "description": sample_expense.description,
            "date": sample_expense.date,
        }
        print_manual_check(
            "test_sample_expense_has_expected_values",
            "The built-in sample expense should match the values in expense.py.",
            expected,
            actual,
        )

        self.assertEqual(sample_expense.amount, 12.5)
        self.assertEqual(sample_expense.category, "Food")
        self.assertEqual(sample_expense.description, "Lunch")
        self.assertEqual(sample_expense.date, date(2026, 5, 13))

    # Tests that future CSV support has the expected field order.
    def test_csv_field_names_are_in_expected_order(self):
        expected = ["amount", "category", "description", "date"]
        actual = CSV_FIELD_NAMES
        print_manual_check(
            "test_csv_field_names_are_in_expected_order",
            "CSV columns should appear in the same order as the Expense fields.",
            expected,
            actual,
        )

        self.assertEqual(CSV_FIELD_NAMES, ["amount", "category", "description", "date"])

    # Tests that validation is planned as a separate component.
    def test_validation_component_is_separate(self):
        expected = "separate"
        actual = VALIDATION_COMPONENT
        print_manual_check(
            "test_validation_component_is_separate",
            "Validation should be tracked as separate from the Expense data model.",
            expected,
            actual,
        )

        self.assertEqual(VALIDATION_COMPONENT, "separate")


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
