# Clinic Tracker: project notes

**Role of this file:** this is the shared source of truth for the build. It is plain English,
not code. Nothing here runs. It exists so that the decisions we make live are written down
somewhere the AI can be pointed back to.

The AI forgets between sessions. When it drifts, paste the relevant section back into the chat.

**Rule zero: synthetic data only. Never real patient information, at any point.**

---

## What the tool does (version 1)

- Add an appointment: patient reference, date, category, cost
- Total spending by category
- Save the list to a file and reopen it later
- Produce a spend summary a clinic manager can read

## What it does NOT do (version 1)

- No interface
- No email or notifications
- No real data, no database

---

## What goes in

| Field | Example | Notes |
|---|---|---|
| `patient_ref` | PT-001 | Required. Format must be `PT-` plus exactly 3 digits |
| `date` | 2026-08-03 | Required. Must be `YYYY-MM-DD` and a real calendar date |
| `category` | Consultation | Must be one of the valid list below (case-insensitive input) |
| `cost` | 120.00 | Required. Must be numeric and zero or above |

**Valid categories:** Consultation, Diagnostics, Procedure, Follow-up, Pharmacy

## What comes out

A total per category, a saved file that can be reopened, and a printed spend summary showing
visits, spend, and share per category with the largest cost driver named.

Saved file for version 1 is `appointments.csv` with this header format:

`patient_ref,date,category,cost`

---

## Tricky cases we decided on purpose

These are our decisions, not the AI's. If the AI does something different, the AI is wrong.

- A cost of zero is **allowed**. Zero means free, not invalid.
- A negative cost is **refused**, not quietly accepted.
- A missing patient reference or date is **refused**.
- A missing cost is **refused**.
- An unknown category is **refused**.
- Category matching is case-insensitive (`consultation` and `Consultation` are the same).
- Patient reference must match `PT-###`.
- Date must be valid format and valid calendar day.
- An empty list totals to nothing. It does not crash.
- A category with no activity shows as zero in the report. It does not disappear.
- If more than one category ties for largest spend, list all tied categories.
- Duplicate `patient_ref` records are refused on save.

---

## The pieces

Built in this order, because each one depends on the one above it.

1. `check_entry` refuse bad input before it gets in
2. `add_appointment` add one appointment to the list
3. `total_by_category` add up spending per category
4. `save` write the list to a file
5. `load` read the list back later
6. `build_report` turn the totals into something a clinic manager would read

Pieces 1 to 5 live in `clinic_tracker.py`. Piece 6 lives in `clinic_report.py`.

### Six pieces, five passes

`save` and `load` are built together in one pass, because neither is useful without the other.
So six pieces become five passes of the 8-step loop:

| Pass | Piece | Where it happens |
|---|---|---|
| 1 | `check_entry` | Built together in the session |
| 2 | `add_appointment` | **You build this one**, in the second half |
| 3 | `total_by_category` | Same loop, run again |
| 4 | `save` and `load` | Same loop, run again |
| 5 | `build_report` | Same loop, run again |

Nothing new is learned between pass one and pass five. Same prompts, same decisions file, same
checks, run again.

---

## How we check the pieces

Checks are printed lines, not a test framework. Each one prints its name, what we expected, what
we got, and PASS or FAIL. You should be able to read the output without knowing any Python.

`check_entry_checks.py` covers five situations:

| Situation | Kind | Expected |
|---|---|---|
| A good entry | normal | accepted |
| A cost of exactly zero | edge, the boundary | accepted |
| A cost of minus 0.01, just below zero | edge, the boundary | refused |
| A clearly negative cost of minus 50 | failure | refused |
| An unknown category | failure | refused |

The two boundary cases sit either side of zero on purpose. Boundaries are where errors hide, and
everyday examples alone would never have caught the difference.

`edge_cases_checks.py` covers additional edge behavior:

- Invalid calendar date is refused
- Missing cost is refused
- Lowercase category input is accepted
- Duplicate `patient_ref` save is refused
- Empty dataset summary is handled without crash
- Tie for largest cost driver returns all tied categories

---

## The numbers we expect

From `appointments_sample.csv`, seven rows:

| Category | Visits | Spend |
|---|---|---|
| Consultation | 2 | 240.00 |
| Diagnostics | 2 | 550.50 |
| Procedure | 1 | 890.00 |
| Follow-up | 1 | 60.00 |
| Pharmacy | 1 | 15.25 |
| **Total** | **7** | **1,755.75** |

If the tool prints anything other than this, the tool is wrong, not the table.

---

## Run all checks

From this folder, run:

- `python3 check_entry_checks.py`
- `python3 edge_cases_checks.py`
