import os
import sys
from scapy.all import *

def create_packet(src_ip,dest_ip,src_port,dest_port):

	packet=IP(src=src_ip,dst=dest_ip)/TCP(sport=int(src_port),dport=int(dest_port))

	return packet

def main():

	send_fun=sys.argv[1]

	src_ip=input("Enter source ip: ")
	dest_ip=input("Enter destination ip: ")

	src_port=int(input("Enter source port: "))
	dest_port=int(input("Enter destination port: "))

	p=create_packet(src_ip,dest_ip,src_port,dest_port)

	if(send_fun=="sr1"):
		sr1(p)
	elif(send_fun=="sr"):
		sr(p)
	elif(send_fun=="srloop"):
		srloop(p)

if os.geteuid() != 0:
    os.execvp('sudo', ['sudo', 'python3'] + sys.argv)
main()
