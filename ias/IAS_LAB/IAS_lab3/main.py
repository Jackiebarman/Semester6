from kamene.all import sniff,conf
# import kamene.all.
import random
import binascii
from packet import Packet
# import conf
pkts= sniff(filter='host 100.100.100.100 and tcp port 80',count=10)
# print(pkts,list(pkts))
packet_array=[]
for pkt in list(pkts):
    print("\n\n")
    packet=Packet(bytes(pkt))
    packet_array.append(packet)
    print(packet)
    print("\n\n"+"="*50)
# print(pkts.summary())