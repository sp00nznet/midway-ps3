# Roadmap

## Next

- **Play a credit.** Each game opens a menu first (Free Play, Free Play
  Settings, Score Attack, Controls). The scripted CROSS presses go through it
  into the attract loop; START then shows the "waiting for others" countdown and
  falls back to the demo. Script the menu on purpose (Free Play, then START).
- **Land the runtime fixes.** Get #185 (Join) and #190 (`cellSail` state
  events) merged, and drop the two source overrides in `CMakeLists.txt` once
  `build-gate` has both.
- **Check the in-FIFO flip from #185.** The Simpsons, on the same engine, lost
  the last draws of each frame without it.
- **Audio.** CRI audio on a mixer thread plus `cellAudio`; not checked.
- **More of the 30 games.** Each `.SR` set is a separate emulator core; try a
  few (Joust, Gauntlet, Mortal Kombat).

## Later

- Register the port in ps3recomp's `tools/regress_ports.toml` (the family's
  conformance harness) so a runtime change that breaks the title shows up in
  the shared regression run.
- Hero GIF of real gameplay once a credit can be played.
- Logo and attract movies: decode the AVIs (`cellSail`) instead of skipping
  them.

## Out of scope

- Distributing ROM sets, disc data, keys or generated source.
- Online features (leaderboards, PSN sign-in).
