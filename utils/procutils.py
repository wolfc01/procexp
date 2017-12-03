# This file is part of the Linux Process Explorer
# See www.sourceforge.net/projects/procexp
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA


import os
import signal
import ctypes
import traceback
import Queue
logQueue = Queue.Queue()
import sys
import PyQt4.QtGui
import threading
import socket

_ipResolver = None

def message(msg):
  errorbox = PyQt4.QtGui.QMessageBox()
  errorbox.setText(msg)
  errorbox.exec_()
  

def logUnhandledException(exc_type, exc_value, exc_traceback):
  """log an unhandled exception"""

  filename, line, dummy, dummy = \
    traceback.extract_tb(exc_traceback).pop()
  filename = os.path.basename(filename)
  error = "%s: %s" % (str(exc_type).split(".")[-1], exc_value)
  msg = error + " on line %d, file %s" % (line, filename) 
  errorbox = PyQt4.QtGui.QMessageBox()
  errorbox.setText("Unhandled exception:\n"+msg)
  errorbox.exec_()
  file("/tmp/procexp.log","ab").write(msg+"\n")
  
sys.excepthook = logUnhandledException

def log(msg):
  """put a log message into the queue"""
  logQueue.put(msg)

def getLog():
  #get almost all logs
  ret_s = ""
  while not logQueue.empty():
    ret_s += logQueue.get(block=False) + "\n"
  return ret_s


lib = ctypes.cdll.LoadLibrary("libc.so.6")
BLOCKSIZE=4096
s = ctypes.create_string_buffer('\000' * BLOCKSIZE)

class FileError(Exception):
  pass

def readFullFileFast(path):
  
  try:
    f = lib.open(path,0)
    if f == -1: raise FileError    
      
    total = ""
      
    eof = lib.read(f, s, BLOCKSIZE)
    if eof == -1: raise FileError
    if eof > 0:
      total = total + s.raw[:eof]
      if eof < BLOCKSIZE:
        lib.close(f)
        return total

    while eof > 0:
      eof = lib.read(f, s, BLOCKSIZE)
      print " ",eof, path
      if eof == -1: raise FileError
      if eof > 0:
        total = total + s.raw[:eof]
 
    lib.close(f)
    return total
  except FileError:
    lib.close(f)
    raise
  
  except:
    log("Unhandled exception: %s" % traceback.format_exc())
    raise
    
def readFullFile(path):
  return readFullFileFast(path)

def killProcess(process):
  try:
    os.kill(int(process), signal.SIGTERM)
  except OSError:
    pass
  
def killProcessHard(process):
  os.kill(int(process), signal.SIGKILL)


def humanReadable(value):
  if value < 1000:
    return "%s B" %str(value)
  elif value >= 1024 and value < 1024*1024:
    return "%4.1f kB" %float(value*1.0/1024.0)
  else:
    return "%4.1f MB" %float(value*1.0/(1024.0*1024.0))


class IpResolver(object):
  """resolve IP numbers, threaded."""
  def __init__(self):
    """init"""
    self._maxResolvers = 20
    self._nrResolvers = 0
    self._resolvedTable = {}
    
  def _doRsolve(self, ip):
    """resolve the given IP"""
    try:
      name = socket.gethostbyaddr(ip)[0]
    except socket.herror:
      #host could not be resolved
      name = ip
    self._resolvedTable[ip] = name
    self._nrResolvers -= 1
    
  def resolveIP(self, ip):
    """resolve IP number"""
    if self._resolvedTable.has_key(ip):
      return self._resolvedTable[ip]
    else:
      if self._nrResolvers < self._maxResolvers:
        self._nrResolvers += 1
        t = threading.Thread(target=self._doRsolve, args=(ip,))
        t.start()
      #because the resolver is working we return the IP for now.
      #hopefully the next request the resolver will have done its job.
      return ip
    
def resolveIP(ip):
  """resolve IP, multithreaded"""
  global _ipResolver
  if _ipResolver is None:
    _ipResolver = IpResolver()     
  return _ipResolver.resolveIP(ip)











