; harness_db.asm — DOUBLE-BUFFER prototype for SCOMPACT playback, tear-free attempt.
; Idea (zero extra RAM): decompress each frame into the screen's BOTTOM THIRD
; bitmap (0x5000-0x57FF) — hidden by black-on-black attrs, so the slow (~1.4
; frame) decompress is INVISIBLE — then on the frame interrupt copy that shadow
; up to the MIDDLE THIRD (0x4800-0x4FFF). Only the copy is visible + synced.
; Measures the copy cost (must beat the beam to the middle third, ~28.7k T).

    DEVICE ZXSPECTRUM48

FRAME1   = 0x6616
FRAMES_END = 0x6590 + 38754
DECOMP   = 0x65F4
SEED     = 0x5C76

    ORG 0x6590
    INCBIN "frames.bin"

    ORG 0xFD00
Start:
    di
    ld sp, 0xFF70
    ; re-point the decompressor at the bottom-third shadow (0x5000-0x57FF):
    ; offset+7 (start hi) 0x48 -> 0x50 ; offset+17 (end test) 0x50 -> 0x58
    ld a, 0x50
    ld (0x65FB), a
    ld a, 0x58
    ld (0x6605), a
    ; attrs: middle third visible (white/black), bottom third HIDDEN (black/black)
    ld hl, 0x5900           ; middle-third attrs
    ld de, 0x5901
    ld bc, 255
    ld (hl), 0x47
    ldir
    ld hl, 0x5A00           ; bottom-third attrs
    ld de, 0x5A01
    ld bc, 255
    ld (hl), 0x00
    ldir
    ld hl, FRAME1
    ld (SEED), hl
    im 1
    ei
Loop:
    call DECOMP             ; decompress one frame INTO shadow (0x5000); BC=next
    ld (SEED), bc
    ld hl, FRAMES_END
    or a
    sbc hl, bc
    jr nc, Cont
    ld hl, FRAME1
    ld (SEED), hl
Cont:
    halt                    ; sync to frame interrupt
CopySite:
    call CopyShadow         ; visible, synced copy shadow -> middle third
    jr Loop

; Copy 2048 bytes 0x5000 -> 0x4800.  (LDIR baseline; measure then optimise.)
CopyShadow:
    di
    ld hl, 0x5000
    ld de, 0x4800
    ld bc, 2048
    ldir
    ei
    ret

    SAVESNA "harness_db.sna", Start
