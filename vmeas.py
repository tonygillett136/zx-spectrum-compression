import sys, re
sys.path.insert(0,"/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/tools")
from zx_shot import Speccy
def reg(zx,n):
    m=re.search(rf"\b{n}=([0-9a-fA-F]{{2,4}})", zx.cmd("get-registers")); return int(m.group(1),16) if m else -1
def partial(zx):
    m=re.search(r"\d+", zx.cmd("get-tstates-partial")); return int(m.group()) if m else -1
CS=0xFD22
with Speccy(port=10000) as zx:
    zx.smartload("/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds_fix/harness_w9.sna")
    zx.sleep(0.8)
    zx.cmd("enter-cpu-step"); zx.cmd(f"set-register PC=0{CS:04X}H")
    durs=[]
    for _ in range(10):
        for _ in range(14):
            if reg(zx,"PC")==CS: break
            zx.cmd("cpu-step")
        zx.cmd("reset-tstates-partial"); zx.cmd("cpu-step-over"); durs.append(partial(zx))
        for _ in range(10):
            if reg(zx,"PC")==CS: break
            zx.cmd("cpu-step-over")
    zx.cmd("exit-cpu-step")
    good=[d for d in durs if 500<d<200000]
    print("per-frame apply T:", good, flush=True)
    if good: print(f"max {max(good)} T ; beam->middle third ~28700 ; TEAR-FREE? {max(good)<28700}", flush=True)
