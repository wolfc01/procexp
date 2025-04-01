# process explorer for Linux

The Linux Process Explorer aims to be a Linux equivalent of  (https://docs.microsoft.com/en-us/sysinternals/downloads/process-explorer). This project is a continuation of my project located at https://sourceforge.net/projects/procexp/. 

Goals of this project
1. Revive the old code, refactor and complete functionality
2. Pack it for Debian, Ubuntu, Redhat, Fedora and Mint
3. Make the process explorer a standard component of above mentioned distro's
4. Everything else which will be needed

## INSTALLATION
download procexp from https://github.com/wolfc01/procexp/archive/refs/heads/master.zip 

### ubuntu 24.04.2
as root:
  apt update
  apt install pip
  apt install python3-venv
  apt install tcpdump

as normal user:
  cd ~
  python3 -m venv ~/procexp
  unzip procexp-master.zip 
  cd procexp-master
  ~/procexp/bin/pip install -r requirements.txt


### Debian 12.10 (QSocket problem, does not run)
as root: 
  apt update
  apt install pip
  apt install python3-venv
  apt install tcpdump

as normal user:
  cd ~
  python3 -m venv ~/procexp
  unzip procexp-master.zip 
  cd procexp-master
  ~/procexp/bin/pip install -r requirements.txt

### last step for all distro's: 
_as a non root user_ :

```
if on wayland:
export QT_QPA_PLATFORM=wayland
cd procexp-master
~/procexp/bin/python3 ./procexp.py
```
