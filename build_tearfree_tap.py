#!/usr/bin/env python3
import re
T={'CLEAR':0xFD,'LOAD':0xEF,'CODE':0xAF,'RESTORE':0xE5,'FOR':0xEB,'READ':0xE3,
'POKE':0xF4,'NEXT':0xF3,'BORDER':0xE7,'PAPER':0xDA,'INK':0xD9,'BRIGHT':0xDC,
'CLS':0xFB,'RANDOMIZE':0xF9,'USR':0xC0,'DATA':0xE4,'GOTO':0xEC,'TO':0xCC}
def num(n):
    return str(int(n)).encode()+bytes([0x0E,0x00,0x00,int(n)&0xFF,(int(n)>>8)&0xFF,0x00])
def tok(spec):
    # spec: list of ('k',name)|('n',val)|('s',string)|('r',rawbytes)
    out=bytearray()
    for kind,v in spec:
        if kind=='k': out.append(T[v])
        elif kind=='n': out+=num(v)
        elif kind=='s': out+=b'"'+v.encode()+b'"'
        elif kind=='r': out+=bytes(v) if isinstance(v,(list,bytes,bytearray)) else v.encode()
    return bytes(out)
COL=[(b'\x3a')]  # statement sep
def line(numl, *specs):
    body=bytearray()
    for i,sp in enumerate(specs):
        if i: body+=b'\x3a'
        body+=tok(sp)
    body+=b'\x0d'
    return bytes([numl>>8,numl&0xFF,len(body)&0xFF,len(body)>>8])+body
applier=list(open("applier.bin","rb").read())
L=len(applier)
prog =line(10,[('k','CLEAR'),('n',25999)])
prog+=line(20,[('k','LOAD'),('s',''),('k','CODE'),('n',26000)])
prog+=line(30,[('k','RESTORE'),('n',100)],[('k','FOR'),('r','n'),('r','='),('n',23296),('k','TO'),('n',23296+L-1)],
              [('k','READ'),('r','d')],[('k','POKE'),('r','n'),('r',','),('r','d')],[('k','NEXT'),('r','n')])
prog+=line(40,[('k','BORDER'),('n',0)],[('k','PAPER'),('n',0)],[('k','INK'),('n',7)],[('k','BRIGHT'),('n',1)],[('k','CLS')])
prog+=line(50,[('k','RANDOMIZE'),('n',26000)],[('k','RANDOMIZE'),('k','USR'),('n',23296)])
prog+=line(60,[('k','FOR'),('r','f'),('r','='),('n',1),('k','TO'),('n',60)],[('k','RANDOMIZE'),('k','USR'),('n',23296)],[('k','NEXT'),('r','f')])
prog+=line(70,[('k','RANDOMIZE'),('n',28077)],[('k','GOTO'),('n',60)])
# DATA line: DATA n,n,n...
dspec=[('k','DATA')]
for i,b in enumerate(applier):
    if i: dspec.append(('r',','))
    dspec.append(('n',b))
prog+=line(100,dspec)

def block(flag,data):
    body=bytes([flag])+data;c=0
    for x in body:c^=x
    return (len(body)+1).to_bytes(2,'little')+body+bytes([c])
def header(typ,name,length,p1,p2):
    nm=name.encode()[:10].ljust(10)
    return block(0,bytes([typ])+nm+length.to_bytes(2,'little')+p1.to_bytes(2,'little')+p2.to_bytes(2,'little'))
deltas=open("deltas_w9.bin","rb").read()
tap =header(0,"W9TEAR",len(prog),10,len(prog))+block(0xFF,prog)   # autostart line 10
tap+=header(3,"DELTAS",len(deltas),26000,32768)+block(0xFF,deltas)
open("worlds9_tearfree.tap","wb").write(tap)
print(f"worlds9_tearfree.tap = {len(tap)} bytes (BASIC {len(prog)}B autostart 10 + DELTAS {len(deltas)}B @26000)")
print(f"applier {L} bytes")
