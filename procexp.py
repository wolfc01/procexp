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
from PyQt4 import QtCore, QtGui
import utils.procutils

app = QtGui.QApplication(sys.argv)

import procreader.reader
import ui.main
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

import cpuaffinity
import signal
import procreader.tcpip_stat as tcpip_stat
import rootproxy
import messageui

g_timer = None
g_reader = None
g_treeProcesses = {} #flat dictionary of processes
g_toplevelItems = {}
g_mainUi = None
g_onlyUser = True
g_greenTopLevelItems = {}
g_redTopLevelItems = {}
g_singleProcessUiList = {}
g_curveCpuHist = None
g_curveCpuSystemHist = None
g_curveIoWaitHist = None
g_curveIrqHist = None
g_curveCpuPlotGrid = None
g_cpuUsageHistory = None
g_cpuUsageSystemHistory = None
g_cpuUsageIoWaitHistory = None
g_cpuUsageIrqHistory = None
g_systemOverviewUi = None
g_networkOverviewUi = None
g_mainWindow = None
g_firstUpdate = True
g_procList = {}

#default settings
g_settings = {}
g_defaultSettings = \
{"fontSize": 10, 
 "columnWidths": [100,60,40,100,30,30,30,30],
 "updateTimer": 1000,
 "historySampleCount": 200
}

g_treeViewcolumns = ["Process","PID","CPU","Command Line", "User", "Chan","#thread"]


def performMenuAction(action):
  ''' perform action from menu
  '''
  global g_procList
  global g_onlyUser
  global g_settings
  global g_systemOverviewUi
  global g_networkOverviewUi
  if action is g_mainUi.actionKill_process:
    try:
      selectedItem = g_mainUi.processTreeWidget.selectedItems()[0]
    except IndexError:
      return
    process = selectedItem.data(1,0).toString()
    utils.procutils.killProcessHard(process)
  elif action is g_mainUi.actionKill_process_tree:
    try:
      selectedItem = g_mainUi.processTreeWidget.selectedItems()[0]
    except IndexError:
      return
    process = selectedItem.data(1,0).toString()
    killProcessTree(process, g_procList)
  elif action is g_mainUi.actionShow_process_from_all_users:
    if g_onlyUser:
      g_reader.noFilterUID()
      clearTree()
      g_onlyUser = False
    else:
      g_reader.setFilterUID(os.geteuid())
      clearTree()
      g_onlyUser = True
  elif action is g_mainUi.actionProperties:
    try:
      selectedItem = g_mainUi.processTreeWidget.selectedItems()[0]
    except IndexError:
      return
    process = str(selectedItem.data(1,0).toString())
    if g_singleProcessUiList.has_key(process):
      g_singleProcessUiList[process].makeVisible()
    else:
      if g_procList.has_key(int(process)):
        g_singleProcessUiList[process] = singleprocess.singleUi(process, g_procList[int(process)]["cmdline"], g_procList[int(process)]["name"], g_reader, int(g_settings["historySampleCount"]))
  elif action is g_mainUi.actionSaveSettings:
    saveSettings()
  elif action is g_mainUi.actionSettings:
    msec, depth, fontSize = settingsMenu.doSettings(int(g_settings["updateTimer"]),\
                                                       int(g_settings["historySampleCount"]), \
                                                       int(g_settings["fontSize"]))
    g_settings["updateTimer"] = int(msec)
    g_settings["historySampleCount"] = int(depth)
    g_settings["fontSize"] = int(fontSize)
    setFontSize(fontSize)
  elif action is g_mainUi.actionSystem_information:
    g_systemOverviewUi.show()
  elif action is g_mainUi.actionNetwork_Information:
    g_networkOverviewUi.show()
  elif action is g_mainUi.actionClose_all_and_exit:
    for window in g_singleProcessUiList:
      g_singleProcessUiList[window].closeWindow()
    g_systemOverviewUi.close()
    g_networkOverviewUi.close()
    g_mainWindow.close()
    if logui.dialog is not None:
      logui.dialog.close()
    if aboutui.dialog is not None:
      aboutui.dialog.close()
  elif action is g_mainUi.actionColor_legend:
    colorlegend.doColorHelpLegend()
  elif action is g_mainUi.actionSet_affinity:
    try:
      selectedItem = g_mainUi.processTreeWidget.selectedItems()[0]
      process = str(selectedItem.data(1,0).toString())
    except IndexError:
      return
    cpuaffinity.doAffinity(g_reader.getCpuCount(), process)
  elif action is g_mainUi.actionLog:
    logui.doLogWindow()
  elif action is g_mainUi.actionAbout:
    aboutui.doAboutWindow()
  elif action is g_mainUi.actionClear_Messages:
    messageui.clearAllMessages()
  else:
    utils.procutils.log("This action (%s)is not yet supported." %action)

