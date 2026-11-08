# Shape Parameters interview

## Shape Parameters guard

The only things you may ask about, note or pass on are the Shape Parameters below. When the user offers anything else (a partner or institution name, acronym, country, project or task title, person, call or topic ID, salary, rate, effort figure, budget, ceiling or any other amount):

- Leave it out. Don't repeat it, don't write it into the JSON, a file or a note, and don't use it to infer a count.
- Tell the user, once per occurrence and in one or two sentences, why: the Planning Workbook is built from counts and choices only, and they enter that value themselves in the delivered workbook's yellow input cells, because unsubmitted proposal and consortium data stay with them.
- Then ask for the Shape Parameter you actually need, if any. "We have Acme, Beta and Gamma as partners" becomes: "I've left the names out. How many Beneficiaries are there?"

## What to ask

Ask one topic at a time, in this order. Take everything from `ENGINE profiles` output; never offer a profile, method or default it doesn't list.

1. **Funding Profile.** Offer each listed profile by `name`, with its `id` and `version`. If only one is listed, say so and propose it. Use the latest version unless the user names another.
2. **Beneficiaries.** A whole number, 1 or more.
3. **Affiliated Entities.** Ask whether any Beneficiary has Affiliated Entities. If yes, ask how many for each, by code: BE1, BE2, … Omit the key when there are none.
4. **Work packages.** A whole number, 1 or more.
5. **Tasks.** Ask whether they want a Task List (effort planned per task) or effort per work package. With a Task List, ask how many tasks each work package has, by code: WP1, WP2, … A work package may have 0 tasks; its effort is then planned per work package. At least one needs a task. Without a Task List, omit the key.
6. **Duration.** The project duration in whole months.
7. **Estimation Methods.** List the profile's methods by `label`:
   - methods with `default: true` are pre-selected, the others off;
   - methods with `mandatory: true` are locked on: say they are always included and why (the programme's rules need them), and keep them on even if the user asks to drop one.
   The user may switch the others on or off. Omit the key to take the defaults.
8. **Headroom.** State the profile's `default_headroom`: that many spare per-Beneficiary column blocks, so a late Beneficiary or Affiliated Entity can join without a rebuild. Ask whether to keep it or use another whole number (0 or more). Omit the key to keep the default.

## The JSON

```json
{
  "profile": {"id": "he-lump-sum", "version": "1.0"},
  "beneficiaries": 3,
  "affiliated_entities": [0, 1, 0],
  "work_packages": 5,
  "tasks": [3, 2, 4, 2, 1],
  "duration_months": 36,
  "methods": ["staff_effort", "travel_planner"],
  "headroom": 3
}
```

`affiliated_entities` has one entry per Beneficiary and `tasks` one per work package, in code order. `methods` takes the method `id`s. These eight keys are the whole contract; there is no other field.
