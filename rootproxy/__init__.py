"""root proxy"""

import subprocess
import os
import time
import uuid
import rootproxy.const

ptoc_file = None
ctop_file = None
procroot = None
ptoc_filename = None
ctop_filename = None
started = False

class CommandException(Exception):
  """exception raised when command has failed"""
  pass

def _write(f, data):
  """write to FIFO"""
  f.write(repr(data)+"\n")
  f.flush()

def isStarted():
  """is procroot running?"""
  return started
  
def start(asRoot = True):
  """start the command process, possible as root if required"""
  global ptoc_file
  global ctop_file
  global ptoc_filename
  global ctop_filename
  global procroot
  global started
  
  ptoc_filename = "/tmp/ptoc"+str(uuid.uuid4()) #ParentTOChild
  ctop_filename = "/tmp/ctop"+str(uuid.uuid4()) #ChildTOParent
    
  if asRoot:
    thisFile = __file__
    thisFile = thisFile.replace(".pyc", ".py")
    procroot = subprocess.Popen(["pkexec", thisFile.replace("__init__", "procroot"), ptoc_filename, ctop_filename])
  else:
    procroot = subprocess.Popen([os.path.abspath(__file__).replace("__init__", "procroot"), ptoc_filename, ctop_filename])

  while True:
    try:
      os.close(os.open(ptoc_filename, flags= os.O_WRONLY)) #does file exist?
      ptoc_file = open(ptoc_filename, "w")
      break
    except IOError:
      import traceback
      time.sleep(0.1)
  while True:
    try:
      ctop_file = open(ctop_filename, "r")
      break
    except IOError:
      time.sleep(0.1)
  started = True

def doCommand(CommandAndArgList):
  """issue command to procroot process and get the result"""
  if started:
    global ptoc_file
    global ctop_file
    _write(ptoc_file, (const.Command.COMMAND, CommandAndArgList))
    result = eval(ctop_file.readline())
    if result[0] == const.Result.FAIL:
      raise CommandException
    else:
      return result[1]

def doListDir(arg):
  if started:
    global ptoc_file
    global ctop_file
    _write(ptoc_file, (const.Command.LISTDIR, arg))
    _data = ctop_file.readline()
    print(_data)
    result = eval(_data)
    if result[0] == const.Result.FAIL:
      raise CommandException
    else:
      return result[1]
  else:
    return os.listdir(arg)
  return

def doReadlink(arg):
  if started:
    global ptoc_file
    global ctop_file
    _write(ptoc_file, (const.Command.READLINK, arg))
    result = eval(ctop_file.readline())
    if result[0] == const.Result.FAIL:
      raise CommandException
    else:
      return result[1]
  else:
    return os.readlink(arg)
  return

def doContinuousCommand(CommandAndArgList, outputFifo):
  """execute command with stdout output to the outputFifo file name. 
     The given command keeps running."""
  global ptoc_file
  if started:
    _write(ptoc_file, (const.Command.CONTINUE, CommandAndArgList, outputFifo))

def stopContinuousCommand(outputFifo):
  """stop command writing in fifo outputFifo."""
  global ptoc_file
  if started:
    _write(ptoc_file, (const.Command.STOP, outputFifo))

def end():
  """stop procroot"""
  if started:
    global ptoc_file
    global ptoc_filename
    global ctop_filename
    
    _write(ptoc_file, (const.Command.END,)) 
    procroot.wait()

