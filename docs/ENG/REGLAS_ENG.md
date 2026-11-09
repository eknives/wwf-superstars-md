# Project rules

Rules of the assignment/conversation; they do not mean that the whole port already complies with them.

1. Noticeable equality and, when a technique is closed, identical to the arcade in input, real pace, collision, physics, reaction, poses and palette. MAME + code/table with an address as the source; do not invent numbers or confuse ticks with 60 Hz frames. Do not report as verified what is missing.
2. Confirm the scope before implementing. Only what is asked; studies do not authorise ROM/code changes. Each version in a new folder, previous base untouched, new ROM and MD5; never reuse a version's name for another ROM.
3. Development priority: Duggan. Hogan is considered a perfect reference to be preserved; do not touch his implementation or the original/1P resources without explicit permission.
4. Preserve the correct palettes of partners, HUD and referee, including borrowed sprite blocks. **Do not touch the upper corner posts or the WWF logo in the ring background**, edited by Emilio.
5. No new AI: the opponent does not attack on its own. START keeps the existing follow function; do not turn it into AI or confuse an uncontrolled opponent with the arcade CPU.
6. Current controls: A=P, B=K; **C is exactly A+B**; **Y switches the controlled wrestler**, requires a 6-button pad. When the 3/20 count ends the match restarts, not the selection. The selection still leads to Duggan/Warrior whatever is chosen.
7. Internal energy independent of vdmg/vlast: human 48, saturated subtraction to 0, no regeneration during the match, zero is not a KO; reset each match. Both wrestlers human. **Every new wrestler must integrate arcade energy and damage**, without adding a fictitious bar or FAQ values as if they were RAM. Energy HUD not authorised in b90/b91.
8. Keep existing graphics/poses as a prefix unless permitted; audit changes and build locally with the fixed environment. Short validations, screenshots and RAM CSVs; fixtures are not equivalent to a full match or an Everdrive test.
9. Do not copy the arcade ROM into this backup. Analyses and converted resources are allowed. Check its reference MD5; obtain the ROM legally and separately if needed for MAME/converters.
10. Do not repeat research already available: first INDICE.md and DESCUBRIMIENTOS.csv. An old note does not prove the current state; the most recent notes and their explicit limits prevail. Discarded experiments are not delivered code.
