# b81 — base b80 preserved

- ROM: `/workspace/b81/wwf_b81.bin`, **1,572,864 bytes**.
- MD5: **ffa3e48e22aee99750cd82af10d6ab31**.
- Base: `/workspace/b80/wwf_b80.bin`, MD5 **d843bac410485579980872341264fda9**, checked intact at the end.
- Local SGDK build; no CloudAgent, nothing published, no remote repositories touched.

## 1. Ropes: short fall identical on left and right

The b80 bug was not only how long the counter lasted: **0x2146E was being interpreted as step→map**. In the arcade there are two distinct levels:

1. **0x21324** starts at step 2 with request `d0=1`, visual phase `d4=3`.
2. **0x213AC** converts step→phase: `1,2,3,2,3,2,3,0`.
3. **0x2146E** converts phase→drawing. It cannot be indexed directly with the step.

In addition, the b80 banks `mp0` and `mp1` have different local indices. For the two equivalent final phases these are used:

| Arcade phase | Left | Right |
|---|---:|---:|
| 3 | mp0[7] | mp1[4] |
| 2 | mp0[6] | mp1[3] |
| 0, rest | mp0[0] | mp1[0] |

The fall now shows **3→2→3→2→3→0**, never the initial running stretch.

Durations from `0x213A4`, steps 2..7: **6,4,3,2,2,1 arcade ticks**. The detail of `0x21324` is also reproduced: it initialises and decrements in the same invocation, and advances before drawing (`0x213B4`). The short clock runs one invocation every two engine iterations, identical for both sides. No pauses are added and time is not multiplied twice.

**Running intact:** the engine branch that runs/bounces and the long sequences `sc0/sc1` are preserved. There is an automatic comparison against the b80 text and running fixtures on both sides.

## 2. Warrior: stomp and jump onto a downed opponent

The previous Warrior jump trajectory based on shifting/scaling `S0C` is removed: it no longer mixes a recorded vertical displacement with a pin sitting height. For Warrior, the move uses the arcade's instructions and tables, not an interpolation of captures.

### Button and position — 0xC706 / 0xC83E / 0xCB3C

Let `s = +1` if the opponent's orientation bit is set, `-1` otherwise. The selection anchor is **rival.x + s*0x28**. In the same plane and with **abs(dy)<0x18**:

- In front of the anchor, **distance <0x20**: **B → sub 0x0C**, jump.
- Behind, **distance <0x30**: **A → sub 5**, stomp; **B → sub 6**, cover/pin.
- The limits are strict: 31 yes / 32 no; 47 yes / 48 no; dy 23 yes / 24 no.

So B is the same button that covers, but the position decides. The invented symmetric 28..100 px band disappears for Warrior. Sub 4 and other holds/inputs unrelated to these two moves are not added. Duggan keeps his previous engine.

### Stomp — 0x1173A / 0x118BC

- Native poses **0x159 and 0x15A**, timers **8 and 4 ticks**.
- Impact on moving to the second step.
- No jump nor X/Y displacement; floor **z=0xBB**. It no longer drops to a pin's sitting height.

### Jump — 0x10A5E / 0x111D0 / 0x156FA / 0x159AC / 0x3E20