def setFontSize(fontSize):
  global g_settings
  g_settings["fontSize"] = fontSize
  font = QtGui.QFont()
  font.setPointSize(fontSize)
  g_mainUi.menuFile.setFont(font)
  g_mainUi.menuOptions.setFont(font)
  g_mainUi.menuView.setFont(font)
  g_mainUi.menuProcess.setFont(font)
  g_mainUi.menuSettings.setFont(font)
  g_mainUi.menubar.setFont(font)
  g_mainUi.processTreeWidget.setFont(font)
  if g_systemOverviewUi is not None:
    g_systemOverviewUi.setFontSize(fontSize)
  if g_networkOverviewUi is not None:
    g_networkOverviewUi.setFontSize(fontSize)

def loadSettings():
  global g_settings
  settingsPath = os.path.expanduser("~/.procexp/settings")
  if os.path.exists(settingsPath):
    f = file(settingsPath,"rb")
    settingsObj = configobj.ConfigObj(infile=f)
    g_settings=settingsObj.dict()
    
  #load default settings for undefined settings
  for item in g_defaultSettings:
    if g_settings.has_key(item):
      pass
    else:
      g_settings[item] = g_defaultSettings[item]
    
  fontsize = int(g_settings["fontSize"])
  setFontSize(fontsize)
  
  #set the columnwidths
  for headerSection in range(g_mainUi.processTreeWidget.header().count()):
    try:
      width = int(g_settings["columnWidths"][headerSection])
    except:
      width = 150
    g_mainUi.processTreeWidget.header().resizeSection(headerSection,width)
    
  #load default settings for undefined settings
  for item in g_defaultSettings:
    if g_settings.has_key(item):
      pass
    else:
      g_settings[item] = g_defaultSettings[item]
      
  global g_cpuUsageHistory
  global g_cpuUsageSystemHistory
  global g_cpuUsageIoWaitHistory
  global g_cpuUsageIrqHistory
  
  g_cpuUsageHistory = [0] * int(g_settings["historySampleCount"])
  g_cpuUsageSystemHistory = [0] * int(g_settings["historySampleCount"])
  g_cpuUsageIoWaitHistory = [0] * int(g_settings["historySampleCount"])
  g_cpuUsageIrqHistory = [0] * int(g_settings["historySampleCount"])


def saveSettings():
  '''save settings to ~.procexp directory, in file "settings"
  '''
  widths = []
  for headerSection in range(g_mainUi.processTreeWidget.header().count()):
    widths.append(g_mainUi.processTreeWidget.header().sectionSize(headerSection))
  g_settings["columnWidths"] = widths
  
  settingsPath = os.path.expanduser("~/.procexp")
  if not(os.path.exists(settingsPath)):
    os.makedirs(settingsPath)
  f = file(settingsPath + "/settings","wb")
  cfg = configobj.ConfigObj(g_settings)
  cfg.write(f)
  f.close()

def onContextMenu(point):
  global g_mainUi
  g_mainUi.menuProcess.exec_(g_mainUi.processTreeWidget.mapToGlobal(point))

def onHeaderContextMenu(point):
  menu = QtGui.QMenu()
  for idx, col in enumerate(g_treeViewcolumns):
    action = QtGui.QAction(col, g_mainUi.processTreeWidget)
    action.setCheckable(True)
    action.setChecked(not g_mainUi.processTreeWidget.isColumnHidden(idx))
    action.setData(idx)
    menu.addAction(action)
  selectedItem = menu.exec_(g_mainUi.processTreeWidget.mapToGlobal(point))
  if selectedItem is not None:
    g_mainUi.processTreeWidget.setColumnHidden(selectedItem.data().toInt()[0], not selectedItem.isChecked())
  
