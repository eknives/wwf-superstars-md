# Duggan and Ultimate Warrior moves — b92 state

Update of the b89 inventory (which contained b83 notes), checked against b90/91 and NOTAS_b92.md. **Yes=usable, not full arcade verification**; no=absent; partial=incomplete. Only the three authorised Duggan attacks and the Warrior Knee regression were tested again; the other states are inherited, not new tests. P=A,K=B,C=A+B,Y=switches control.

## FAQ controls (legend)

| Symbol | Meaning |
|--------|-------------|
| P / K | Punch / Kick (A / B on Mega Drive) |
| P+K | Run |
| U+P | Up + Punch |
| *R / *U | Reversible / irreversible (FAQ) |

---

## Duggan (`"HACKSAW" JIM DUGGAN`)

| Move | FAQ input | State | Short note |
|------------|-----------|--------|------------|
| Punch | P (1 after 3) | yes | FD70+FD7C combo by presses (inherited b87); Duggan's native dispatch is different, see energy study |
| Kick | K (1 after 2) | yes | B standing (`mv=2`) |
| Run | P+K | yes | A+B or C (b89) → `rn=1`; bounce on the rope |
| Clothesline | P while running | yes | Collision on contact + opponent fall 0x17 face up (b86–b88, MAME); back/rope variants missing |
| High Knee | K while running | no | B while running does not launch an attack |
| Body Slam | U+P in grappling | no | There is no U+A in the grapple |
| Headlock | P in grappling | no | Only generic grappling (b70), no Headlock hold |
| Bulldog | P from Headlock (*U) | no | Hold finisher absent |
| Back Suplex | K from Headlock (*R) | no | Hold finisher absent |
| Irish Whip | K in grappling | yes | After grappling: `trStart` → throw to the ropes (both) |
| Back Body Drop | P vs runner | no | No "Against Running" branch |
| Drop Kick | K vs runner | no | Same |
| Pick Up | P next to head | no | Grabbing the lying wrestler not ported (`NOTAS_b82`) |
| Stomp | P next to body | yes (b92 tested) | Native Duggan engine, zone CB75,159/15A, damage1, arcTick; limits23/24 and no refiltering checked |
| Elbow Drop | K next to head | partial (b92) | Native solver/poses/reaction/damage5 and miss−2; floor/mirror/variant contacts checked. Visible cadence pending |
| Pin | K next to body | yes | B close → `pinStart`; referee count (b71+) |
| Dropkick (post, standing) | P/K from turnbuckle | no | The corner post can be **climbed**; there is no attack from the top |
| Elbow Drop (post, lying) | P/K from turnbuckle | partial (b92) | Sub2F, P/K trajectory/damage10/A2 checked; visible cadence pending |

**Duggan:** 7 yes / 2 partial / 9 no (18 from the FAQ; yes = usable, not a general certification identical to the arcade).

---

## Ultimate Warrior

| Move | FAQ input | State | Short note |
|------------|-----------|--------|------------|
| Punch | P (1 after 3) | yes | FD70+FD7C combo by presses, inherited b87; not touched in b92 |
| Kick | K (1 after 2) | yes | B standing |
| Run | P+K | yes | Same as Duggan (A+B or C) |
| Clothesline | P while running | yes | Same as Duggan (b86–b88) |
| Shoulder Tackle | K while running | no | B while running does not attack |
| Body Slam | U+P in grappling | no | — |
| Headlock | P in grappling | no | — |
| GORILLA PRESS | P from Headlock | no | Finisher absent |
| Atomic Drop | K from Headlock (*R) | no | Finisher absent |
| Irish Whip | K in grappling | yes | Symmetric `trStart` (W1E tracks) |
| Back Body Drop | P vs runner | no | — |
| Dropkick | K vs runner | no | — |
| Pick Up | P next to head | no | In floor zone A → stomp, not pick up (`NOTAS_b82`) |
| Stomp | P next to body | yes | Zone 2 + A → `gs=13` / arcade sub 5 (`warriorGroundStart`) |
| Knee Drop | K next to head | yes (b90/91 inherited) | Native engine/solver, variant76/77 without7D, A2 and energy; b92 contact/energy regression yes. No changes in b92 |
| Pin | K next to body | yes | Zone 2 + B if `w82PinOK` → Warrior pin |
| Dropkick (post, standing) | P/K turnbuckle | no | Climbs the post; no aerial attack |
| Knee Drop (post, lying) | P/K turnbuckle | partial (b90/91) | Contact/damage10 implemented; visible cadence pending LOW "polish at the end". Not fixed in b92 |

**Warrior:** 8 yes / 1 partial / 9 no (18 from the FAQ; state inherited from b91, no new techniques in b92).

---

## Shared / system (count for both)

| System | State | Note |
|---------|--------|------|
| Grappling / lock-up (2 struggles + reverse) | yes | b70: `grTry` / `grStep`; mash → whip |
| Irish Whip to the ropes + bounce | yes | Incl. short vibration on crashing/falling (b78–b81) |
| Fall / lying / getting up | yes | Reactions + get-up (slower b70) |
| Floor attacks | partial | Duggan independent engine b92; Warrior unchanged from b91. Elbow/post still with visible cadence pending |
| Pin + 3 count + kick-out on 1st pin | yes | Both cover; referee (b71+) |
| Count-out 20 / 3 count → restarts match | yes | b89: does not go back to selection |
| Title screen + arcade SELECT PLAYERS | yes | b89; the choice still does not change wrestlers |
| Climbing/descending corner posts | yes | Finishers against a lying opponent partially implemented; against a standing opponent still absent |
| Leaving/entering the ring (side / back) | yes | `sx` / `bx` |
| Short rope vibration (collide+fall / kick-out nearby) | yes | b78–b81 |
| AI / opponent attacks on its own | no | Opponent only with START (follow); Y switches control (b89) |
| "Against Running" attacks | no | — |
| Attacks from the turnbuckle | partial | Only the finisher against a lying opponent; see each wrestler's limits |
| Pick Up / grabbing the lying wrestler | no | Confirmed pending |

---

## Current evidence

- Duggan: `src/duggan92.h`, `duggan92_poses.h` and entry branches in main.c. They replace only its old gs5/gs11 activations; pin and other moves remain.
- Warrior: `src/knee90.h`, `native81.h`, warriorGround* functions unmodified; regression of five cases.
- Native addresses, damage, contacts, measured cadences and limits: `NOTAS_b92.md`, `shots92/validation92.json`, `pose92_refreshes.csv`.
- Original historical inventory: `MOVIMIENTOS_DUGGAN_WARRIOR_b89.md`. Do not use its b83 summaries as the current state. Energy vs pin/getting up is still pending; no new AI, only START follows.

ROM `d9af08525a0f49f4bdc025ed00499135`.
