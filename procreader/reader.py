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


#reader.py
#class which reads data from /proc

import time
import os
import utils.procutils
import singleprocess
import subprocess
import rootproxy
import struct
import socket

UNKNOWN = "---"


class cpuhistoryreader(object):
  def __init__(self, cpu, prefixDir=""):
    self.__cpu__ = cpu
    self.__prevUserMode__ = None
    self.__prevUserNiceMode__ = None
    self.__prevSystemMode__ = None
    self.__prevIdleMode__ = None
    self.__prevIoWait__ = None
    self.__prevIrqMode__ = None
    self.__prevSoftIrqMode__ = None
    self.__deltaUserMode__ = None
    self.__deltaUserMode__ = None
    self.__deltaUserNiceMode__ = None
    self.__deltaSystemMode__ = None
    self.__deltaIdleMode__ = None
    self.__deltaIoWait__ = None
    self.__deltaIrqMode__ = None
    self.__deltaSoftIrqMode__ = None
    self.__newjiffies = None
    self.__overallUserCpuUsage__    = 0
    self.__overallSystemCpuUsage__  = 0
    self.__overallIoWaitCpuUsage__  = 0
    self.__overallIrqCpuUsage__     = 0
    self._prefixdir = prefixDir
    
  def update(self):
    jiffyStr = utils.procutils.readFullFile(self._prefixdir+'/proc/stat').split("\n")[self.__cpu__+1]
    userMode = int(jiffyStr.split()[1])
    userNiceMode = int(jiffyStr.split()[2])
    systemMode = int(jiffyStr.split()[3])
    idleMode = int(jiffyStr.split()[4]) 
    
    ioWait = int(jiffyStr.split()[5])
    irqMode = int(jiffyStr.split()[6])
    softIrqMode = int(jiffyStr.split()[7])
    
    self.__newjiffies = userMode + userNiceMode + systemMode + idleMode + ioWait + irqMode + softIrqMode
     
    if self.__deltaUserMode__ == None:
      self.__prevUserMode__ = userMode
      self.__prevUserNiceMode__ = userNiceMode
      self.__prevSystemMode__ = systemMode
      self.__prevIdleMode__ = idleMode
      self.__prevIoWait__ = ioWait
      self.__prevIrqMode__ = irqMode
      self.__prevSoftIrqMode__ = softIrqMode
      
      self.__deltaUserMode__ = 0
      self.__deltaUserNiceMode__ = 0
      self.__deltaSystemMode__ = 0
      self.__deltaIdleMode__ = 0
      self.__deltaIoWait__ = 0
      self.__deltaIrqMode__ = 0
      self.__deltaSoftIrqMode__ = 0
      
    else:
      self.__deltaUserMode__ = userMode - self.__prevUserMode__
      self.__deltaUserNiceMode__ = userNiceMode - self.__prevUserNiceMode__
      self.__deltaSystemMode__ = systemMode - self.__prevSystemMode__
      self.__deltaIdleMode__ = idleMode - self.__prevIdleMode__
      self.__deltaIoWait__ = ioWait - self.__prevIoWait__
      self.__deltaIrqMode__ = irqMode - self.__prevIrqMode__
      self.__deltaSoftIrqMode__ = softIrqMode - self.__prevSoftIrqMode__
      
      
      self.__prevUserMode__ = userMode
      self.__prevUserNiceMode__ = userNiceMode
      self.__prevSystemMode__ = systemMode
      self.__prevIdleMode__ = idleMode
      self.__prevIoWait__ = ioWait
      self.__prevIrqMode__ = irqMode
      self.__prevSoftIrqMode__ = softIrqMode
      
    
    
    total = float(self.__deltaUserMode__ + 
            self.__deltaUserNiceMode__ + 
            self.__deltaSystemMode__ + 
            self.__deltaIdleMode__ +
            self.__deltaIoWait__ +
            self.__deltaIrqMode__ +
            self.__deltaSoftIrqMode__)
    
    self.__overallUserCpuUsage__    = round(((self.__deltaUserMode__ + self.__deltaUserNiceMode__)*1.0 / total)*100, 1) if total > 0 else 0
    self.__overallSystemCpuUsage__  = round((self.__deltaSystemMode__ *1.0 / total)*100, 1) if total > 0 else 0
    self.__overallIoWaitCpuUsage__  = round((self.__deltaIoWait__*1.0 / total)*100, 1) if total > 0 else 0
    self.__overallIrqCpuUsage__     = round(((self.__deltaIrqMode__ + self.__deltaSoftIrqMode__) *1.0 / total)*100, 1) if total > 0 else 0
      
  def overallUserCpuUsage(self):
    return self.__overallUserCpuUsage__
  def overallSystemCpuUsage(self):
    return self.__overallSystemCpuUsage__
  def overallIoWaitCpuUsage(self):
    return self.__overallIoWaitCpuUsage__
  def overallIrqCpuUsage(self):
    return self.__overallIrqCpuUsage__
  def newjiffies(self):
    return self.__newjiffies
 
