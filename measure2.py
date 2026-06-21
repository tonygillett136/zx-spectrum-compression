import sys, time, re
sys.path.insert(0,"/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/tools")
from zx_shot import Speccy
def num(s):
    m=re.search(r"-?\d+", s.replace(",",""));  return int(m.group()) if m else -1
with Speccy(port=10000) as zx:
    zx.smartload("/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds_fix/harness.sna")
    zx.sleep(1.2)
    zx.screenshot("/tmp/harness2.png")
    print("seed ptr:", zx.read_mem(0x5C76,2).hex())
    zx.cmd("enable-breakpoints")
    print("set-bp:", zx.cmd("set-breakpoint 1 PC=0FD17H")[:60])
    durs=[]
    for k in range(10):
        zx.cmd("enter-cpu-step")
        zx.cmd("run")
        time.sleep(0.2)
        r=zx.cmd("get-registers"); pc=re.search(r"PC=([0-9a-f]{4})",r)
        zx.cmd("reset-tstates-partial")
        zx.cmd("cpu-step-over")
        t=num(zx.cmd("get-tstates-partial"))
        durs.append((pc.group(1) if pc else "?", t))
    zx.cmd("clear-membreakpoints"); zx.cmd("disable-breakpoints")
    F=69888
    print("(PC_at_stop, decompress_T):")
    for pc,t in durs:
        print(f"  PC={pc} T={t}  = {t/F:.3f} frames" if t>0 else f"  PC={pc} T={t}")
