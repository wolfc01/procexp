# Process Explorer for Linux

This tool is a 'swiss army knife' for programmers and system administrators to study per-process memory usage, IO usage, runtime memory leaks, TCP/UDP usage, and also process hierarchy.

The Linux Process Explorer was inspired by [the Sysinternals Process Explorer tool by Microsoft](https://docs.microsoft.com/en-us/sysinternals/downloads/process-explorer).

## INSTALLATION

For now, download the bleeding edge: `procexp` from https://github.com/wolfc01/procexp/archive/refs/heads/master.zip 

### Ubuntu 24.04.2, Mint 22.1

```sh
sudo apt update
sudo apt install pip
sudo apt install python3-venv
sudo apt install tcpdump
```

#### Then:

```sh
cd ~
python3 -m venv ~/procexp
unzip procexp-master.zip 
cd procexp-master
~/procexp/bin/pip install -r requirements.txt
```

## start process explorer: 

_As a non root user:_

If on wayland:

```sh
export QT_QPA_PLATFORM=wayland
```

Then, start the process explorer as follows:

```sh
cd procexp-master
~/procexp/bin/python3 ./procexp.py
```

## UNINSTALL

For packages `pip`, `python3-venv` and `tcpdump`: those are standard packages, and can be removed using their uninstall instructions. For process explorer removal, remove `~/procexp` and `~/procexp-master`. Then your system is clean from all `procexp` traces.
