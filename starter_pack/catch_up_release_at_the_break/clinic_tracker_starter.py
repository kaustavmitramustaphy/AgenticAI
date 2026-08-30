"""
Clinic Tracker: starter file for your own pass.

WHAT THIS FILE IS FOR
Pass 1 (check_entry) was built together in the session, and it is already finished below.
Pass 2 (add_appointment) is yours. It is named but not built, which is a to-do list,
not a failure.

Use the Step 4 prompt from your playbook. Build only add_appointment.
Do not let the AI build anything else yet.

If you fell behind during the session, this file puts you back on the same footing
as everyone else. Start from Step 4.

SYNTHETIC DATA ONLY. Never enter real patient information.
"""

# The only categories this clinic uses. Anything else is refused.
VALID_CATEGORIES = ["Consultation", "Diagnostics", "Procedure", "Follow-up", "Pharmacy"]


# ---------------------------------------------------------------------------
# PASS 1: check_entry. Built together in the session. Do not change this.
# ---------------------------------------------------------------------------

def check_entry(patient_ref, date, category, cost):
    """
    Check one entry before it is added.
    Returns a list of problems. An empty list means the entry is fine.
    """
    problems = []

    if not patient_ref:
        problems.append("Patient reference is missing.")

    if not date:
        problems.append("Date is missing.")

    if category not in VALID_CATEGORIES:
        problems.append("Unknown category: " + str(category))

    try:
        cost_value = float(cost)
    except (TypeError, ValueError):
        problems.append("Cost is not a number.")
        return problems

    # A decision we made on purpose: a negative cost is refused, not quietly accepted.
    if cost_value < 0:
        problems.append("Cost cannot be negative.")

    return problems


# ---------------------------------------------------------------------------
# PASS 2: add_appointment. This one is yours.
#
# What project_notes.md says it must do:
#   - Add one appointment to the list: patient_ref, date, category, cost
#   - Refuse anything that fails check_entry. Do not add it quietly.
#   - Give the caller back the list
#
# Before you ask the AI for anything, write down what you expect to happen when
# you add a good entry, and when you add one with a cost of minus 50.
# ---------------------------------------------------------------------------

def add_appointment(appointments, patient_ref, date, category, cost):
    """Add one appointment to the list. Refuses anything that fails check_entry."""
    pass


# ---------------------------------------------------------------------------
# Your checks for pass 2 go here, or in a separate file.
# Copy the pattern from check_entry_checks.py: name, expected, got, PASS or FAIL.
# Three situations is enough. Choose them before you write them.
# ---------------------------------------------------------------------------