- Floor: **0xBB**. Vertical impulse: **0x500**; gravity **0x50**.
- X target: native table `0x111D0`, **rival.x ±0x20**, according to orientation. Y target: the opponent's Y.
- Velocities computed with the loop at `0x159AC`: it divides the distance by the number of flight steps. A divisor from a recorded track is not used.
- Integrator at `0x3E20`: `x+=2*vx`, `y+=2*vy`, `z+=2*vz`, `vz-=2*g`, every arcade tick.
- Wind-up of **4 ticks**; normal sequence **0x61/0x62/0x7A/0x7B**, variant **0x61/0x62/0x76/0x77** when it starts at `propio.y+2 < rival.y`.
- Air timers from `0x112F0`: **9 ticks, 5 ticks, wait for contact**.
- Descending contact from **z≤0xCB** with the exact point and rectangle of `0x10FCC`, `0x11084` and `0x110A4`; not a generic 48 px reach.
- Impact: **z=0xBB**, **y=rival.y−1+10**, like `0x10D9E/0x10F04` for id 0. Auxiliary object **0x7D**, opposite orientation and offsets from `0x1152A`; it is composed into the visual resource, not into the wrestler's physics.
- Resting on him for **12 ticks**, recovery action 5, pose **0x1A**, **8 ticks** (`0xAA00[0]`).
- If the opponent gets up first: no false pin/impact is granted. Miss branch `0x10C4A` and bounce action 8/sub 5 (`0x9FCC`, physics `0x27D2[0x19]`: vz=0x300, g=0x40; poses 0x1CF/0x16), before returning to the b80 lying engine.

### Resources and provenance

Native poses are added without modifying the previous resources: `spr_tab.bin` and `spr_tiles.bin` keep the b80 prefix intact. The conversion checks pose 0x159 **pixel by pixel** against the resource already present in b80 and keeps its origin/palette, without drawing new pixels. All fit within Warrior's 64-tile window.

**All the logic/measurements come from `/workspace/wwf_sgdk/analisis`.** To convert the pixels, the original graphics dependency declared by `analisis/tools/render_obj.py` is used: `/workspace/wwf/port_35/sprtiles.npy`. It is an array of original decoded tiles, not move code from another port. This dependency is made explicit in `tools/native81.py`.

## Tests and captures

- **19 fixtures** in MAME with the **Genesis** driver, prepared states and real A/B presses: four variants/sides of the jump, both stomps, pin on both sides, collision and running on both sides, six included/excluded limits and the miss when the opponent gets up.
- In addition: **natural kickout next to the left and right ropes**, from strikes/pin with the pad, without writing the animation request. Both end with `RESULT ok_rope_vib`.
- In the four jumps, **16 X/Z samples** are compared against an independent integrator of the arcade's instructions: solver horizon **34 steps**, maximum **z=232 (BB+45)**, landing **z=187/y=rival+9**. Both sides are symmetric.
- Ropes with a settled camera: equivalent phase transitions on **exactly the same frames** on both sides. MAME callbacks may observe repeated VDP frames while the engine works; those callbacks are not confused with arcade machine ticks.
- The dy23 fixture observed a load transition during a callback in the middle of the loop; it is checked that it does not persist for more than two VBlanks. No claim is made of a general flicker/hardware audit in this version.
- `VALIDACION_b81.txt`: results and internal **SGDK XOR** checksum, as in b80.
- **Final captures: `/workspace/b81/shots/FINAL_b81/`**. Sequences `ropeL_secuencia.png`, `ropeR_secuencia.png`, `diveR_secuencia.png`, `diveL_secuencia.png`, variants, stomps and miss. Includes individual unlabelled PNGs and labelled contact sheets.
- `ARCADE_b81.txt`: recovered instructions, addresses, table bytes and hash of the reference program ROM.

**Scope of validation:** the behaviour was compared with the disassembly; the captures in this delivery are of the port in MAME Genesis, not a new run of the original arcade nor a physical console. Energy/AI/counts and the general reactions from b80 are preserved except for the visual/physical routes described; this is not presented as a complete port of those other systems.

## Reproduce

```sh
cd /workspace/b81
python3 tools/native81.py
# make no siempre detecta cambios dentro de BIN: forzar recursos tras regenerarlos.
touch res/res.res
PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk
cp out/rom.bin wwf_b81.bin
md5sum wwf_b81.bin
python3 tools/validate81.py
```

(The comment says: make does not always detect changes inside BIN files; force resources after regenerating them.)

Final build: `BUILD_b81_final.log`; sprite generation: `NATIVE_b81.log`; diff: `CAMBIO_b81.patch`.
