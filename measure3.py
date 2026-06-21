import sys, time, re
sys.path.insert(0,"/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/tools")
from zx_shot import Speccy
def pc(zx):
    m=re.search(r"PC=([0-9a-fA-F]{4})", zx.cmd("get-registers")); return int(m.group(1),16) if m else -1
def num(s):
    m=re.search(r"-?\d+", s.replace(",","")); return int(m.group()) if m else -1
with Speccy(port=10000) as zx:
    zx.smartload("/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds_fix/harness.sna")
    zx.sleep(1.0)
    zx.cmd("enter-cpu-step")
    print("partial-tstates probe:", zx.cmd("get-tstates-partial")[:40])
    durs=[]
    for trial in range(6):
        # single-step until at CallSite 0xFD17
        for _ in range(40):
            if pc(zx)==0xFD17: break
            zx.cmd("cpu-step")
        zx.cmd("reset-tstates-partial")
        zx.cmd("cpu-step-over")           # run the whole CALL DECOMP
        t=num(zx.cmd("get-tstates-partial"))
        durs.append(t)
        # one more step-over chunk to advance to next iteration's CallSite
        for _ in range(6):
            zx.cmd("cpu-step")
    zx.cmd("exit-cpu-step")
    F=69888
    print("decompress durations (T):", durs)
    for t in durs:
        if t>0: print(f"  {t} T = {t/F:.3f} frame  ({t//224} scanlines)")
