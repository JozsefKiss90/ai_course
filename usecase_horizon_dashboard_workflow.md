# Use Case: Horizon Dashboard + Perplexity + Claude Cowork
## "Should We Apply? A Data-Driven Call Assessment"

**Scenario:** Your university's PI wants to submit a proposal to a Horizon Europe call in Cluster 4 (Digital, Industry, and Space). Before investing weeks of proposal writing, you need a data-driven go/no-go recommendation. This workflow combines official EU statistics, AI-powered research, and collaborative analysis.

---

## Step 1: Pull Official Data from the Horizon Dashboard

### 1.1 Navigate to the Dashboard

Open: **https://dashboard.tech.ec.europa.eu/extensions/HorizonDashboard/HorizonDashboard.html**

This is the official Horizon Europe statistics dashboard hosted on the EU Funding & Tenders Portal.

### 1.2 Explore Success Rates

Navigate to the **"Proposals & Success Rates"** section (or equivalent -- the Dashboard reorganizes periodically). You are looking for data that shows:

- Overall success rates for Horizon Europe
- Success rates broken down by Cluster or programme part
- Number of proposals submitted vs. funded
- Budget requested vs. budget available

**What to look for specifically:**
- Filter by **Cluster 4** (or "Digital, Industry, and Space")
- Look at the success rate trend across the most recent work programme years
- Note the number of eligible proposals vs. funded proposals
- Check if there's a breakdown by action type (RIA vs. IA)

**Record these key numbers:**

| Metric | Value |
|--------|-------|
| Overall success rate (Cluster 4) | ___% |
| Number of proposals submitted (latest call) | ___ |
| Number of projects funded (latest call) | ___ |
| Average EU contribution per project | EUR ___ |
| Success rate for RIA vs. IA (if available) | RIA: ___% / IA: ___% |

### 1.3 Check Country Participation

Navigate to the **"Participation"** or **"Countries"** section. Filter for your country:

- How many participations from your country in Cluster 4?
- How many as coordinator vs. partner?
- What is your country's success rate compared to the EU average?

### 1.4 Export CSV Data

Most Dashboard views have a **download/export button** (look for a download icon, a "CSV" link, or right-click on the data table). Export the data that shows success rates by call topic within Cluster 4.

**If direct CSV export is not available on the current view:**
- Use the table view and select all data (Ctrl+A), then copy-paste into a spreadsheet
- Or screenshot the data table as a fallback
- Check if there is an "Open Data" or "Raw Data" link at the bottom of the page

**Save the file as:** `horizon_cluster4_success_rates.csv`

**Expected CSV structure (example):**
```
Call Topic,Proposals Submitted,Proposals Funded,Success Rate,EU Contribution
HORIZON-CL4-2024-DATA-01-01,87,12,13.8%,42000000
HORIZON-CL4-2024-DIGITAL-01-03,134,18,13.4%,63000000
HORIZON-CL4-2024-TWIN-01-02,56,8,14.3%,28000000
...
```

> **Note:** The exact structure depends on which view you export. Any tabular data from the Dashboard will work for the next steps.

---

## Step 2: Research Context with Perplexity

### 2.1 Open Perplexity

Open: **https://www.perplexity.ai**

### 2.2 Query 1 -- Success Rate Context

```
What are the typical success rates for Horizon Europe Cluster 4
(Digital, Industry, and Space) proposals in 2024 and 2025?
Break down by action type (RIA vs IA) if possible. What are
the main reasons proposals in this cluster get rejected according
to evaluation summary reports?
```

**What to check in the response:**
- Do the success rate numbers match what you found on the Dashboard?
- Are the sources cited? Click at least 2 citations and verify.
- Note any information Perplexity provides that the Dashboard does NOT (e.g., evaluator feedback, common weaknesses, qualitative insights)

**Record the key findings:**

| Finding | Source Cited? | Matches Dashboard? |
|---------|-------------|-------------------|
| | Y / N | Y / N / N/A |
| | Y / N | Y / N / N/A |
| | Y / N | Y / N / N/A |

### 2.3 Query 2 -- Competitive Landscape

