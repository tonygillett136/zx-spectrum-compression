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
    # force clean start: SEED=first frame, PC=CallSite
    zx.write_mem(0x5C76, bytes([0x16,0x66]))     # 0x6616
    zx.cmd("set-register PC=0FD17H")
    out("forced PC=", hex(reg(zx,"PC")), " SEED=", zx.read_mem(0x5C76,2).hex())
    durs=[]
    for trial in range(12):
        if reg(zx,"PC")!=0xFD17:
            # walk back to CallSite (jr Loop is a few instrs)
            for _ in range(8):
                if reg(zx,"PC")==0xFD17: break
                zx.cmd("cpu-step")
        zx.cmd("reset-tstates-partial")
        zx.cmd("cpu-step-over")
        durs.append(partial(zx))
        # advance past ld(seed),bc + checks to next CallSite
        for _ in range(8):
            if reg(zx,"PC")==0xFD17: break
            zx.cmd("cpu-step")
    zx.cmd("exit-cpu-step")
    F=69888
    out("durations (T):", durs)
    good=[t for t in durs if 1000<t<200000]
    for t in good: out(f"  {t} T = {t/F:.3f} frame = {t//224} lines")
    if good: out(f"AVG {sum(good)//len(good)} T = {sum(good)/len(good)/F:.3f} frame ; MAX {max(good)} = {max(good)/F:.3f} frame")
