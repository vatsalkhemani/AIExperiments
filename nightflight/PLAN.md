# Nightflight — working plan & continuity notes

Purpose: lets any session (or a cheaper model) resume mid-stream. Update the
checklist as you go. App = single `index.html`, Three.js r160 vendored in
`lib/`, no build step. Serve with `python3 -m http.server` from this folder.

## Current milestone: "golden hour" quality pass — ✅ DONE (all six steps)

- [x] 1. **Fixed sunset lighting** — remove the day/night cycle (`DAYP`, `mix3`,
      palette arrays, and the per-frame "sun cycle" block in `tick()`); replace
      with one static golden-hour setup (warm low sun = key light with shadows,
      cool moon fill, warm horizon sky, lighter fog, stars faint). Keep the
      per-frame lines that make sun/moon FOLLOW `rig.position` so shadows stay
      crisp. Goal: consistent visibility — never too dark, never blown out.
- [x] 2. **Normal-mapped stone** — add `normalFromHeight(draw)` helper (Sobel on
      a canvas heightmap of the same ashlar block pattern as `greystone`);
      apply to `stoneM`, hall `wallM`, classroom walls. This is the "brick
      relief" upgrade — raking sunset light makes it pop.
- [x] 3. **People in the Great Hall** — two InstancedMeshes (robed capsule
      bodies + skin-tone heads, ~115 students on the benches, 5 staff at the
      high table). Classrooms + Quidditch already have people.
- [x] 4. **Retake screenshots** (brighter + more zoomed out) into
      `screenshots/` with the SAME filenames (`great-hall.jpg`,
      `castle-approach.jpg`, `quidditch.jpg`) so README links hold.
      Method: temporarily add `window.__shot` (canvas→jpeg dataURL),
      `window.__tp` (teleport), and a `go.click()` autostart; run
      `scratchpad shot_receiver.py`-style local POST receiver on :8125; page
      fetches each shot to it. REMOVE all three debug lines after.
      Camera spots: hall (0, 142, -58, yaw 0) · exterior (0, 95, 760, yaw 0)
      · quidditch (505, 92, -80, yaw -PI/2).
- [x] 5. **README updates** — this project's README + `../README.md` table row:
      say "perpetual golden-hour/sunset", drop the sun-cycle bullet.
- [x] 6. **Commit** in the AIExperiments repo (already authorized). Do NOT push
      unless Vatsal says so (branch already 1 ahead of origin).

## Gotchas learned (do not rediscover these)

- **Chrome caches index.html between navigates** — after editing, always load with a
  fresh query string (`index.html?v=N`) or you will debug a stale build. This
  cost a full detour ("missing" Quidditch stands that were never missing).

- Browser-automation clicks sometimes miss (screenshot px ≠ CSS px when DPR
  shifts) → prefer the autostart line + `__tp` over UI clicks while testing.
- The automation channel occasionally delivers phantom key events after
  `navigate` — app is fine (proven with an event trap); ignore stray motion.
- `save_to_disk` screenshots go somewhere unfindable; JS tool blocks base64
  return. The local-POST-receiver trick is the reliable capture path.
- Debug spawn/autostart lines are marked `// DEBUG` — always grep them out
  before committing.

## Key code landmarks (index.html)

- Lighting rig: `moon`, `sun`, `hemi`, `amb`, `bloom` near top; sky uniforms at
  `window.__skyU`; lit windows material `window.__winMat`; hall ceiling
  `window.__vaultMat`; candle materials `window.__flameMats`.
- Hall constants: `HALL={W:64,H:58,L:210,fy:PLA,zC:-155}` (interior z −260…−50).
- `terrainH(x,z)` = analytic ground truth for mesh AND flight clamp.
- `colliders[]` = solid world (boxes + cylinders), resolved in `tick()`.
