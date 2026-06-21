    DEVICE ZXSPECTRUM48
    ORG 0x6590
    INCBIN "frames.bin"
    ORG 0x5B00
    INCBIN "fix_db.bin"
    ORG 0xFD00
Start:
    di
    ld sp,0xFF70
    ld a,0x50
    ld (0x65FB),a          ; retarget decompress start -> 0x5000
    ld a,0x58
    ld (0x6605),a          ; retarget decompress end   -> 0x58
    ld hl,0x5800
    ld de,0x5801
    ld bc,255
    ld (hl),0x00           ; top third black (clean shot)
    ldir
    ld hl,0x5900
    ld de,0x5901
    ld bc,255
    ld (hl),0x47           ; middle third visible
    ldir
    ld hl,0x5A00
    ld de,0x5A01
    ld bc,255
    ld (hl),0x00           ; bottom third hidden (shadow)
    ldir
    ld hl,0x6616
    ld (0x5C76),hl
    im 1
    ei
Loop:
    call 0x5B00            ; production routine: decompress+halt+copy, BC=next
    ld (0x5C76),bc
    ld hl,0x6590+38754
    or a
    sbc hl,bc
    jr nc,Cont
    ld hl,0x6616
    ld (0x5C76),hl
Cont:
    jr Loop
    SAVESNA "harness_prod.sna", Start
