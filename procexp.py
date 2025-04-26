#!/usr/bin/python
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

#Thanks to the following developers helping:
#
#  Diaa Sami, making the GUI more usable
#


#create qt app early, in order to show unhandled exceptions graphically.
import sys
from PyQt6 import QtCore, QtGui, uic, QtWidgets
import utils.procutils

app = QtWidgets.QApplication(sys.argv)

import procreader.reader
import logui
import aboutui
import os
import singleprocess
import systemoverview
import configobj
import settings as settingsMenu

import plotobjects
import networkoverview
import colorlegend

import cpuaffinitypriority
import signal
import procreader.tcpip_stat as tcpip_stat
import rootproxy
import messageui
import subprocess


version = "2.0.0"


class procexp:
  def __init__(self):
    self._timer = None
    self._reader = None
    self._treeProcesses = {} #flat dictionary of processes
    self._toplevelItems = {}
    self._mainUi = None
    self._onlyUser = True
    self._greenTopLevelItems = {}
    self._redTopLevelItems = {}
    self._singleProcessUiList = {}
    self._curveCpuHist = None
    self._curveCpuSystemHist = None
    self._curveIoWaitHist = None
    self._curveIrqHist = None
    self._curveCpuPlotGrid = None
    self._cpuUsageHistory = None
    self._cpuUsageSystemHistory = None
    self._cpuUsageIoWaitHistory = None
    self._cpuUsageIrqHistory = None
    self._systemOverviewUi = None
    self._networkOverviewUi = None
    self._mainWindow = None
    self._firstUpdate = True
    self._procList = {}
    self._stateCtr = 0

    #default settings
    self._settings = {}
    self._defaultSettings = \
    {"fontSize": 10, 
    "columnWidths": [100,60,40,100,30,30,30,30],
    "updateTimer": 1000,
    "historySampleCount": 200
    }

    self._treeViewcolumns = ["Process","PID","CPU","Command Line", "User", "Chan","#thread"]

    self._mainWindow = QtWidgets.QMainWindow()
    self._mainUi = uic.loadUi(os.path.join(os.path.dirname(__file__), "./ui/main.ui"), baseinstance=self._mainWindow)
    self.prepareUI(self._mainUi)
    self.loadSettings()

    self._mainWindow.setWindowTitle(self._mainWindow.windowTitle()+":"+version)
    self._mainWindow.show()

    app.processEvents()
    runningAsRoot = rootproxy.start(asRoot=True)

    self._messageui = messageui.settingsDialog() 

    if not runningAsRoot:
      self._messageui.doMessageWindow("Process explorer has no root privileges. TCPIP traffic monitoring (using tcpdump) will not be available.")

    self._reader = procreader.reader.procreader(int(self._settings["updateTimer"]), int(self._settings["historySampleCount"]))

    self._timer.start(int(self._settings["updateTimer"]))

    if self._onlyUser:
      self._reader.setFilterUID(os.geteuid())

    self._systemOverviewUi = systemoverview.systemOverviewUi(self._reader.getCpuCount(), int(self._settings["historySampleCount"]), self._reader)
    self._networkOverviewUi = networkoverview.networkOverviewUi(self._reader.getNetworkCards(), int(self._settings["historySampleCount"]), self._reader)

    self._systemOverviewUi.setFontSize(int(self._settings["fontSize"]))
    self._networkOverviewUi.setFontSize(int(self._settings["fontSize"]))    
  

  def performMenuAction(self, action):
    ''' perform action from menu
    '''
    if action is self._mainUi.actionKill_process:
      try:
        selectedItem = self._mainUi.processTreeWidget.selectedItems()[0]
      except IndexError:
        return
      process = selectedItem.data(1,0)
      utils.procutils.killProcessHard(process)
    elif action is self._mainUi.actionKill_process_tree:
      try:
        selectedItem = self._mainUi.processTreeWidget.selectedItems()[0]
      except IndexError:
        return
      process = selectedItem.data(1,0)
      self.killProcessTree(process, self._procList)
    elif action is self._mainUi.actionShow_process_from_all_users:
      if self._onlyUser:
        self._reader.noFilterUID()
        self.clearTree()
        self._onlyUser = False
      else:
        self._reader.setFilterUID(os.geteuid())
        self.clearTree()
        self._onlyUser = True
    elif action is self._mainUi.actionProperties:
      try:
        selectedItem = self._mainUi.processTreeWidget.selectedItems()[0]
      except IndexError:
        return
      process = str(selectedItem.data(1,0))
      if process in self._singleProcessUiList:
        self._singleProcessUiList[process].makeVisible()
      else:
        if int(process) in self._procList:
          if self._procList[int(process)]["runstatus"] == "Z":
            self._singleProcessUiList[process] = singleprocess.singleUi(process, self._procList[int(process)]["cmdline"], "["+self._procList[int(process)]["name"]+"]", self._reader, int(self._settings["historySampleCount"]))
          else:
            self._singleProcessUiList[process] = singleprocess.singleUi(process, self._procList[int(process)]["cmdline"], self._procList[int(process)]["name"], self._reader, int(self._settings["historySampleCount"]))
    elif action is self._mainUi.actionSaveSettings:
      self.saveSettings()
    elif action is self._mainUi.actionSettings:
      msec, depth, fontSize = settingsMenu.doSettings(int(self._settings["updateTimer"]),\
                                                        int(self._settings["historySampleCount"]), \
                                                        int(self._settings["fontSize"]))
    
      self._settings["fontSize"] = int(fontSize)
      self.setFontSize(fontSize)

      if self._settings["historySampleCount"] != int(depth):
        self._settings["historySampleCount"] = int(depth)
        self._cpuUsageHistory = [0] * int(self._settings["historySampleCount"])
        self._cpuUsageSystemHistory = [0] * int(self._settings["historySampleCount"])
        self._cpuUsageIoWaitHistory = [0] * int(self._settings["historySampleCount"])
        self._cpuUsageIrqHistory = [0] * int(self._settings["historySampleCount"])
        if self._reader is not None:
          self._reader.setNewHistoryDepth(int(depth)) 
        for process in self._singleProcessUiList:   
          if self._singleProcessUiList[process] is not None: 
            self._singleProcessUiList[process].setNewDepth(depth)
      self._settings["updateTimer"] = int(msec)
      self._timer.start(int(self._settings["updateTimer"]))
    elif action is self._mainUi.actionSystem_information:
      self._systemOverviewUi.show()
    elif action is self._mainUi.actionNetwork_Information:
      self._networkOverviewUi.show()
    elif action is self._mainUi.actionClose_all_and_exit:
      for window in self._singleProcessUiList:
        self._singleProcessUiList[window].closeWindow()
      self._systemOverviewUi.close()
      self._networkOverviewUi.close()
      self._mainWindow.close()
      logui.closeLogWindow()
    elif action is self._mainUi.actionColor_legend:
      colorlegend.doColorHelpLegend()
    elif action is self._mainUi.actionSet_affinityPriority:
      try:
        selectedItem = self._mainUi.processTreeWidget.selectedItems()[0]
        process = str(selectedItem.data(1,0))
      except IndexError:
        return
      cpuaffinitypriority.doAffinityPriority(self._reader.getCpuCount(), process)
    elif action is self._mainUi.actionLog:
      logui.doLogWindow()
    elif action is self._mainUi.actionAbout:
      aboutui.doAboutWindow()
    elif action is self._mainUi.actionClear_Messages:
      self._messageui.clearAllMessages()
    elif action is self._mainUi.actionSuspend_process:
      selectedItem = self._mainUi.processTreeWidget.selectedItems()[0]
      process = str(selectedItem.data(1,0))
      p = subprocess.Popen(["kill", "-s", "SIGSTOP", str(process)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      data = p.communicate()
      result =p.returncode
      if p.returncode != 0:
        utils.procutils.message("suspend process %s failed \n\nmessage=%s" %(process, data[1].decode()))
    elif action is self._mainUi.actionResume_process:
      selectedItem = self._mainUi.processTreeWidget.selectedItems()[0]
      process = str(selectedItem.data(1,0))
      p = subprocess.Popen(["kill", "-s", "SIGCONT", str(process)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      data = p.communicate()
      result =p.returncode
      if p.returncode != 0:
        utils.procutils.message("resume process %s failed \n\nmessage=%s" %(process, data[1].decode()))
    else:
      utils.procutils.log("This action (%s)is not yet supported." %action)

  def setFontSize(self, fontSize):
    self._settings["fontSize"] = fontSize
    font = QtGui.QFont()
    font.setPointSize(fontSize)
    self._mainUi.menuFile.setFont(font)
    self._mainUi.menuOptions.setFont(font)
    self._mainUi.menuView.setFont(font)
    self._mainUi.menuProcess.setFont(font)
    self._mainUi.menuSettings.setFont(font)
    self._mainUi.menubar.setFont(font)
    self._mainUi.processTreeWidget.setFont(font)
    if self._systemOverviewUi is not None:
      self._systemOverviewUi.setFontSize(fontSize)
    if self._networkOverviewUi is not None:
      self._networkOverviewUi.setFontSize(fontSize)

  def loadSettings(self):
    settingsPath = os.path.expanduser("~/.procexp/settings")
    if os.path.exists(settingsPath):
      f = open(settingsPath,"rb")
      settingsObj = configobj.ConfigObj(infile=f)
      self._settings=settingsObj.dict()
      
    #load default settings for undefined settings
    for item in self._defaultSettings:
      if item in self._settings:
        pass
      else:
        self._settings[item] = self._defaultSettings[item]
      
    fontsize = int(self._settings["fontSize"])
    self.setFontSize(fontsize)
    
    #set the columnwidths
    for headerSection in range(self._mainUi.processTreeWidget.header().count()):
      try:
        width = int(self._settings["columnWidths"][headerSection])
      except:
        width = 150
      self._mainUi.processTreeWidget.header().resizeSection(headerSection,width)
      
    #load default settings for undefined settings
    for item in self._defaultSettings:
      if item in self._settings:
        pass
      else:
        self._settings[item] = self._defaultSettings[item]
        
    self._cpuUsageHistory = [0] * int(self._settings["historySampleCount"])
    self._cpuUsageSystemHistory = [0] * int(self._settings["historySampleCount"])
    self._cpuUsageIoWaitHistory = [0] * int(self._settings["historySampleCount"])
    self._cpuUsageIrqHistory = [0] * int(self._settings["historySampleCount"])


  def saveSettings(self):
    '''save settings to ~.procexp directory, in file "settings"
    '''
    widths = []
    for headerSection in range(self._mainUi.processTreeWidget.header().count()):
      widths.append(self._mainUi.processTreeWidget.header().sectionSize(headerSection))
    self._settings["columnWidths"] = widths
    
    settingsPath = os.path.expanduser("~/.procexp")
    if not(os.path.exists(settingsPath)):
      os.makedirs(settingsPath)
    f = open(settingsPath + "/settings","wb")
    cfg = configobj.ConfigObj(self._settings)
    cfg.write(f)
    f.close()

  def onContextMenu(self, point):
    self._mainUi.menuProcess.exec(self._mainUi.processTreeWidget.mapToGlobal(point))

  def onHeaderContextMenu(self, point):
    menu = QtGui.QMenu()
    for idx, col in enumerate(self._treeViewcolumns):
      action = QtGui.QAction(col, self._mainUi.processTreeWidget)
      action.setCheckable(True)
      action.setChecked(not self._mainUi.processTreeWidget.isColumnHidden(idx))
      action.setData(idx)
      menu.addAction(action)
    selectedItem = menu.exec(self._mainUi.processTreeWidget.mapToGlobal(point))
    if selectedItem is not None:
      self._mainUi.processTreeWidget.setColumnHidden(selectedItem.data().toInt()[0], not selectedItem.isChecked())
  
  def prepareUI(self, mainUi):
    """ prepare the main UI, setup plots and menu triggers
    """
    mainUi.processTreeWidget.setColumnCount(len(self._treeViewcolumns))
    mainUi.processTreeWidget.setHeaderLabels(self._treeViewcolumns)
    mainUi.processTreeWidget.header().setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
    mainUi.processTreeWidget.header().customContextMenuRequested.connect(self.onHeaderContextMenu)

    #create a timer which triggers the process explorer to update its contents
    self._timer = QtCore.QTimer(mainUi.processTreeWidget)
    self._timer.timeout.connect(self.updateUI)
    mainUi.processTreeWidget.customContextMenuRequested.connect(self.onContextMenu)
    mainUi.menuFile.triggered.connect(self.performMenuAction)
    mainUi.menuProcess.triggered.connect(self.performMenuAction)
    mainUi.menuOptions.triggered.connect(self.performMenuAction)
    mainUi.menuSettings.triggered.connect(self.performMenuAction)
    mainUi.menuView.triggered.connect(self.performMenuAction)
    mainUi.menuHelp.triggered.connect(self.performMenuAction)
    
    #prepare the plot    
    self._curveCpuHist = plotobjects.niceCurve("CPU History",
                            1 , (0,255,0),(0,170,0), 
                            mainUi.plotOverallCpuHist, 100)
    
    self._curveCpuSystemHist = plotobjects.niceCurve("CPU Kernel History",
                            1, (255,0,0),(170,0,0), 
                            mainUi.plotOverallCpuHist, 100)
                            
    self._curveIoWaitHist = plotobjects.niceCurve("CPU IO wait history",
                            1, (0,0,255),(0,0,127), 
                            mainUi.plotOverallCpuHist, 100)
    
    self._curveIrqHist = plotobjects.niceCurve("CPU irq history",
                            1, (0,255,255),(0,127,127), 
                            mainUi.plotOverallCpuHist, 100)

    scale = plotobjects.scaleObject()
    scale.min = 0
    scale.max = 100
    _ = plotobjects.procExpPlot(mainUi.plotOverallCpuHist, scale, hasGrid=False)
  
  def clearTree(self):
    """ clear the tree of processes.
    """
    self._mainUi.processTreeWidget.clear()
    self._treeProcesses = {}
    self._toplevelItems = {}
    self._greenTopLevelItems = {}
    self._redTopLevelItems = {}
  
  def killProcessTree(self, proc, procList):
    """ Kill a tree of processes, the hard way
    """
    self.killChildsTree(int(str(proc)), procList)
    utils.procutils.killProcessHard(int(str(proc)))

  def killChildsTree(self, proc, procList):
    """ kill all childs of given process
    """
    for aproc in procList:
      if procList[aproc]["PPID"] == proc:
        self. killChildsTree(aproc, procList)
        utils.procutils.killProcess(aproc)
     
  def addProcessAndParents(self, proc, procList):
    """ adds a process and its parents to the tree of processes
    """
    if proc in self._treeProcesses: #process already exists, do nothing
      return self._treeProcesses[proc]
      
    self._treeProcesses[proc] = QtWidgets.QTreeWidgetItem([])
    self._greenTopLevelItems[proc] = self._treeProcesses[proc]
    
    if procList[proc]["PPID"] > 0 and procList[proc]["PPID"] in procList: #process has a parent
      parent = self.addProcessAndParents(procList[proc]["PPID"],procList)
      parent.addChild(self._treeProcesses[proc])
    else: #process has no parent, thus it is toplevel. add it to the treewidget
      self._mainUi.processTreeWidget.addTopLevelItem(self._treeProcesses[proc])
      self._toplevelItems[proc] = self._treeProcesses[proc]
    return self._treeProcesses[proc]
          
  def expandChilds(self, parent):
    """ expand all childs of given parent
    """
    for index in range(parent.childCount()):
      thechild = parent.child(index)
      if thechild != None:
        self._mainUi.processTreeWidget.expandItem(thechild)
        self.expandChilds(thechild)
      else:
        self._mainUi.processTreeWidget.expandItem(parent)

  def expandAll(self):
    """ expand all subtrees
    """
    for topLevelIndex in range(self._mainUi.processTreeWidget.topLevelItemCount()):
      item = self._mainUi.processTreeWidget.topLevelItem(topLevelIndex)
      self.expandChilds(item)
      self._mainUi.processTreeWidget.expandItem(item)
  
  def updateUI(self):
    """update"""
    tcpip_stat.tcpStat().tick()
    try:
      if self._mainUi.freezeCheckBox.isChecked():
        return
      
      deletedChildItems = {}
      self._reader.doReadProcessInfo()
      self._procList, closedProc, newProc = self._reader.getProcessInfo()

      #color all green processes from previous cycle with default background
      for proc in self._greenTopLevelItems:
        for column in range(self._greenTopLevelItems[proc].columnCount()):
          self._greenTopLevelItems[proc].setBackground(column, self._mainUi.processTreeWidget.palette().window().color())
      self._greenTopLevelItems = {}

      def removeChildren(parent):
        allChilds = []
        extraRedRemoved = []
        for idx in range(parent.childCount()):
          allChilds.append(parent.child(idx)) 
        for widgetItem in allChilds:
          #check if this one is already red
          try:
            procId = [proc for proc, item in self._redTopLevelItems.items() if item == widgetItem][0]
            #this process is also red, so widget item can be removed
            extraRedRemoved.append(procId)
            continue
          except IndexError:
            pass
          
          #process not in red list, reparent to existing process parent or root if it has no parent process anymore.
          try:
            procId = [proc for proc, item in self._treeProcesses.items() if item == widgetItem][0]
            parentWidget = self._treeProcesses[self._procList[procId]["PPID"]]
            parent.removeChild(widgetItem)
            parentWidget.addChild(widgetItem)
          except KeyError:
            #process does not exist, reparent it to toplevel, so it can be colored red the next update cycle
            parent.removeChild(widgetItem)
            self._mainUi.processTreeWidget.addTopLevelItem(widgetItem)
            deletedChildItems[procId] = widgetItem
        return extraRedRemoved

      #delete all red widgetItems from previous cycle
      childsRemoved = []
      for proc in self._redTopLevelItems:
        if proc in childsRemoved:
          continue
        parent = self._redTopLevelItems[proc].parent()
        if parent is not None:
          index = parent.indexOfChild(self._redTopLevelItems[proc])
          child = parent.child(index)
          childsRemoved.append(removeChildren(child))
          child = parent.takeChild(index)
        else:
          index = self._mainUi.processTreeWidget.indexOfTopLevelItem(self._redTopLevelItems[proc])
          self._mainUi.processTreeWidget.takeTopLevelItem(index)
      self._redTopLevelItems = {}
      
      #create new items and mark items to be deleted red
      #draw tree hierarchy of processes
      for proc in newProc:
        self.addProcessAndParents(proc, self._procList)

      #get default backgroundcolor once
      
      #copy processed to be deleted to the red list      
      for proc in closedProc:
        self._redTopLevelItems[proc] = self._treeProcesses.pop(proc)

      for proc in deletedChildItems:
        self._redTopLevelItems[proc] = deletedChildItems[proc]
      deletedChildItems = {}


      #color all deleted processed red
      for proc in self._redTopLevelItems:
        for column in range(self._redTopLevelItems[proc].columnCount()):
          self._redTopLevelItems[proc].setBackground(column, QtGui.QColor(255,0,0))

      #update status information about the processes  
      for proc in self._procList:
        if self._procList[proc]["runstatus"] == "Z": #zombie
          self._treeProcesses[proc].setData(0, 0, "["+self._procList[proc]["name"]+"]")
        else:
          self._treeProcesses[proc].setData(0, 0, self._procList[proc]["name"])
        self._treeProcesses[proc].setData(1, 0, str(proc))
        self._treeProcesses[proc].setData(2, 0, self._procList[proc]["cpuUsage"])
        self._treeProcesses[proc].setData(3, 0, self._procList[proc]["cmdline"])
        self._treeProcesses[proc].setData(4, 0, self._procList[proc]["uid"])
        self._treeProcesses[proc].setData(5, 0, self._procList[proc]["wchan"])
        self._treeProcesses[proc].setData(6, 0, self._procList[proc]["nfThreads"])

      #color all new processes green
      if self._firstUpdate == False:
        for proc in self._greenTopLevelItems:
          item = self._greenTopLevelItems[proc]
          for column in range(item.columnCount()):
            item.setBackground(column, QtGui.QColor(0,255,0))
        
      if (len(closedProc) > 0) or (len(newProc) > 0):
        self.expandAll()
      
      for ui in self._singleProcessUiList:
        self._singleProcessUiList[ui].update()
        
      #update CPU plots
      self._systemOverviewUi.update()
      
      #network plots
      self._networkOverviewUi.update()
        
      #update the cpu graph      
      self._cpuUsageHistory.append(self._reader.overallUserCpuUsage()+
                            self._reader.overallSystemCpuUsage()+
                            self._reader.overallIoWaitCpuUsage()+
                            self._reader.overallIrqCpuUsage())
      self._cpuUsageHistory = self._cpuUsageHistory[1:]
      
      self._cpuUsageSystemHistory.append(self._reader.overallSystemCpuUsage()+
                                  self._reader.overallIoWaitCpuUsage()+
                                  self._reader.overallIrqCpuUsage())
      self._cpuUsageSystemHistory = self._cpuUsageSystemHistory[1:]

      self._cpuUsageIoWaitHistory.append(self._reader.overallIoWaitCpuUsage() +
                                  self._reader.overallIrqCpuUsage())
      self._cpuUsageIoWaitHistory = self._cpuUsageIoWaitHistory[1:]

      self._cpuUsageIrqHistory.append(self._reader.overallIrqCpuUsage())
      self._cpuUsageIrqHistory = self._cpuUsageIrqHistory[1:]

      self._curveCpuHist.setData(range(int(self._settings["historySampleCount"])), self._cpuUsageHistory)
      self._curveCpuSystemHist.setData(range(int(self._settings["historySampleCount"])), self._cpuUsageSystemHistory)
      self._curveIoWaitHist.setData(range(int(self._settings["historySampleCount"])), self._cpuUsageIoWaitHistory)
      self._curveIrqHist.setData(range(int(self._settings["historySampleCount"])), self._cpuUsageIrqHistory)
      #TODO self._mainUi.qwtPlotOverallCpuHist.replot()

      logui.update()

      #update memory figures
      mem = self._reader.getMemoryUsage()
      totalSwap = mem[5]
      actualSwap = mem[4]
      self._mainUi.memory.setValue(int(mem[0]-mem[1]))
      self._mainUi.memory.setMaximum(int(mem[0])) 
      self._mainUi.swap.setValue(int(actualSwap))
      if totalSwap > 0:
        self._mainUi.swap.setMaximum(int(totalSwap))
      else:
        self._mainUi.swap.setMaximum(1)
      self._firstUpdate = False
    except:
      self._firstUpdate = False
      raise

if __name__ == "__main__":
  processExplorer = procexp()
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  app.exec()

