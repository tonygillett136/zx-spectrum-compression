import sys, re
sys.path.insert(0,"/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/tools")
from zx_shot import Speccy
def out(*a): print(*a); sys.stdout.flush()
with Speccy(port=10000) as zx:
    zx.smartload("/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds_fix/harness.sna")
    zx.sleep(1.0)
    zx.cmd("enter-cpu-step")
    out("regs:", zx.cmd("get-registers")[:60])
    out("get-tstates   :", repr(zx.cmd("get-tstates")[:40]))
    out("get-tstates-p :", repr(zx.cmd("get-tstates-partial")[:40]))
    out("one cpu-step  :", repr(zx.cmd("cpu-step")[:60]))
    out("get-tstates2  :", repr(zx.cmd("get-tstates")[:40]))
    out("step-over试    :", repr(zx.cmd("cpu-step-over")[:60]))
    out("get-tstates3  :", repr(zx.cmd("get-tstates")[:40]))
    zx.cmd("exit-cpu-step")
