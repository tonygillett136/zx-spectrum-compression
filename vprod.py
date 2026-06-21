import sys
sys.path.insert(0,"/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/tools")
from zx_shot import Speccy
with Speccy(port=10000) as zx:
    zx.smartload("/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds_fix/harness_prod_w9.sna")
    zx.sleep(1.0); zx.screenshot("/tmp/prodw9_0.png")
    zx.sleep(0.5); zx.screenshot("/tmp/prodw9_1.png")
    zx.sleep(0.5); zx.screenshot("/tmp/prodw9_2.png")
    print("seed:", zx.read_mem(0x5C76,2).hex(), flush=True)
