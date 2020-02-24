# process explorer for Linux

The Linux Process Explorer aims to be a Linux equivalent of  (https://docs.microsoft.com/en-us/sysinternals/downloads/process-explorer). This project is a continuation of my project located at https://sourceforge.net/projects/procexp/. 

Goals of this project
1. Revive the old code, refactor and complete functionality
2. Pack it for Debian, Ubuntu, Redhat, Fedora and Mint
3. Make the process explorer a standard component of above mentioned distro's
4. Everything else which will be needed

## INSTALLATION
### install dependencies for Ubuntu 16.04.3 LTS, Mint 18.3
_as user root_:
```
apt-get install python-qwt5-qt4 python-configobj
```
### install dependencies for Debian 9
_as user root_:
```
apt-get install python-qwt5-qt4 python-configobj tcpdump
```
### install dependencies for Fedora 27
_as user root_:
```
yum install PyQwt
yum install python-configobj
```
### install dependencies for CentOS 7

for CentOS version 7 PyQwt is not available in standard and EPEL repositories: --> build from source
Download PyQwt5 sources from https://kent.dl.sourceforge.net/project/pyqwt/pyqwt5/PyQwt-5.2.0/PyQwt-5.2.0.tar.gz

_as user root_:
```
yum install epel-release
sudo yum group install "Development Tools"
yum install PyQt4-devel
yum install qwt
yum install qwt-devel
tar -xvzf PyQwt-5.2.0/PyQwt-5.2.0.tar.gz
cd PyQwt-5.2.0/configure
python configure.py -Q ../qwt-5.2
make
make install
```
### last step for all distro's: download procexp python sources, unzip and run
_as a non root user_ :

download procexp from github as zip file from https://github.com/wolfc01/procexp/archive/master.zip
```
unzip master.zip
cd procexp-master
./procexp.py
```
