# Rebuild

A rebuild is for a consortium shape the delivered workbook can no longer absorb: more Beneficiaries or Affiliated Entities than its spare blocks hold, another number of work packages or tasks, or another set of Estimation Methods. It delivers a fresh blank Planning Workbook and a re-paste guide. The guide tells the human which input block of their old workbook to copy where in the new one.

You never ask for, open or read the old workbook, not even its file name or path. Everything comes from two sets of Shape Parameters: the old ones and the new ones. The **Shape Parameters guard** in [interview.md](interview.md) applies to both.

## Steps

1. **Old Shape Parameters.** Ask the user to open their old workbook themselves and read you the Provenance block on its Cover Sheet: Funding Profile, profile version, Beneficiaries, Affiliated Entities per Beneficiary, work packages, tasks per work package, duration, Estimation Methods and headroom. Tell them to read only that block, which holds counts and choices, never names or figures. Write the values into the old JSON exactly as given. The Cover lists methods by id, the same ids the JSON takes. "none" for tasks means you leave the `tasks` key out.
   Done when you hold every old Shape Parameter, as the Cover Sheet shows it.
2. **New Shape Parameters.** Run the interview in [interview.md](interview.md) from topic 2 on, proposing each old value as the starting point. Skip topic 1. A rebuild keeps the old Funding Profile version, even when `ENGINE profiles` lists a newer one: input-block layouts are a contract within one version, and the rules must not change mid-proposal. If the user wants a newer version, offer a fresh build instead (the steps in [SKILL.md](SKILL.md)); they then re-enter their inputs by hand, with no re-paste guide.
   Done when you hold a value, or a stated default, for every new Shape Parameter.
3. **Confirm.** Pipe both to `ENGINE confirm-rebuild` as one object, and show the user its read-back verbatim:

   ```json
   {"old": { ...old Shape Parameters... }, "new": { ...new Shape Parameters... }}
   ```

   You may leave `profile` out of `new`, and it takes the old one. Ask the user to confirm both halves or correct them. On a correction, re-run and show the new read-back.
   Done when the user has said yes to the latest read-back. A refusal (exit 2) names `old` or `new` and the key: go back to step 1 or 2 for it.
4. **Rebuild, check and deliver.** Choose the package directory as [handover-package.md](handover-package.md) says, then pipe the same object to `ENGINE rebuild --out "<directory>"`. It runs exactly what `deliver` runs ([build-steps.md](build-steps.md)) for the new Shape Parameters: generate, structural checks, the Synthetic Check in Excel, the Handover Package. It then writes `re-paste-guide.md` into the package. Use the same foreground run and timeout as `deliver`.
   Done when the command has exited.
5. **Report.** As step 4 of [SKILL.md](SKILL.md), with four paths on success. Then the re-paste steps:
   - The re-paste guide lists blocks to copy (old range, new range, per sheet), what is new and has to be filled in fresh, and what has no place in the new workbook.
   - The user copies each block with Paste Special > Values, so the new workbook keeps its own formats, dropdowns and formulas.
   - Blocks are matched by BE/AE nr, WP nr and task nr. If the partner, work package or task that left was not the last one, they match those blocks themselves. Every block of a kind has the same layout, so any of them pastes into any other.
   - The old workbook stays with them. You will not open the new one either, once it is filled in.

   On a failure nothing was delivered, and no re-paste guide was written.
   Done when the user has the package's four paths and the re-paste steps, or the failed step and its error output.
