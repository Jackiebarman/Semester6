import sys
class packet:
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
		prot  = "Protocol : " + self.protocol + "\n"
		macAddr = "mac src : " + '.'.join(list(map(lambda x: str(x), self.macAddress["source"]))) + "  mac dest : " + '.'.join(list(map(lambda x:str(x), self.macAddress["destination"]))) + "\n" 
		ipAddr = "ip src : " + '.'.join(list(map(lambda x: str(x), self.ipAddress["source"]))) + " ip dest : " + '.'.join(list(map(lambda x:str(x), self.ipAddress["destination"]))) + "\n" 
		portNo = "port src: " + str(self.portNumber["source"]) + " port dest :" + str(self.portNumber["destination"]) + "\n"
		return prot + macAddr + ipAddr + portNo




def main():

	testcase=sys.argv[1]
	print(testcase)
	file=open(testcase)
	str_test=file.read()
	print(str_test)
    
	pk=packet(str_test)
	pk.hexdumpParser()

	print(pk)


	# var_check_src=pk.ipAddress["source"]
	# if(var_check_src[0]==10 and var_check_src[1]==100 and var_check_src[2]==54):
	# 	print("allow")
	# else:
	# 	print("deny")

main()