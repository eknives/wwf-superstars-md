# b50 (from b49)
ROM: wwf_b50.bin  md5 68f778ed3bbc111e38fa0ebeb78e93df
- Billboard: the top-right face had the bottom piece (rows 10-11, col 38-41) of another face (id 3). The correct Macho Man piece has been put in (arcade table 0x2197A id 2). In the arcade the 4 faces are set according to the wrestlers in the match (routine 0x1F50C); here they stay fixed.
- Blue margins: filled with the arcade stage (RLE 0x1F474 + columns 0x1F5C8, 768 px world). Background x = arcade x-96, y = arcade y+16. 444 cells, 254 new tiles (res/ex50_tiles.bin, ids behind the crowd).
- Rows 0-3 (crowd duplicated by the arcade's 512 px wrap) in black; the animated crowd no longer writes there.
- Empty HUD on the window plane (rows 0-3, fixed): 2 boxes, double frame (outer/inner), black inside, PAL3. Frame colour approximate (blue), to be confirmed.
- Same as b49: free camera, crowd and sound. No ropes.
- New map: res/bgb_map50.bin (already in RAM format).
