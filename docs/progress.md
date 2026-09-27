# Progress log

Newest first. Fixes are in [ps3recomp](https://github.com/sp00nznet/ps3recomp)
unless noted.

## 2026-09-27: day one, in game

From a decrypted EBOOT to Vindicators Part II running in its bezel. The lift
built first time (10,060 functions, 191 imports); everything after that was
three blockers, each a black screen.

| Symptom | Cause | Fix |
|---|---|---|
| Every draw dropped at PSO build (`pso=12` per frame); `[pso-bail] fragment program size reads as zero ... 64 KB from here is entirely zero` | The front end's render job runs on a SPURS job chain named `crTaskRunJobList`. Its two binaries are raw code+data, not ELFs, so `extract_spu_images.py` finds nothing, and both jobs MISSed and completed empty. The 41,856-byte one DMAs each frame's fragment programs, vertices and indices into the IO heap after the command buffer | This repo: `relift.sh` cuts both from `.data` (vaddr `0x291F80`, `0x29C300`) and lifts them |
| After the first frame, nothing but clears and flips. The main loop runs, but no draws | The game plays `LICENSOR.AVI` and `DEVELOPER.AVI` through `cellSail` first. Its driver (`func_00044068`, polled every frame) boots the player and then waits for a `PLAYER_STATE_CHANGED` event saying CLOSED before it creates a descriptor. The runtime sent only `CALL_COMPLETED` | `cellSail.c` reports every state it passes through: `STATE_CHANGED` (major 3, arg0 = the SDK state) around each call, and since nothing decodes the stream, RUNNING drops straight back to OPENED, which is how the game sees a movie end ([#190](https://github.com/sp00nznet/ps3recomp/pull/190)) |
| Title and menus drawn, but a third of draws dropped: `X3504: array index out of bounds`, and 687 of 1,309 pixel shaders with opcodes like STR, SFL and DP2A | `cellSpursJoinJobChain` returned at once. The game runs Run → Join → flush every frame, so the RSX parsed the flush before the render job had written that frame's fragment programs. Each draw has its own ring slot (stride `0x180`), so it decoded whatever the slot last held. `PPU_WWATCH` saw no PPU writes to a slot; `SPU_WATCHEA` showed the job's `PUT` | Join waits for the chain walker. Same bug and same fix as The Simpsons Arcade Game (same Backbone/CRI engine), in [#185](https://github.com/sp00nznet/ps3recomp/pull/185). PSO drops 116,855 → 0 |

How the Sail wait was found: the HLE trace's list of first calls ended at
`cellSailPlayerBoot`. `PPU_WWATCH=32E064` on the driver object (the player
sits at `+0x218`, `0x32E078`) showed its state word at `+0x204` stuck at 2.
The event handler (`func_00044518`) takes events off its queue with
`sys_event_queue_tryreceive`. It maps `STATE_CHANGED` arg0 0–8 through a
table to its own states (CLOSED → 9, OPENED → 4, RUNNING → 6), clears its busy
flag on `CALL_COMPLETED` whatever the minor, and ignores every other major
except 7 (pause). That table matches the SDK numbering, not the
`CELL_SAIL_PLAYER_STATE_*` values in ps3recomp's `cellSail.h`.

`PS3_NO_SAIL=1`, which reports player creation as failed, does not help. The
game boots the player anyway and waits the same way.

Open: a credit starts, shows Vindicators' "waiting for others to join"
countdown, then falls back to the demo. Not investigated yet.
