# The Handover Package

## Choosing the directory

`deliver` needs a new or empty directory, so no file from an earlier package can pass for part of this one. Propose:

```
<user's Documents folder>/Planning Workbooks/<profile id>-<version>-<YYYYMMDD-HHMM>
```

Use the current date and time, and let the user choose another new or empty directory. The directory name should stay neutral. If the user wants the project's acronym in it, they can rename the folder themselves after delivery. Keep the package outside this repository, because the user will fill the workbook in and a filled workbook must never be committed.

## What is in it

- `planning-workbook.xlsx`: the blank Planning Workbook. Its Cover Sheet holds the provenance, the Checks panel, the fill-in order and the colour legend: light yellow cells are inputs, white cells are derived, and guards are coloured by status.
- `synthetic-check-report.md`: the evidence that the blank workbook calculates correctly.
- `fill-in-guide.md`: per sheet, what to enter, the unit and the source, and step by step how to transfer the Transfer Views into the Submission Budget.

## What to tell the user

- The three paths, as `deliver` printed them.
- Whether the Synthetic Check ran on a provisional scenario (from the report's scenario line).
- Next steps: open the workbook in Excel 2021 or 365 and fill it in following the Cover Sheet's fill-in order and `fill-in-guide.md`, entering names and all other values only in the yellow cells.
- From here on the workbook is theirs alone. You will never open it, not even for a small fix. A different consortium shape needs a new build.
