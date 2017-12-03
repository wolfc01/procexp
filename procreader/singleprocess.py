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

UNKNOWN = "---"

import os
import utils.procutils
import datetime

class singleProcessDetailsAndHistory(object):
  def __init__(self, pid, historyDepth, prefixDir = ""):
    self._prefixDir = prefixDir
    self.__pid__ = str(pid)
    self.__pathPrefix__ = self._prefixDir+"/proc/"+self.__pid__+"/"
    self.__pwd__ = UNKNOWN
    self.__exepath__ = UNKNOWN
    self.openFiles = {}
    self.__memMap__ = ""
    self.cpuUsageHistory = [0] * historyDepth
    self.cpuUsageKernelHistory = [0] * historyDepth
    self.rssUsageHistory = [0] * historyDepth
    self.IOHistory = [0] * historyDepth
    self.HistoryDepth = historyDepth
    self.cmdline = None
    self.startedtime = None
    self.ppid = None
    self.threads = {}

  def __getFileDetails__(self, hasListener):
    if hasListener:
      try:
        allfds = os.listdir(self.__pathPrefix__ + "fd")
        self.openFiles = {}
        for fd in allfds:
          self.openFiles[fd] = {"path":os.readlink(self.__pathPrefix__ + "fd"+"/"+fd)}

          #get fileinfo : kernel 2.6.22 and higher

          try:
            fileInfo = utils.procutils.readFullFile(self.__pathPrefix__ + "fdinfo/"+fd)
            self.openFiles[fd]["fdinfo"] = fileInfo
          except:
            self.openFiles[fd]["fdinfo"] = "??"

      except OSError:
        pass

  def _getThreadsInfo__(self, hasListener):
    self.threads = {}
    if hasListener:
      try:
        alldirs = os.listdir(self.__pathPrefix__ + "task/")
        for t in alldirs:
          try:
            wchan = utils.procutils.readFullFile(self.__pathPrefix__ + "task/" + str(t) + "/wchan")
            sched = utils.procutils.readFullFile(self.__pathPrefix__ + "task/" + str(t) + "/sched")
            wakeupcount = int(sched.split("\n")[23].split(":")[1]) #23 is wakeupcount
            self.threads[t] = [wchan, wakeupcount]
          except:
            pass
      except OSError:
        pass

  def update(self, cpuUsage, cpuUsageKernel, totalRss, IO, hasListener):
    if cpuUsage > 100:
      cpuUsage = 0
    if cpuUsageKernel > 100:
      cpuUsageKernel = 0
    if self.__pwd__ == UNKNOWN:
      try:
        self.__pwd__ = os.readlink(self.__pathPrefix__ + "cwd")
      except:
        self.__pwd__ = UNKNOWN
    self.cpuUsageHistory.append(cpuUsage)
    self.cpuUsageKernelHistory.append(cpuUsageKernel)
    self.rssUsageHistory.append(totalRss)
    self.IOHistory.append(IO)

    self.cpuUsageHistory = self.cpuUsageHistory[1:]
    self.cpuUsageKernelHistory = self.cpuUsageKernelHistory[1:]
    self.rssUsageHistory = self.rssUsageHistory[1:]
    self.IOHistory = self.IOHistory[1:]


    try:
      self.cwd = os.readlink(self.__pathPrefix__ + "cwd")
    except OSError, val:
      self.cwd = "<"+val.strerror+">"
    except :
      raise

    if self.cmdline == None:
      #do below only once
      try:
        self.cmdline = utils.procutils.readFullFile(self.__pathPrefix__ + "cmdline").replace("\x00"," ")
      except OSError, val:
        self.cmdline = "<"+val.strerror+">"
      except utils.procutils.FileError:
        self.cmdline = "---"
      except:
        raise

    try:
      self.exe = os.readlink(self.__pathPrefix__ + "exe")
    except OSError, val:
      self.exe = "<"+val.strerror+">"
    except :
      raise

    #started time of a process
    if self.startedtime == None:
      try:
        procstartedtime_seconds = utils.procutils.readFullFile(self.__pathPrefix__ + "stat").split(" ")[21]


        procstat = utils.procutils.readFullFile(self._prefixDir+"/proc/stat").split("\n")
        for line in procstat:
          if line.find("btime") != -1:
            systemstarted_seconds = line.split(" ")[1]
        HZ = os.sysconf(os.sysconf_names["SC_CLK_TCK"])
        epoch = datetime.datetime(month=1,day=1,year=1970)


        procstarted = epoch + \
                      datetime.timedelta(seconds=int(systemstarted_seconds)) + \
                      datetime.timedelta(seconds=int(int(procstartedtime_seconds)/(HZ*1.0)+0.5))

        self.startedtime = procstarted.strftime("%A, %d. %B %Y %I:%M%p")
      except utils.procutils.FileError:
        self.startedtime = "--"

    #process parent pid
    if self.ppid is None:
      try:
        self.ppid = utils.procutils.readFullFile(self.__pathPrefix__ + "stat").split(" ")[3]
      except utils.procutils.FileError:
        self.ppid = None

    #all threads
    self._getThreadsInfo__(hasListener)

    #get fileInfo
    self.__getFileDetails__(hasListener)
