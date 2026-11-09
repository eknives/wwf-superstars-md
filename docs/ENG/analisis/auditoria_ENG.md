# Audit of the analysis (31-10-2026)

Sample: 38 entries of R (12 from the first half by address and 26 from the second; seed 20261031, tools/audit_sample.py). Each one was re-read in full in arc_rec.dis. 6 of them are "data" entries (correctly discarded).

## Result (32 code routines)
- OK: 24.
- Wrong: 4 (12.5 %). In addition, another error came up outside the sample (0x1E62).
  - 0x22040 choque_poste: the damage condition was inverted. The code deals damage if the action ≠ 8 OR if it is action 8 with sub 0xA, and the annotation said «action 8 except sub 0xA». NOTE: the port's comment (s66 wip19 main.c, line 124) copies the wrong version («act != 8 || a45 != 10»). I have not touched the port.
  - 0x230FC fondo_anim_publico: the condition was the opposite. It exits if 1C1890 == 1.
  - 0x945C correr_init: the angle is 0x40/0xC0, not 0/0x80.
  - 0x8AD8 intro_escena: 0x25408 is the wipe, not «music 1».
  - 0x1E62 (outside the sample): 0x24B54 is the palette fade, not text.
- Incomplete: 4.
  - 0x4000: the condition on 1C0027 was missing.
  - 0x1EC44: the CPU branch was missing.
  - 0x20D60: it only said «Same».
  - 0xE2CC: the call to 0xE7E8 is missing (left as is, it is minor).
- Coverage: 0x73E8–0x7478 (random choice with 0x450A) now has its own entry (tfuera_azar).

All of the above is corrected in tools/anot2.py (copy in anot2.py.bak_auditoria) and regenerated.

## UNCONFIRMED
- 0x6BA0: moves to C. Emilio has seen in the arcade that these are the crowd's camera flashes.
- 0x1F86 and 0x7E4A remain UNCONFIRMED (they still need to be seen in MAME).

## Discrepancies with the s66 port
sistemas/discrepancias.md was out of date. The comparison was done in sistemas/discrepancias_s66.md against s66/wip19/main.c (sha256 3d216c78…). I have checked it again in the code:
- Own kick-out: C. Lines 292/396 say kick-outs are always the partner.
- Energy 0 → 13/16: C. Lines 322 and 410: `(random()&15)>=3`.
- lieBand e/12: C (line 366).
- Time on the floor /2 and +0x20 from outside: C. They do not exist in the port.
- Clock: C. There is no trace of it.
- Count-out outside the ring: C. There is no trace of it.
- Sound driver: C. Line 124 says only the id is stored.
- random() instead of 0x450A: C. The crowd already uses a private rng with s67 (CA_RNG=0); the AI and the pin use random().
- Still V (they need MAME): the CPU's initial energy 55 and the rule of covering with energy < 16.

## Recommendation
With 12.5 % errors and another 12.5 % incomplete annotations, all the errors come from quick reading: inverted conditions and assumed subroutine names. I recommend re-reading the entire second half (≥ 0x13000). Before that, two things above all need checking: the conditional branches and that the names of the called subroutines match their entry in R.

## 0x7E4A (follow-up)
1C078E is a pick-up-and-throw object from outside the ring (id 1). It is used by 0xE2CC (throwing it), 0xE234 (breaking it) and 0xE6E0 (moves to id 2 and creates 1C089A).
In matches 4/9 (André's, according to Emilio) it is not created, and in addition all the object pick-up logic is disabled (0x1A6C0, 0x1CDA8 and 0x1C90E).
The hypothesis that it is removed because André needs the VRAM or the palette is not proven. The code decides it by match number.
Which object it is visually remains UNCONFIRMED. Mr. Fuji is ruled out.

## Full re-read (indices 0–483), 31/10/2026
Method: disassemble each routine again and compare it with its annotation. Fixes in tools/reread/fixes1–12.py; applied with tools/reread/apply.py, which now respects lines with several entries.
- First half: 31 corrections. Second half: 24 corrections (fixes9–12) plus the new entry 0x73E8.
- Bugs in the original game: 0x19D96 (movea.w), 0x1BD5C (writes d0 instead of d1), 0x1BEE4, 0x1D0E2 (energy is not taken into account).
- Conditions that were inverted in the notes: 0x1AE44, 0x1B7FA, 0x1B88C, 0x1B120, 0x23406, 0x244EE/0x24554 (pose restoration).
- Renames: 0x21420 cuerda_dibujar_1 (previously portrait); 0x21A4E… textos_luchadores/texto_*; 0x2553C txt_destino_abs; 0x25570 txt_desplaz_tile; 0x73E8 tfuera_azar.
- UNCONFIRMED: names of the texts of 0x21BB8 (undecoded letter table); which of lim_fuera/lim_ring is reversed in 0x244EE; meaning of 0x4000/0x8000 in 0x26548; endless loop of 0x740E if 1C0069 is full; 0x74C4/0x7552; bank 0x0F chair.
