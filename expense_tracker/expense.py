import csv
import os
from dataclasses import dataclass
from datetime import date, datetime

CSV_FIELD_NAMES = ["amount", "category", "description", "date"]
# ASSUMPTION: CSV files should always use this exact column order and these exact names.
# VERIFY: Confirm future CSV files and user-provided files use these headers.
#TODO: Add stronger handling for missing, extra, or reordered CSV columns if needed.
VALIDATION_COMPONENT = "separate"
# ASSUMPTION: Validation should remain outside the Expense dataclass.
# VERIFY: Confirm this stays appropriate as the app grows.
#TODO: Consider moving validation closer to object creation if invalid Expense objects become a problem.
DEFAULT_CSV_FILE = "expenses.csv"
# ASSUMPTION: The app should read and write expenses.csv in the current working directory.
# VERIFY: Confirm users will run the program from the directory where expenses.csv should live.
#TODO: Add a configurable file path if users need to store data elsewhere.


@dataclass
class Expense:
    """Represents a single expense record."""

    # ASSUMPTION: Amounts can be represented accurately enough as float values.
    # VERIFY: Confirm cents-level rounding is acceptable for this beginner project.
    #TODO: Consider Decimal for more precise money handling.
    amount: float
    # ASSUMPTION: Categories are free-form text entered by the user.
    # VERIFY: Confirm there is no required fixed category list.
    #TODO: Add predefined categories if consistent reporting becomes important.
    category: str
    # ASSUMPTION: Descriptions are optional free-form text.
    # VERIFY: Confirm blank descriptions are acceptable.
    #TODO: Add length limits or required descriptions if needed.
    description: str
    # ASSUMPTION: Dates are stored as datetime.date objects internally.
    # VERIFY: Confirm the rest of the app should not store dates as raw strings.
    #TODO: Add timezone or datetime support if expenses need time-of-day tracking.
    date: date


class ExpenseManager:
    """Manages the in-memory collection of expenses."""

    # Initializes an empty list to store Expense objects.
    def __init__(self):
        # ASSUMPTION: In-memory list storage is enough while the program is running.
        # VERIFY: Confirm expense volume will stay small enough for a simple list.
        #TODO: Replace with a database or indexed structure if the dataset grows.
        self.expenses = []

    # Validates expense data, creates an Expense object, and stores it.
    def add_expense(self, amount, category=None, description=None, expense_date=None):
        # ASSUMPTION: Existing Expense objects passed here are already valid.
        # VERIFY: Confirm no outside code can create and pass invalid Expense objects.
        #TODO: Revalidate Expense instances here if direct construction becomes risky.
        if isinstance(amount, Expense):
            expense = amount
        else:
            # ASSUMPTION: Raw field values should be validated before storing.
            # VERIFY: Confirm every user-facing add path calls this manager method.
            #TODO: Add tests for manager-level validation failures.
            expense = validate_expense_data(amount, category, description, expense_date)

        self.expenses.append(expense)
        return expense

    # Returns all stored Expense objects.
    def get_all_expenses(self):
        # ASSUMPTION: Returning the internal list directly is acceptable for this simple app.
        # VERIFY: Confirm callers will not accidentally mutate manager state.
        #TODO: Return a copy if external mutation becomes a concern.
        return self.expenses

    # Calculates total expense amounts grouped by category.
    def get_totals_by_category(self):
        # ASSUMPTION: Category names should match exactly after validation trims whitespace.
        # VERIFY: Confirm categories like "Food" and "food" should remain separate.
        #TODO: Add case normalization if reports should combine differently cased categories.
        totals = {}

        for expense in self.expenses:
            # ASSUMPTION: Float addition is acceptable for category totals.
            # VERIFY: Check whether displayed totals can tolerate normal floating-point behavior.
            #TODO: Use Decimal or integer cents if exact financial arithmetic is required.
            totals[expense.category] = totals.get(expense.category, 0) + expense.amount

        return totals

    # Saves all stored Expense objects to a CSV file.
    def save_to_csv(self, file_path):
        # ASSUMPTION: Saving should overwrite the existing file with current in-memory data.
        # VERIFY: Confirm users do not expect append-only behavior or backups.
        #TODO: Add backup or confirmation behavior before overwriting if needed.
        save_to_csv(self.expenses, file_path)

    # Loads Expense objects from a CSV file into the manager.
    def load_from_csv(self, file_path):
        # ASSUMPTION: Loading should replace any expenses currently in memory.
        # VERIFY: Confirm loading is only called at startup in normal use.
        #TODO: Add merge behavior if users need to import additional files later.
        self.expenses = load_from_csv(file_path)


