    DEVICE ZXSPECTRUM48
SEED=0x5C76
KEYFRAME=0x6590
DELTA0=0x6DAD
DEND=0xFC4C
    ORG 0x6590
    INCBIN "deltas_w9.bin"
    ORG 0xFD00
Start:
    di
    ld sp,0xFF70
    ld hl,0x5800
    ld de,0x5801
    ld bc,0x2FF
    ld (hl),0x47          ; bright white ink / black paper, whole screen
    ldir
    ld hl,KEYFRAME
    ld (SEED),hl
    im 1
    ei
    call ApplyDelta       ; cold: keyframe -> BC=delta0
    ld (SEED),bc
Loop:
    halt                  ; sync
CallSite:
    call ApplyDelta       ; apply one delta; BC=next ptr
    ld hl,DEND
    and a
    sbc hl,bc
    jr nz,Wstore
    ld bc,DELTA0          ; wrap
Wstore:
    ld (SEED),bc
    jr Loop
ApplyDelta:
    ld hl,(SEED)
ADrun:
    ld e,(hl)
    inc hl
    ld d,(hl)
    inc hl
    ld a,d
    or e
    jr z,ADdone
    ld c,(hl)
    inc hl
    ld b,0
    ldir
    jr ADrun
ADdone:
    ld b,h
    ld c,l
    ret
    SAVESNA "harness_w9.sna", Start
