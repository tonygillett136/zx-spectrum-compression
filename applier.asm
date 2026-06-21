    ORG 0x5B00
SEED = 0x5C76
    ld hl,(SEED)       ; delta/keyframe pointer (from RANDOMIZE)
    halt               ; sync to 50Hz frame interrupt
    di
run:
    ld e,(hl)
    inc hl
    ld d,(hl)
    inc hl             ; DE = destination screen address
    ld a,d
    or e
    jr z,done          ; 0x0000 terminator -> end of this frame
    ld c,(hl)
    inc hl
    ld b,0             ; BC = run length (1..255)
    ldir               ; copy run -> screen
    jr run
done:
    ei
    ld b,h
    ld c,l             ; return next-frame pointer in BC (RANDOMIZE stores to SEED)
    ret
