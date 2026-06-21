import sys, time
sys.path.insert(0,"/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/tools")
from zx_shot import Speccy
def out(*a): print(*a); sys.stdout.flush()
TAP="/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds9.tap"
zx=Speccy(port=10000, extra_args=["--tape",TAP,"--fastautoload","--emulatorspeed","6000"])
try:
    for t in range(12):
        time.sleep(2.0)
        sc=zx.read_mem(26000,4).hex()           # SCOMPACT loaded?
        end=zx.read_mem(26134+30000,4).hex()     # has gen reached ~frame 50+?
        ocr=zx.ocr().replace("\n"," ").strip()[:40]
        out(f"t={t*2:>3}s  sc@26000={sc}  far@56134={end}  ocr='{ocr}'")
    # capture frame data
    data=zx.read_mem(26134, 40000)
    open("/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds_fix/w9_real.bin","wb").write(data)
    out("saved w9_real.bin (40000 bytes from 26134)")
finally:
    zx.close()
