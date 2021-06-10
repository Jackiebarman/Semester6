import sys
class packet :
	def __init__(self,dump):
		self.dump=dump
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


	
	def hexdumpParser(self):
		cleanDump = list(map(lambda x: int(x,16), self.dump.split()))
		if cleanDump[13] != 00:
			print("Packet is not IPv4 packet, cannot process any further")
			self.isIPv4 = False
			return

		self.macAddress["destination"] = list(map(lambda x: hex(x)[2:], cleanDump[0:6]))
		self.macAddress["source"] = list(map(lambda x: hex(x)[2:], cleanDump[6:12]))
		self.frameLength = cleanDump[12:14]
		self.protocol = "UDP" if cleanDump[23] == 17 else "TCP"

		self.ipVesrion = cleanDump[14] >> 4
		self.ipAddress["source"] = cleanDump[26:30]
		self.ipAddress["destination"] = cleanDump[30:34]

		self.portNumber["source"] = (cleanDump[34] << 8) + cleanDump[35]
		self.portNumber["destination"]=(cleanDump[36] << 8) + cleanDump[37]


	def __str__(self):
		if self.isIPv4 == False :
			return "Packet is not IPv4"
		print()	
		print("IPv4 PACKET INFORMATION: ")	
		prot  = "Protocol Used: " + self.protocol + "\n"
		macAddr = "Source macAddress : " + '.'.join(list(map(lambda x: str(x), self.macAddress["source"]))) + "    Destination macAddress : " + '.'.join(list(map(lambda x:str(x), self.macAddress["destination"]))) + "\n" 
		ipAddr = "Source ipAddress : " + '.'.join(list(map(lambda x: str(x), self.ipAddress["source"]))) + "    Destination ipAddress : " + '.'.join(list(map(lambda x:str(x), self.ipAddress["destination"]))) + "\n" 
		portNo = "Source Port : " + str(self.portNumber["source"]) + "    Destination Port :" + str(self.portNumber["destination"]) + "\n"
		return prot + macAddr + ipAddr + portNo


# file=open("testcase5.txt")
# str_test=file.read();

# pk=packet(str_test)
# pk.hexdumpParser()
# print(pk)

def main():

	testcase=sys.argv[1]
	file=open(testcase)
	str_test=file.read();

	pk=packet(str_test)
	pk.hexdumpParser()

	print(pk)

	var_check_src=pk.ipAddress["source"]
	#print(var_check_src)
	#print(testcase[8])
	if testcase[8]=='1':
	    if(var_check_src[0]==10 and var_check_src[1]==100 and var_check_src[2]==54):
		    print("ACTION: ACCESS ALLOWED")
	    else:
		    print("ACTION: DENY")
	elif testcase[8]=='2':
	    if(pk.portNumber["destination"]=="80"):
	        print("ACTION: DENY")
	    else:
	        print("ACTION: ACCESS ALLOWED")  
	elif testcase[8]=='3':
	    if(pk.ipAddress["destination"][0]==10 and pk.ipAddress["destination"][1]==100 and pk.ipAddress["destination"][2]==53 and pk.ipAddress["destination"][3]==1 and pk.portNumber["destination"]=="443"):
	        print("ACTION: DENY")
	    else:
	        print("ACTION: ACCESS ALLOWED") 
	elif testcase[8]=='4':
	    if(pk.ipAddress["destination"][0]==10 and pk.ipAddress["destination"][1]==100 and pk.ipAddress["destination"][2]==53):
	        print("ACTION: DENY")
	    else:
	        print("ACTION: ACCESS ALLOWED")                       	    
	else:
	    print("ACTION: DENY")
			

main()