def prepareUI(mainUi):
  """ prepare the main UI, setup plots and menu triggers
  """
  global g_timer
  
  mainUi.processTreeWidget.setColumnCount(len(g_treeViewcolumns))
  
  mainUi.processTreeWidget.setHeaderLabels(g_treeViewcolumns)
  mainUi.processTreeWidget.header().setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
  mainUi.processTreeWidget.header().customContextMenuRequested.connect(onHeaderContextMenu)

  #create a timer which triggers the process explorer to update its contents
  g_timer = QtCore.QTimer(mainUi.processTreeWidget)
  QtCore.QObject.connect(g_timer, QtCore.SIGNAL("timeout()"), updateUI)
  QtCore.QObject.connect(mainUi.processTreeWidget, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), onContextMenu)
  QtCore.QObject.connect(mainUi.menuFile,  QtCore.SIGNAL('triggered(QAction*)'), performMenuAction)
  QtCore.QObject.connect(mainUi.menuProcess,  QtCore.SIGNAL('triggered(QAction*)'), performMenuAction)
  QtCore.QObject.connect(mainUi.menuOptions,  QtCore.SIGNAL('triggered(QAction*)'), performMenuAction)
  QtCore.QObject.connect(mainUi.menuSettings, QtCore.SIGNAL('triggered(QAction*)'), performMenuAction)
  QtCore.QObject.connect(mainUi.menuView, QtCore.SIGNAL('triggered(QAction*)'), performMenuAction)
  QtCore.QObject.connect(mainUi.menuHelp, QtCore.SIGNAL('triggered(QAction*)'), performMenuAction)
  
  #prepare the plot
  global g_curveCpuHist
  global g_curveCpuSystemHist
  global g_curveIoWaitHist
  global g_curveIrqHist
  global g_curveCpuPlotGrid
  
  g_curveCpuHist = plotobjects.niceCurve("CPU History",
                           1 , QtGui.QColor(0,255,0),QtGui.QColor(0,170,0), 
                           mainUi.qwtPlotOverallCpuHist)
  
  g_curveCpuSystemHist = plotobjects.niceCurve("CPU Kernel History",
                           1, QtGui.QColor(255,0,0),QtGui.QColor(170,0,0), 
                           mainUi.qwtPlotOverallCpuHist)
                           
  g_curveIoWaitHist = plotobjects.niceCurve("CPU IO wait history",
                           1, QtGui.QColor(0,0,255),QtGui.QColor(0,0,127), 
                           mainUi.qwtPlotOverallCpuHist)
  
  g_curveIrqHist = plotobjects.niceCurve("CPU irq history",
                           1, QtGui.QColor(0,255,255),QtGui.QColor(0,127,127), 
                           mainUi.qwtPlotOverallCpuHist)

  scale = plotobjects.scaleObject()
  scale.min = 0
  scale.max = 100
  _ = plotobjects.procExpPlot(mainUi.qwtPlotOverallCpuHist, scale, hasGrid=False)
  
def clearTree():
  """ clear the tree of processes.
  """
  global g_mainUi
  global g_treeProcesses
  global g_toplevelItems
  global g_greenTopLevelItems
  global g_redTopLevelItems
  
  g_mainUi.processTreeWidget.clear()
  g_treeProcesses = {}
  g_toplevelItems = {}
  g_greenTopLevelItems = {}
  g_redTopLevelItems = {}
  
def killProcessTree(proc, procList):
  """ Kill a tree of processes, the hard way
  """
  killChildsTree(int(str(proc)), procList)
  utils.procutils.killProcessHard(int(str(proc)))

def killChildsTree(proc, procList):
  """ kill all childs of given process
  """
  for aproc in procList:
    if procList[aproc]["PPID"] == proc:
      killChildsTree(aproc, procList)
      utils.procutils.killProcess(aproc)
     
def addProcessAndParents(proc, procList):
  """ adds a process and its parents to the tree of processes
  """
  global g_mainUi
  
  if g_treeProcesses.has_key(proc): #process already exists, do nothing
    return g_treeProcesses[proc]
    
  g_treeProcesses[proc] = QtGui.QTreeWidgetItem([])
  g_greenTopLevelItems[proc] = g_treeProcesses[proc]
  
  if procList[proc]["PPID"] > 0 and procList.has_key(procList[proc]["PPID"]): #process has a parent
    parent = addProcessAndParents(procList[proc]["PPID"],procList)
    parent.addChild(g_treeProcesses[proc])
  else: #process has no parent, thus it is toplevel. add it to the treewidget
    g_mainUi.processTreeWidget.addTopLevelItem(g_treeProcesses[proc])
    g_toplevelItems[proc] = g_treeProcesses[proc]
  
  return g_treeProcesses[proc]
  
