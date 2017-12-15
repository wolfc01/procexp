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

#Here the statistics for tcp connections is calculated. The connections can be
#found in the module dictionary 'connections':
#
# A connection is a dictionary key like:
#      'a1.b1.c1.d1.portnrfrom > a2.b2.c2.d2.portnrto'   # one direction
#      'a1.b1.c1.d1.portnrto > a2.b2.c2.d2.portnrfrom'   # other direction
#
# Thus each connection appears mostly twice, one for each direction.
#
# When for a long TIMEOUT time no packages come in, the corresponding connection is cleared
 
import Queue
import threading
import datetime
import rootproxy
import uuid
import os
import threading
_TIMEOUT=10
_TIMEOUTIDX=1
_COUNTIDX=0
_TOTALIDX=3
BYTESPERSECONDIDX=2

_tcpStatInstance=None

def tcpStat():
  """singleton of tcp statistics reader"""
  global _tcpStatInstance
  if _tcpStatInstance is None:
    _tcpStatInstance = _TcpStat()
  return _tcpStatInstance

class _TcpStat(object):
  """tcp statistics reader"""
  def __init__(self):
    self._prevTime = None 
    self._started = False
    self._fifo = None
    self._connections = {}
    self.connectionsLock = threading.Lock()

  def _readFifo(self):
    """read fifo containing tcdump results"""
    fifo = open(self._fifo, "r")
    while True:
      msg = fifo.readline()
      if msg.startswith("IP") and msg.find(" tcp ") != -1: #thus also contains ipv6 connections
        try:
          nfbytes = int(msg[msg.rfind(" "):])
          conn = msg[msg.find(" ")+1:msg.find(": tcp")]
          with self.connectionsLock:
            if self._connections.has_key(conn):
              self._connections[conn][_COUNTIDX] += nfbytes+64
              self._connections[conn][_TOTALIDX] += nfbytes+64
              self._connections[conn][_TIMEOUTIDX] = _TIMEOUT
            else:
              self._connections[conn] = [nfbytes, _TIMEOUT, 0, 0]
        except ValueError:
          pass  
  
  def connections(self):
    """connections"""
    return self._connections

  def start(self):
    """start measuring"""
    if self._started == False:
      self._fifo = "/tmp/procexp_"+str(uuid.uuid4())
      os.mkfifo(self._fifo)
      rootproxy.doContinuousCommand(["tcpdump", "-U" , "-l", "-q", "-nn", "-t", "-i",  "any"], self._fifo)
      self._started = True
      t = threading.Thread(target=self._readFifo)
      t.daemon = True    
      t.start()
  
  def started(self):
    return self._started
  
  def stop(self):
    """stop"""
    self._started = False
    if self._fifo:
      rootproxy.stopContinuousCommand(self._fifo)
      os.remove(self._fifo)
  
  def tick(self):
    if self._prevTime is None:
      self._prevTime = datetime.datetime.now()
    else:
      now = datetime.datetime.now()
      delta = now - self._prevTime
      self._prevTime = now
      deltasecs = delta.seconds + delta.microseconds*1.0 / 1000000.0
      todelete = []
      with self.connectionsLock:
        for conn in self._connections:
          if self._connections[conn][_TIMEOUTIDX] == 0:
            todelete.append(conn)
          else:
            self._connections[conn][_TIMEOUTIDX] -= 1
            self._connections[conn][BYTESPERSECONDIDX] = int(self._connections[conn][_COUNTIDX]*1.0 / deltasecs)
            self._connections[conn][_COUNTIDX] = 0 
        for conn in todelete:
          self._connections.pop(conn)