class procreader(object):
  def __init__(self, timerValue, historyCount, prefixDir = ""):
    self._prefixDir = prefixDir
    self.__initReader__()
    self.__uidFilter__ = None
    self.__updateTimer__ = timerValue
    self.__historyCount__ = historyCount
    self.__allcpu__ = cpuhistoryreader(-1, prefixDir=prefixDir)
    self.__overallUserCpuUsage__ = 0
    self.__overallSystemCpuUsage__  = 0
    self.__processList__ = {}
    self.__deltaJiffies__ = 0
    self.__prevJiffies__ = 0    
    self.__closedProcesses__ = set()
    self.__newProcesses__ = set()
    self.__passwdfile = utils.procutils.readFullFile("/etc/passwd").split("\n")
    self.__allConnections__ = {}
    self.__cpuCount__ = 0
    self.__networkCards__= {}
    self.__cpuArray__ = []
    self.__prevTimeStamp__ = None
    self.__allUDP__ = {}
    self.__totalMemKb   = 0
    self.__actualMemKb  = 0
    self.__buffersMemKb = 0
    self.__cachedMemKb  = 0
    self.__swapUsed = 0
    self.__swapTotal = 0
    self.__loadavg__ = 0
    self.__noofprocs__ = 0
    self.__noofrunningprocs__ = 0
    self.__lastpid__ = 0

    cpuinfo = utils.procutils.readFullFile(self._prefixDir+"/proc/cpuinfo").split("\n")
    for line in cpuinfo:
      if line.startswith("processor"):
        self.__cpuArray__.append(cpuhistoryreader(self.__cpuCount__, prefixDir=prefixDir))
        self.__cpuCount__ += 1
    
    #network cards
    data = utils.procutils.readFullFile(self._prefixDir+'/proc/net/dev').split("\n")[2:]
    for line in data:
      cardName = line.split(":")[0].strip()
      if len(cardName) > 0:
        self.__networkCards__[cardName] = {"actual":[0, 0, 0, 0],  #in/s out/s previn, prevout]
                                           "speed":None}
    #try to find speeds if ethtool is available and accessible
    utils.procutils.log("network card speed detection results")
    utils.procutils.log("------------------------------------")
    
    ethtoolerror = False
    for card in self.__networkCards__:
      speed = None
      try:
        ethtool = subprocess.Popen(["ethtool", card], stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        data = ethtool.communicate()
      except (OSError, ValueError):
        ethtoolerror = True
      
      if data[0] is not None:
        for line in data[0].split("\n"):
          if line.find("Speed") != -1:
            try:
              speed = int(line.split(":")[1].split("Mb/s")[0])
            except:
              speed = None
      
      if speed is not None:
        utils.procutils.log("  ethernet device %s has speed %s Mb/s according to ethtool" %(card, speed))
        self.__networkCards__[card]["speed"] = speed
      else:
        utils.procutils.log("  ethernet device %s has unknown speed" %card)
        utils.procutils.log("  network graph scaling for %s is set to autoscale" %card)
    if ethtoolerror:
      utils.procutils.log("  ** ethtool not found, or access denied. For better results, allow access to ethtool")

  def __initReader__(self):
    self.__processList__ = {}
    self.__closedProcesses__ = None
    self.__newProcesses__ = None
    self.__prevJiffies__ = None
    self.__deltaJiffies__ = None
    
    self.__overallUserCpuUsage__ = 0
    self.__overallSystemCpuUsage__  = 0
    
  def __getGlobalJiffies__(self):
    newjiffies = self.__allcpu__.newjiffies()
    if self.__deltaJiffies__ == None:
      self.__prevJiffies__ = newjiffies
      self.__deltaJiffies__ = 1
    else:
      self.__deltaJiffies__ = newjiffies - self.__prevJiffies__
      self.__prevJiffies__ = newjiffies    
  
  def __updateCPUs(self):
    self.__allcpu__.update()
    for cpu in self.__cpuArray__:
      cpu.update()

  
  def overallUserCpuUsage(self):
    return self.__allcpu__.overallUserCpuUsage()
  def overallSystemCpuUsage(self):
    return self.__allcpu__.overallSystemCpuUsage()
  def overallIoWaitCpuUsage(self):
    return self.__allcpu__.overallIoWaitCpuUsage()
  def overallIrqCpuUsage(self):
    return self.__allcpu__.overallIrqCpuUsage()
    
  def getSingleCpuUsage(self, cpu):
    data = (self.__cpuArray__[cpu].overallUserCpuUsage(),
           self.__cpuArray__[cpu].overallSystemCpuUsage(),
           self.__cpuArray__[cpu].overallIoWaitCpuUsage(),
           self.__cpuArray__[cpu].overallIrqCpuUsage())
    return data

    
  def setFilterUID(self,uid):
    self.__uidFilter__ = uid
    self.__initReader__()
    
  def noFilterUID(self):
    self.__uidFilter__ = None
    self.__initReader__()
    
  def getProcUid(self,proc):
    try:
      uid = os.stat(self._prefixDir + "/proc/"+proc).st_uid
    except OSError:
      uid = 0
    return uid
    
  def __getAllProcesses__(self):
    alldirs = os.listdir(self._prefixDir + "/proc")   
    
    if self.__uidFilter__ != None:
      newProcessSetAll = [ process for process in alldirs if process.isdigit() ]
      newProcessList = [ int(process) for process in newProcessSetAll if self.getProcUid(process) == self.__uidFilter__ ]
      #newProcessList.append(1)
      newProcessSet=set(newProcessList)
        
    else:
      newProcessSet = set([ int(process) for process in alldirs if process.isdigit() ])
    
    oldProcessSet = set([ process for process in self.__processList__ ])
    
    self.__closedProcesses__ = oldProcessSet.difference(newProcessSet)
    self.__newProcesses__ = newProcessSet.difference(oldProcessSet)
    
    for process in self.__closedProcesses__:
      del self.__processList__[process]
      
    for process in self.__newProcesses__:
      self.__processList__[process] = \
        {"name": "", \
        "env": UNKNOWN, \
        "prevJiffy":0, \
        "prevJiffyKernel":0, \
        "prevIO":0, \
        "PPID":None, \
        "cpuUsage":0, \
        "cmdline" : UNKNOWN, \
        "uid":UNKNOWN, \
        "wchan":UNKNOWN, \
        "nfThreads":UNKNOWN, \
        "history":singleprocess.singleProcessDetailsAndHistory(process,self.__historyCount__, prefixDir=self._prefixDir),\
        "hasListener": False}

  def __getUIDName__(self, uid):
    """get the users realname from the password file"""
    for line in self.__passwdfile:
      try:
        if line.split(":")[2] == uid:
          name = line.split(":")[0]
          return name
      except IndexError:
        pass
    return "???"
    
    
  def __removeUnknownParents__(self):#useful when filtered on UID
    for process in self.__processList__:
      if self.__processList__[process]["PPID"] > 0:
        if not(self.__processList__.has_key(self.__processList__[process]["PPID"])):
          self.__processList__[process]["PPID"] = 0

  def __getProcessDetails__(self):
    for process in self.__processList__:
      if self.__processList__[process]["hasListener"]:
        try:
          env = utils.procutils.readFullFile(self._prefixDir + "/proc/"+str(process)+"/environ").split("\0")
          self.__processList__[process]["env"] = env
        except: #pylint:disable=W0702
          pass
      
  def __getProcessCpuDetails__(self):
    for process in self.__processList__:
      procStat = None
      try:
        procStat = utils.procutils.readFullFile(self._prefixDir + "/proc/"+str(process)+"/stat")
        if self.__processList__[process]["cmdline"] == UNKNOWN:
          cmdLine = utils.procutils.readFullFile(self._prefixDir + "/proc/"+str(process)+"/cmdline")
          self.__processList__[process]["cmdline"] = cmdLine.replace("\x00"," ")

        #get UID of process
        if self.__processList__[process]["uid"] == UNKNOWN:
          uid = str(os.stat(self._prefixDir + "/proc/"+str(process))[4])
          self.__processList__[process]["uid"] = self.__getUIDName__(uid)        
      except:
        pass #pylint:disable=W0702
      
      try:    
        statm = utils.procutils.readFullFile(self._prefixDir + "/proc/"+str(process)+"/statm")
        totalRssMem = int(statm.split(' ')[1])*4 #in 4k pages

        #smaps = utils.procutils.readFullFile("/proc/"+str(process)+"/smaps").split("kB\nRss:")
        #totalRssMem = 0
        #for line in smaps:
          #if line.startswith(" "):
            #totalRssMem += int(line.split("kB")[0].strip())
            
      except: #pylint:disable=W0702
        totalRssMem = 0
      if self.__processList__[process]["hasListener"]:
        try:
          wchan = utils.procutils.readFullFile(self._prefixDir + "/proc/"+str(process)+"/wchan")
          self.__processList__[process]["wchan"] = wchan
        except: #pylint:disable=W0702
          self.__processList__[process]["wchan"] = UNKNOWN
      else:
        self.__processList__[process]["wchan"] = UNKNOWN
        
      if procStat != None:
        procStatSplitted =  [procStat.split(" (")[0]]+[procStat.split(" (")[1].split(") ")[0]]+procStat.split(") ")[1].split()
        nextJiffy = int(procStatSplitted[13]) + int(procStatSplitted[14])
        try:
          cpuUsage = round(((nextJiffy - self.__processList__[process]["prevJiffy"]) / (self.__deltaJiffies__ * 1.0)) * 100, 1)
        except ZeroDivisionError:
          cpuUsage = 0.0
        
        nextJiffyKernel = int(procStatSplitted[14])
        try:
          cpuUsageKernel = round(((nextJiffyKernel - self.__processList__[process]["prevJiffyKernel"]) / (self.__deltaJiffies__ * 1.0)) * 100, 1)
        except ZeroDivisionError:
          cpuUsageKernel = 0
        #IO accounting
        try:
          io = utils.procutils.readFullFile(self._prefixDir + "/proc/"+str(process)+"/io").split("\n")
          iototal = int(io[0].split(": ")[1]) + int(io[1].split(": ")[1])
        except: #pylint:disable=W0702
          iototal = 0
        
        if self.__processList__[process]["prevIO"] == 0: #first time
          deltaio = 0
        else:
          deltaio = iototal - self.__processList__[process]["prevIO"]
        self.__processList__[process]["prevIO"] = iototal
        
        self.__processList__[process]["cpuUsage"] = cpuUsage
        self.__processList__[process]["prevJiffy"] = nextJiffy
        self.__processList__[process]["cpuUsageKernel"] = cpuUsageKernel
        self.__processList__[process]["prevJiffyKernel"] = nextJiffyKernel
        self.__processList__[process]["PPID"] = int(procStatSplitted[3])
        self.__processList__[process]["name"] = procStatSplitted[1]
        
        self.__processList__[process]["Rss"] = totalRssMem
        self.__processList__[process]["history"].update(cpuUsage, cpuUsageKernel, totalRssMem, deltaio/1024,self.__processList__[process]["hasListener"])
        self.__processList__[process]["nfThreads"] = procStatSplitted[19]
      else:
        self.__processList__[process]["PPID"] = 1
        
  def getIOAccounting(self):
    """to be implemented in the future"""
    pass
    #~ Description
    #~ -----------

    #~ rchar: (unsigned long long)

    #~ The number of bytes which this task has caused to be read from storage.
    #~ This is simply the sum of bytes which this process passed to read() and
    #~ pread(). It includes things like tty IO and it is unaffected by whether
    #~ or not actual physical disk IO was required (the read might have been
    #~ satisfied from pagecache)


    #~ wchar: (unsigned long long)

    #~ The number of bytes which this task has caused, or shall cause to be written
    #~ to disk. Similar caveats apply here as with rchar.


    #~ syscr: (unsigned long long)

    #~ I/O counter: read syscalls
    #~ Attempt to count the number of read I/O operations, i.e. syscalls like read()
    #~ and pread().


    #~ syscw: (unsigned long long)

    #~ I/O counter: write syscalls
    #~ Attempt to count the number of write I/O operations, i.e. syscalls like write()
    #~ and pwrite().


    #~ read_bytes: (unsigned long long)

    #~ I/O counter: bytes read
    #~ Attempt to count the number of bytes which this process really did cause to
    #~ be fetched from the storage layer. Done at the submit_bio() level, so it is
    #~ accurate for block-backed filesystems. <please add status regarding NFS and CIFS
    #~ at a later time>


    #~ write_bytes: (unsigned long long)

    #~ I/O counter: bytes written
    #~ Attempt to count the number of bytes which this process caused to be sent to
    #~ the storage layer. This is done at page-dirtying time.


    #~ cancelled_write_bytes: (unsigned long long)

    #~ The big inaccuracy here is truncate. If a process writes 1MB to a file and
    #~ then deletes the file, it will in fact perform no writeout. But it will have
    #~ been accounted as having caused 1MB of write.
    #~ In other words: The number of bytes which this process caused to not happen,
    #~ by truncating pagecache. A task can cause "negative" IO too. If this task
    #~ truncates some dirty pagecache, some IO which another task has been accounted
    #~ for (in its write_bytes) will not be happening. We _could_ just subtract that
    #~ from the truncating task's write_bytes, but there is information loss in doing
    #~ that.


    #~ Note:

    #~ At it`s current implementation state, it's a bit racy on 32-bit machines: if process
    #~ A reads process B's /proc/pid/io while process B is updating one of those 64-bit
    #~ counters, process A could see an intermediate result.  


  def __getAllSocketInfo__(self):
    self.__allConnections__ = {} #list of connections, organized by inode
    ipv4data = utils.procutils.readFullFile(self._prefixDir + "/proc/net/tcp").split("\n")[1:][:-1]
    ipv6data = utils.procutils.readFullFile(self._prefixDir + "/proc/net/tcp6").split("\n")[1:][:-1]
    for connection in ipv4data+ipv6data:
      self.__allConnections__[connection.split()[9]] = connection.split()
  def __getAllUDPInfo__(self):
    self.__allUDP__ = {} #list of connections, organized by inode
    data = utils.procutils.readFullFile(self._prefixDir + "/proc/net/udp").split("\n")
    for udp in data:
      if len(udp) > 1:
        self.__allUDP__[udp.split()[9]] = udp.split()

  def __getMemoryInfo(self):
    mem = utils.procutils.readFullFile(self._prefixDir + "/proc/meminfo").split("\n")
    mem = [l.replace("kB", "").split(":") for l in mem if l]
    memDict = {}
    for l in mem:
      memDict[l[0].upper()] = int(l[1])

    self.__totalMemKb   = memDict["MEMTOTAL"]
    self.__actualMemKb  = memDict["MEMFREE"]
    self.__buffersMemKb = memDict["BUFFERS"]
    self.__cachedMemKb  = memDict["CACHED"]
    self.__swapUsed     = memDict["SWAPTOTAL"]-memDict["SWAPFREE"]
    self.__swapTotal    = memDict["SWAPTOTAL"]
  
  def __getAverageLoad(self):
    load = utils.procutils.readFullFile(self._prefixDir + "/proc/loadavg").split()
    self.__loadavg__ = (load[0],load[1],load[2])
    self.__noofprocs__ = load[3].split("/")[1]
    self.__noofrunningprocs__ = load[3].split("/")[0]
    self.__lastpid__ = load[4]
    
  def getNetworkCards(self):
    return self.__networkCards__

  def getNetworkCardUsage(self, cardName):
    return self.__networkCards__[cardName]["actual"][0], self.__networkCards__[cardName]["actual"][1]
  
  def getNetworkCardData(self, cardName):
    return self.__networkCards__[cardName]
    
  def getAllProcessSockets(self,process):
    
    allFds = {}
    allUDP = {}
    try:
      __allFds = rootproxy.doListDir(self._prefixDir + "/proc/" + str(process) + "/fd")
      #__allFds = os.listdir(self._prefixDir + "/proc/" + str(process) + "/fd")
    except OSError:
     __allFds = ""
    for _idx, fd in enumerate(__allFds):
      try:
        link = rootproxy.doReadlink(self._prefixDir + "/proc/" + str(process) + "/fd/" + fd)
        #link = os.readlink(self._prefixDir + "/proc/" + str(process) + "/fd/" + fd)
      except (OSError, rootproxy.CommandException):
        link = ""
      if link.startswith("socket"):
        inode = link.split("[")[1].split("]")[0]
        try:
          allFds[inode] = self.__allConnections__[inode]
        except KeyError:
          pass
        try:
          allUDP[inode] = self.__allUDP__[inode]
        except KeyError:
          pass
    return allFds, allUDP
    
  def __getNetworkCardUsage(self):
    data = utils.procutils.readFullFile(self._prefixDir + '/proc/net/dev').split("\n")[2:]
    actTime = time.time()
    for line in data:
      cardName = line.split(":")[0].strip()
      if len(cardName) > 0:
        splittedLine = line.split(":")[1].split()
        recv = int(splittedLine[0])
        sent = int(splittedLine[8])

        if self.__prevTimeStamp__ != None:
          if self.__networkCards__[cardName]["actual"][2] == 0:
            pass
          else:
            self.__networkCards__[cardName]["actual"][0] = (recv - self.__networkCards__[cardName]["actual"][2]) / (actTime - self.__prevTimeStamp__)
            self.__networkCards__[cardName]["actual"][1] = (sent - self.__networkCards__[cardName]["actual"][3]) / (actTime - self.__prevTimeStamp__)
          if self.__networkCards__[cardName]["actual"][0] <0:
            self.__networkCards__[cardName]["actual"][0] = 0
          if self.__networkCards__[cardName]["actual"][1] <0:
            self.__networkCards__[cardName]["actual"][1] = 0
            
          self.__networkCards__[cardName]["actual"][2] = recv
          self.__networkCards__[cardName]["actual"][3] = sent
        
        self.__networkCards__[cardName]["recerrors"]  = int(splittedLine[2])
        self.__networkCards__[cardName]["recdrops"]   = int(splittedLine[3])
        self.__networkCards__[cardName]["senderrors"] = int(splittedLine[10])
        self.__networkCards__[cardName]["senddrops"]  = int(splittedLine[11])
        self.__networkCards__[cardName]["sendcoll"]   = int(splittedLine[13])
        self.__networkCards__[cardName]["recbytes"]   = int(splittedLine[0])        
        self.__networkCards__[cardName]["recpackets"]   = int(splittedLine[1])        
        self.__networkCards__[cardName]["sendbytes"]   = int(splittedLine[8])        
        self.__networkCards__[cardName]["sendpackets"]   = int(splittedLine[9])          
  
  def doReadProcessInfo(self):
    self.__updateCPUs()
    self.__getGlobalJiffies__()
    self.__getAllProcesses__()
    self.__getProcessCpuDetails__()
    self.__removeUnknownParents__()
    self.__getProcessDetails__()
    self.__getAllSocketInfo__()
    self.__getAllUDPInfo__()
    self.__getMemoryInfo()
    self.__getAverageLoad()
    self.__getNetworkCardUsage()
    #keep line below as last command
    self.__prevTimeStamp__ = time.time()
    
  def getProcessInfo(self):
    return self.__processList__, self.__closedProcesses__, self.__newProcesses__

  def hasProcess(self, process):
    return self.__processList__.has_key(int(process))
  def setListener(self, process):
    if self.__processList__.has_key(int(process)):
      self.__processList__[int(process)]["hasListener"]=True
  def getProcessCpuUsageHistory(self, process):
    return self.__processList__[int(process)]["history"].cpuUsageHistory
  def getcwd(self, process):
    return self.__processList__[int(process)]["history"].cwd
  def getexe(self, process):
    return self.__processList__[int(process)]["history"].exe
  def getstartedtime(self, process):
    return self.__processList__[int(process)]["history"].startedtime
  def getcmdline(self, process):
    return self.__processList__[int(process)]["history"].cmdline
  def getppid(self, process):
    return self.__processList__[int(process)]["history"].ppid
  def getProcessCpuUsageKernelHistory(self, process):
    return self.__processList__[int(process)]["history"].cpuUsageKernelHistory
  def getProcessRssUsageHistory(self, process):
    return self.__processList__[int(process)]["history"].rssUsageHistory
  def getIOHistory(self, process):
    return self.__processList__[int(process)]["history"].IOHistory
  def getEnvironment(self,process):
    return self.__processList__[int(process)]["env"]
  def getHistoryDepth(self, process):
    return self.__processList__[int(process)]["history"].HistoryDepth
  def getCpuCount(self):
    return self.__cpuCount__
  def getMemoryUsage(self):
    return self.__totalMemKb, self.__actualMemKb, self.__buffersMemKb, self.__cachedMemKb, self.__swapUsed, self.__swapTotal
  def getLoadAvg(self):
    return  self.__loadavg__, self.__noofprocs__, self.__noofrunningprocs__, self.__lastpid__
  def getThreads(self, process):
    return self.__processList__[int(process)]["history"].threads
  def getFileInfo(self, process):
    return self.__processList__[int(process)]["history"].openFiles
