# from pypacker.layer12 import ethernet
# from pypacker.layer3 import ip
# from pypacker.layer4 import tcp
# from pypacker.layer4 import udp
import re
import binascii

class Packet:
    def __init__(self,pkt):
        bcode= binascii.hexlify(bytes(pkt))
        self.bcode= [bcode[i:i+2].decode(encoding='UTF-8') for i in range(0, len(bcode), 2)]
        print(" ".join(self.bcode))
        if(self.bcode[13]!='00'):
            self.isIPV4=False
        else:
            self.isIPV4=True
            self.macAddress={
                "src": ".".join(self.bcode[6:12]),
                "dst": ".".join(self.bcode[0:6])
            }
            
            self.ipAddress={
                "src": ".".join(list(map(lambda x:str(int(x,16)),self.bcode[26:30]))),
                "dst": ".".join(list(map(lambda x:str(int(x,16)),self.bcode[30:34])))
            }
            
            self.portNum={
                "src": (int(self.bcode[34],16)<<8)+int(self.bcode[35],16),
                "dst": (int(self.bcode[36],16)<<8)+int(self.bcode[37],16)
            }
            self.frameLength=len(self.bcode)
            self.tcpOrUdp="TCP" if self.bcode[23]=="06" else "UDP"
            # self.bytecode=bcode_arr

    def __str__(self):
        # print(" ".join(self.bcode))
        if(self.isIPV4):
            returnString="Protocol: "+self.tcpOrUdp+"\n"
            returnString+="MAC Address:\n"
            returnString+="\tSource: "+self.macAddress['src']+"\n"
            returnString+="\tDestination: "+self.macAddress['dst']+"\n"
            returnString+="IP Address:\n"
            returnString+="\tSource: "+self.ipAddress['src']+"\n"
            returnString+="\tDestination: "+self.ipAddress['dst']+"\n"
            returnString+="Ports:\n"
            returnString+="\tSource: "+str(self.portNum['src'])+"\n"
            returnString+="\tDestination: "+str(self.portNum['dst'])
            return returnString
        else:
            return "IP Packet is IPv6, which is not supported..."
    
    def accessControlManager(self,rule):
        flag=True
        if(rule["ptsrc"]!="any"):
            if(int(rule["ptsrc"])!=self.portNum["src"]) :
                flag=False
        #print(flag)
        if(rule["ptdst"]!="any"):
            if(int(rule["ptdst"])!=self.portNum["dst"]) :
                flag=False
        
        if(rule["ipsrc"]!="any"):
            lis = rule["ipsrc"].split('.')
            lis2 = self.ipAddress['src'].split('.')
            flg=True
            for i in range(len(lis)) :
                if(lis[i]=='*') :
                    break
                else :
                    if(lis[i]==lis2[i]) :
                        continue
                    else :
                        flg=False
                        break
            if(flg==False) :
                flag=False
        #print(flag)
        if(rule["ipdst"]!="any"):
            lis = rule["ipdst"].split('.')
            lis2 = self.ipAddress['dst'].split('.')
            flg=True
            for i in range(len(lis)) :
                if(lis[i]=='*') :
                    break
                else :
                    if(lis[i]==lis2[i]) :
                        continue
                    else :
                        flg=False
                        break
            if(flg==False) :
                flag=False
        
        if(flag==False and rule["action"]=="deny") :
            flag = True
        elif(flag==True and rule["action"]=="deny") :
            flag=False
        return flag

