import os
import sys
import subprocess as sub
import time
import tkinter as tk
from tkinter import ttk
from threading import Thread 

# Try importing required libraries; install them if missing
try:
    import requests
    from PIL import Image, ImageTk
except:
    os.system("python3 -m pip install requests")
    os.system("python3 -m pip install requests[socks]")
    os.system("python3 -m pip install pillow")
    import requests
    from PIL import Image, ImageTk

# Check if script is run as root
if not os.geteuid() == 0:
    print("Please run this tool with root privileges.")
    sys.exit()


class Main:
    """Handles TOR installation, status checking, and IP change."""

    def __init__(self):
        self.status = False  # TOR running status
        if not self.check_tor():
            self.install_tor()

    def check_tor(self):
        """Check if TOR is installed."""
        try:
            sub.check_output("which tor", shell=True)
            return True
        except sub.CalledProcessError:
            return False

    def install_tor(self):
        """Install TOR if not installed."""
        os.system("sudo apt update")
        os.system("sudo apt install tor -y")

    def start_tor(self):
        """Start the TOR service."""
        os.system("service tor start")
        self.status = True
        cmd = f"notify-send -i /home/kali/Pictures/v.png 'TOR_SSC2025' 'Tor started!'"
        os.system(cmd)

    def stop_tor(self):
        """Stop the TOR service."""
        os.system("service tor stop")
        self.status = False
        cmd = f"notify-send -i /home/kali/Pictures/v.png 'TOR_SSC2025' 'Tor Stoped!'"
        os.system(cmd)

    def change_ip(self):
        """Reload TOR to change IP."""
        os.system("service tor reload")

    def my_ip(self):
        """Get current public IP using TOR network."""
        url = "http://checkip.amazonaws.com"
        proxies = {"http": "socks5://127.0.0.1:9050", "https": "socks5://127.0.0.1:9050"}
        try:
        	ip = requests.get(url, proxies=proxies)
        except :
        	ip = requests.get(url)
        return ip.text.strip()


class Driver(Main):
    """Controls TOR IP changing and status notification."""

    def __init__(self):
        super().__init__()
        self.running = True
        self.timeout = 3 
        

    def start(self):
        """Start TOR and continuously change IP."""
        self.show_status()
        self.start_tor()
        time.sleep(5)  # Wait for TOR to start
        while self.running:
            self.change_ip()
            time.sleep(self.timeout)

    def show_ip(self):
        """Display current IP in a notification."""
        ip = self.my_ip()
        cmd = f"notify-send -i /home/kali/Pictures/v.png 'TOR_SSC2025' 'Your IP is: {ip}'"
        os.system(cmd)

    def show_status(self):
        """Show TOR status in a notification."""
        if not self.status:
            text = "TOR_SSC2025 is NOT running! \nYou are NOT under the TOR network!"
        else:
            text = "TOR_SSC2025 is running! \nYou are under the TOR network!"
        cmd = f"notify-send -e -i /home/kali/Pictures/v.png 'TOR_SSC2025' '{text}'"
        os.system(cmd)

    def stop(self):
        """Stop IP rotation."""
        self.running = False
        self.stop_tor()


class Gui(tk.Tk):
    """Graphical User Interface using Tkinter."""

    def __init__(self):
        super().__init__()
        self.driver = Driver()
        #self.geometry("300x250")
        self.title("TOR Control Panel")

        # Set theme
        self.style = ttk.Style()
        if os.path.exists("./name.th"):
        	with open("./name.th" ) as f:
        		self.name = f.read()
        		
        else:
        	self.name = "clam"
        self.style.theme_use(self.name)
	
        # Image path
        self.image_path = "/home/kali/Pictures/v.png"

        # Create UI elements
        self.create_all()

    def create_all(self):
        """Create UI elements (Frames, Buttons, Labels)."""

        # Main container frame
        self.div1 = ttk.Frame(self, relief="solid", borderwidth=2)
        self.div1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.div2 = ttk.Frame(self)
        self.div2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Sub-frames inside div1
        self.indiv1 = ttk.Frame(self.div1, relief="solid", borderwidth=1)
        self.indiv1.grid(row=0, column=0, padx=5, pady=5)

        self.indiv2 = ttk.Frame(self.div1, relief="solid", borderwidth=1)
        self.indiv2.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.indiv2 , text="TOR_SSC2025").grid(row = 1 , column=1 , pady=5 , padx = 5)
        ttk.Label(self.indiv2 , text="Be Anonymus Over Internet!").grid(row = 2 , column=1 , pady=5 , padx = 5)
        
	
	
	
        # Load & Resize Image
        image = Image.open(self.image_path)
        image = image.resize((80, 80))
        self.tk_image = ImageTk.PhotoImage(image)

        # Image Label
        self.image_label = ttk.Label(self.indiv1, image=self.tk_image)
        self.image_label.grid(row=1, column=0,  pady=2)
        
        ttk.Label(self.div2, text = "Interval (s): " , ).grid(row = 1 , column = 1 ) 
        
        self.timeoutbox = ttk.Spinbox(self.div2 , from_=1 , to = 100000  )
        self.timeoutbox.grid(row = 1 , column = 2 ,pady = 4 ) 
        self.timeoutbox.set(3)
        
        
        ttk.Label(self.div2, text = "Theme: " , ).grid(row = 2 , column = 1 ) 
        self.themebox = ttk.Combobox(self.div2 , values=self.style.theme_names())
        self.themebox.grid(row=2 , column = 2 , columnspan = 2 , padx=3 , pady=3)
        self.themebox.set(self.name) 
        self.themebox.bind("<<ComboboxSelected>>" , self.applytheme)
        
        self.togglebutton = ttk.Button(self.div2 , text = 'start' , command=self.togglestart )
        self.togglebutton.grid(row=4 , column = 1, pady=3 , padx = 2  , ) 
        
        
        ttk.Button(self.div2 , text = 'Status',command = self.driver.show_status).grid(row=4 , column = 2 , pady = 2 , padx = 2 )
        
        ttk.Button(self.div2 , text ="My IP" , command = self.driver.show_ip).grid(row=5 , column = 2 , pady=3 , padx = 3 )
        
        ttk.Button(self.div2 , text ="Hide Window" , command = self.destroy).grid(row=5 , column = 1 , pady=3 , padx = 3 )
        
    def applytheme(self, *g):
        name = self.themebox.get()
        self.style.theme_use(name) 
        with open("./name.th", 'w' ) as f:
        	f.write(name) 
        
    def togglestart(self , *r) :
        if not self.driver.status:
        	self.driver.timeout = int(self.timeoutbox.get())
        	self.driver.running = True
        	self.timeoutbox.configure(state='disabled' ) 
        	t = Thread(target=self.driver.start)
        	t.daemon = True 
        	t.start() 
        	self.togglebutton.configure(text = "Stop" ,) 
        	
        else :
        	self.driver.stop()
        	self.togglebutton.configure(text = "Start" ,) 
        	self.timeoutbox.configure(state='normal' ) 
	

if __name__ == "__main__":
    g = Gui()
    g.mainloop()
