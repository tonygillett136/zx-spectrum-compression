# Fix 1 — the minimal "HALT" sync (1 instruction of real work)

**What it does:** makes every frame's decompress START at the 50 Hz interrupt,
so the redraw always begins at the same point in the TV frame. Converts the
rolling/shimmering tear into a single STABLE seam (much less noticeable). It does
NOT fully eliminate tearing, because one middle-third decompress measures
1.0–2.0 frames (avg ~1.4) — longer than a frame — so the beam still overtakes it
partway. But it's a one-minute change and may well be good enough to your eye.

**Why a tiny machine-code stub:** BASIC has no "wait for interrupt". The stub is
`HALT : JP 26100` — it waits for the frame interrupt, then jumps into Angelo's
playback entry (26100). It lives in the printer buffer at 23296 (0x5B00), which
is free during a normal RUN.

## Changes to WORLDS9

1. Install the 4-byte stub once, at the start of the playback section. Add to
   line 1000 (or wherever playback begins):

   ```
   POKE 23296,118: POKE 23297,195: POKE 23298,244: POKE 23299,101
   ```
   (118=HALT, 195,244,101 = JP 26100.)

2. Change the playback loop (line 1010) to call the stub instead of 26100, and
   drop the PAUSE (the HALT replaces it):

   ```
   1010 RANDOMIZE 26134: FOR f=1 TO 60: RANDOMIZE USR 23296: NEXT f: GO TO 1010
   ```

That's all. `RANDOMIZE USR 23296` still works exactly as before — the stub runs
the decompressor, which returns the next frame address in BC, and RANDOMIZE
stores it back in the SEED variable for the next frame.

## A/B test on hardware
- Before: `RANDOMIZE USR 26100` (rolling shimmer on the moving worlds).
- After:  `RANDOMIZE USR 23296` (stable seam, no shimmer).
Flip line 1010 between the two to compare.

If the residual seam still bugs you, use Fix 2 (double-buffer).
