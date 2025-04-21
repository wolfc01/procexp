# Process Explorer for Linux

This tool is a 'swiss army knife' for programmers and system administrators to study per-process memory usage, IO usage, runtime memory leaks, TCP/UDP usage, and also process hierarchy.

The Linux Process Explorer was inspired by [the Sysinternals Process Explorer tool by Microsoft](https://docs.microsoft.com/en-us/sysinternals/downloads/process-explorer).

## INSTALLATION

For now, download the bleeding edge: `procexp` from https://github.com/wolfc01/procexp/archive/refs/heads/master.zip 

### Ubuntu 24.04.2, Mint 22.1

1. ```sh
   #!/usr/bin/env sh
   sudo apt update
   sudo apt install pip
   sudo apt install python3-venv
   sudo apt install tcpdump
   sudo apt install libxcb-cursor-dev
   ```

1. ```bash
   #!/usr/bin/env bash
   cd ~
   python3 -m venv ~/procexp
   unzip procexp-master.zip 
   cd procexp-master
   ~/procexp/bin/pip install -r requirements.txt
   ```

### fedora workstation 41
1. ```
   #!/usr/bin/env sh
   sudo dnf install python3-pip
   ```   

## Start Process Explorer: 

_As a non-superuser user:_

1. If on Wayland:

   ```bash
   #!/usr/bin/env bash
   export QT_QPA_PLATFORM=wayland
   ```

1. Then, start the process explorer as follows:

   ```bash
   #!/usr/bin/env bash
   cd procexp-master
   ~/procexp/bin/python3 ./procexp.py
   ```

## UNINSTALL

- For packages `pip`, `python3-venv` and `tcpdump`: those are standard packages, and can be removed using their uninstall instructions.
- For process explorer removal, remove `~/procexp` and `~/procexp-master`. Then your system is clean from all `procexp` traces.
