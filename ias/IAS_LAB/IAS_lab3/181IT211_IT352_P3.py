from scapy.all import *
from previous import ACL
import binascii
def main():
	ip_src, ip_dest, port_src, port_dest=None, None, None, None

	print("Destination IP  Only\n")
	
	option=2#int(input("Please enter the desired option : "))
	if option==1:
		ip_src=input("Please enter the Source IP address : ")
	elif option==2:
		ip_dest=input("Please enter the Destination IP address : ")
	elif option==3:
		ip_src=input("PLease enter the Source IP address : ")
		ip_dest=input("Please enter the Destination IP address : ")
	else:
		ip_src=input("Enter the Source IP address : ")
		ip_dest=input("Enter the Destination IP address : ")
		port_src=int(input("Enter the Source Port number : "))
		port_dest=int(input("Enter the Destination Port number : "))
	no_pkts=1

	hexdump_fin=sniff_pkts(ip_src, ip_dest, port_src, port_dest, no_pkts, option)
	print("The following packets are sniffed: \n", hexdump_fin)

	for a in range(len(hexdump_fin)):
		ACL(hexdump_fin[a],(a+1) )

def sniff_pkts(ip_src, ip_dest, port_src, port_dest, no_pkts, option):
	if option==1:
		fltr="src host "+str(ip_src)
	elif option==2:
		fltr="dst host "+str(ip_dest)
	elif option==3:
		fltr="src host "+str(ip_src)+" and dst host "+str(ip_dest)
	else:
		fltr="src host "+str(ip_src)+" and dst host "+str(ip_dest)+" and src port "+str(port_src)+" and dst port "+str(port_dest)


	print("** Please run 181IT211_IT352_P3b.py file **")
	pkts=sniff(filter=fltr, count=no_pkts)
	raw_pkt=[]
	for a in range(no_pkts):
		raw_pkt.append(raw(pkts[a]))

	print("The captured packet's raw format is as follows : \n", raw_pkt)

	hexdump_pkts=[]
	for a in range(no_pkts):
		bnry=binascii.hexlify(raw_pkt[a])
		hexdump_pkts.append(bnry.decode())

	hexdump_pkts_res=[]
	for a in hexdump_pkts:
		hexdump=""
		for b in range(len(a)):
			if b%2==0 and b!=0:
				hexdump+=" "
			hexdump+=a[b]
		hexdump_pkts_res.append(hexdump)

	return hexdump_pkts_res

if __name__ == '__main__':
	main()