```
What are the most active countries and organizations participating
in Horizon Europe Cluster 4 Digital and AI-related calls? Which
institutions have the highest success rates as coordinators?
Are there any notable trends in consortium composition for
successful proposals?
```

**What to check:**
- Does this align with the country participation data from the Dashboard?
- Are there strategic insights about consortium building?
- Note any specific organizations or countries that dominate

**Key findings to carry forward:**
1. ________________________________________________________________________
2. ________________________________________________________________________
3. ________________________________________________________________________

### 2.4 Query 3 -- Call-Specific Intelligence

```
What are the expected priorities and new topics in the Horizon
Europe Cluster 4 2025 work programme? Are there any shifts in
focus compared to 2024? What TRL levels are typically expected
for RIA projects in this cluster?
```

**Key findings to carry forward:**
1. ________________________________________________________________________
2. ________________________________________________________________________
3. ________________________________________________________________________

### 2.5 Compile Perplexity Findings

Copy the most important findings from all three queries into a single text block. Include the key statistics, qualitative insights, and source URLs. You will paste this into Claude Cowork in the next step.

**Example compiled text:**

```
PERPLEXITY RESEARCH FINDINGS -- Horizon Europe Cluster 4

SUCCESS RATES:
- Overall success rate for Cluster 4 in 2024: ~14% (Source: [URL])
- RIA proposals: ~13%, IA proposals: ~16% (Source: [URL])
- Common rejection reasons: lack of novelty, weak impact pathways,
  unrealistic work plans (Source: [URL])

COMPETITIVE LANDSCAPE:
- Top coordinator countries: Germany, France, Spain, Italy
- Average consortium size for funded RIA: 10-12 partners
- Growing emphasis on SME participation (Source: [URL])

2025 PRIORITIES:
- Increased focus on AI Act compliance in research projects
- New topics on digital twins for manufacturing
- TRL 2-5 expected for most RIA topics (Source: [URL])
```

---

## Step 3: Analyze in Claude Cowork

### 3.1 Open Claude

Open: **https://claude.ai**

If using **Claude Cowork** (collaborative workspace), invite your team members to join the session. If using standard Claude, proceed individually.

### 3.2 Upload the Dashboard CSV

Click the attachment/file upload button in Claude. Upload `horizon_cluster4_success_rates.csv`.

### 3.3 Prompt 1 -- Dashboard Data Analysis

```
I've uploaded a CSV export from the official EU Horizon Dashboard
showing success rates for Horizon Europe Cluster 4 call topics.

Please analyze this data and provide:

1. OVERVIEW: What is the overall success rate across all topics?
   Which topics have the highest and lowest success rates?

2. TRENDS: Are success rates increasing or decreasing across
   recent calls? Any notable patterns?

3. COMPETITION LEVEL: Which topics received the most proposals?
   Which are most competitive (lowest success rate with highest
   number of submissions)?

4. BUDGET ANALYSIS: What is the average EU contribution per funded
   project? Are there differences by topic?

5. STRATEGIC IMPLICATIONS: Based on this data alone, which topic
   areas offer the best odds for a new applicant?

Format as a structured briefing with a summary table.
```

**Expected output:** Claude will produce a structured analysis of the official data, identifying patterns, outliers, and strategic opportunities. Review the numbers -- they should match what you saw on the Dashboard since Claude is analyzing the same data.

### 3.4 Prompt 2 -- Integrate Perplexity Research

Now paste your compiled Perplexity findings as additional context:

```
Now I have additional research context from verified sources.
Please integrate this with your analysis of the Dashboard data:

[PASTE YOUR COMPILED PERPLEXITY FINDINGS HERE]

Based on BOTH the official Dashboard statistics AND this research
context, provide:

1. COMBINED ASSESSMENT: How do the official numbers compare with
   the research findings? Any discrepancies?

2. STRATEGIC POSITIONING: Given the success rates, competition
   levels, common rejection reasons, and 2025 priorities, what
   positioning would give a new proposal the best chance?

3. RISK FACTORS: What are the top 3 risks for a proposal in
   this cluster, supported by both data and research?

4. CONSORTIUM ADVICE: Based on the country participation data
   and competitive landscape, what consortium composition would
   be strategically strong?
```

