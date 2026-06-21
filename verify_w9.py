import sys, time, re
sys.path.insert(0,"/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/tools")
from zx_shot import Speccy
def out(*a): print(*a); sys.stdout.flush()
def reg(zx,n):
    m=re.search(rf"\b{n}=([0-9a-fA-F]{{2,4}})", zx.cmd("get-registers")); return int(m.group(1),16) if m else -1
def partial(zx):
    m=re.search(r"\d+", zx.cmd("get-tstates-partial")); return int(m.group()) if m else -1
CS=0
for l in open("/tmp/w9.sym"):
    if l.startswith("CallSite"): CS=int(re.search(r"0x0000([0-9A-Fa-f]{4})",l).group(1),16)
with Speccy(port=10000) as zx:
    zx.smartload("/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds_fix/harness_w9.sna")
    zx.sleep(1.0); zx.screenshot("/tmp/w9_v0.png")
    zx.sleep(0.4); zx.screenshot("/tmp/w9_v1.png")
    zx.sleep(0.4); zx.screenshot("/tmp/w9_v2.png")
    # measure per-frame apply time
    zx.cmd("enter-cpu-step"); zx.cmd(f"set-register PC=0{CS:04X}H")
    durs=[]
    for _ in range(8):
        for _ in range(12):
            if reg(zx,"PC")==CS: break
            zx.cmd("cpu-step")
        zx.cmd("reset-tstates-partial"); zx.cmd("cpu-step-over"); durs.append(partial(zx))
        for _ in range(10):
            if reg(zx,"PC")==CS: break
            zx.cmd("cpu-step-over")
    zx.cmd("exit-cpu-step")
    good=[d for d in durs if 500<d<200000]
    out("apply T/frame:",good)
    if good: out(f"max {max(good)} T ; beam->middle third ~28700 ; tear-free? {max(good)<28700}")
