# To study — open questions, not a list of authorised changes

- **CPU/DMA/scroll and post cadence:** identify which work crosses VBlank and separate CPU cost, DMA transfer, SAT and logic clock. b91 only observed crossings, not a definitive attribution. LOW PRIORITY, polish at the end. Do not recycle `experimental_post91.c.txt` as a validated solution.
- **Crowd sound:** measure whether the dropout comes from the PCM4 samples, repeated triggers, Z80/mixing or timing; compare the OKI/Z80 IDs/driver from the analysis with the converted WAV resources. Symptom reported, cause pending.
- **Green Macho / borrowed palettes:** locate the effective slot/bank and the CRAM mapping; do not assume it is a broken sprite or modify the ring palette. Technical reference b88, `46A0`.
- **Remaining clotheslines:** investigate back/ropes/CPU/late variant and its FFFE link; do not apply bonus/duplication to the path that avoids them. See energy 162BC/1642A and collision 16634.
- **Duggan floor tracks:** the new study already identifies 159/15A and 61/62/1CB/1CC, variant 1CD/1CE and post 2F. b92 already replaces the old gs5/gs11 activations and measures the MD per refresh; the visible Elbow cadence and an exhaustive graphics audit are missing. Limits 23/24 and the absence of stomp refiltering were tested; other corners/outside remain uncertified. See the Duggan study.
- **Energy against pin and getting up:** B flags, remaining counter, AF66/AF6A/AF72, CPU vs human, partner rescue and E0. The energy report contains formulas; a full comparison with the port's model is missing before integrating.
- **Quality of the decompilation:** prefer `arc_rec.dis`; the linear `arc.dis` has 94 misaligned targets according to the analysis. A historical "100% read" does not mean every deduction is correct; check auditoria.md/sin_confirmar.md and later studies.
- **Tests outside fixtures:** fractions/planes, four corners, opponent/human/CPU, PAL/NTSC and Everdrive. The physical frequency of the board has not been measured; MAME's 57.444852941 Hz uses estimated totals.

## Added in b92
Profile the visible publication/loading of Duggan's Elbow before proposing a global fix. Inconclusive private SAT discarded. Data pose92_refreshes.csv in 02_arcade_decompilado/notas_historicas/b92/shots92. Duggan outside, other corners, post miss, natural match and Everdrive are missing; this does not authorise Warrior/render changes.