**Expected output:** Claude will synthesize the quantitative Dashboard data with the qualitative Perplexity research into a comprehensive strategic assessment.

### 3.5 Prompt 3 -- Generate the Go/No-Go Memo

```
Based on all the analysis above, draft a 1-page go/no-go
assessment memo for our Research Director.

Our situation:
- We are a [mid-sized / large] European university in [country]
- Our PI's expertise is in [specific topic area]
- We have existing partnerships with [X] organizations in [Y] countries
- We are considering call topic [specific topic ID if known]
- Our proposed project would be at TRL [X-Y]
- Estimated consortium size: [X] partners

The memo should include:
- Executive recommendation (Go / No-Go / Conditional Go)
- Key data points supporting the recommendation (cite the
  Dashboard statistics)
- Competitive landscape summary
- Key risks and mitigation strategies
- Recommended next steps if "Go"
- Timeline considerations

Tone: Professional, concise, suitable for senior management.
Format: Clear headers, bullet points, no longer than 1 page.
Mark any assumptions with [ASSUMPTION].
```

**Expected output:** A polished, data-driven memo that a Research Director could actually use to make a decision. The memo will reference specific success rates from the Dashboard and strategic insights from the Perplexity research.

---

## Step 4: Verify the Output

### Verification Checklist

Go through the final memo and check:

| Check | Status |
|-------|--------|
| Success rate numbers match the Dashboard? | Y / N |
| Country participation data is accurate? | Y / N |
| No fabricated statistics? | Y / N |
| Perplexity citations were real? (click 2-3) | Y / N |
| Recommendations logically follow from the data? | Y / N |
| [ASSUMPTION] tags used where appropriate? | Y / N |
| Tone is appropriate for senior management? | Y / N |

### Common Issues to Watch For

| Issue | What to Do |
|-------|-----------|
| Claude cites a success rate you didn't provide | Ask: "Where did you get the X% figure? Is it from the CSV I uploaded or from your training data?" Flag any numbers not from the Dashboard. |
| Perplexity's numbers differ from Dashboard | Trust the Dashboard for official statistics. Note the discrepancy in the memo: "Official Dashboard data shows X%; other sources suggest Y%." |
| Claude makes overly confident recommendations | Check that the recommendation is hedged appropriately. A 14% success rate means 86% of proposals fail -- the memo should acknowledge this. |
| Missing [ASSUMPTION] tags | Ask Claude to review and mark all assumptions. |

---

## Summary: The Tool Chain

```
Horizon Dashboard          Perplexity AI              Claude Cowork
(Official Data)            (Research Context)         (Analysis & Writing)

[Export CSV] ─────────────────────────────────────────> [Upload CSV]
                           [Research findings] ──────> [Paste as context]

                                                      [Prompt 1: Analyze data]
                                                      [Prompt 2: Integrate research]
                                                      [Prompt 3: Draft memo]

                                                      --> Go/No-Go Memo

                           *** HUMAN QUALITY GATE ***
                           Research Director reviews
                           and decides
```

### Why Each Tool?

| Tool | Why Not the Others? |
|------|-------------------|
| **Horizon Dashboard** | Only source of authoritative, official EU statistics. No AI tool can replace this. |
| **Perplexity** | Provides narrative context, evaluator insights, and trend analysis WITH citations. Claude would draw on training data (possibly outdated); NotebookLM can only analyze documents you upload. |
| **Claude Cowork** | Best at synthesizing multiple inputs into a polished written deliverable. Can process CSV data. Supports collaborative review with team members. |

### What You Get

A go/no-go memo that is:
- **Data-driven** -- grounded in official Dashboard statistics, not AI guesses
- **Context-rich** -- informed by current research and evaluator feedback
- **Verifiable** -- every number traces back to either the Dashboard or a cited source
- **Professional** -- formatted for senior management decision-making
- **Reusable** -- the prompts can be saved and reused for every new call assessment
