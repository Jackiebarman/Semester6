import math
import xlrd

def main():
	input_file=open("hex-dump-eval.txt", "r+")
	doc=input_file.readlines()
	new_doc=[]
	for line in doc:
		line=line.rstrip("\n")
		if line != '':
			new_doc.append(line)

	#print(new_doc)
	frame_count=1
	for dump in new_doc:
		ACL(dump, frame_count)
	input_file.close()



def address_comp(s1, s2):
	# print(s1, s2)
	if s1=="Any":
		return True
	else:
		for i in range(len(s2)):
			if s1[i]!=s2[i]:
				if s1[i]!="*":
					return False
				else:
					return True
	return True

def prt_comp(p1, p2):
	if p1==p2 or p1=="Any":
		return True
	return False


def IP(ip_sec):
	type_o_s=ip_sec[1]
	print("Type Of Service : ", type_o_s, "\n")
	pkt_len=""
	pkt_len=str(ip_sec[2])+str(ip_sec[3])
	pkt_len=int(pkt_len, 16)
	print("Packet Length : ", pkt_len, "\n")
	IPID=""
	IPID=str(ip_sec[4])+str(ip_sec[5])
	IPID=int(IPID, 16)
	print("IPID : ", IPID, "\n")
	TTL=str(ip_sec[8])
	TTL=int(TTL, 16)
	print("Time To Live : ", TTL, "\n")
	embedded_prtcl=str(ip_sec[9])
	embedded_prtcl=int(embedded_prtcl, 16)
	if embedded_prtcl==6:
		print("Embedded Protocol : TCP\n")
	elif embedded_prtcl==17:
		print("Embedded Protocol : UDP\n")
	IP_chksm=str(ip_sec[10])+str(ip_sec[11])
	IP_chksm=int(IP_chksm, 16)
	print("IP Checksum : ", IP_chksm, "\n")
	add_src_ip=str(int(str(ip_sec[12]), 16))+"."+str(int(str(ip_sec[13]), 16))+"."+str(int(str(ip_sec[14]), 16))+"."+str(int(str(ip_sec[15]), 16))
	print("Source IP Address : ", add_src_ip, "\n")
	add_dest_ip=str(int(str(ip_sec[16]), 16))+"."+str(int(str(ip_sec[17]), 16))+"."+str(int(str(ip_sec[18]), 16))+"."+str(int(str(ip_sec[19]), 16))
	print("Destination IP Address : ", add_dest_ip, "\n")
	return [embedded_prtcl, add_src_ip, add_dest_ip]

def TCP(tcp_sec):
	port_src=str(tcp_sec[0])+str(tcp_sec[1])
	port_src=int(port_src, 16)
	print("Source Port Number : ", port_src, "\n")
	port_dest=str(tcp_sec[2])+str(tcp_sec[3])
	port_dest=int(port_dest, 16)
	print("Destination Port Number : ", port_dest, "\n")
	seq_num=str(tcp_sec[4])+str(tcp_sec[5])+str(tcp_sec[6])+str(tcp_sec[7])
	seq_num=int(seq_num, 16)
	print("Sequence Number : ", seq_num, "\n")
	ack_no=str(tcp_sec[8])+str(tcp_sec[9])+str(tcp_sec[10])+str(tcp_sec[11])
	ack_no=int(ack_no, 16)
	print("ACK Number : ", ack_no, "\n")
	tcp_hdr_len=int(tcp_sec[12])//10
	tcp_hdr_len=int(str(tcp_hdr_len), 16)
	print("TCP Header Length : ", (tcp_hdr_len*4), "\n")
	tcp_flg_fld=str(tcp_sec[13])
	tcp_flg_fld="{0:08b}".format(int(tcp_flg_fld, 16))
	print("TCP Flag Field : ", tcp_flg_fld, "\n")
	size_window=str(tcp_sec[14])+str(tcp_sec[15])
	size_window=int(size_window, 16)
	print("Window Size : ", size_window, "\n")
	TCP_chksm=str(tcp_sec[16])+str(tcp_sec[17])
	TCP_chksm=int(TCP_chksm, 16)
	print("TCP Checksum : ", TCP_chksm, "\n")
	urg_ptr=str(tcp_sec[18])+str(tcp_sec[19])
	urg_ptr=int(urg_ptr, 16)
	print("Urgent PTR : ", urg_ptr, "\n")
	return [port_src, port_dest]
