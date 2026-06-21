#!/usr/bin/env python3
"""Reproduce WORLDS9's orbiting-worlds frame generation in Python (faithful to the
Spectrum: exact Sinclair RND + PLOT/DRAW), render 60 middle-third frames, pack into
SCOMPACT's 2048-byte layout. Output = 60 frames for delta encoding."""
import math
PI=math.pi
class RND:
    def __init__(s,seed=1): s.seed=seed
    def __call__(s):
        s.seed=((s.seed+1)*75)%65537-1
        return s.seed/65536

# WORLDS9 params (lines 85-87)
framecount=60; elementcount=150
orbitwidth1=90; orbitwidth2=100; orbitheight=15
psb=10; psf=4

def render_frame(f):
    bmp=[[0]*256 for _ in range(192)]   # bmp[py][px], py 0=top
    def setpx(x,y):                      # Spectrum PLOT coords: x 0-255, y 0-175 (0=bottom)
        xi=int(round(x)); yi=int(round(y))
        if 0<=xi<256 and 0<=yi<=175:
            py=175-yi
            if 0<=py<192: bmp[py][xi]=1
    def square(x,y):                     # PLOT;DRAW1,0;DRAW0,1;DRAW-1,0 = 2x2 dot
        setpx(x,y); setpx(x+1,y); setpx(x+1,y+1); setpx(x,y+1)
    rnd=RND(1)                           # line 110 RANDOMIZE 1 (same dot pattern each frame)
    d=2*PI*(f/60)
    sinf=math.sin(f*2*PI/framecount); sinf2=math.sin(f*2*PI/framecount+PI)
    cosf=math.cos(f*2*PI/framecount);  cosf2=math.cos(f*2*PI/framecount+PI)
    ps=(-psf*cosf)+psb; ps2=(-psf*cosf2)+psb
    for q in range(elementcount+1):
        r=rnd()*2*PI+d
        s=rnd()*2*PI
        if math.cos(s)*math.cos(r)>=0:   # 165: small world 1
            square((128+orbitwidth1*sinf)+ps*math.sin(s),
                   (80+orbitheight*cosf)+ps*math.cos(r+PI/2)*math.cos(s))
        if math.cos(s)*math.cos(r)<=0:   # 170: small world 2
            square((128+orbitwidth2*sinf2)+ps2*math.sin(s),
                   (80+orbitheight*cosf2)+ps2*math.cos(r+PI/2)*math.cos(s))
        # 180 central world: PLOT then conditional square
        cx=128+28*math.cos(r+PI/2)*math.sin(s); cy=80+28*math.cos(s)
        setpx(cx,cy)
        if math.sin(s)*math.cos(r)<=0:   # 190
            setpx(cx+1,cy); setpx(cx+1,cy+1); setpx(cx,cy+1)
    # pack middle third (pixel rows 64-127) into 2048-byte SCOMPACT block
    block=bytearray(2048)
    for charrow in range(8):
        for pixline in range(8):
            y=64+charrow*8+pixline
            for col in range(32):
                byte=0
                for bit in range(8):
                    if bmp[y][col*8+bit]: byte|=(0x80>>bit)
                block[pixline*256+charrow*32+col]=byte
    return bytes(block)

imgs=[render_frame(f+1) for f in range(framecount)]   # f=1..60 as in BASIC
import pickle; pickle.dump(imgs, open("w9_frames.pkl","wb"))
# quick stats + render a couple to PNG
from PIL import Image
for fi in (0,15,30,45):
    im=Image.new("1",(256,64)); px=im.load()
    for charrow in range(8):
        for pixline in range(8):
            for col in range(32):
                b=imgs[fi][pixline*256+charrow*32+col]
                y=charrow*8+pixline
                for bit in range(8): px[col*8+bit,y]=0 if (b<<bit)&0x80 else 1
    im.resize((512,128)).save(f"/tmp/w9_f{fi}.png")
print("rendered 60 orbiting frames; samples /tmp/w9_f0,15,30,45.png")
