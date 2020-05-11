import json
import os
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(), f))]

getfield=input('Enter the fields you want to extract seperated with comma: ')

print (onlyfiles)
dcc=open('azparseddata.csv','w')
getfield=getfield.split(',')
for hh in getfield:
	dcc.write(hh+';')
dcc.write('\n')

for i in onlyfiles:
	k=i.split('.')
	if len(k)==2:
		if k[1]=='json':
			try:
				print (i)
				f=open(i,'r')
				q=f.read()
				q=q.strip()
				f.close()
				#print (q)
				#input('..')
				#y = json.loads(i)
				q=q.replace('[','')
				q=q.replace(']','')
				res = q.split(',{') 
				#print (res[0])
				cjj=0
				#print (len(res))
				for jj in res:
					if len(res)==1:
						break
					if cjj==0:
						#res[cjj]=jj+'}'
						pass
					else:
						res[cjj]='{'+jj
					cjj+=1
				for nn in res:
					print (nn)
					print ('\n\n\n')
					ydd = json.loads(nn)
					for rer in getfield:
						try:
							dcc.write(ydd[rer]+';')
						except:
							dcc.write('-'+';')
					dcc.write('\n')
				#print (res)
				#input('.')
				pass
			except:
				pass

dcc.close()
