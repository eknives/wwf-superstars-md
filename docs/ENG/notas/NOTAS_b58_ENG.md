# b58 (from b57)

ROM: `wwf_b58.bin`  md5 `cbe3a2b0976a142ceb25068edc660869`

b57 intact (md5 `8651e4ef71af09be6260350b1489e20d`). Only the referee changes from static to alive.

## Referee rules (confirmed by Emilio)

1. **Like the others:** HIGH priority + colour zones (green / purple / orange / yellow) + drawing order by feet vs Duggan; **keeps walking around** (`refAvoid`).
2. **HUD:** any referee piece whose screen `y` touches the HUD (`y < HUD_H`, 34) is forced to **LOW**; the rest are not.
3. **Sides:** the limit is kept — he does not step on the side ropes (`RF_MARGIN 16` inside `RING_XL`/`RING_XR` with the perspective `e`).
4. **Walks around the ring:** follows Duggan when he goes further than `RF_KEEP` (56 px), 1 px/frame (s41 logic / arcade state 0).

## Clamp (origin)

`rfClamp` in `src/main.c`:

- Y: `RING_Y0+8` … `RING_Y1-4`, plus `ylim` (HUD ceiling / camera).
- X: `lo = RING_XL + e + RF_MARGIN`, `hi = RING_XR - e - RF_MARGIN` with `e = (rfy-RING_Y0)/6`.
- `RF_MARGIN = 16` (s51 slack). It is called before and after `refAvoid`.

`RING_XL=616`, `RING_XR=917` (right limit from b55).

## Walk (origin)

- **Follow:** `rfStep` — if `|ox-rfx|` or `|oy-rfy|` > `RF_KEEP`, advances 1 px towards Duggan (dominant axis; diagonal if both are large). Source: series s / s41 return home / arcade follow state 0.
- **Walk around:** `refAvoid` ported from **s51** (1 actor = Duggan): if it overlaps in X with feet lower on screen, it looks for a gap below / ±X without violating the side margin.
- **Anim:** `spr_tab` poses **510–512** (`PT_RWK`) come **without a head** (first piece at dy=16). In b58:
  - idle / sideways movement or towards the camera → pose **8** + H-flip if going right;
  - only when moving away (`hy>0`, no `hx`) → alternates **508/509** (back, with head).

## Palettes

No change from b57:

| Line | Use |
|---|---|
| 0/1 | background + crowd + ropes + HUD + **referee** |
| 2 | Duggan |
| 3 | partners (Macho/Hogan) |

Referee VRAM: `RF_T0=1088` (28 t), `RF_T1=1512` (rest). Ropes at 1120 untouched.

## What was not touched

Partners, Duggan, ropes, corner posts, WWF logo (still pending, manual), controls, sound, `RING_XR`.

## Shots

- `shots/b58_idle.png` — idle with head
- `shots/b58_walk1.png` … `b58_walk4.png` — follow around the ring (rfx 768→887 in the MAME run)
- MAME: `test/t58.lua` + `test/o_b58/`

Pending, manual (no change): top corner posts + patched WWF logo.
