# process explorer for Linux

This tool is a 'swiss army knife' for programmers and system administrators to study per process memory usage, IO usage, runtime memory leaks, TCP/UDP usage, and also process hierarchy.

The Linux Process Explorer was inspired by the sysinternals process explorer tool of Microsoft.  (https://docs.microsoft.com/en-us/sysinternals/downloads/process-explorer). 

## INSTALLATION
for now download the bleeding edge: procexp from https://github.com/wolfc01/procexp/archive/refs/heads/master.zip 

### ubuntu 24.04.2, mint 22.1
```
sudo apt update
sudo apt install pip
sudo apt install python3-venv
sudo apt install tcpdump
```
### debian 12.10 (as root)
```
apt update
apt install pip
apt install python3-venv
apt install tcpdump
```
### fedora workstation 41 (as root)
```
dnf install python3-pip
```
#### then for all distro's, as normal user:
```
cd ~
python3 -m venv ~/procexp
unzip procexp-master.zip 
cd procexp-master
~/procexp/bin/pip install -r requirements.txt
```
## start process explorer: 
_as a non root user_ :

if on wayland:
```
export QT_QPA_PLATFORM=wayland
```

then start the process explorer as follows:
```
cd procexp-master
~/procexp/bin/python3 ./procexp.py
```