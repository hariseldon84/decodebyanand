# Video 7 Work: "Data is the New Real Estate"

## Research & Script Status
- Script: `docs/work/epic-2/scripts/fullscripts/video-7-data-as-real-estate.md` — 2,400-word deep dive into India’s data center boom and governance.
- Research notebook: _Pending_. Create `docs/work/epic-2/scripts/research-notes/video-7-data-as-real-estate.md` compiling MeitY capacity forecasts, state policies (Maharashtra, Telangana), CEEW electricity projections, and industry reports (JLL, NTT).
- Updates: Confirm latest GSAT-20 launch timeline (S2) if referenced in overlays and gather new investment announcements from AdaniConneX, Yotta, or Hiranandani.

## Pre-Production Checklist
- **Scene Prep:** OBS profile `Decode_CyanGold`; background: stylised server rack animation. Frame Obsbot Tiny 2 slightly off-center to allow data overlays.
- **Audio Chain:** Blue Yeti Nano cardioid, gain 10 o’clock; filters—high-pass 80 Hz, RNNoise, compressor (-18 dB), limiter -3 dB.
- **Lighting:** Cool key light to mimic data hall; add warm backlight for separation. White balance 4900K.
- **Visual Assets:** Canva infographics (capacity growth chart, state incentive map, energy mix pie). Export to `assets/graphics/video-7/`. Prepare motion graphic of data center stack (land, power, fiber layers).
- **B-Roll:** iPhone footage of server rack props (LED strip), Noida skyline, fiber cables. OBS capture of submarine cable map (TeleGeography), state policy PDFs. Document attributions.

## Recording Plan
1. Rehearse script with emphasis on explaining technical terms (PUE, Ka-band).  
2. Record two VO takes; check pronunciation of company names (AdaniConneX, Equinix).  
3. Export WAVs; use Audacity to remove low-frequency hum and apply light compression.  
4. Capture screen walkthrough of Canva slides + portal data points.  
5. Organize assets in `/videos/raw/video-7/` with subfolders.

## Editing Blueprint (Premiere Pro)
- Sequence 3840 × 2160, 25 fps.  
- Use motion graphics template to animate bar chart progression (2018–2026 capacity).  
- Color grading: cool look (Temperature -5, Tint +4).  
- Audio: Normalize to -16 LUFS; ambient hum track (low-level) at -35 dB under server footage; main bed “Data Flow” (YouTube Audio Library) at -28 LUFS.  
- Graphics: Insert on-screen definitions for PUE, data trust; transitions with digital wipe.  
- Captions: ensure technical terms spelled right; export `video-7-data-real-estate-captions.srt`.

## Thumbnail & Branding
- Tech & Society template with gold accent.  
- Option A: “Data = Property” with server rack + skyline; Option B: “India’s Data Land Rush.”  
- Save PNG (<2 MB) to `/assets/thumbnails/video-7/`; produce mobile preview.

## Metadata & Scheduling
- TODO metadata `docs/work/epic-2/metadata/video-7-metadata.md` highlighting keywords “data center India”, “DPDP Act”, “GSAT-20 broadband”.  
- Upload plan: export master `video-7-data-real-estate_4k.mp4` (H.264, 35 Mbps); upload Unlisted Monday 13:00 IST; schedule Monday 18:00 IST. End screen linking to Tech & Society playlist and upcoming Aadhaar episode.

## Social Distribution Copy
- **Twitter/X:** Thread with 3 charts (capacity, state incentives, energy mix) + CTA question “Which city should host next hyperscale park?”  
- **LinkedIn:** Emphasize investment/green energy interplay; tag MeitY, state IT departments, Brookfield, AdaniConneX.  
- **Instagram carousel:** 5 slides—hook, capacity chart, state incentives map, green energy callout, citizen rights tip.

## Post-Publish Monitoring
- Track comments from industry professionals; capture quotes for newsletter.  
- Analytics: watch for retention around policy-heavy Act 3; adjust pacing if drop >15%.  
- Update `analytics/batch-production-efficiency.md` with actual hours once edit completes.
