import sys, re
sys.path.insert(0,"/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/tools")
from zx_shot import Speccy
def out(*a): print(*a); sys.stdout.flush()
def reg(zx,name):
    m=re.search(rf"\b{name}=([0-9a-fA-F]{{2,4}})", zx.cmd("get-registers")); return int(m.group(1),16) if m else -1
def partial(zx):
    m=re.search(r"\d+", zx.cmd("get-tstates-partial")); return int(m.group()) if m else -1
with Speccy(port=10000) as zx:
    zx.smartload("/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds_fix/harness.sna")
    zx.sleep(1.0)
    zx.cmd("enter-cpu-step")
    durs=[]
    for trial in range(6):
        # step until at CallSite 0xFD17
        ok=False
        for _ in range(30):
            if reg(zx,"PC")==0xFD17: ok=True; break
            zx.cmd("cpu-step")
        if not ok: out("trial",trial,"never reached CallSite, PC=",hex(reg(zx,"PC"))); continue
        zx.cmd("reset-tstates-partial")
        zx.cmd("cpu-step-over")        # execute CALL DECOMP (whole frame decompress)
        durs.append(partial(zx))
    zx.cmd("exit-cpu-step")
    F=69888
    out("decompress durations (T):", durs)
    for t in durs:
        if t>0: out(f"  {t} T = {t/F:.3f} frame = {t//224} scanlines")
    good=[t for t in durs if t>0]
    if good: out(f"avg {sum(good)//len(good)} T = {sum(good)/len(good)/F:.3f} frame")
