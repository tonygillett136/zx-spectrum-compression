#!/usr/bin/env python3
"""Convert a SCOMPACT frame blob (RLE full middle-third frames) into a tear-free
DELTA blob: a keyframe + per-frame change-runs. Format per frame:
  run = [addr_lo][addr_hi][len(1..255)][data*len]  ; addr = absolute screen addr
  terminator = [00][00]
Frame sequence is circular: keyframe = frame[N-1]; then delta[i]=changes
frame[i-1]->frame[i]. Cold start applies keyframe; loop applies delta[0..N-1]."""
import sys
MIDDLE = 0x4800
def decode_one(data,pos,n=2048):
    esc=data[pos]; pos+=1; out=bytearray()
    while len(out)<n:
        b=data[pos]; pos+=1
        if b==esc:
            l=data[pos]; pos+=1; l=l or 256; v=data[pos]; pos+=1; out.extend([v]*l)
        else: out.append(b)
    return bytes(out[:n]),pos

def encode_runs(prev,cur,maxgap=3):
    diffs=[i for i in range(2048) if prev[i]!=cur[i]]
    blob=bytearray()
    if diffs:
        merged=[]; s=p=diffs[0]
        for x in diffs[1:]:
            if x-p<=maxgap: p=x
            else: merged.append((s,p)); s=p=x
        merged.append((s,p))
        for s,e in merged:
            i=s
            while i<=e:
                L=min(255,e-i+1)
                addr=MIDDLE+i
                blob+=bytes([addr&0xFF,addr>>8,L])+cur[i:i+L]
                i+=L
    blob+=bytes([0,0])   # terminator
    return blob

def keyframe_runs(img):
    blob=bytearray(); i=0
    while i<2048:
        L=min(255,2048-i); addr=MIDDLE+i
        blob+=bytes([addr&0xFF,addr>>8,L])+img[i:i+L]; i+=L
    blob+=bytes([0,0]); return blob

frames=open(sys.argv[1] if len(sys.argv)>1 else "frames.bin","rb").read()
pos=134; imgs=[]
for _ in range(60):
    img,pos=decode_one(frames,pos); imgs.append(img)
N=len(imgs)
blob=bytearray()
key=keyframe_runs(imgs[N-1]); key_off=0; blob+=key
delta_off=len(blob)
deltas=[]
for i in range(N):
    d=encode_runs(imgs[i-1],imgs[i]); deltas.append((len(blob),len(d))); blob+=d
open("deltas.bin","wb").write(blob)
print(f"N={N} frames; blob={len(blob)} bytes (orig frames were 38620)")
print(f"keyframe at blob+{key_off} ({len(key)} B); delta0 at blob+{delta_off}")
print(f"per-delta sizes: min {min(s for _,s in deltas)} max {max(s for _,s in deltas)}")
# emit pointer constants for load at 0x6590
LOAD=0x6590
print(f"if loaded at 0x{LOAD:04X}: KEYFRAME_PTR=0x{LOAD+key_off:04X} ({LOAD+key_off}), DELTA0_PTR=0x{LOAD+delta_off:04X} ({LOAD+delta_off})")
print(f"blob ends at 0x{LOAD+len(blob):04X}")