# Saves Expense objects to a CSV file using CSV_FIELD_NAMES.
def save_to_csv(expenses, file_path):
    # ASSUMPTION: The target file path is writable and its parent directory exists.
    # VERIFY: Confirm file permission errors are acceptable to surface as exceptions.
    #TODO: Add user-friendly handling for file write failures.
    with open(file_path, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELD_NAMES)
        writer.writeheader()

        for expense in expenses:
            # ASSUMPTION: Every item being saved is an Expense with a date object.
            # VERIFY: Confirm no other record type can enter the expenses list.
            #TODO: Add type checks or serialization tests for malformed records.
            writer.writerow(
                {
                    "amount": expense.amount,
                    "category": expense.category,
                    "description": expense.description,
                    "date": expense.date.isoformat(),
                }
            )


# Loads Expense objects from a CSV file.
def load_from_csv(file_path):
    # ASSUMPTION: A missing CSV file means the user has no saved expenses yet.
    # VERIFY: Confirm missing files should not be treated as an error.
    #TODO: Add a startup message if users need to know no file was found.
    if not os.path.exists(file_path):
        return []

    expenses = []

    # ASSUMPTION: The CSV file is plain text using the platform default encoding.
    # VERIFY: Confirm non-ASCII descriptions or files from other systems load correctly.
    #TODO: Specify an encoding such as utf-8 if portability issues appear.
    with open(file_path, "r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        for row_number, row in enumerate(reader, start=2):
            try:
                # ASSUMPTION: Invalid CSV rows should be skipped instead of stopping startup.
                # VERIFY: Confirm users prefer partial load over failing fast.
                #TODO: Track skipped rows and summarize them after loading.
                expense = validate_expense_data(
                    row.get("amount", ""),
                    row.get("category", ""),
                    row.get("description", ""),
                    row.get("date", ""),
                )
                expenses.append(expense)
            except ValueError as error:
                print(f"Skipping invalid row {row_number}: {error}")

    return expenses


# Validates that amount is numeric and greater than zero.
def validate_amount(amount):
    try:
        # ASSUMPTION: User input like "12.50" should be accepted and converted to float.
        # VERIFY: Confirm currency symbols, commas, and localized decimal formats are not required.
        #TODO: Add stricter or more flexible parsing if real-world input demands it.
        amount = float(amount)
    except (TypeError, ValueError):
        raise ValueError("Amount must be a valid number.")

    # ASSUMPTION: Zero and negative expenses are invalid.
    # VERIFY: Confirm refunds, credits, or adjustments should not be entered as negative values.
    #TODO: Add a separate transaction type if income/refunds must be tracked.
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    return amount


# Validates that category is not blank.
def validate_category(category):
    # ASSUMPTION: None and blank categories are invalid.
    # VERIFY: Confirm uncategorized expenses should not be allowed.
    #TODO: Add a default "Uncategorized" category if blanks should be accepted.
    if category is None:
        raise ValueError("Category cannot be blank.")

    # ASSUMPTION: Leading and trailing spaces are accidental and should be removed.
    # VERIFY: Confirm preserving exact category whitespace is never needed.
    #TODO: Add broader normalization such as title case if reporting needs it.
    category = category.strip()

    if not category:
        raise ValueError("Category cannot be blank.")

    return category


# Cleans the optional description field.
def validate_description(description):
    # ASSUMPTION: Missing descriptions should become an empty string.
    # VERIFY: Confirm descriptions are optional in every workflow.
    #TODO: Add required-description validation if project requirements change.
    if description is None:
        return ""

    # ASSUMPTION: Leading and trailing description spaces are accidental.
    # VERIFY: Confirm users do not need exact whitespace preserved.
    #TODO: Add length or content validation if descriptions are displayed elsewhere.
    return description.strip()


# Validates that date uses YYYY-MM-DD format.
def validate_date(expense_date):
    # ASSUMPTION: Existing date objects can be trusted and returned unchanged.
    # VERIFY: Confirm callers will not pass datetime objects where time information matters.
    #TODO: Handle datetime separately if time-of-day data is introduced.
    if isinstance(expense_date, date):
        return expense_date

    try:
        # ASSUMPTION: The only accepted typed date format is YYYY-MM-DD.
        # VERIFY: Confirm users do not need formats like MM/DD/YYYY.
        #TODO: Add alternate date parsing only if it will not confuse validation.
        return datetime.strptime(expense_date.strip(), "%Y-%m-%d").date()
    except (AttributeError, TypeError, ValueError):
        raise ValueError("Date must be in YYYY-MM-DD format.")


# Validates all fields needed to create one Expense object.
def validate_expense_data(amount, category, description, expense_date):
    # ASSUMPTION: Validation should return a fully constructed Expense object.
    # VERIFY: Confirm no caller needs the cleaned individual field values separately.
    #TODO: Add tests for combined validation across all fields.
    return Expense(
        amount=validate_amount(amount),
        category=validate_category(category),
        description=validate_description(description),
        date=validate_date(expense_date),
    )


# Displays the command-line menu options.
def display_menu():
    # ASSUMPTION: The app should expose exactly four menu options.
    # VERIFY: Confirm no separate save-without-exit option is required.
    #TODO: Add more menu options if editing or deleting expenses is introduced.
    print("\nPersonal Expense Tracker")
    print("1. Add expense")
    print("2. View all expenses")
    print("3. View totals by category")
    print("4. Save and exit")


# Prompts the user for expense fields.
def prompt_for_expense():
    # ASSUMPTION: All expense fields should be collected as raw strings from the CLI.
    # VERIFY: Confirm validation should happen after all fields are entered.
    #TODO: Add field-by-field retry prompts for a smoother user experience.
    amount = input("Amount: ")
    category = input("Category: ")
    description = input("Description: ")
    expense_date = input("Date (YYYY-MM-DD): ")

    return amount, category, description, expense_date


# Displays all expenses in a readable command-line format.
def display_expenses(expenses):
    # ASSUMPTION: An empty expense list should be reported as "No expenses found."
    # VERIFY: Confirm this message is clear enough for first-time users.
    #TODO: Add a distinction between no file loaded and no expenses stored if needed.
    if not expenses:
        print("No expenses found.")
        return

    for index, expense in enumerate(expenses, start=1):
        # ASSUMPTION: A simple pipe-separated line is readable enough for this CLI.
        # VERIFY: Confirm alignment or table formatting is not required.
        #TODO: Add tabular formatting if expense lists become hard to scan.
        print(
            f"{index}. {expense.date.isoformat()} | "
            f"{expense.category} | "
            f"${expense.amount:.2f} | "
            f"{expense.description}"
        )


# Displays category totals in a readable command-line format.
def display_category_totals(totals_by_category):
    # ASSUMPTION: Empty totals mean there are no expenses to summarize.
    # VERIFY: Confirm no separate "all totals are zero" state is needed.
    #TODO: Add total count and grand total if summary reporting expands.
    if not totals_by_category:
        print("No expenses found.")
        return

    for category, total in totals_by_category.items():
        # ASSUMPTION: Insertion order from the dictionary is acceptable for display.
        # VERIFY: Confirm users do not need alphabetical or highest-total-first sorting.
        #TODO: Sort categories if predictable report order becomes important.
        print(f"{category}: ${total:.2f}")


# Coordinates startup, user choices, saving, and exiting.
def main():
    manager = ExpenseManager()
    # ASSUMPTION: Expenses should load automatically from the default CSV file on startup.
    # VERIFY: Confirm users should not choose the file interactively.
    #TODO: Add file selection or command-line arguments if multiple files are needed.
    manager.load_from_csv(DEFAULT_CSV_FILE)

    while True:
        display_menu()
        # ASSUMPTION: Menu choices are entered as text and compared to "1" through "4".
        # VERIFY: Confirm numeric parsing is unnecessary for this simple menu.
        #TODO: Add command aliases like "add" or "quit" if useful.
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            try:
                amount, category, description, expense_date = prompt_for_expense()
                # ASSUMPTION: manager.add_expense is the single path that validates and stores input.
                # VERIFY: Confirm no other code appends directly to manager.expenses.
                #TODO: Make expenses private if direct mutation becomes a problem.
                manager.add_expense(amount, category, description, expense_date)
                print("Expense added.")
            except ValueError as error:
                # ASSUMPTION: Validation errors should be printed and the menu should continue.
                # VERIFY: Confirm users should re-enter the whole expense after one invalid field.
                #TODO: Add targeted retry prompts for the invalid field.
                print(f"Error: {error}")
        elif choice == "2":
            # ASSUMPTION: Viewing all expenses should not reload from disk.
            # VERIFY: Confirm in-memory data is the source of truth during a session.
            #TODO: Add manual reload if external file edits need to be reflected.
            display_expenses(manager.get_all_expenses())
        elif choice == "3":
            # ASSUMPTION: Category totals should be calculated from current in-memory expenses.
            # VERIFY: Confirm unsaved new expenses should appear in the summary immediately.
            #TODO: Add date filters or category filters if summary needs grow.
            display_category_totals(manager.get_totals_by_category())
        elif choice == "4":
            # ASSUMPTION: Exiting should always save current expenses to the default CSV file.
            # VERIFY: Confirm users should not be allowed to exit without saving.
            #TODO: Add save failure handling so users do not lose data silently.
            manager.save_to_csv(DEFAULT_CSV_FILE)
            print(f"Expenses saved to {DEFAULT_CSV_FILE}. Goodbye.")
            break
        else:
            # ASSUMPTION: Invalid menu input should show an error and continue the loop.
            # VERIFY: Confirm repeated invalid input does not need a maximum retry limit.
            #TODO: Add help text if users repeatedly enter invalid choices.
            print("Error: Please enter a valid option from 1 to 4.")


sample_expense = Expense(
    # ASSUMPTION: This module-level sample is useful for simple verification tests.
    # VERIFY: Confirm production code should keep sample data in the main module.
    #TODO: Move sample data into tests if it starts cluttering application code.
    amount=12.5,
    category="Food",
    description="Lunch",
    date=date(2026, 5, 13),
)

assert sample_expense.amount == 12.5
assert sample_expense.category == "Food"
assert sample_expense.description == "Lunch"
assert sample_expense.date == date(2026, 5, 13)


if __name__ == "__main__":
    main()
