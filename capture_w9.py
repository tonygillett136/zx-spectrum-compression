import sys, time, re
sys.path.insert(0,"/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/tools")
from zx_shot import Speccy
def out(*a): print(*a); sys.stdout.flush()
SC="/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds_fix/scompact.bin"
zx=Speccy(port=10000, extra_args=["--emulatorspeed","6000"])
try:
    zx.cmd('smartload "/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds9_gen.tap"', timeout=25)
    time.sleep(2.0)
    out("at PAUSE? PC=", re.search(r"PC=([0-9a-f]{4})",zx.cmd("get-registers")).group(1))
    out("load-binary:", zx.cmd(f'load-binary "{SC}" 26000 134')[:50])
    out("sc@26000:", zx.read_mem(26000,8).hex(), "(expect 0600c5782100400...)")
    # release PAUSE 0 with a keypress
    zx.cmd('send-keys-string 200 " "')
    time.sleep(0.5)
    # watch generation
    last=-1
    for t in range(20):
        time.sleep(1.5)
        far=zx.read_mem(26134+34000,4).hex()
        ocr=zx.ocr().replace("\n"," ").strip()[:30]
        pc=re.search(r"PC=([0-9a-f]{4})",zx.cmd("get-registers")).group(1)
        out(f"t={t}: far@60134={far} pc={pc} ocr='{ocr}'")
        if far!="00000000" and far==last: out("generation appears complete"); break
        last=far
    data=zx.read_mem(26134,40000)
    open("/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds_fix/w9_real.bin","wb").write(data)
    out("saved w9_real.bin")
finally:
    zx.close()
