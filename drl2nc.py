Z_END = 11.11
Z_FAST = 2.2
Z_SLOW = 1.1
Z_DRILL = -2.5 

FEED = .1
SPEED = 22222

CNC_IP = '192.168.255.18'

import os,sys,re,time

print sys.argv
print 'NOW',time.localtime()[:6]

DRL_FILE = sys.argv[1]
DRL_FILE_H = open(DRL_FILE) ; print 'drill:',DRL_FILE
SRC = DRL_FILE_H.readlines()
DRL_FILE_H.close()

BAT=open(re.sub(r'\.drl$',r'.bat',DRL_FILE),'w')
BAT_NCS={}
print >>BAT,'rem',DRL_FILE,'\n'

SVG_DX=SVG_DY=10
SVG_FILE = re.sub(r'\.drl',r'.svg',DRL_FILE)
SVG = open(SVG_FILE,'w')
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

DRILLS={'00':'00.00'}
DRILL=''

FILLS={'00':'black','01':'red','02':'green','03':'blue','04':'magenta','05':'cyan','06':'brown','07':'darkyellow'}

MINX=MINY=1e9
MAXX=MAXY=-1e9

NC_FILE_H=open('nul','w')
def NC_OPEN(TFN):
    print 'file:',TFN
    global NC_FILE_H ; NC_FILE_H=open(TFN,'w')
    global BAT_NCS ; BAT_NCS[TFN]=1

def NC_CLOSE():
    NC_FILE_H.write('G0 Z%s\nM30\n%%\n'%Z_END)
    NC_FILE_H.close()

SCALE=0
for i in SRC:
    if re.match(r'^METRIC,.+',i):
        print 'format:',i[:-1],
        SCALE=10**len(re.findall(r'\.(0+)',i)[0])
    if re.match(r'^T\d+C.+',i):
        print 'drill:',i[:-1]
        X,Y=re.findall(r'T(.+)C(.+)',i)[0] ; DRILL=X ; DRILLS[DRILL]=Y
    if re.match(r'^T\d+$',i):
        NC_FILE='%s_%s.nc'%(re.sub(r'\.drl$',r'',DRL_FILE),i[:-1])
        DRILL = re.findall(r'T(\d+)',i)[0] ; print 'DRILL',DRILL
        NC_CLOSE() ; NC_OPEN(NC_FILE)
        print >>NC_FILE_H,'%%\n( drill: )\n( T%s %s )\n\nM3 S%s\nG4 P2\nG0 Z%s\n\n'%(DRILL,DRILLS[DRILL],SPEED,Z_FAST)
    if re.match(r'^X.+Y.+$',i):
        X,Y=re.findall(r'X(.+)Y(.+)',i)[0] ; X,Y=map(lambda z:float(z)/SCALE,[X,Y])
        print i[:-1],X,Y
        print >>SVG,'<circle cx="%smm" cy="%smm" r="%smm" fill="%s"/>'%(X+SVG_DX,100-Y+SVG_DY,float(DRILLS[DRILL])/2,FILLS[DRILL])
        MINX=min(MINX,X) ; MAXX=max(MAXX,X)
        MINY=min(MINY,Y) ; MAXY=max(MAXY,Y)
        print >>NC_FILE_H,'G0 X%s Y%s ( next hole )\nG1 Z%s F1 \nG1 Z%s F%s ( work )\nG1 Z%s F1\nG0 Z%s\n'%(X,Y,Z_SLOW,Z_DRILL,FEED,Z_SLOW,Z_FAST)

print >>NC_FILE_H,'G1 X%s Y%x F0.01\nG1 X%s Y%s F0.01\n'%(MINX,MINY,MAXX,MAXY)        
NC_CLOSE()

print MINX,MINY,'..',MAXX,MAXY
#print >>SVG,'<rect x="%smm" y="%smm" width="%smm" height="%smm" fill="none" stroke="black" stroke-width="0.2mm"/>'%(MINX-5+SVG_DX,MINY-5+SVG_DY,abs(MINX-MAXX)+10,abs(MINY-MAXY)+10)
print >>SVG,'</svg>'
SVG.close()

for i in sorted(BAT_NCS.keys()):
    print >>BAT,'\npause\n',r'\IMES\IMESc.exe',i,CNC_IP

BAT.close()

print '.'
