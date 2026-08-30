# Your session pack

**Applications of AI and Agentic AI in Healthcare, Week 2 Mentor-Led Session**
AI-Assisted Coding with Codex in VS Code

**Rule zero: synthetic data only. Never real patient information, at any point.**
Not in a prompt, not in a file, not in a screenshot.

---

## Before the session

1. Make a clean, empty folder on your computer. Open it as your VS Code workspace.
2. Copy the files from this pack into it.
3. That is all. You do not need to install or read anything else.

You will not be writing code from memory. You will be asking for it, reading it back, and
deciding whether it is safe to use.

---

## What is in here

| File | What it is |
|---|---|
| `project_notes.md` | The decisions. Plain English, nothing runs. This is what we point the AI back to when it drifts. Read it before the session. |
| `appointments_sample.csv` | Seven made-up appointment rows. No real patient data anywhere. |
| `check_entry_checks.py` | Five checks that prove one piece behaves. You will run this in Step 6. |
| `catch_up_release_at_the_break/` | Do not open this until your mentor says so. |

There are no finished `.py` files in this pack on purpose. Handing over the answers before you
build undercuts the whole point. You will get them after the session.

---

## The two file types, and why the difference matters

> The `.md` files hold the decisions. The `.py` files hold the work.

`project_notes.md` is plain text. It runs nothing and breaks nothing. That is exactly why it is
the right place for requirements: you can read it, edit it, and argue with it without touching
anything that executes.

`clinic_tracker.py` is the thing the computer actually runs.

A decision that only lives in the chat window is a decision the AI will forget.

---

## Write this down before the session starts

From `appointments_sample.csv`, Consultation is two visits at 120.00 each.

**You should see 240.00.**

Write that number on paper. Knowing the answer before you ask is the single most useful habit
in this session, and you will use this number three separate times.

---

## After the session

You will be sent a second folder containing the finished code, the report step, and the checks.
Slide 33 of the deck tells you what to do with it. The short version: rebuild one piece on your
own, and confirm the report prints 1,755.75 across seven appointments.
