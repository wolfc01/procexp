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

TIMEOUT=10
TIMEOUTIDX=1
COUNTIDX=0
TOTALIDX=3
BYTESPERSECONDIDX=2

q = Queue.Queue()
_g_prevTime = None 
_g_started = False
_g_fifo = None
connections = {}

def readFifo():
  """read fifo containing tcdump results"""
  global connections
  fifo = open(_g_fifo, "r")
  while True:
    msg = fifo.readline()
    if msg.find("UDP") == -1:
      try:
        nfbytes = int(msg[msg.rfind(" "):])
        msg = msg[3:msg.rfind(":")]
      
        if connections.has_key(msg):
          connections[msg][COUNTIDX] += nfbytes+64
          connections[msg][TOTALIDX] += nfbytes+64
          connections[msg][TIMEOUTIDX] = TIMEOUT
        else:
          connections[msg] = [nfbytes, TIMEOUT, 0, 0]
      except ValueError:
        pass  
  
def start():
  """start measuring"""
  global _g_fifo
  global _g_started
  if _g_started == False:
    _g_fifo = "/tmp/procexp_"+str(uuid.uuid4())
    os.mkfifo(_g_fifo)
    rootproxy.doContinuousCommand(["tcpdump", "-U" , "-l", "-q", "-nn", "-t", "-i",  "any"], _g_fifo)
    _g_started = True
    t = threading.Thread(target=readFifo)
    t.daemon = True    
    t.start()
  
def started():
  return _g_started
  
def stop():
  """stop"""
  global _g_fifo
  _g_started = False
  if _g_fifo:
    rootproxy.stopContinuousCommand(_g_fifo)
    os.remove(_g_fifo)
  
def tick():
  global _g_prevTime
  global connections
  if _g_prevTime is None:
    _g_prevTime = datetime.datetime.now()
  else:
    now = datetime.datetime.now()
    delta = now - _g_prevTime
    _g_prevTime = now
    deltasecs = delta.seconds + delta.microseconds*1.0 / 1000000.0
    todelete = []
    for conn in connections:
      if connections[conn][TIMEOUTIDX] == 0:
        todelete.append(conn)
      else:
        connections[conn][TIMEOUTIDX] -= 1
        connections[conn][BYTESPERSECONDIDX] = int(connections[conn][COUNTIDX]*1.0 / deltasecs)
        connections[conn][COUNTIDX] = 0 
    for conn in todelete:
      connections.pop(conn)

