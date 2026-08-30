import csv
import re
from datetime import datetime


VALID_CATEGORIES = [
    "Consultation",
    "Diagnostics",
    "Procedure",
    "Follow-up",
    "Pharmacy",
]

CATEGORY_LABELS = {category.lower(): category for category in VALID_CATEGORIES}

DATA_FILE_NAME = "appointments.csv"
CSV_FIELDS = ["patient_ref", "date", "category", "cost"]
CATEGORY_ORDER = VALID_CATEGORIES.copy()


def check_entry(patient_ref, date, category, cost):
    problems = []

    if patient_ref is None or str(patient_ref).strip() == "":
        problems.append("patient_ref is required")
    elif re.fullmatch(r"PT-\d{3}", str(patient_ref).strip()) is None:
        problems.append("patient_ref must match PT-###")

    if date is None or str(date).strip() == "":
        problems.append("date is required")
    else:
        date_text = str(date).strip()
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
        except ValueError:
            problems.append("date must be a valid YYYY-MM-DD calendar date")

    if category is None or str(category).strip() == "":
        problems.append("category is required")
    elif str(category).strip().lower() not in CATEGORY_LABELS:
        problems.append("category must be valid")

    if cost is None or str(cost).strip() == "":
        problems.append("cost is required")
    elif isinstance(cost, bool) or not isinstance(cost, (int, float)):
        problems.append("cost must be numeric")
    elif cost < 0:
        problems.append("cost cannot be negative")

    return problems


def add_appointment(patient_ref, date, category, cost):
    patient_ref_input = "" if patient_ref is None else str(patient_ref).strip().upper()
    date_input = "" if date is None else str(date).strip()
    category_input = "" if category is None else str(category).strip()

    cost_input = cost
    if isinstance(cost, str):
        trimmed_cost = cost.strip()
        if trimmed_cost == "":
            cost_input = ""
        else:
            try:
                cost_input = float(trimmed_cost)
            except ValueError:
                cost_input = trimmed_cost

    problems = check_entry(patient_ref_input, date_input, category_input, cost_input)
    if problems:
        return str(problems)

    entry = {
        "patient_ref": patient_ref_input,
        "date": date_input,
        "category": CATEGORY_LABELS.get(category_input.lower(), category_input),
        "cost": cost_input,
    }

    if save(entry, DATA_FILE_NAME) is True:
        print(load(DATA_FILE_NAME))
        return "Data saved and here is the full data"

    return "Data was not saved"


def save(entry, file_name):
    try:
        appointments = load(file_name)
        new_patient_ref = str(entry.get("patient_ref", "")).strip().upper()
        existing_patient_refs = {
            str(appointment.get("patient_ref", "")).strip().upper()
            for appointment in appointments
        }
        if new_patient_ref in existing_patient_refs:
            return False

        appointments.append(entry)
        with open(file_name, "w", newline="", encoding="utf-8") as file_handle:
            writer = csv.DictWriter(file_handle, fieldnames=CSV_FIELDS)
            writer.writeheader()
            for appointment in appointments:
                writer.writerow({
                    "patient_ref": appointment["patient_ref"],
                    "date": appointment["date"],
                    "category": appointment["category"],
                    "cost": f"{float(appointment['cost']):.2f}",
                })
        return True
    except (OSError, TypeError, ValueError, KeyError):
        return False


def load(file_name):
    try:
        with open(file_name, "r", newline="", encoding="utf-8") as file_handle:
            reader = csv.DictReader(file_handle)
            appointments = []
            for row in reader:
                appointments.append({
                    "patient_ref": row["patient_ref"],
                    "date": row["date"],
                    "category": row["category"],
                    "cost": float(row["cost"]),
                })
    except FileNotFoundError:
        return []
    except (OSError, ValueError, KeyError):
        return []

    return appointments


def _compute_category_summary(appointments):
    totals = {category: {"visits": 0, "spend": 0.0} for category in CATEGORY_ORDER}
    skipped_rows = 0

    for appointment in appointments:
        if not isinstance(appointment, dict):
            skipped_rows += 1
            continue

        category_text = str(appointment.get("category", "")).strip().lower()
        category_name = CATEGORY_LABELS.get(category_text)
        if category_name is None:
            skipped_rows += 1
            continue

        try:
            cost_value = float(appointment.get("cost", 0))
        except (TypeError, ValueError):
            skipped_rows += 1
            continue

        totals[category_name]["visits"] += 1
        totals[category_name]["spend"] += cost_value

    total_visits = sum(item["visits"] for item in totals.values())
    total_spend = sum(item["spend"] for item in totals.values())

    if total_spend > 0:
        highest_spend = max(item["spend"] for item in totals.values())
        largest_cost_drivers = [
            category for category in CATEGORY_ORDER if totals[category]["spend"] == highest_spend
        ]
    else:
        largest_cost_drivers = []

    return {
        "totals": totals,
        "total_visits": total_visits,
        "total_spend": total_spend,
        "largest_cost_drivers": largest_cost_drivers,
        "skipped_rows": skipped_rows,
    }


def total_by_category(file_name=DATA_FILE_NAME):
    appointments = load(file_name)
    summary = _compute_category_summary(appointments)
    totals = summary["totals"]
    total_visits = summary["total_visits"]
    total_spend = summary["total_spend"]
    largest_cost_drivers = summary["largest_cost_drivers"]
    skipped_rows = summary["skipped_rows"]

    print("Spend summary")
    for category in CATEGORY_ORDER:
        visits = totals[category]["visits"]
        spend = totals[category]["spend"]
        share = (spend / total_spend * 100) if total_spend > 0 else 0.0
        print(f"{category}: visits={visits}, spend={spend:.2f}, share={share:.2f}%")
    print(f"Total: visits={total_visits}, spend={total_spend:.2f}")

    if largest_cost_drivers:
        print("Largest cost driver: " + ", ".join(largest_cost_drivers))
    else:
        print("Largest cost driver: None")

    if skipped_rows > 0:
        print(f"Skipped rows: {skipped_rows}")

    return {
        "saved_file": file_name,
        "reopened_data": appointments,
        "totals": totals,
        "largest_cost_driver": largest_cost_drivers,
        "skipped_rows": skipped_rows,
    }


def generate_manager_report(file_name=DATA_FILE_NAME):
    from clinic_report import build_report

    return build_report(file_name)


def main():
    print("Enter appointment details")
    patient_ref = input("patient_ref (example PT-001): ")
    date = input("date (YYYY-MM-DD): ")
    category = input("category: ")
    cost = input("cost: ")

    result = add_appointment(patient_ref, date, category, cost)
    print(result)

    if result == "Data saved and here is the full data":
        total_by_category(DATA_FILE_NAME)
        generate_manager_report(DATA_FILE_NAME)


if __name__ == "__main__":
    main()
