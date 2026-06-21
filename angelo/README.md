# SCOMPACT — by Angelo Colucci

**Source:** *Your Sinclair* magazine, issue #28, April 1988.
**Author:** Angelo Colucci.

SCOMPACT is a 134-byte ZX Spectrum screen-RLE compressor/decompressor — a
remarkable piece of work for its time. It loads at address **26000** (0x6590)
and has two entry points:

| Entry | Address | Job |
|---|---|---|
| COMPRESS | 26000 (0x6590) | Read a screen, emit a compressed blob |
| DECOMPRESS / PLAYBACK | 26100 (0x65F4) | Read a compressed blob, paint the screen |

The data pointer is passed via the Spectrum system variable **SEED**
(0x5C76 / 23670) — set with `RANDOMIZE n` before calling, and SCOMPACT writes
the next-frame pointer back into SEED on return. This trick lets a tight
`FOR f = 1 TO 60: RANDOMIZE USR 26100: NEXT f` loop walk through a stream of
compressed frames with no BASIC bookkeeping. The whole thing fits in 134
bytes; once you understand the trick, the elegance speaks for itself.

## Algorithm — the RLE format

SCOMPACT uses a self-describing run-length encoding. Each compressed block
begins with an **escape byte** (a value chosen at compression time that is
rare in the data). Then the bytes stream:

- A byte that **isn't** the escape value is copied verbatim to the screen.
- The escape value introduces a run: `[ESC][LEN][VALUE]` paints `VALUE`
  `LEN` times (with `LEN = 0` interpreted as 256, the standard byte-saver).

That's the entire format. Reproduced in Python in
[`../make_deltas.py`](../make_deltas.py) for the decoder side — see the
`decode_one` function — which is byte-for-byte compatible with the original
routine. The Python encoder (also in `make_deltas.py`) is for the new delta
format; Angelo's original encoder lives in the 134 bytes themselves.

## Files

- `SCOMPACT.TAP` — Angelo's original tape file (41,862 bytes; standard
  Spectrum tape format). Loads SCOMPACT to 26000 ready to use.
- `scompact.bin` — the 134-byte routine as a raw binary, extracted from
  the running tape. Loads at 26000.

## Why it matters here

This whole repo is a study built on top of SCOMPACT. The WORLDS9 demo (60
frames of orbiting planets) uses SCOMPACT to fit ~38 KB of animation into
a 48K Spectrum and still leave room for BASIC. The tearing fixes in this
repo (HALT sync, double-buffer, delta encoding) are all built **on top of
Angelo's routine** — none replace it. Fix 2 even calls SCOMPACT verbatim;
it just changes two bytes of the destination address.

## Credit and licence

All credit for SCOMPACT belongs to Angelo Colucci. It is included here as a
historical reference, properly attributed. No licence claim is made over
Angelo's original work.
