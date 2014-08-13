import os,sys,time,re

batname=re.sub(r'\.py',r'.bat',sys.argv[0])
bat=open(batname,'w')

for i in os.listdir('.'):
    if i.split('.')[-1]=='drl':
        print >>bat,'python drl2nc.py %s'%i
        
bat.close()

os.system('notepad %s'%batname)
