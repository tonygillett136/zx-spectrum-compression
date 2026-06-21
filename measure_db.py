import sys, re
sys.path.insert(0,"/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/tools")
from zx_shot import Speccy
def out(*a): print(*a); sys.stdout.flush()
def reg(zx,n):
    m=re.search(rf"\b{n}=([0-9a-fA-F]{{2,4}})", zx.cmd("get-registers")); return int(m.group(1),16) if m else -1
def partial(zx):
    m=re.search(r"\d+", zx.cmd("get-tstates-partial")); return int(m.group()) if m else -1
COPY=0x0
for line in open("/tmp/db.sym"):
    if "CopySite" in line:
        COPY=int(re.search(r"0x0000([0-9A-Fa-f]{4})",line).group(1),16)
out("CopySite=",hex(COPY))
with Speccy(port=10000) as zx:
    zx.smartload("/Volumes/SSD1/code/retro_computing/zxspectrum/mastery/worlds_fix/harness_db.sna")
    zx.sleep(1.5)
    zx.screenshot("/tmp/db_run.png")
    zx.cmd("enter-cpu-step")
    zx.cmd(f"set-register PC=0{COPY:04X}H")
    durs=[]
    for t in range(6):
        for _ in range(10):
            if reg(zx,"PC")==COPY: break
            zx.cmd("cpu-step")
        zx.cmd("reset-tstates-partial")
        zx.cmd("cpu-step-over")     # the CALL CopyShadow
        durs.append(partial(zx))
        for _ in range(12):         # advance to next CopySite (jr Loop; decompress; halt)
            if reg(zx,"PC")==COPY: break
            zx.cmd("cpu-step-over")
    zx.cmd("exit-cpu-step")
    F=69888; BEAM_MID=28700
    out("copy durations (T):", durs)
    good=[d for d in durs if 1000<d<200000]
    if good:
        out(f"copy avg {sum(good)//len(good)} T ; beam reaches middle third at ~{BEAM_MID} T")
        out("fits before beam?" , all(d<BEAM_MID for d in good))
