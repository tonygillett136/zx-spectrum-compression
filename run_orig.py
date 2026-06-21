import sys, time
sys.path.insert(0,"/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/tools")
from zx_shot import Speccy
TAP="/Volumes/SSD1/code/retro_computing/zxspectrum/software_archive/TONY/SCOMPACT.TAP"
with Speccy(port=10000) as zx:
    zx.smartload(TAP)
    zx.sleep(4.0)
    zx.screenshot("/tmp/worlds_orig_1.png")
    zx.sleep(0.7)
    zx.screenshot("/tmp/worlds_orig_2.png")
    # is the decompressor present at 0xFFDC?
    print("FFDC bytes:", zx.read_mem(0xFFDC,12).hex())
    print("frame ptr 5C76:", zx.read_mem(0x5C76,2).hex())
