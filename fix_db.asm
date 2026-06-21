    ORG 0x5B00
    call 0x65F4        ; decompress current frame INTO shadow (0x5000); BC=next
    push bc
    halt               ; sync to frame interrupt
    di
    ld hl,0x5000       ; shadow (hidden bottom third)
    ld de,0x4800       ; middle third (visible)
    ld bc,2048
    ldir
    ei
    pop bc             ; return next-frame ptr so RANDOMIZE updates SEED
    ret
