import sys, time, re
sys.path.insert(0,"/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/tools")
from zx_shot import Speccy
def out(*a): print(*a); sys.stdout.flush()
zx=Speccy(port=10000, extra_args=["--emulatorspeed","6000"])
try:
    out("smartload:", zx.cmd('smartload "/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds9.tap"', timeout=25)[:60])
    for t in range(8):
        time.sleep(1.5)
        prog=zx.read_mem(0x5C53,2)            # PROG sysvar (23635) -> program start
        pp=prog[0]|(prog[1]<<8)
        sc=zx.read_mem(26000,4).hex()
        r=zx.cmd("get-registers"); pc=re.search(r"PC=([0-9a-f]{4})",r)
        far=zx.read_mem(26134+20000,4).hex()
        out(f"t={t}: PROG={pp:#06x} firstprogbytes={zx.read_mem(pp,6).hex() if pp else '----'} sc@26000={sc} PC={pc.group(1) if pc else '?'} far={far}")
finally:
    zx.close()
