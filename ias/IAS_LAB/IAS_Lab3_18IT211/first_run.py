import os
import sys
from scapy.all import *

class A :
	def __init__(self,data):
		self.data=data
		self.macAddress = {
			"source" : None,
			"destination" : None
		}
		self.frameLength = None
		self.ipVesrion = None
		self.ipAddress = {
			"source" : None,
			"destination" : None	
		}
		self.portNumber = {
			"source" : None,
			"destination" : None		
		}	
		self.isIPv4 = True
		self.protocol = None


	
	def fun(self):

		cleandata = list(map(lambda x: int(x,16), self.data.split()))
		
		if cleandata[13] != 00:
			print("Packet is not IPv4 packet, cannot process any further")
			self.isIPv4 = False
			return

		self.macAddress["destination"] = list(map(lambda x: hex(x)[2:], cleandata[0:6]))
		self.macAddress["source"] = list(map(lambda x: hex(x)[2:], cleandata[6:12]))
		self.frameLength = cleandata[12:14]
		self.protocol = "UDP" if cleandata[23] == 17 else "TCP"

		self.ipVesrion = cleandata[14] >> 4
		self.ipAddress["source"] = cleandata[26:30]
		self.ipAddress["destination"] = cleandata[30:34]

		self.portNumber["source"] = (cleandata[34] << 8) + cleandata[35]
		self.portNumber["destination"]=(cleandata[36] << 8) + cleandata[37]


	def __str__(self):
		if self.isIPv4 == False :
			return "Packet is not IPv4"
		prot  = "Protocol : " + self.protocol + "\n"
		macAddr = "Source macAddress : " + '.'.join(list(map(lambda x: str(x), self.macAddress["source"]))) +"\n"+ "Destination macAddress : " + '.'.join(list(map(lambda x:str(x), self.macAddress["destination"]))) + "\n" 
		ipAddr = "Source ipAddress : " + '.'.join(list(map(lambda x: str(x), self.ipAddress["source"]))) + "\n"+"Destination ipAddress : " + '.'.join(list(map(lambda x:str(x), self.ipAddress["destination"]))) + "\n" 
		portNo = "Source port: " + str(self.portNumber["source"]) +"\n"+ "Destination port :" + str(self.portNumber["destination"]) + "\n"
		return "IPV4 packet\n" +prot + macAddr + ipAddr + portNo


if os.geteuid() != 0:
    os.execvp('sudo', ['sudo', 'python3'] + sys.argv)

testcase=sys.argv[1]
dest_ip=input("Enter destination ip: ")
s1="host "+dest_ip
packet = sniff( filter=s1,count = 1)
p= chexdump(packet[0], dump=True)

data=""
for i in range(2,len(p),6):
	data=data+p[i]+p[i+1]+" "
print()
print("Packet in raw format:")
print()
print(p)
print()
print(data)
print()
print()
print("Packet in human readable form:")
print()
obj=A(data)
obj.fun()

print(obj)
print()
if(testcase=="testcase1"):

	if(obj.ipAddress["source"][0]==10 and obj.ipAddress["source"][1]==10 and obj.ipAddress["source"][2]==1 and obj.ipAddress["source"][3]==1 and obj.portNumber["destination"]==80):
		print("deny")
	else:
		print("allow")

elif(testcase=="testcase2"):

	if(obj.ipAddress["destination"][0]==100 and obj.ipAddress["destination"][1]==100 and obj.ipAddress["destination"][2]==100 and obj.ipAddress["destination"][3]==100 and obj.portNumber["destination"]==80):
		print("deny")
	else:
		print("allow")

elif(testcase=="testcase3"):

	if(obj.ipAddress["destination"][0]==100 and obj.ipAddress["destination"][1]==100 and obj.ipAddress["destination"][2]==100 and obj.ipAddress["destination"][3]==100 and obj.portNumber["destination"]==400)  :
		print("deny")
	else:
		print("allow")

elif(testcase=="testcase4"):

	if(obj.ipAddress["destination"][0]==200 and obj.ipAddress["destination"][1]==200 and obj.ipAddress["destination"][2]==200 and obj.ipAddress["destination"][3]==200) :
		print("deny")
	else:
		print("allow")
