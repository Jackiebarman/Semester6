from scapy.all import *

def main():
	ip_src=input("Enter the Source IP address : ")
	ip_dest=input("Enter the Destination IP address : ")
	port_src=int(input("Enter the Source Port number : "))
	port_dest=int(input("Enter the Destination Port number : "))
	type_prtcl=input("Enter the protocol (TCP or UDP) : ")
	func=input("Enter the type of send/ receive func : ")
	no_pkts=1

	x=Ether()
	y=IP()
	y.src=ip_src
	y.dst=ip_dest
	if type_prtcl=="TCP" or type_prtcl=="tcp":
		z=TCP()
		z.sport=port_src
		z.dport=port_dest
	elif type_prtcl=="UDP" or type_prtcl=="udp":
		z=UDP()
		z.sport=port_src
		z.dport=port_dest
	else:
		print("Protocol type is not valid")

	pkt=y/z	
	for k in range(no_pkts):
		if func=="sr":
			sr(pkt, timeout=1)
		elif func=="sr1":
			sr1(pkt, timeout=1)
		else:
			srloop(pkt)
if __name__ == '__main__':
	main()