# Reading the source documents

A new version starts from documents, never from a filled-in Planning Workbook (ADR-0001). Typical sources:

- a new Programme Guide (Erasmus+), or new General Annexes or Work Programme (Horizon Europe)
- a new or amended unit-cost decision, such as an amendment of C(2024)5405 for travel, accommodation and subsistence
- a new release of the Official Budget Table (the Submission Budget's own layout)

## What to do

1. Ask the user which documents changed, and for each one the exact version or decision number and its date. Get the file into `excel_module/docs/` (the user downloads it if you cannot).
2. Run `ENGINE profiles` to see the accepted versions, and read the latest one of the profile (`profiles/data/<id>/<version>.json`). Its `provenance` lists the documents it was built from.
3. Read the new document against the parts of the profile it can touch: Profile Constants, unit-cost tables, cost categories and the Submission Budget layout, Staff Categories, Estimation Methods, rule checks and Lump Sum Tiers. Note every difference with its page.
4. Present the list of changes to the user: what changes, from what to what, and the source and page for each. Say plainly where the document is ambiguous instead of choosing for them.
5. Agree the new version number with the user. Suggest a minor step (1.0 to 1.1) for changed amounts or constants, and a major step (1.0 to 2.0) for a changed layout or method set. Input-block layouts are a contract within a version, so a layout change always means a new version too.

Done when the user has agreed the list and the version number.
