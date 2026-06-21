#!/usr/bin/env python3
"""Generate WORLDS9 orbiting frames with the VALIDATED engine (round-half-up,
proven byte-identical to Angelo's frames), then delta-encode for tear-free play.
Output: deltas_w9.bin + keyframe/delta pointers + budget check."""
import math
PI=math.pi
def rhu(v): return int(math.floor(v+0.5))     # validated Spectrum PLOT rounding
class RND:
    def __init__(s,seed=1): s.seed=seed
    def __call__(s): s.seed=((s.seed+1)*75)%65537-1; return s.seed/65536
framecount=60; elementcount=150
orbitwidth1=90; orbitwidth2=100; orbitheight=15; psb=10; psf=4
def render(f):
    bmp=[[0]*256 for _ in range(192)]
    def setpx(x,y):
        xi=rhu(x); yi=rhu(y)
        if 0<=xi<256 and 0<=yi<=175:
            py=175-yi
            if 0<=py<192: bmp[py][xi]=1
    def sq(x,y): setpx(x,y);setpx(x+1,y);setpx(x+1,y+1);setpx(x,y+1)
    rnd=RND(1); d=2*PI*(f/60)
    sinf=math.sin(f*2*PI/framecount); sinf2=math.sin(f*2*PI/framecount+PI)
    cosf=math.cos(f*2*PI/framecount);  cosf2=math.cos(f*2*PI/framecount+PI)
    ps=(-psf*cosf)+psb; ps2=(-psf*cosf2)+psb
    for q in range(elementcount+1):
        r=rnd()*2*PI+d; s=rnd()*2*PI
        if math.cos(s)*math.cos(r)>=0: sq((128+orbitwidth1*sinf)+ps*math.sin(s),(80+orbitheight*cosf)+ps*math.cos(r+PI/2)*math.cos(s))
        if math.cos(s)*math.cos(r)<=0: sq((128+orbitwidth2*sinf2)+ps2*math.sin(s),(80+orbitheight*cosf2)+ps2*math.cos(r+PI/2)*math.cos(s))
        cx=128+28*math.cos(r+PI/2)*math.sin(s); cy=80+28*math.cos(s)
        setpx(cx,cy)
        if math.sin(s)*math.cos(r)<=0: setpx(cx+1,cy);setpx(cx+1,cy+1);setpx(cx,cy+1)
    block=bytearray(2048)
    for cr in range(8):
        for pl in range(8):
            y=64+cr*8+pl
            for col in range(32):
                byte=0
                for bit in range(8):
                    if bmp[y][col*8+bit]: byte|=0x80>>bit
                block[pl*256+cr*32+col]=byte
    return bytes(block)
imgs=[render(f+1) for f in range(framecount)]
import pickle; pickle.dump(imgs,open("w9_imgs.pkl","wb"))

MIDDLE=0x4800
def enc_runs(prev,cur,maxgap=3):
    diffs=[i for i in range(2048) if prev[i]!=cur[i]]; blob=bytearray()
    if diffs:
        m=[];s=p=diffs[0]
        for x in diffs[1:]:
            if x-p<=maxgap:p=x
            else:m.append((s,p));s=p=x
        m.append((s,p))
        for s,e in m:
            i=s
            while i<=e:
                L=min(255,e-i+1);a=MIDDLE+i
                blob+=bytes([a&0xFF,a>>8,L])+cur[i:i+L];i+=L
    blob+=bytes([0,0]); return blob
def keyframe(img):
    blob=bytearray();i=0
    while i<2048:
        L=min(255,2048-i);a=MIDDLE+i;blob+=bytes([a&0xFF,a>>8,L])+img[i:i+L];i+=L
    blob+=bytes([0,0]);return blob

blob=bytearray(); blob+=keyframe(imgs[59]); delta0=len(blob); sizes=[]
for i in range(60):
    d=enc_runs(imgs[i-1],imgs[i]); sizes.append(len(d)); blob+=d
open("deltas_w9.bin","wb").write(blob)
LOAD=0x6590
# apply-time estimate per delta: written bytes*21 + runs*24 (worst-case contended-ish)
def apply_T(d):
    # parse runs to count written bytes + run count
    i=0;wb=0;rc=0
    while True:
        a=d[i]|(d[i+1]<<8);i+=2
        if a==0:break
        L=d[i];i+=1;i+=L;wb+=L;rc+=1
    return wb*21+rc*24, wb, rc
maxT=0
for i in range(60):
    off=delta0+sum(sizes[:i]); d=blob[off:off+sizes[i]]
    T,wb,rc=apply_T(d); maxT=max(maxT,T)
print(f"orbiting deltas: blob={len(blob)}B; delta sizes min {min(sizes)} max {max(sizes)} avg {sum(sizes)//60}")
print(f"worst-case apply ~{maxT} T (beam->middle third ~28700 T). tear-free? {maxT<28700}")
print(f"loaded at 0x{LOAD:04X}: KEYFRAME=0x{LOAD:04X}  DELTA0=0x{LOAD+delta0:04X}  ends 0x{LOAD+len(blob):04X}")
