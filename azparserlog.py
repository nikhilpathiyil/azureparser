import json
import os
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(), f))]

getfield=input('Enter the fields you want to extract seperated with comma: ')
orgfield=['version-number','request-start-time','operation-type','request-status','http-status-code','end-to-end-latency-in-ms','server-latency-in-ms','authentication-type','requester-account-name','owner-account-name','service-type','request-url','requested-object-key','request-id-header','operation-count','requester-ip-address','request-version-header','request-header-size','request-packet-size','response-header-size','response-packet-size','request-content-length','request-md5','server-md5','etag-identifier','last-modified-time','conditions-used','user-agent-header','referrer-header','client-request-id>']


dcc=open('azparseddata.csv','w')
getfield=getfield.split(',')
for hh in getfield:
	dcc.write(hh+';')
dcc.write('\n')

indexlist=[]
for jc in getfield:
	indexlist.append(orgfield.index(jc))




print (onlyfiles)
def charposition(string, char):
    pos = [] #list to store positions for each 'char' in 'string'
    for n in range(len(string)):
        if string[n] == char:
            pos.append(n)
    return pos


for i in onlyfiles:
	k=i.split('.')
	if len(k)==2:
		if k[1]=='log':
			try:
				
				#print (i)
				f=open(i,'r')
				q=f.read()
				q=q.strip()
				f.close()
				#print (q,'--')
				#input('..')
				#y = json.loads(i)
				q=q.replace('""','-')
				q=q.replace('"','-')
				q=q.replace("'",'-')
				res = q.split('\n') 
				#print (res[0])
				cjj=0
				#print (len(res))
				#print (res)
				for jj in res:
					#print ('\n')
					#print (jj)
					if len(jj)<2:
						continue
					hy=jj.split(';')
					fr=[]
					fir1=''
					las1=''
					totalstring=''
					#print ('\n')
					#print (hy)
					for ju in hy:
						if ju=='':
							totalstring=totalstring+';'+'-'
							continue
						#print (ju)
						if ju.startswith('-') and ju.endswith('-'):
							totalstring=totalstring+';'+ju
						elif ju.startswith('-'):
							fir1=ju
						elif ju[len(ju)-1]=='-':
							las1=ju
							#fr.append(fir1+las1)
							totalstring=totalstring+';'+fir1+las1
						else:
							#fr.append(ju)
							totalstring=totalstring+';'+ju
						#print (totalstring)
						#input ('.')
						pass
					totalstring=totalstring[1:]
					#print (totalstring)
					totalstring=totalstring.split(';')
					for ded in indexlist:
						dcc.write(totalstring[ded]+';')
					dcc.write('\n')
				"""
				for nn in fr:
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
				"""
				pass
			except Exception as e:
				#print (e)
				pass
#request-start-time,operation-type,request-status,authentication-type,request-url,requester-ip-address,user-agent-header
dcc.close()
