import sys
sys.path.insert(0,"/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/tools")
from zx_shot import Speccy
with Speccy(port=10000) as zx:
    zx.smartload("/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds_fix/harness_prod.sna")
    zx.sleep(1.5); zx.screenshot("/tmp/prod1.png")
    zx.sleep(0.6); zx.screenshot("/tmp/prod2.png")
    print("seed:", zx.read_mem(0x5C76,2).hex(), "(advancing = running)")
