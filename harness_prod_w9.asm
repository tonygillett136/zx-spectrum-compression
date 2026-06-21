    DEVICE ZXSPECTRUM48
SEED=0x5C76
    ORG 0x5B00
    INCBIN "applier.bin"          ; the EXACT 25-byte production applier
    ORG 0x6590
    INCBIN "deltas_w9.bin"
    ORG 0xFD00
Start:
    di
    ld sp,0xFF70
    ld hl,0x5800
    ld de,0x5801
    ld bc,0x2FF
    ld (hl),0x47
    ldir
    ld hl,26000
    ld (SEED),hl
    im 1
    ei
    call 0x5B00                   ; keyframe (internal HALT); BC=delta0
    ld (SEED),bc
Loop:
    call 0x5B00                   ; delta; BC=next
    ld hl,0xFC4C
    and a
    sbc hl,bc
    jr nz,St
    ld bc,0x6DAD
St:
    ld (SEED),bc
    jr Loop
    SAVESNA "harness_prod_w9.sna", Start
