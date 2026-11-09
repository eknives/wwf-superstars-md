# Sound: Z80 driver, OKI and bell

Source: ROM 24ab-0.12 (Z80, 32 KB) and OKI ROMs 24a9-0.46 + 24j8-0.45.
Tools: tools/z80rec.py (listing in /tmp/z80.lst) and tools/oki.py (generates oki/sXX.wav).
All reached Z80 code has been read: 1,200 instructions and 2,523 bytes, plus the sequencer opcode handlers 0x468–0x6C0.

## Hardware and flow
- The 68K writes to latch 0x180009. That triggers an NMI on the Z80, which pushes the byte into queue 0x8400.
- The YM2151 generates the 0x38 IRQ with its timer. The main loop is at 0x100 and the dispatcher at 0x18F.

## Commands
- 0 = reset.
- Bit7 set = stop.
- 0xF0, 0xF1 and 0xF2 change the handler (0x821A).
- 0xFE and 0xFF = reset.
- Table 0x1000: 0x67 entries of 4 bytes.

| Range | Meaning |
|---|---|
| 0x01–0x17 | FM music. 8 channels at 0x8000 with stride 0x40; sequencer opcode table 0x8CF (C0–EA). 0x16 is a duplicate of 0x0A. |
| 0x18–0x1F | Filler entries (they play sample 1). |
| 0x20–0x49 | OKI sample = command − 0x1F. Driver at 0xC4B, 4 voices at 0x8310. |
| 0x50 / 0x51 / 0x52 | Sample sequences (0xD79/0xDAA) with data at 0x1152/0x117A/0x11A2. 0x50 and 0x51 are crowd waves (samples 3 and 4); 0x52 is a rhythm with sample 5 and the 68K never sends it. |
| 0x55–0x67 | The «entries» overlap the sequence data: they are not real commands. |
| > 0x67 | Goes to 0x345, which only writes 0x821F, and nothing reads it: it is a NO-OP. That is why the clock's 0x70 warning does not sound. |

Valid samples are 1–0x2A.

## Bell (resolved)
- **0x20 = start bell.** Sample 1: 1.5 s, spectral peak at 2,360 Hz and exponential decay. Only inicio_combate (0x84A2) sends it.
- **0x21 = repeated bell.** Sample 2: same peak (2,350 Hz), sustained 2.3 s. Sent by musica_combate (0x179A) and the end of time (0x26548 / 0x2657A / 0x2658E).
- 0x3B (sample 0x1C), previously assumed to be the bell, **is not**.
- This is deduced from the spectrum and the call context; nobody has listened to it.

## Other identified IDs

| ID | Sample | Use |
|---|---|---|
| 0x22 / 0x23 | 3 / 4 | Crowd |
| 0x24 | 5 | Footsteps |
| 0x29 | 0xA | Dull thud |
| 0x32 | — | Rolling out of the ring |
| 0x33 | 0x14 | Rope |
| 0x47 | 0x28 | Post |
| 0x3D / 0x3E / 0x3F | — | Referee count voices: 1, 2, 3 |

The complete list of which routine sends each ID is in sonido_ids_llamadas.txt.
