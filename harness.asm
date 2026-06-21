; harness.asm — drive Angelo's SCOMPACT decompressor faithfully, to measure +
; verify a vblank-sync fix.  Reality (from the DEMO BASIC):
;   - routine + frames both load at 26000 (0x6590); FRAMES = [134B routine][frames@26134]
;   - DECOMPRESS/playback entry = 26100 (0x65F4); data ptr passed in SEED (23670/0x5C76)
;   - the embedded routine is PRE-PATCHED to redraw the middle third only (writes ~0x4800+)
; Assemble with -DSYNC to insert the HALT (vblank) fix at the top of the loop.

    DEVICE ZXSPECTRUM48

FRAMES_BASE = 0x6590
FRAME1      = 0x6590 + 134          ; first compressed frame = 26134 = 0x6616
FRAMES_END  = 0x6590 + 38754        ; 0xFCF2
DECOMP      = 0x65F4                 ; playback entry (26100)
SEED        = 0x5C76                 ; 23670 — data pointer lives here

    ORG FRAMES_BASE
    INCBIN "frames.bin"             ; pre-patched routine @0x6590 + frames @0x6616

    ORG 0xFD00
Start:
    di
    ld sp, 0xFF70
    ld hl, 0x5800                   ; attrs: bright white ink, black paper (like the demo)
    ld de, 0x5801
    ld bc, 767
    ld (hl), 0x47
    ldir
    ld hl, FRAME1
    ld (SEED), hl
    im 1                            ; stock ROM interrupt (as when called from BASIC)
    ei
Loop:
    IFDEF SYNC
    halt                            ; <-- the fix: each redraw starts at the frame interrupt
    ENDIF
CallSite:
    call DECOMP                     ; decompress one frame -> middle third; BC = next frame ptr
    ld (SEED), bc
    ld hl, FRAMES_END
    or a
    sbc hl, bc
    jr nc, Cont
    ld hl, FRAME1                   ; wrap
    ld (SEED), hl
Cont:
    jr Loop

    SAVESNA "harness.sna", Start
