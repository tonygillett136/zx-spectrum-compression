# zx-spectrum-compression

A small ZX Spectrum compression study — three progressively better ways to play
back a 60-frame compressed animation **without tearing**, built around
**SCOMPACT**, a 134-byte screen RLE compressor/decompressor written by
**Angelo Colucci** and published in *Your Sinclair* magazine, **issue #28
(April 1988)**.

The original demo (WORLDS9) compresses 60 middle-third screens of orbiting
planets and plays them back via SCOMPACT. It's beautiful but it tears: a full
middle-third decompress takes ~1.4 frames, longer than a TV frame, so the
electron beam catches the routine partway through the buffer. This repo
documents three increasingly principled fixes for that tearing, all written
on top of Angelo's original routine, and includes a self-contained tape that
plays the orbiting worlds **fully tear-free** on real hardware.

See [`angelo/README.md`](angelo/README.md) for Angelo's original code and full
credit.

## The three fixes

| Fix | Idea | Tearing | Cost |
|---|---|---|---|
| [**FIX_1_HALT.md**](FIX_1_HALT.md) | 4-byte stub: `HALT` then `JP 26100`. Every decompress begins at the 50 Hz interrupt. | Tear becomes one stable seam (no shimmer). Not eliminated. | 4 bytes; ~1 minute change. |
| [**FIX_2_DOUBLEBUFFER.md**](FIX_2_DOUBLEBUFFER.md) | Decompress into the screen's hidden bottom third (worlds live in the middle third, bottom third is unused), then LDIR up to the visible middle on the interrupt. | Decompress fully hidden; copy can still leave a faint stable seam. | 20 bytes + 2-byte poke into SCOMPACT to re-point its destination. **Zero extra RAM** (re-uses the bottom-third bitmap as a shadow buffer). |
| [**FIX_3_TEARFREE_DELTA.md**](FIX_3_TEARFREE_DELTA.md) | Pre-compute inter-frame deltas (lists of `[addr][len][bytes]` runs). Per-frame change ≤710 bytes; the whole update lands during the top border. | **Fully tear-free, by construction. 3,900–4,900 T-states per frame vs ~28,700 budget — 6× margin.** | 25-byte applier; deltas blob (~38 KB). Identical animation. |

Fix 3 is the production answer. The tape `worldstf.tap` is the self-contained
build: BASIC player + delta blob + 25-byte applier, autoloading and playing
tear-free.

## Animation fidelity

The delta-encoded animation is **byte-identical** to what Angelo's original
generator produces. I reproduced his Sinclair-RND + PLOT/DRAW generator in
Python (the round-half-up coordinate trick the ROM uses turned out to matter)
and verified all **60/60 frames byte-for-byte against his saved frames**.

## Try it

- `worldstf.tap` is the headline artefact — load on a real Spectrum or any
  standard emulator (note: ZEsarUX headless `smartload` stalls on multi-block
  tapes; a normal tape load is fine).
- To regenerate the deltas: `python3 build_w9_deltas.py` renders the orbiting
  frames with the validated engine and emits `deltas_w9.bin`. Then
  `python3 build_tearfree_tap.py` packages the tape.

## Repo layout

```
.
├── angelo/
│   ├── SCOMPACT.TAP           Angelo's original 1988 Your Sinclair listing (binary tape)
│   ├── scompact.bin           134-byte SCOMPACT decompressor (extracted)
│   └── README.md              credit + algorithm sketch
├── FIX_1_HALT.md              the minimal sync fix
├── FIX_2_DOUBLEBUFFER.md      shadow-buffer fix
├── FIX_3_TEARFREE_DELTA.md    delta-encoded tear-free fix (the production answer)
├── applier.asm                25-byte tear-free applier
├── build_w9_deltas.py         renders WORLDS9 frames + emits the delta blob
├── build_tearfree_tap.py      packages worldstf.tap
├── worldstf.tap               playable tape (Fix 3)
├── make_deltas.py             generic SCOMPACT-frames-to-deltas converter
├── worlds9_gen.py             validated Python reproduction of Angelo's generator
└── (harnesses, measurement scripts, captures — see file list)
```

## Credit

- **SCOMPACT** (the 134-byte RLE compressor/decompressor and the WORLDS9 demo
  techniques it enables) is by **Angelo Colucci** — *Your Sinclair* issue #28,
  April 1988. All credit for the original routine is his. See
  [`angelo/README.md`](angelo/README.md).
- The three tearing fixes (HALT sync, shadow-buffer, delta encoding) and the
  validated generator reproduction were developed by Tony Gillett with
  Claude Code (2026).

## Licence

The new code in this repo (the three fixes, the Python tooling, the
documentation) is released under the [MIT licence](LICENSE).

Angelo's original SCOMPACT is included as a historical reference and credited
to him as its author; no licence claim is made over his work.
