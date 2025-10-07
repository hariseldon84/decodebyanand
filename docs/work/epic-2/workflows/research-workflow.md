# Research Workflow & Fact-Check Protocol
This workflow keeps every video grounded in credible evidence while staying nimble with Markdown notes and the available toolset.

## 1. Plan & Scope (30 minutes)
- Define the core question and intended pillar.
- List sub-questions that require data, expert quotes, or historical context.
- Create a research notes file under `../scripts/research-notes/{video-slug}.md`.

## 2. Source Hunting (2–4 hours per topic)
- Prioritize Indian government portals (MeitY, RBI, NITI Aayog), think tanks (IDFC Institute, Takshashila), academic journals (EPW, Nature India), and credible media (The Hindu, Indian Express, Bloomberg).
- For international context, use IMF, World Bank, McKinsey (cross-check against Indian data).

### Evaluation Criteria
| Criterion | Questions | Action |
| --- | --- | --- |
| Credibility | Who authored it? What is the publication's track record? Is the data primary? | Favor official/peer-reviewed sources; flag opinion pieces. |
| Bias | Does the source have a declared agenda or funding? Is language loaded? | Note bias in research log; balance with opposing view. |
| Recency | When was it published? Is newer data available? | Prefer sources ≤24 months old unless historical reference. |

## 3. Note-Taking Structure
Use the following Markdown skeleton inside each research note file:
```markdown
# {Video Title} – Research Notes

## Source Table
| Ref | Source | Credibility (1-5) | Bias Notes | Recency | Key Insight |
| --- | --- | --- | --- | --- | --- |

## Narrative Threads
- Thread 1: Summary + supporting sources
- Thread 2: Counterpoints + sources
- Thread 3: Indian context tie-ins

## Data & Quotes
- {S1} Figure / Quote / Statistic
- {S2} Figure / Quote / Statistic

## Fact-Check Flags
- Claim needing 3-source verification
- Potentially controversial statement + planned disclaimer

## B-Roll / Visual Ideas
- OBS screen capture cue
- Canva infographic concept

## Open Questions
- [ ] Outstanding interview / expert outreach
- [ ] Missing dataset?
```

## 4. Fact-Checking Protocol
1. **3-Source Rule:** Any statistic, projection, or bold claim must be validated across at least three credible references. Record source IDs (`{S1}`, `{S2}`, `{S3}`) directly in the script margin.
2. **Conflicting Data:** If sources diverge, document each perspective and explain the divergence in-script. Transparency maintains intellectual honesty.
3. **Speculative Content:** Tag lines with `(speculative)` when evidence is suggestive, not conclusive. Prepare on-screen disclaimer.
4. **Date Check:** Revisit fast-changing metrics (funding totals, user counts) within 48 hours of recording to confirm nothing materially shifted.

## 5. Citation Format
```
Author Last, First (Year). "Title." Publication Name. URL. Accessed: YYYY-MM-DD.
```
- Include citation block at script end.
- In-script, reference as `{S1 @ 05:12}` to bind to timeline.

## 6. Pre-Recording Review (30 minutes)
- Skim notes with script open; mark any weak evidence.
- Confirm all citations exist in Markdown file and script.
- Log outstanding TODOs in Notion or preferred tracker.

## 7. Post-Publish Maintenance
- Archive research notes under `../scripts/research-notes/archive/` once video is live.
- Append updated stats or corrections in the note file with date stamps for future revisits.
