import sys, time, re
sys.path.insert(0,"/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/tools")
from zx_shot import Speccy

def num(s):
    m=re.search(r"\d+", s.replace(",",""))
    return int(m.group()) if m else -1

with Speccy(port=10000) as zx:
    zx.smartload("/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds_fix/harness.sna")
    zx.sleep(1.5)
    zx.screenshot("/tmp/harness_frame.png")   # confirm a real frame renders
    print("frame ptr now:", zx.read_mem(0x5C76,2).hex())
    # measure several decompress calls
    zx.cmd("enable-breakpoints")
    zx.cmd("set-breakpoint 1 PC=0FD0AH")
    durations=[]
    for k in range(8):
        # run to breakpoint (CallSite)
        zx.cmd("exit-cpu-step")
        time.sleep(0.25)
        # should be stopped at CallSite; confirm
        r=zx.cmd("get-registers")
        pc=re.search(r"PC=([0-9a-f]{4})", r)
        zx.cmd("reset-tstates-partial")
        zx.cmd("cpu-step-over")          # execute the CALL DECOMP fully
        t=num(zx.cmd("get-tstates-partial"))
        durations.append(t)
    zx.cmd("clear-membreakpoints")
    zx.cmd("disable-breakpoints")
    FRAME=69888
    print("decompress durations (T-states):", durations)
    for t in durations:
        if t>0: print(f"  {t} T = {t/FRAME:.2f} frames")
