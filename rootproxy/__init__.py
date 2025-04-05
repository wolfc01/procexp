"""root proxy"""

import subprocess
import os
import time
import uuid
from rootproxy import const

rootProxySingleton = None

class CommandException(Exception):
  """exception raised when command has failed"""
  pass

def _write(f, data):
  """write to FIFO"""
  f.write(repr(data)+"\n")
  f.flush()

class rootProxyObject:
  def __init__(self, asRoot=True):
    self._ptoc_file = None
    self._ctop_file = None
    self._ptoc_filename = "/tmp/ptoc"+str(uuid.uuid4()) #ParentTOChild
    self._ctop_filename = "/tmp/ctop"+str(uuid.uuid4()) #ChildTOParent
    self._procroot = None
    self.started = None
          
    if asRoot:
      thisFile = __file__
      thisFile = thisFile.replace(".pyc", ".py")
      self._procroot = subprocess.Popen(["pkexec", thisFile.replace("__init__", "procroot"), self._ptoc_filename, self._ctop_filename])
    else:
      self._procroot = subprocess.Popen([os.path.abspath(__file__).replace("__init__", "procroot"), self._ptoc_filename, self._ctop_filename])

    while True:
      try:
        os.close(os.open(self._ptoc_filename, flags= os.O_WRONLY)) #does file exist?
        self._ptoc_file = open(self._ptoc_filename, "w")
        break
      except IOError:
        time.sleep(0.1)
    while True:
      try:
        self._ctop_file = open(self._ctop_filename, "r")
        break
      except IOError:
        time.sleep(0.1)
    self.started = True
  
  def doCommand(self, CommandAndArgList):
    _write(self._ptoc_file, (const.Command.COMMAND, CommandAndArgList))
    result = eval(self._ctop_file.readline())
    if result[0] == const.Result.FAIL:
      raise CommandException
    else:
      return result[1]

  def doListDir(self, arg):
    _write(self._ptoc_file, (const.Command.LISTDIR, arg))
    _data = self._ctop_file.readline()
    result = eval(_data)
    if result[0] == const.Result.FAIL:
      raise CommandException
    else:
      return result[1]

  def doReadlink(self, arg):
    _write(self._ptoc_file, (const.Command.READLINK, arg))
    result = eval(self._ctop_file.readline())
    if result[0] == const.Result.FAIL:
      raise CommandException
    else:
      return result[1]

  def doContinuousCommand(self, CommandAndArgList, outputFifo):
    """execute command with stdout output to the outputFifo file name. 
      The given command keeps running."""
    _write(self._ptoc_file, (const.Command.CONTINUE, CommandAndArgList, outputFifo))

  def stopContinuousCommand(self, outputFifo):
    """stop command writing in fifo outputFifo."""
    _write(self._ptoc_file, (const.Command.STOP, outputFifo))

  def end(self):
    """stop procroot"""      
    _write(self._ptoc_file, (const.Command.END,)) 
    self._procroot.wait()

def isStarted():
  """is procroot running?"""
  if rootProxySingleton is not None:
    return rootProxySingleton.started
  else:
    return False
  
def start(asRoot = True):
  global rootProxySingleton
  """start the command process, possible as root if required"""
  rootProxySingleton = rootProxyObject(asRoot)

def end():
  if rootProxySingleton is not None: 
    rootProxySingleton.end()

def doListDir(arg):
  if isStarted():
    return rootProxySingleton.doListDir(arg)
  else:
    os.listdir(arg)

def doReadlink(arg):
  if isStarted():
    return rootProxySingleton.doReadlink(arg)

def doContinuousCommand(CommandAndArgList, outputFifo):
  if isStarted():
    return rootProxySingleton.doContinuousCommand(CommandAndArgList, outputFifo)

def stopContinuousCommand(outputFifo):
  if isStarted():
    rootProxySingleton.stopContinuousCommand(outputFifo)

def doCommand(CommandAndArgList):
  if isStarted():
    return rootProxySingleton.doCommand(CommandAndArgList)
  