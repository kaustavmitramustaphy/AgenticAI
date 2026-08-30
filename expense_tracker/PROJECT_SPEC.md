# PROJECT SPEC - Personal Expense Tracker

## What We Are Building
A command-line personal expense tracker in Python.
Users can add, view, summarize, save, and load expenses.

## Components and Status
- [DONE] Component 1: Data Structure (`Expense` dataclass in `expense.py`)
- [DONE] Component 2: Core Manager / `ExpenseManager`
- [DONE] Component 3: File I/O (`save_to_csv`, `load_from_csv`)
- [DONE] Component 4: Input Validation
- [DONE] Component 5: Main Application Loop

## Key Decisions Made
- Expenses are stored as Python dataclasses in `expense.py`
- `CSV_FIELD_NAMES` defines the canonical field order for CSV persistence
- Validation is planned as a separate component from the data model
- Date format is `YYYY-MM-DD`
- The implementation should stay in a single file and use only the Python standard library
- Validation should raise `ValueError` with clear messages

## Current Task
- Implement the core manager, CSV persistence, validation, and main loop in `expense.py`
