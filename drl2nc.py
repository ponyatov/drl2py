
S_FILE = 'Through.drl'
T_FILE = S_FILE+'.nc'

S_FILE_H = open(S_FILE) ; print 'drill:',S_FILE
T_FILE_H = open(T_FILE,'w') ; print 'gcode:',T_FILE

S_FILE_H.close()
T_FILE_H.close()

print '.'
