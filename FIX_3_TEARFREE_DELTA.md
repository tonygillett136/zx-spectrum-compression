# Fix 3 — fully tear-free (dirty-rectangle / delta encoding)

This is the proper, fully tear-free solution. **Measured: 3,900–4,900 T-states per
frame to redraw, against the ~28,700 the beam gives you before it reaches the middle
third — a 6× margin.** No seam, no shimmer, by construction.

## The idea

A full middle-third redraw (2048 bytes) can't beat the beam. But between two
adjacent frames of a 60-step orbit, only a little changes. So instead of redrawing
the whole third each frame, store only the **bytes that differ from the previous
frame** and write just those, synced to the interrupt. The orbiting worlds change
≤710 bytes/frame — small enough that the whole update lands during the top border,
before the beam ever reaches the middle third. Where the changed pixels are doesn't
matter; only the total matters, and it's tiny.

- Cold start applies a **keyframe** (the full image, once, on a black screen — its
  one slow write is invisible).
- Then each frame applies a **delta**: a list of `[screen-addr][len][bytes]` runs,
  terminated by `0000`. Frames loop seamlessly (the deltas are circular).

## Fidelity — identical to your WORLDS9

The animation is byte-identical to what WORLDS9's own BASIC produces. I reproduced
Angelo's generator (Sinclair RND + PLOT/DRAW, with the round-half-up coordinate
rounding the ROM uses) and **verified it against his actual saved frames: 60/60
frames byte-for-byte identical.** Same engine, your orbit parameters → your exact
animation, just delta-encoded.

## Memory — fits, no sacrifice

- `deltas_w9.bin` = **38,588 bytes** (about the same as the original frame blob),
  loads at 26000 (0x6590). No shadow buffer needed — deltas write straight to the
  screen because they're small.
- Applier = **25 bytes** at 23296 (0x5B00, the printer buffer).

## The applier (25 bytes at 23296)

```
ld hl,(23670)   ; frame pointer (from RANDOMIZE)
halt            ; sync to the 50 Hz interrupt
di
run: ld e,(hl):inc hl: ld d,(hl):inc hl   ; DE = screen address
     ld a,d:or e: jr z,done                ; 0000 = end of frame
     ld c,(hl):inc hl: ld b,0: ldir         ; copy one run to screen
     jr run
done: ei: ld b,h: ld c,l: ret              ; return next pointer (RANDOMIZE stores it)
```
DATA: `42,118,92,118,243,94,35,86,35,122,179,40,8,78,35,6,0,237,176,24,240,251,68,77,201`

## Use it

**Easiest:** load `worldstf.tap` — it's self-contained (BASIC player +
deltas), autostarts, and plays tear-free. (Standard two-block tape; loads on real
hardware. Note: ZEsarUX headless `smartload` stalls on multi-block tapes, but a real
Spectrum / normal emulator tape load is fine.)

**Or integrate the player** (the deltas as a CODE block at 26000):
```
10 CLEAR 25999
20 LOAD ""CODE 26000                         : REM the deltas blob
30 RESTORE 100: FOR n=23296 TO 23320: READ d: POKE n,d: NEXT n   : REM applier
40 BORDER 0: PAPER 0: INK 7: BRIGHT 1: CLS
50 RANDOMIZE 26000: RANDOMIZE USR 23296      : REM apply keyframe (-> delta0)
60 FOR f=1 TO 60: RANDOMIZE USR 23296: NEXT f: REM play 60 deltas, tear-free
70 RANDOMIZE 28077: GO TO 60                 : REM loop (28077 = delta0 ptr)
100 DATA 42,118,92,118,243,94,35,86,35,122,179,40,8,78,35,6,0,237,176,24,240,251,68,77,201
```
`RANDOMIZE n` sets the frame pointer (in the SEED sysvar, 23670); `RANDOMIZE USR`
runs the applier and stores the returned next-frame pointer back into SEED — Angelo's
own pointer-passing trick, reused.

## Regenerating (for other WORLDS variants)

`build_w9_deltas.py` renders the orbiting frames with the validated engine and emits
`deltas_w9.bin`. Change the orbit parameters at the top to match any WORLDS edit, or
point `make_deltas.py` at a captured frame blob. The applier is unchanged.

## Verified

- Reproduces Angelo's frames 60/60 byte-identical (engine fidelity).
- Orbiting animation runs correctly from the exact 25-byte applier + deltas (emulator).
- Per-frame apply 3,942 / 4,869 T measured (delta0/delta1) vs 28,700 budget → tear-free.
- Final word is your CRT, as always.
