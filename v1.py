# -*- coding: cp1251 -*-

DRL = r'\\arhive\Public\ponyatov\�������\15.09.2014\I-all_holes.drl'

SVG_MAX_Y = 222

R_DELTA = 0.5#e-6

CNC_IP = '192.168.255.18'

S_SPEED = 22222
F_FEED_IN = 0.1
F_FEED_OUT = 1.0
Z_END = 55.55
Z_FAST = 2.2
Z_SLOW = 1.1
Z_DRILL = -2.5

import os,sys,time,re

print time.localtime()[:6],sys.argv

############################ DRL PARSER #############################

DRL_F = open(DRL)

SVG = open('svg.svg','w')
print >>SVG,'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
    "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1"
     baseProfile="full"
     xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     xmlns:ev="http://www.w3.org/2001/xml-events"
     width="100%" height="100%">
'''

BITS={'00':'0.0',None:'0.0'}

REX_BIT=r'^T(\d+)C(.+)\n$'
REX_SET=r'^T(\d+)\n$'
REX_COORD = r'^X(.+)(\d{2})Y(.+)(\d{2})\n$'
REX_IGNORE = r'^(%|M48|M30)\n$'

HOLES={}
CURRENT=None

for i in DRL_F.readlines():
    if re.match(REX_BIT,i):
        A,B=re.findall(REX_BIT,i)[0]
        BITS[A]=B
    elif re.match(REX_SET, i):
        CURRENT=re.findall(REX_SET, i)[0]
    elif re.match(REX_COORD,i):
        X1,X2,Y1,Y2=re.findall(REX_COORD,i)[0]
        X='%s.%s'%(X1,X2)
        Y='%s.%s'%(Y1,Y2)
        R=max(R_DELTA,float(BITS[CURRENT])/2)
        COLOR='black'
        if R*2>.5:
            COLOR='green'
        if R*2>1:
            COLOR='blue'
        if abs(R*2-1.111)<1e-6:
            COLOR='red'
        print >>SVG,'<circle cx="%smm" cy="%smm" r="%smm" fill="%s"/>'%(X,SVG_MAX_Y-float(Y),R,COLOR)
        T='X %s Y %s'%(X,Y)
        try:
            HOLES[CURRENT]+=[T]
        except KeyError:
            HOLES[CURRENT] =[T]
    elif re.match(REX_IGNORE,i):
        pass
    else:
        print i[:-1]

DRL_F.close()

print >>SVG,'</svg>'
SVG.close()

############################ NC SENDER #############################

print BITS
print
for i in sorted(HOLES):
    raw_input('-')
    NCFNAME='%s.nc'%i
    F=open(NCFNAME,'w')
    HEADLINE = '%%\n( T[%s] drill %s )\n'%(i,BITS[i])
    print HEADLINE 
    print >>F, HEADLINE
    print >>F,'G0 Z%s\nM3 S%s\nG4 P2\nG0 Z%s'%(Z_END,S_SPEED,Z_FAST)
    for j in HOLES[i]:
        print >>F,'\nG0 %s\nG0 Z%s\nG1 Z%s F%s\nG1 Z%s F%s\nG0 Z%s'%(j,Z_SLOW,Z_DRILL,F_FEED_IN,Z_SLOW,F_FEED_OUT,Z_FAST)
    print >>F,'\nG0 Z%s\nM30\n%%'%Z_END
    F.close()
    CMD=r'\IMES\IMESc.exe %s %s'%(NCFNAME,CNC_IP)
    print 'CMD:',CMD,
    print os.system(CMD)

raw_input('.')
