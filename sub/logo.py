import os
from colorama import Fore
class Logo:
    def __init__(self):
        self.gr = Fore.LIGHTBLACK_EX
        self.yl = Fore.YELLOW
        self.wh = Fore.WHITE


    def logo(self):
        os.system("clear")
        print(f"""      
{self.gr}
██   ██  █████  ██████  ███    ███ ███████ {self.yl}██     ██  █████  ██    ██{self.gr} 
██   ██ ██   ██ ██   ██ ████  ████ ██      {self.yl}██     ██ ██   ██  ██  ██ {self.gr} 
███████ ███████ ██████  ██ ████ ██ ███████ {self.yl}██  █  ██ ███████   ████   {self.gr}
██   ██ ██   ██ ██   ██ ██  ██  ██      ██ {self.yl}██ ███ ██ ██   ██    ██    {self.gr}
██   ██ ██   ██ ██   ██ ██      ██ ███████  {self.yl}███ ███  ██   ██    ██    {self.wh}
        """)
