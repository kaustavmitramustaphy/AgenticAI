"""
Checks for check_entry.

Run it with:   python check_entry_checks.py

There is no test framework here on purpose. Each check prints one line showing
what you expected, what you got, and PASS or FAIL. You should be able to read
the output without knowing any Python.

Five situations, three kinds:
  normal  - what a clinic sees every day
  edge    - exact boundary values, where errors hide
  failure - things that must be refused

SYNTHETIC DATA ONLY. Never enter real patient information.
"""

try:
    from clinic_tracker import check_entry
except ImportError:
    print("")
    print("There is no clinic_tracker.py in this folder yet, or it has no check_entry piece.")
    print("That is expected before Step 4. Build check_entry first, save it as clinic_tracker.py")
    print("in this same folder, then run this file again.")
    print("")
    raise SystemExit(0)


def run_check(name, problems, should_be_refused):
    """
    One check. 'problems' is what check_entry gave back.
    An empty list means the entry was accepted.
    """
    was_refused = len(problems) > 0
    expected = "refused" if should_be_refused else "accepted"
    got = "refused" if was_refused else "accepted"
    verdict = "PASS" if was_refused == should_be_refused else "FAIL"
    print("  {:<40} expected {:<9} got {:<9} {}".format(name, expected, got, verdict))
    return verdict == "PASS"


print("")
print("CHECKS FOR check_entry")
print("")

results = []

# normal
results.append(run_check(
    "a good entry",
    check_entry("PT-001", "2026-08-03", "Consultation", 120.00),
    should_be_refused=False))

# edge: the exact boundary. Zero means free, not invalid.
results.append(run_check(
    "a cost of exactly zero",
    check_entry("PT-001", "2026-08-03", "Consultation", 0),
    should_be_refused=False))

# edge: just below the boundary. This is where errors hide.
results.append(run_check(
    "a cost of minus 0.01, just below zero",
    check_entry("PT-001", "2026-08-03", "Consultation", -0.01),
    should_be_refused=True))

# failure
results.append(run_check(
    "a clearly negative cost of minus 50",
    check_entry("PT-001", "2026-08-03", "Consultation", -50),
    should_be_refused=True))

results.append(run_check(
    "an unknown category",
    check_entry("PT-001", "2026-08-03", "Astrology", 50),
    should_be_refused=True))

print("")
print("  {} of {} checks passed.".format(sum(results), len(results)))
print("")
print("Now do one by hand, on paper, before you trust any of this:")
print("  Consultation is two visits at 120.00 each. You should see 240.00.")
