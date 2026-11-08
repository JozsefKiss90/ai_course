# Planning Workbooks change shape without macros

Because the agent never touches a filled-in Planning Workbook (ADR-0001), a workbook must absorb consortium changes on its own. We use no VBA. Instead: row-wise growth (Beneficiaries, Affiliated Entities, work packages, tasks) comes from Excel Tables with structured references and dynamic-array formulas. Per-Beneficiary column blocks are built with spare capacity up to a profile-defined maximum. Larger reshapes are done by generating a fresh blank workbook and re-pasting human inputs into its stable, documented layouts. This deliberately departs from the Official Budget Table's macro-driven "Add BE / Add WP" pattern. Macros would mean `.xlsm` security prompts, Mac and Excel-online gaps, and VBA the agent cannot test against real data.

**Consequences**: Planning Workbooks require Excel 2021 / Microsoft 365 (dynamic arrays). Input-block layouts are a contract: changing them breaks re-paste.
