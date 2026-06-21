import sys, re
sys.path.insert(0,"/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/tools")
from zx_shot import Speccy
# compute real delta start offsets from the blob
blob=open("deltas_w9.bin","rb").read()
def walk(off):
    while True:
        a=blob[off]|(blob[off+1]<<8); off+=2
        if a==0: return off
        L=blob[off]; off+=1+L
starts=[0]                       # keyframe at 0
o=walk(0); starts.append(o)      # delta0 start
for _ in range(5): o=walk(o); starts.append(o)   # a few more delta starts
LOAD=0x6590
addrs=[LOAD+s for s in starts[1:7]]   # delta0..delta5 (skip keyframe=2048B)
def pnum(zx):
    m=re.search(r"\d+", zx.cmd("get-tstates-partial")); return int(m.group()) if m else -1
with Speccy(port=10000) as zx:
    zx.smartload("/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds_fix/harness_w9.sna")
    zx.sleep(0.8); zx.cmd("enter-cpu-step")
    res=[]
    for ptr in addrs:
        zx.write_mem(0x5C76, bytes([ptr&0xFF, ptr>>8]))
        zx.cmd("set-register PC=0FD22H")     # CallSite (call ApplyDelta)
        zx.cmd("reset-tstates-partial")
        zx.cmd("cpu-step-over")
        res.append((hex(ptr), pnum(zx)))
    zx.cmd("exit-cpu-step")
    print("delta apply T:", res, flush=True)
    g=[t for _,t in res if 200<t<200000]
    if g: print(f"max {max(g)} T ; beam->mid-third ~28700 ; TEAR-FREE? {max(g)<28700}", flush=True)
