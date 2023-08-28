import psutil,subprocess,re,random
import scapy.all as scapy

class CollectData:
    def __init__(self):
        pass

    #check if interface is available
    def  check_interface_available(self,iface):
        all_interfaces = []
        interface_available = False
        interfaces = psutil.net_if_addrs()
        for interface,addrs in interfaces.items():
            all_interfaces.append(interface)
        for interface in all_interfaces:
            if interface == iface:
                interface_available = True
        return interface_available
                

        


    #gets ip of interface
    def get_Interface_ip(self,iface):
        iface_ip = None
        interfaces = psutil.net_if_addrs()
        for interface,addrs in interfaces.items():
            if interface==iface:
                ip = addrs[0].address
                iface_ip = ip
                break
        return iface_ip

    #get subnet of interface ip
    def get_subnet_ip(self,iface):
        ip = self.get_Interface_ip(iface)
        subnet_mask = "255.255.255.0"
        ip_parts = [int(part) for part in ip.split('.')]
        subnet_parts = [int(part) for part in subnet_mask.split('.')]
        network_parts = [ip_parts[i] & subnet_parts[i] for i in range(4)]
        network_ip = '.'.join(map(str, network_parts))
        return network_ip

    #get default gateway ip of interface
    def get_default_gateway_ip(self,iface):
        try:
            result = subprocess.check_output(['ip', 'route', 'show', 'default', 'dev', iface]).decode('utf-8')
            gateway = result.split(' ')[2]
            return gateway
        except subprocess.CalledProcessError:
            return None
        except IndexError:
            return None

    #get default gateway mac of interface
    def get_default_gateway_mac(self,iface):
        gatewayMac =None
        if(self.check_interface_available(iface)==True):
            gateway_ip = self.get_default_gateway_ip(iface)
            subnet = self.get_subnet_ip(iface)+"/24"
            arp_request = scapy.ARP(pdst = subnet)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast/arp_request
            answered_list = scapy.srp(arp_request_broadcast,timeout=1,verbose=0)[0]
            for target in answered_list:
                if target[1].psrc == gateway_ip:
                    gatewayMac = target[1].hwsrc
                    break
        
        return gatewayMac

    #scan all targets in network
    def scanNetwork(self,iface):
        all_targets =[]
        if(self.check_interface_available(iface)==True):
            gateway_ip = self.get_default_gateway_ip(iface)
            subnet = self.get_subnet_ip(iface)+"/24"
            arp_request = scapy.ARP(pdst = subnet)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast/arp_request
            answered_list = scapy.srp(arp_request_broadcast,timeout=1,verbose=0)[0]
            all_targets.append({"ip":answered_list[0][1].pdst,"mac":answered_list[0][1].hwdst,"you":True,"selected":False})
            for target in answered_list:
                targetObject = {"ip":target[1].psrc,"mac":target[1].hwsrc,"you":False,"selected":False}
                all_targets.append(targetObject)
        return all_targets
        
    
    #check if target is available on network
    def check_target_available(self,iface,targetIP):
        available = False
        targets = self.scanNetwork(iface)
        for target in targets:
            if target["ip"] == targetIP:
                available =True
                break
        return available

    #get target MAC address
    def get_target_mac_address(self,iface,targetIP):
        target_mac = None
        targets = self.scanNetwork(iface)
        target_available = self.check_target_available(iface, targetIP)
        if(target_available == True):
            for target in targets:
                if target["ip"] == targetIP:
                    target_mac = target["mac"]
                    break
        return target_mac

    #validate mac address format (for mac spoofing)
    def vallidate_mac_address(self,mac):
        pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        return re.match(pattern, mac)is not None

    #validate ip address (when user entering target ip address)
    def validate_ip_address(self,ip):
        pattern = r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return re.match(pattern, ip)is not None

    #generate random mac address (for mac spoofer)
    def generate_random_mac_address(self):
        mac_bytes = [random.randint(0x00, 0xff) for _ in range(6)]
        mac_address = ':'.join(format(byte, '02x') for byte in mac_bytes)
        return mac_address





                

            






    



                
        

