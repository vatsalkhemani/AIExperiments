# ROAD CLASH 🏍️

A Road Rash–inspired 3D motorcycle combat racer that runs entirely in the browser —
no build step, no install, no network needed (Three.js is bundled in `lib/`).

## What's in it

- **Scenic valley landscape** — a winding ~3.5 km road through procedurally generated
  rolling hills, pine forests, bushes, rocks, a snow-capped mountain ring, drifting
  clouds, sun glow, and distance fog.
- **Road Rash combat** — 5 named rivals (Viper, Natasha, Biff, Slater, Axel). Ride up
  beside one and punch them off their bike. Watch out — they kick back.
- **Race loop** — 3 laps, live position tracking, minimap, speedometer, countdown
  start, crash/wipeout handling, win/lose screen.
- **Feel** — leaning bike, speed-based FOV stretch, chase camera, engine sound that
  pitches with your speed (WebAudio), grass that slows you down off the asphalt.

## How to play

Serve the folder with any static server (browsers block ES modules over `file://`):

```bash
# from this folder
python3 -m http.server 8000
# then visit http://localhost:8000
```

| Key | Action |
| --- | --- |
| `W` / `↑` | Throttle |
| `S` / `↓` | Brake |
| `A` `D` / `←` `→` | Steer |
| `Space` / `F` | Punch a rival beside you |
| `Enter` | Start race |
| `R` | Restart after finishing |

On touch devices, on-screen buttons appear and the throttle is automatic.

## Tech

Single HTML file + [Three.js](https://threejs.org) r160 (vendored in `lib/`, wired up via import map).
The world is fully procedural: seeded RNG, value-noise terrain with height-based
coloring, a Catmull-Rom spline track with geometry extruded along it, instanced
meshes for vegetation, and canvas-generated textures for the road, clouds, and
banner. No assets to download beyond the Three.js library.
