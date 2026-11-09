# WWF b69 (base b68, md5 b68 3a41cd79ddf5d3b669c0475ca56ca20c, untouched)

ROM: `wwf_b69.bin`, md5 `b3d460cb3f2bd3bc97338e499f1c2046`

## Changes
1. **Falling on the back**: if he faces right, the head ends up on the LEFT; if he faces left, on the RIGHT (shots 01 and 07).
2. **Floor hits + reaction, for both**: with the opponent lying, A = elbow (poses 521-523) and the one on the floor shakes. B, at 16-100 px from the body, = jump and stomp (poses 537-554), which lands on the body. While being hit, the opponent stays lying (shots 02-05 and 08-10).
3. **Warrior with the same engine as Duggan**: runs (A+B), leaves and enters the ring and climbs up and down the back and front corner posts (shots 13-17).
4. **C = switch control Duggan ↔ Warrior**. It only changes whom the controls command; sprites and positions stay the same (shot 06).
5. **START**: the opponent (the one you don't control) chases you; another START stops him (shots 11-12).

## Technical fixes
- Warrior's tiles have been moved to VRAM 1672, because at 1525 they got corrupted (garbage appeared in the crowd).
- The stomp jump no longer adds an extra height: the height already comes in the poses.
- The chaser does not get on top of you: if he is closer than 20 px, he moves away.

## Approximations and pending items
- If the player walks over the opponent, the sprites may overlap.
- The HUD stays the same as in b68 (for example, the "DUGGAN" label appears even if you control Warrior).
- The offsets of the elbow and stomp have been reviewed by eye with MAME captures, not by comparing them frame by frame with the arcade.