def delChild(item, childtodelete):
  """ Delete child, search recursively
  """
  if item != None:
    for index in xrange(item.childCount()):
      thechild = item.child(index)
      if thechild != None:
        if thechild == childtodelete:
          item.takeChild(index)
        else:
          delChild(thechild, childtodelete)
          
def expandChilds(parent):
  """ expand all childs of given parent
  """
  global g_mainUi
  for index in xrange(parent.childCount()):
    thechild = parent.child(index)
    if thechild != None:
      g_mainUi.processTreeWidget.expandItem(thechild)
      expandChilds(thechild)
    else:
      g_mainUi.processTreeWidget.expandItem(parent)

def expandAll():
  """ expand all subtrees
  """
  global g_mainUi
  for topLevelIndex in xrange(g_mainUi.processTreeWidget.topLevelItemCount()):
    item = g_mainUi.processTreeWidget.topLevelItem(topLevelIndex)
    expandChilds(item)

def updateUI():
  """update"""
  tcpip_stat.tick()
  try:
    global g_procList
    global g_treeProcesses, g_greenTopLevelItems, g_redTopLevelItems
    global g_mainUi
    global g_firstUpdate
    
    if g_mainUi.freezeCheckBox.isChecked():
      return
    
    g_reader.doReadProcessInfo()
    g_procList, closedProc, newProc = g_reader.getProcessInfo()

    #color all green processes with default background
    defaultBgColor = app.palette().color(QtGui.QPalette.Base)  
    for proc in g_greenTopLevelItems:
      for column in xrange(g_greenTopLevelItems[proc].columnCount()):
        g_greenTopLevelItems[proc].setBackgroundColor(column, defaultBgColor)
    g_greenTopLevelItems = {}
   
    #delete all red widgetItems
    for proc in g_redTopLevelItems:
      for topLevelIndex in xrange(g_mainUi.processTreeWidget.topLevelItemCount()):
        topLevelItem = g_mainUi.processTreeWidget.topLevelItem(topLevelIndex)
        delChild(topLevelItem, g_redTopLevelItems[proc])
        if topLevelItem == g_redTopLevelItems[proc]:
          g_mainUi.processTreeWidget.takeTopLevelItem(topLevelIndex)
          
    g_redTopLevelItems = {}
    
    #create new items and mark items to be deleted red
    #draw tree hierarchy of processes
    for proc in newProc:
      widgetItem = addProcessAndParents(proc, g_procList)

    #if the process has childs which do still exist, "reparent" the child.
    for proc in g_procList:
      if g_procList[proc]["PPID"] == 0:
        item = g_treeProcesses[proc]
        if item.parent() is not None:
          parentItem = item.parent()
          for idx in xrange(parentItem.childCount()):
            if item == parentItem.child(idx):
              parentItem.takeChild(idx)
          g_mainUi.processTreeWidget.addTopLevelItem(g_treeProcesses[proc])

    #copy processed to be deleted to the red list      
    for proc in closedProc:
      try:
        g_redTopLevelItems[proc] = g_treeProcesses[proc]
      except KeyError:
        pass
     
    #color all deleted processed red
    for proc in g_redTopLevelItems:
      try:
        for column in xrange(g_redTopLevelItems[proc].columnCount()):
          g_redTopLevelItems[proc].setBackgroundColor(column, QtGui.QColor(255,0,0))
      except RuntimeError:
        pass 
    
    #update status information about the processes  
    try:
      for proc in g_procList:
        g_treeProcesses[proc].setData(0, 0, g_procList[proc]["name"])
        g_treeProcesses[proc].setData(1, 0, str(proc))
        g_treeProcesses[proc].setData(2, 0, g_procList[proc]["cpuUsage"])
        g_treeProcesses[proc].setData(3, 0, g_procList[proc]["cmdline"])
        g_treeProcesses[proc].setData(4, 0, g_procList[proc]["uid"])
        g_treeProcesses[proc].setData(5, 0, g_procList[proc]["wchan"])
        g_treeProcesses[proc].setData(6, 0, g_procList[proc]["nfThreads"])
    except RuntimeError:
      #underlying c++ object has been deleted
      pass

    for proc in closedProc:
      try:
        del g_treeProcesses[proc]
      except KeyError:
        pass

    #color all new processes 'green'
    if g_firstUpdate == False:
      for proc in g_greenTopLevelItems:
        item = g_greenTopLevelItems[proc]
        for column in xrange(item.columnCount()):
          item.setBackgroundColor(column, QtGui.QColor(0,255,0))
      
    if (len(closedProc) > 0) or (len(newProc) > 0):
      expandAll()
    
    for ui in g_singleProcessUiList:
      g_singleProcessUiList[ui].update()
      
    #update CPU plots
    g_systemOverviewUi.update()
    
    #network plots
    g_networkOverviewUi.update()
      
    #update the cpu graph
    global g_cpuUsageHistory
    global g_cpuUsageSystemHistory
    global g_cpuUsageIoWaitHistory
    global g_cpuUsageIrqHistory
    
    global g_curveCpuHist
    global g_curveCpuSystemHist
    global g_curveIrqHist
    global g_curveIoWaitHist
    global g_curveCpuPlotGrid
    
    g_cpuUsageHistory.append(g_reader.overallUserCpuUsage()+
                           g_reader.overallSystemCpuUsage()+
                           g_reader.overallIoWaitCpuUsage()+
                           g_reader.overallIrqCpuUsage())
    g_cpuUsageHistory = g_cpuUsageHistory[1:]
    
    g_cpuUsageSystemHistory.append(g_reader.overallSystemCpuUsage()+
                                 g_reader.overallIoWaitCpuUsage()+
                                 g_reader.overallIrqCpuUsage())
    g_cpuUsageSystemHistory = g_cpuUsageSystemHistory[1:]

    g_cpuUsageIoWaitHistory.append(g_reader.overallIoWaitCpuUsage() +
                                 g_reader.overallIrqCpuUsage())
    g_cpuUsageIoWaitHistory = g_cpuUsageIoWaitHistory[1:]

    g_cpuUsageIrqHistory.append(g_reader.overallIrqCpuUsage())
    g_cpuUsageIrqHistory = g_cpuUsageIrqHistory[1:]

    g_curveCpuHist.setData(range(int(g_settings["historySampleCount"])), g_cpuUsageHistory)
    g_curveCpuSystemHist.setData(range(int(g_settings["historySampleCount"])), g_cpuUsageSystemHistory)
    g_curveIoWaitHist.setData(range(int(g_settings["historySampleCount"])), g_cpuUsageIoWaitHistory)
    g_curveIrqHist.setData(range(int(g_settings["historySampleCount"])), g_cpuUsageIrqHistory)
    g_mainUi.qwtPlotOverallCpuHist.replot()

    logui.update()

    #update memory figures
    mem = g_reader.getMemoryUsage()
    totalSwap = mem[5]
    actualSwap = mem[4]
    g_mainUi.memory.setValue(mem[0]-mem[1])
    g_mainUi.memory.setMaximum(mem[0])
    g_mainUi.swap.setValue(actualSwap)
    if totalSwap > 0:
      g_mainUi.swap.setMaximum(totalSwap)
    else:
      g_mainUi.swap.setMaximum(1)

  except:
    import traceback
    utils.procutils.log("Unhandled exception:%s" %traceback.format_exc())
    print traceback.format_exc()
  
  g_firstUpdate = False

