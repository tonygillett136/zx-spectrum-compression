import sys, re
sys.path.insert(0,"/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/tools")
from zx_shot import Speccy
def pnum(zx):
    m=re.search(r"\d+", zx.cmd("get-tstates-partial")); return int(m.group()) if m else -1
with Speccy(port=10000) as zx:
    zx.smartload("/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds_fix/harness_w9.sna")
    zx.sleep(0.8)
    zx.cmd("enter-cpu-step")
    res=[]
    for ptr in (0x6DAD, 0x7000, 0x8000, 0x9000, 0xB000, 0xE000):  # various deltas
        zx.write_mem(0x5C76, bytes([ptr&0xFF, ptr>>8]))
        zx.cmd("set-register PC=0FD22H")     # ApplyDelta entry (after CallSite's CALL target)
        zx.cmd("reset-tstates-partial")
        zx.cmd("cpu-step-over")              # run whole ApplyDelta from entry
        res.append((hex(ptr), pnum(zx)))
    zx.cmd("exit-cpu-step")
    print("ApplyDelta(entry) durations:", res, flush=True)
    good=[t for _,t in res if 200<t<200000]
    if good: print(f"max {max(good)} T ; beam~28700 ; TEAR-FREE? {max(good)<28700}", flush=True)