def ACL(dump, frame_count):
	print("--------------------------------------------------------")
	print("Frame Number : ", frame_count, "\n")
	print("--------------------------------------------------------")
	dump=dump.split(' ')
	type_fld=ethernet(dump[:14])
	if type_fld=="IP":
		ver=int(dump[14])//10
		IP_headr_len=int(dump[14])%10
		if ver==6:
			print("This is an IPv6 packet\n")
			exit(0)
		elif ver==4:
			print("This is an IPv4 packet\n")
			res=IP(dump[14:(14+(ver*IP_headr_len))])
			embedded_prtcl=res[0]
			ip_addrss=res[1:]
			if embedded_prtcl==6:
				port_nos=TCP(dump[(14+(ver*IP_headr_len)):])
			elif embedded_prtcl==17:
				port_nos=UDP(dump[(14+(ver*IP_headr_len)):])
	elif type_fld=="ARP":
		ARP(dump[14:])
	frame_count+=1

	loc=("/home/jacky/Desktop/IAS_lab3/ACL-File-Lab-Program-3.xlsx")
	wb=xlrd.open_workbook(loc)
	sheet=wb.sheet_by_index(0)
	sheet.cell_value(0, 0)
	excel=[]
	for i in range(2, 8):
		excel.append(sheet.row_values(i))
	for i in range(len(excel)):
		excel[i].pop(0)
	#print(excel)

	if type_fld=="IP":
		for i in range(len(excel)):
			c1=address_comp(excel[i][0], ip_addrss[0])
			c3=address_comp(excel[i][2], ip_addrss[1])
			c2=prt_comp(excel[i][1], port_nos[0])
			c4=prt_comp(excel[i][3], port_nos[1])
			if c1 is True and c2 is True and c3 is True and c4 is True:
				print("The Action corresponding to the ACL is : ", excel[i][4], "\n")
				if excel[i][4]=="Allow":
					break
			else:
				print("The Action corresponding to the ACL is : Deny\n")
def ethernet(ethernet_sec):
	mac_add_dest=""
	mac_add_dest=str(ethernet_sec[0])+"."+str(ethernet_sec[1])+"."+str(ethernet_sec[2])+"."+str(ethernet_sec[3])+"."+str(ethernet_sec[4])+"."+str(ethernet_sec[5])
	mac_add_dest=""
	mac_add_dest=str(ethernet_sec[6])+"."+str(ethernet_sec[7])+"."+str(ethernet_sec[8])+"."+str(ethernet_sec[9])+"."+str(ethernet_sec[10])+"."+str(ethernet_sec[11])
	type_fld=""
	type_fld=str(ethernet_sec[12])+str(ethernet_sec[13])
	print("The Destination MAC Address : ", mac_add_dest, "\n")

	print(" The Source MAC Address : ", mac_add_dest, "\n")
	if type_fld == "0800":
		type="IP"
	elif type_fld == "0806":
		type="ARP"
	print("The Type of Field : ",type, "\n")
	return type
def UDP(UDP_sec):
	port_src=str(UDP_sec[0])+str(UDP_sec[1])
	port_src=int(port_src, 16)
	print("Source Port Number : ", port_src, "\n")
	port_dest=str(UDP_sec[2])+str(UDP_sec[3])
	port_dest=int(port_dest, 16)
	print("Destination Port Number : ", port_dest, "\n")
	UDP_hdr_len=str(UDP_sec[4])+str(UDP_sec[5])
	UDP_hdr_len=int(UDP_hdr_len, 16)
	print("UDP Header Length : ", UDP_hdr_len, "\n")
	UDP_chksm=str(UDP_sec[6])+str(UDP_sec[7])
	UDP_chksm=int(UDP_chksm, 16)
	print("UDP Checksum : ", UDP_chksm, "\n")
	return [port_src, port_dest]

def ARP(ARP_sec):
	type_hrdwre=str(ARP_sec[0])+str(ARP_sec[1])
	type_hrdwre=int(type_hrdwre, 16)
	print("Hardware Type : ", type_hrdwre, "\n")
	type_prtcl=str(ARP_sec[2])+str(ARP_sec[3])
	type_prtcl=int(type_prtcl, 16)
	print("Protocol Type : ", type_prtcl, "\n")
	len_hrdwr_add=str(ARP_sec[4])
	len_hrdwr_add=int(len_hrdwr_add, 16)
	print("Hardware Address Length : ", len_hrdwr_add, "\n")
	prtcl_add_len=str(ARP_sec[5])
	prtcl_add_len=int(prtcl_add_len, 16)
	print("Protocol Address Length : ", prtcl_add_len, "\n")
	opc=str(ARP_sec[7])
	opc=int(opc, 16)
	print("Opcode : ", opc,"\n")
	hard_add_send=str(ARP_sec[8])+"."+str(ARP_sec[9])+"."+str(ARP_sec[10])+"."+str(ARP_sec[11])+"."+str(ARP_sec[12])+"."+str(ARP_sec[13])
	sender_prtcl_add=str(int(str(ARP_sec[14]), 16))+"."+str(int(str(ARP_sec[15]), 16))+"."+str(int(str(ARP_sec[16]), 16))+"."+str(int(str(ARP_sec[17]), 16))
	hard_add_tar=str(ARP_sec[18])+"."+str(ARP_sec[19])+"."+str(ARP_sec[20])+"."+str(ARP_sec[21])+"."+str(ARP_sec[22])+"."+str(ARP_sec[23])
	target_prtcl_add=str(int(str(ARP_sec[24]), 16))+"."+str(int(str(ARP_sec[25]), 16))+"."+str(int(str(ARP_sec[26]), 16))+"."+str(int(str(ARP_sec[27]), 16))
	print("Sender Hardware Address : ", hard_add_send, "\n")
	print("Target Hardware Address : ", hard_add_tar, "\n")
	print("Sender Protocol Address : ", sender_prtcl_add, "\n")
	print("Target Protocol Address : ", target_prtcl_add, "\n")

if __name__ == '__main__':
	main()
