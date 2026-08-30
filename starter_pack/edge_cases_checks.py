"""
Edge checks for clinic tracker.

Run it with:   python3 edge_cases_checks.py

No test framework on purpose. Each check prints expected vs got with PASS/FAIL.
"""

import os
import tempfile

from clinic_tracker import (
    CATEGORY_ORDER,
    check_entry,
    load,
    save,
    total_by_category,
)


def run_check(name, condition, expected_text, got_text):
    verdict = "PASS" if condition else "FAIL"
    print("  {:<48} expected {:<20} got {:<20} {}".format(
        name,
        expected_text,
        got_text,
        verdict,
    ))
    return verdict == "PASS"


def make_temp_csv_path():
    file_handle = tempfile.NamedTemporaryFile(prefix="clinic_edge_", suffix=".csv", delete=False)
    file_handle.close()
    os.unlink(file_handle.name)
    return file_handle.name


print("")
print("EDGE CHECKS")
print("")

results = []

# 1) Zero cost boundary is accepted.
results.append(run_check(
    "check_entry accepts exact zero cost",
    check_entry("PT-001", "2026-08-03", "Consultation", 0) == [],
    "accepted",
    "accepted" if check_entry("PT-001", "2026-08-03", "Consultation", 0) == [] else "refused",
))

# 2) Real calendar validation catches impossible dates.
invalid_date_problems = check_entry("PT-001", "2026-02-30", "Consultation", 50)
results.append(run_check(
    "check_entry refuses invalid calendar date",
    len(invalid_date_problems) > 0,
    "refused",
    "refused" if len(invalid_date_problems) > 0 else "accepted",
))

# 2b) Invalid date format is refused.
invalid_date_format_problems = check_entry("PT-001", "2026/08/03", "Consultation", 50)
results.append(run_check(
    "check_entry refuses invalid date format",
    len(invalid_date_format_problems) > 0,
    "refused",
    "refused" if len(invalid_date_format_problems) > 0 else "accepted",
))

# 3) Missing cost is explicitly refused.
missing_cost_problems = check_entry("PT-001", "2026-08-03", "Consultation", "")
results.append(run_check(
    "check_entry refuses missing cost",
    "cost is required" in missing_cost_problems,
    "cost is required",
    "cost is required" if "cost is required" in missing_cost_problems else str(missing_cost_problems),
))

# 4) Category validation is case-insensitive.
case_result = check_entry("PT-099", "2026-08-12", "consultation", 120.00)
results.append(run_check(
    "check_entry accepts lowercase category",
    case_result == [],
    "accepted",
    "accepted" if case_result == [] else "refused",
))

# 4b) Missing patient reference is refused.
missing_patient_ref = check_entry("", "2026-08-12", "Consultation", 120.00)
results.append(run_check(
    "check_entry refuses missing patient_ref",
    "patient_ref is required" in missing_patient_ref,
    "patient_ref is required",
    "patient_ref is required" if "patient_ref is required" in missing_patient_ref else str(missing_patient_ref),
))

# 4c) Missing date is refused.
missing_date = check_entry("PT-099", "", "Consultation", 120.00)
results.append(run_check(
    "check_entry refuses missing date",
    "date is required" in missing_date,
    "date is required",
    "date is required" if "date is required" in missing_date else str(missing_date),
))

# 4d) Missing category is refused.
missing_category = check_entry("PT-099", "2026-08-12", "", 120.00)
results.append(run_check(
    "check_entry refuses missing category",
    "category is required" in missing_category,
    "category is required",
    "category is required" if "category is required" in missing_category else str(missing_category),
))

# 4e) Invalid patient_ref formats are refused.
bad_ref_short = check_entry("PT-1", "2026-08-12", "Consultation", 120.00)
bad_ref_long = check_entry("PT-0001", "2026-08-12", "Consultation", 120.00)
results.append(run_check(
    "check_entry refuses invalid patient_ref format",
    "patient_ref must match PT-###" in bad_ref_short and "patient_ref must match PT-###" in bad_ref_long,
    "refused",
    "refused" if (
        "patient_ref must match PT-###" in bad_ref_short
        and "patient_ref must match PT-###" in bad_ref_long
    ) else "accepted",
))

# 4f) Non-numeric cost is refused.
non_numeric_cost = check_entry("PT-099", "2026-08-12", "Consultation", "abc")
results.append(run_check(
    "check_entry refuses non-numeric cost",
    "cost must be numeric" in non_numeric_cost,
    "cost must be numeric",
    "cost must be numeric" if "cost must be numeric" in non_numeric_cost else str(non_numeric_cost),
))

# 4g) Boolean cost is refused.
boolean_cost = check_entry("PT-099", "2026-08-12", "Consultation", True)
results.append(run_check(
    "check_entry refuses boolean cost",
    "cost must be numeric" in boolean_cost,
    "cost must be numeric",
    "cost must be numeric" if "cost must be numeric" in boolean_cost else str(boolean_cost),
))

