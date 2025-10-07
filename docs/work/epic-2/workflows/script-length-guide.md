# Script Length & Timing Guide
Use this calculator to keep long-form scripts within the 15–20 minute target while preserving pacing for OBS recording and Premiere editing.

## Baseline Assumptions
- **Speaking pace:** 140 words per minute (Blue Yeti Nano, cardioid)
- **Target duration:** 18 minutes (acceptable range 15–20)
- **Total word count:** 2,100–2,800 words
- **Pause buffer:** Reserve ~5% of on-camera time for natural pauses and visual beats; do not script every second.

## Section Targets
| Segment | Duration | Word Count | Notes |
| --- | --- | --- | --- |
| Opening Hook | 0:30 | 70 ±10 | Fast cut visuals; punchy lines, no long sentences |
| Introduction | 1:00 | 210 ±20 | Context + roadmap; break into 2-3 short paragraphs |
| Act 1 | 4:30 | 630–720 | Define problem or framework; include 3 visual beats |
| Act 2 | 4:30 | 630–720 | Deepen analysis; compare viewpoints |
| Act 3 | 4:30 | 630–720 | Project implications; offer actions |
| Conclusion | 2:00 | 260–300 | Summarize + reflective question |
| Outro | 0:30 | 70 ±10 | CTA + next episode tease |

## Quick Calculator
```
target_words = target_minutes * speaking_pace_wpm
buffer = target_words * 0.05
usable_words = target_words - buffer
act_words = usable_words * 0.75  # 3 acts share 75%
act_per_section = act_words / 3
```

**Example (18-minute video):**
- `target_words = 18 * 140 = 2520`
- `buffer = 2520 * 0.05 = 126`
- `usable_words = 2394`
- `act_words = 2394 * 0.75 = 1795.5`
- `act_per_section ≈ 599` → round to 630 by borrowing from buffer.

## Editing Safety Margin
- Keep main Acts at 600–700 words each. If any section exceeds 750 words, split into two mini-sections to maintain pacing.
- Flag lines for emphasis or pause using `(beat)` notation, which helps maintain rhythm when recording in OBS Studio.

## Tracking Worksheet
- Maintain a running word count spreadsheet (Google Sheets or Notion) with columns: `Video`, `Hook`, `Intro`, `Act1`, `Act2`, `Act3`, `Conclusion`, `Outro`, `Total`.
- After recording, log actual runtime and note variances to refine future scripts.
