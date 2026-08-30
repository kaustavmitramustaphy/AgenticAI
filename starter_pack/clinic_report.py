from clinic_tracker import (
    CATEGORY_ORDER,
    DATA_FILE_NAME,
    _compute_category_summary,
    load,
)


def build_report(file_name=DATA_FILE_NAME, print_output=True):
    appointments = load(file_name)
    summary = _compute_category_summary(appointments)
    totals = summary["totals"]
    total_visits = summary["total_visits"]
    total_spend = summary["total_spend"]
    largest_cost_drivers = summary["largest_cost_drivers"]
    skipped_rows = summary["skipped_rows"]

    lines = []
    lines.append("Clinic Spend Summary")
    lines.append(f"Source file: {file_name}")
    lines.append("")

    for category in CATEGORY_ORDER:
        visits = totals[category]["visits"]
        spend = totals[category]["spend"]
        share = (spend / total_spend * 100) if total_spend > 0 else 0.0
        lines.append(
            f"- {category}: visits={visits}, spend={spend:.2f}, share={share:.2f}%"
        )

    lines.append("")
    lines.append(f"Total visits: {total_visits}")
    lines.append(f"Total spend: {total_spend:.2f}")

    if largest_cost_drivers:
        lines.append("Largest cost driver: " + ", ".join(largest_cost_drivers))
    else:
        lines.append("Largest cost driver: None")

    if skipped_rows > 0:
        lines.append(f"Skipped rows: {skipped_rows}")

    report = "\n".join(lines)
    if print_output:
        print(report)
    return report