if __name__ == "__main__":

  g_mainWindow = QtGui.QMainWindow()
  g_mainUi = ui.main.Ui_MainWindow()
  g_mainUi.setupUi(g_mainWindow)

  prepareUI(g_mainUi)
  loadSettings()

  g_mainWindow.show()
  app.processEvents()

  rootproxy.start(asRoot=True)
  if not rootproxy.isStarted():
    messageui.doMessageWindow("Process explorer has no root privileges. TCPIP traffic monitoring (using tcpdump) will not be available.")

  g_reader = procreader.reader.procreader(int(g_settings["updateTimer"]), int(g_settings["historySampleCount"]))

  g_timer.start(int(g_settings["updateTimer"]))

  if g_onlyUser:
    g_reader.setFilterUID(os.geteuid())

  g_systemOverviewUi = systemoverview.systemOverviewUi(g_reader.getCpuCount(), int(g_settings["historySampleCount"]), g_reader)
  g_networkOverviewUi = networkoverview.networkOverviewUi(g_reader.getNetworkCards(), int(g_settings["historySampleCount"]), g_reader)

  g_systemOverviewUi.setFontSize(int(g_settings["fontSize"]))
  g_networkOverviewUi.setFontSize(int(g_settings["fontSize"]))

  updateUI()

  signal.signal(signal.SIGINT, signal.SIG_DFL)

  app.exec_()
  tcpip_stat.stop()
  rootproxy.end()
  sys.exit()

