import sys, time
sys.path.insert(0,"/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/tools")
from zx_shot import Speccy
print("start",flush=True)
with Speccy(port=10000) as zx:
    print("launched",flush=True)
    zx.smartload("/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds_fix/harness_w9.sna")
    zx.sleep(1.0); zx.screenshot("/tmp/w9_v0.png")
    zx.sleep(0.4); zx.screenshot("/tmp/w9_v1.png")
    zx.sleep(0.4); zx.screenshot("/tmp/w9_v2.png")
    print("seed:", zx.read_mem(0x5C76,2).hex(), flush=True)
print("done",flush=True)