# 5) Duplicate patient_ref is refused by save().
duplicate_path = make_temp_csv_path()
first_save = save({
    "patient_ref": "PT-001",
    "date": "2026-08-03",
    "category": "Consultation",
    "cost": 120.00,
}, duplicate_path)
second_save = save({
    "patient_ref": "PT-001",
    "date": "2026-08-04",
    "category": "Diagnostics",
    "cost": 300.00,
}, duplicate_path)
loaded_after_duplicate = load(duplicate_path)
results.append(run_check(
    "save refuses duplicate patient_ref",
    first_save is True and second_save is False and len(loaded_after_duplicate) == 1,
    "first save true, second false, 1 row",
    f"{first_save}, {second_save}, {len(loaded_after_duplicate)} row(s)",
))

# 6) Empty file path loads as empty list and summary does not crash.
empty_path = make_temp_csv_path()
empty_summary = total_by_category(empty_path)
empty_total_visits = sum(item["visits"] for item in empty_summary["totals"].values())
empty_total_spend = sum(item["spend"] for item in empty_summary["totals"].values())
all_categories_present = set(empty_summary["totals"].keys()) == set(CATEGORY_ORDER)
results.append(run_check(
    "total_by_category handles empty dataset",
    empty_total_visits == 0 and empty_total_spend == 0 and all_categories_present,
    "0 visits, 0 spend, all categories",
    f"{empty_total_visits} visits, {empty_total_spend:.2f} spend, categories={all_categories_present}",
))

# 7) Largest cost driver includes all ties.
tie_path = make_temp_csv_path()
save({"patient_ref": "PT-010", "date": "2026-08-01", "category": "Consultation", "cost": 100.0}, tie_path)
save({"patient_ref": "PT-011", "date": "2026-08-02", "category": "Diagnostics", "cost": 100.0}, tie_path)
tie_summary = total_by_category(tie_path)
tie_result = tie_summary["largest_cost_driver"]
results.append(run_check(
    "total_by_category returns all tied cost drivers",
    tie_result == ["Consultation", "Diagnostics"],
    "[Consultation, Diagnostics]",
    str(tie_result),
))

# 8) Unknown category row in file is safely skipped.
skip_unknown_path = make_temp_csv_path()
save({"patient_ref": "PT-020", "date": "2026-08-01", "category": "Consultation", "cost": 100.0}, skip_unknown_path)
with open(skip_unknown_path, "a", encoding="utf-8") as file_handle:
    file_handle.write("PT-021,2026-08-02,Unknown,250.00\n")
skip_summary = total_by_category(skip_unknown_path)
results.append(run_check(
    "summary skips unknown-category file row",
    skip_summary["skipped_rows"] == 1 and skip_summary["totals"]["Consultation"]["visits"] == 1,
    "1 skipped row, consultation=1",
    f"{skip_summary['skipped_rows']} skipped, consultation={skip_summary['totals']['Consultation']['visits']}",
))

# 9) Corrupt cost row is safely skipped.
corrupt_cost_path = make_temp_csv_path()
with open(corrupt_cost_path, "w", encoding="utf-8") as file_handle:
    file_handle.write("patient_ref,date,category,cost\n")
    file_handle.write("PT-030,2026-08-01,Consultation,100.00\n")
    file_handle.write("PT-031,2026-08-02,Diagnostics,not_a_number\n")
corrupt_summary = total_by_category(corrupt_cost_path)
results.append(run_check(
    "summary skips corrupt cost file row",
    corrupt_summary["skipped_rows"] == 1 and corrupt_summary["totals"]["Consultation"]["visits"] == 1,
    "1 skipped row, consultation=1",
    f"{corrupt_summary['skipped_rows']} skipped, consultation={corrupt_summary['totals']['Consultation']['visits']}",
))

# 10) Save fails safely when target path cannot be written as a file.
blocked_path = tempfile.mkdtemp(prefix="clinic_blocked_")
save_to_dir_result = save(
    {
        "patient_ref": "PT-040",
        "date": "2026-08-03",
        "category": "Consultation",
        "cost": 100.00,
    },
    blocked_path,
)
results.append(run_check(
    "save handles unwritable target path",
    save_to_dir_result is False,
    "False",
    str(save_to_dir_result),
))

# 11) Load fails safely when target path cannot be opened as a file.
load_from_dir_result = load(blocked_path)
results.append(run_check(
    "load handles unreadable target path",
    load_from_dir_result == [],
    "[]",
    str(load_from_dir_result),
))

for path in [duplicate_path, empty_path, tie_path, skip_unknown_path, corrupt_cost_path]:
    try:
        if os.path.exists(path):
            os.remove(path)
    except OSError:
        pass

try:
    if os.path.exists(blocked_path):
        os.rmdir(blocked_path)
except OSError:
    pass

print("")
print("  {} of {} checks passed.".format(sum(results), len(results)))
print("")
