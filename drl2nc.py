Z_CLEARANCE = 11.11

import os,sys,re,time

print sys.argv
print 'NOW',time.localtime()[:6]

DRL_FILE = 'Through.drl'
DRL_FILE_H = open(DRL_FILE) ; print 'drill:',DRL_FILE
SRC = DRL_FILE_H.readlines()
DRL_FILE_H.close()

SVG_DX=SVG_DY=10
SVG_FILE = DRL_FILE+'.svg'
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
<rect x="'''+str(SVG_DX)+'''mm" y="'''+str(SVG_DY)+'''mm" width="80mm" height="50mm" fill="lightyellow" stroke="black" stroke-width="0.2mm"/>
'''

DRILLS={'00':'00.00'}
DRILL=''

FILLS={'00':'black','01':'red','02':'green','03':'blue'}

NC_FILE_H=open(DRL_FILE+'.nc','w')

def T_OPEN(TFN):
    global NC_FILE_H ; NC_FILE_H=open(TFN,'w')
T_OPEN(DRL_FILE+'.nc')
def T_CLOSE():
    NC_FILE_H.write('G0 Z%s\nM30\n%%\n'%Z_CLEARANCE)
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
        NC_FILE='%s.%s.nc'%(DRL_FILE,i[:-1])
        DRILL = re.findall(r'T(\d+)',i)[0] ; print 'DRILL',DRILL
        print 'file:',NC_FILE
        T_CLOSE() ; T_OPEN(NC_FILE)
        NC_FILE_H.write('%%\n%% drill: %s %s\n\n'%(DRILL,DRILLS[DRILL]))
    if re.match(r'^X.+Y.+$',i):
        X,Y=re.findall(r'X(.+)Y(.+)',i)[0]
        X=float(X)/SCALE
        Y=float(Y)/SCALE
        print i[:-1],X,Y
        print >>SVG,'<circle cx="%smm" cy="%smm" r="%smm" fill="%s"/>'%(X+SVG_DX,Y+SVG_DY,float(DRILLS[DRILL])/2,FILLS[DRILL])
        
T_CLOSE()

print >>SVG,'</svg>'
SVG.close()

print '.'
