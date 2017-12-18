# procexp
Process explorer for linux


The Linux Process Explorer aims to be a Linux equivalent of  (https://docs.microsoft.com/en-us/sysinternals/downloads/process-explorer). This project is a continuation of my project located at https://sourceforge.net/projects/procexp/. 

Goals of this project
1. Revive the old code, refactor and complete functionality
2. Pack it for Debian, Ubuntu, Redhat, Fedora and Mint
3. Make the process explorer a standard component of above mentioned distro's
4. Everything else which will be needed

# INSTALLATION

- *Ubuntu 16.04.3 LTS*

### install dependencies

```
apt-get install python-qwt5-qt4
apt-get install python-configobj
```

### download and install

download procexp from github as zip file from https://github.com/wolfc01/procexp/archive/master.zip

```
unzip master.zip
cd procexp-master
./procexp.py
```

