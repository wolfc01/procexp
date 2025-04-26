#!/usr/bin/python3

#
# This process runs as root and gets all commands from the ptoc fifo
#
import sys
import subprocess
import const
import os
import traceback

os.mkfifo(sys.argv[1], 0o666) #ParentToChild
os.mkfifo(sys.argv[2], 0o666) #ChildTOParent

os.chmod(sys.argv[1], 0o666)
os.chmod(sys.argv[2], 0o666)

ptoc_fifo = open(sys.argv[1], "r")
ctop_fifo = open(sys.argv[2], "w")

def _write(f, data):
  """write to FIFO"""
  f.write(data+"\n")
  f.flush()

processes = {}

while True:
  data = ptoc_fifo.readline()
  if data == "":
    break
  subprocesscommand = eval(data)
  if subprocesscommand[0] == const.Command.END:
    #end all processing
    break 
  elif subprocesscommand[0] == const.Command.COMMAND:
    #execute command, and return result immediately
    try: 
      result = (const.Result.OK, subprocess.check_output(subprocesscommand[1]))
    except subprocess.CalledProcessError as e:
      result = (const.Result.FAIL, e.output)
    _write(ctop_fifo, repr(result))
  elif subprocesscommand[0] == const.Command.CONTINUE:
    # start process and 
    # create fifo and from given fifo file name
    # then output to given existing fifo
    os.mkfifo(subprocesscommand[2], 0o666) #ParentToChild
    os.chmod(subprocesscommand[2], 0o666)
    f = open(subprocesscommand[2], "w")
    processes[subprocesscommand[2]] = subprocess.Popen(subprocesscommand[1], stdout=f)
  elif subprocesscommand[0] == const.Command.LISTDIR:
    try:
      result = os.listdir(subprocesscommand[1])
      _write(ctop_fifo, repr((const.Result.OK, result)))
    except PermissionError:
      _write(ctop_fifo, repr((const.Result.OK, [])))
    except:
      tb = traceback.format_exc()
      _write(ctop_fifo, repr((const.Result.FAIL, tb)))
  elif subprocesscommand[0] == const.Command.READLINK:
    try:
      result = os.readlink(subprocesscommand[1])
      _write(ctop_fifo, repr((const.Result.OK, result)))
    except:
      tb = traceback.format_exc()
      _write(ctop_fifo, repr((const.Result.FAIL, tb)))
  elif subprocesscommand[0] == const.Command.STOP:
    #start process and output to given existing fifo
    processes[subprocesscommand[1]].kill()
    processes[subprocesscommand[1]].wait()
    os.remove(subprocesscommand[1])
    
os.remove(sys.argv[1])  
os.remove(sys.argv[2])  
 
for proc in processes:
  try:
    processes[proc].kill()
  except OSError:
    pass 