# Fix 2 — double-buffer (the proper fix), and the memory answer

## Is there enough memory? YES — with no sacrifice.

The demo is already ~780 bytes from the top of a 48K machine (routine + ~38 KB of
frames + the BASIC), so a *separate* 2 KB shadow buffer would NOT fit. But two
unused areas give us everything for free:

- **The screen's BOTTOM THIRD bitmap (0x5000–0x57FF = exactly 2048 bytes)** is
  unused in this demo — the worlds live in the middle third. Hide it behind
  black-on-black colour attributes and it becomes a perfect off-screen buffer.
- **The printer buffer (0x5B00, 256 bytes)** holds the new routine.

So: **zero extra RAM, no frames dropped.**

## How it works

1. Decompress each frame into the hidden bottom third (0x5000). The slow
   ~1.4-frame decompress is now INVISIBLE — no garbage ever shows.
2. On the frame interrupt (HALT), copy the finished image up to the visible
   middle third (0x4800). Only this copy is visible, and it's synced.

The decompressor is just re-pointed at the bottom third by changing two bytes
(its destination address), so no change to Angelo's 134-byte routine itself.

## The new routine (20 bytes, at 23296 / 0x5B00)

`CALL 26100` (decompress to shadow) · `PUSH BC` · `HALT` · `DI` ·
`LDIR 0x5000→0x4800, 2048` · `EI` · `POP BC` · `RET`
(returns the next-frame pointer in BC so RANDOMIZE updates SEED as before.)

## Changes to WORLDS9

Replace line 1000 and add a DATA line. (This runs once, after frame generation,
before playback.)

```
1000 BORDER 0: PAPER 0: INK 7: BRIGHT 1: CLS: POKE 26107,80: POKE 26117,88: RESTORE 1005: FOR n=23296 TO 23315: READ d: POKE n,d: NEXT n: FOR n=23040 TO 23295: POKE n,0: NEXT n
1005 DATA 205,244,101,197,118,243,33,0,80,17,0,72,1,0,8,237,176,251,193,201
```

- `POKE 26107,80: POKE 26117,88` re-points the DECOMPRESSOR at the bottom third
  (0x5000–0x57FF). (Frame *generation* still reads the middle third, so leave the
  generation section untouched.)
- The first FOR loads the 20-byte routine at 23296.
- The second FOR sets the bottom-third attributes (23040–23295 = 0x5A00–0x5AFF)
  to 0 = black ink on black paper, hiding the shadow.

Change the playback loop to call the new routine:

```
1010 RANDOMIZE 26134: FOR f=1 TO 60: RANDOMIZE USR 23296: NEXT f: GO TO 1010
```

## What to expect on hardware

- The decompress is fully hidden, and the visible write drops from ~98 k T-states
  (the bare decompress) to ~58 k (the copy), synced — so this is strictly better
  than Fix 1 and should look much cleaner.
- Honest caveat (measured): a full 2048-byte copy to the contended screen takes
  ~58 k T-states, which is still longer than the ~29 k the beam gives you before
  it reaches the middle third — so a faint, STABLE seam low in the third is
  possible. It will not shimmer.
- If you want it 100% tear-free, the remaining step is to redraw only the worlds'
  bounding box instead of the whole third (a smaller copy that fully beats the
  beam). That needs a change to the frame format + the generator — say the word
  and I'll build it.

## Why not just copy faster?
I measured the alternatives: LDIR ≈ 21 T/byte, unrolled LDI ≈ 16, stack-blit
≈ 10.5. None get a 2 KB copy under the ~29 k-T beam budget for a full third,
and the fast versions are also too big for the 256-byte printer buffer. The win
that matters here is hiding the decompress; the copy is the new (smaller) limit.
