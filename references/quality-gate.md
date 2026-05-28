# Video Quality Gate

Use this gate before delivering any generated animation or finished Remotion
video. The goal is to catch visual defects early, repair them deliberately, and
ship the best faithful output rather than the first successful render.

## Candidate Artifacts

Keep each reviewed attempt in a numbered folder:

```text
out/review/attempt-1/
out/review/attempt-2/
out/review/attempt-3/
```

Each attempt should include:

| Artifact | Purpose |
|---|---|
| `stills/` | Representative frames from scene starts, peaks, transitions, and the ending |
| `check.mp4` | A short frame-range render that covers the riskiest motion |
| `video.mp4` | The full candidate render when the short check passes |
| `cover.png` | A still frame suitable as the video cover |
| `review.md` | Short notes with defects found, fixes applied, and final decision |

Do not commit these generated artifacts unless the user explicitly asks for
source-controlled examples.

## Visual Checks

Inspect representative stills before rendering the full video:

```bash
pnpm exec remotion still Main --frame=0 out/review/attempt-1/stills/0000.png
pnpm exec remotion still Main --frame=30 out/review/attempt-1/stills/0030.png
pnpm exec remotion still Main --frame=90 out/review/attempt-1/stills/0090.png
```

Choose frames that reveal:

- opening layout, title, and subject identity;
- every major scene after its entrance animation settles;
- transitions, overlays, captions, lower thirds, and charts;
- any 3D camera move, model reveal, or texture-heavy section;
- the proposed cover frame.

Check the stills for:

- no blank, black, transparent, or loading-only frames;
- no clipped text, unreadable captions, or accidental overlaps;
- stable composition with the important subject visible and correctly framed;
- faithful depiction of requested objects, data, interface states, or physical
  layouts;
- readable contrast, restrained motion blur, and no unintended pixelation;
- consistent typography, color semantics, spacing, and safe margins;
- no off-brand placeholders, debug UI, missing assets, or console errors.

Then render a short motion check for the riskiest segment:

```bash
pnpm exec remotion render Main out/review/attempt-1/check.mp4 --frames=0-120
```

Watch for jitter, frozen animations, timing gaps, audio/video drift, subtitle
lag, transition flashes, and elements appearing in the wrong order.

## Retry Policy

If the candidate fails the visual checks, repair the source and render a new
candidate. Retry at most three total attempts:

1. Attempt 1: first complete implementation.
2. Attempt 2: targeted fixes for concrete defects found in attempt 1.
3. Attempt 3: final repair pass focused only on remaining delivery blockers.

Avoid speculative rewrites during retries. Keep each pass tied to observed
defects such as clipped labels, missing assets, incorrect motion timing, camera
framing, contrast failures, or audio sync problems.

If all three attempts still have imperfections, choose the best candidate by
this priority order:

1. Faithfulness to the user's requested subject, data, flow, and real-world
   details.
2. Clear visibility of the main subject throughout the video.
3. Absence of severe visual defects such as blank frames, overlaps, clipping,
   flashing, or missing media.
4. Smooth motion, audio sync, and readable captions.
5. Overall visual polish.

Document the selected attempt in `review.md` and mention any residual risk in
the final response.

## Full Render And Merge

Render the chosen candidate at delivery quality:

```bash
pnpm exec remotion render Main out/video.mp4 --codec=h264 --crf=18
```

If the project renders scenes as separate segments, merge only the reviewed
segments in timeline order. Prefer Remotion composition-level rendering when
possible; use `ffmpeg` concat only when segment rendering is necessary:

```text
file 'scene-01.mp4'
file 'scene-02.mp4'
file 'scene-03.mp4'
```

```bash
ffmpeg -f concat -safe 0 -i out/segments/concat.txt -c copy out/video.mp4
```

After merging, play or probe the merged video and verify duration, audio, and
scene order. If concat copy fails because segment codecs differ, re-render the
single Remotion composition instead of stacking ad hoc transcodes.

## Cover Still

Export a cover from the chosen candidate, usually from a frame where the main
subject is visible, the title is readable, and the composition is not mid-motion:

```bash
pnpm exec remotion still Main --frame=90 out/cover.png
```

The cover should:

- communicate the topic at a glance;
- avoid closed eyes, motion smear, half-transition states, and cropped subjects;
- leave safe margins for platform UI overlays;
- match the final video's visual system.

Deliver both `out/video.mp4` and `out/cover.png` when the user asks for a
finished video.
