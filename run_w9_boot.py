import sys
sys.path.insert(0,"/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/tools")
from zx_shot import Speccy
def out(*a): print(*a); sys.stdout.flush()
with Speccy(port=10000) as zx:
    out("turbo:", repr(zx.cmd("set-cpu-turbo-speed 8")[:40]))
    zx.smartload("/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds9.tap")
    zx.sleep(3.0)
    zx.screenshot("/tmp/w9_boot.png")
    out("OCR:", zx.ocr()[:120].replace("\n"," "))
    out("mem@26134:", zx.read_mem(26134,8).hex())
