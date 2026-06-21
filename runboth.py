import sys
sys.path.insert(0,"/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/tools")
from zx_shot import Speccy
for tag,sna in [("sync","harness_sync.sna"),("nosync","harness.sna")]:
    with Speccy(port=10000) as zx:
        zx.smartload(f"/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds_fix/{sna}")
        zx.sleep(1.5)
        p=zx.read_mem(0x5C76,2).hex()
        zx.screenshot(f"/tmp/h_{tag}.png")
        print(f"{tag}: seed advanced to {p} (non-frozen if changing), shot /tmp/h_{tag}.png")
