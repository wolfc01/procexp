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


#
# Display system overview
#


from PyQt4 import QtCore, QtGui
import PyQt4.Qwt5 as Qwt
import ui.systeminformation
import plotobjects


class memoryPlotObject(object):
  def __init__(self, plot, depth, reader):
    self.__curveMemHist__ = plotobjects.niceCurve("Memory History", 
                             1 ,QtGui.QColor(217,137,123), QtGui.QColor(180,70,50), 
                             plot)
    self.__depth__ = depth
    self.__reader__ = reader
    self.__first__ = False
    self.__plot__ = plot
    #adapt the memory plot
    
    self.__memoryUsageHistory__ = [0] * int(self.__depth__)
    
  def update(self, values):
    if self.__first__ == False:
      self.__first__ = True
      scale = plotobjects.scaleObject()
      scale.min = 0
      scale.max = values[0]
      self.__adaptedmemoryplot = plotobjects.procExpPlot(self.__plot__, scale)
    
    self.__memoryUsageHistory__.append(values[0]-values[1])
    self.__memoryUsageHistory__ = self.__memoryUsageHistory__[1:]
    self.__curveMemHist__.setData(range(self.__depth__), self.__memoryUsageHistory__)
    self.__plot__.replot()
                             
class cpuPlotObject(object):
  def __init__(self, plot, depth, reader, cpu):
    self.__curveCpuHist__ = plotobjects.niceCurve("CPU History", 
                             1 , QtGui.QColor(0,255,0),QtGui.QColor(0,170,0), 
                             plot)
    
    self.__curveCpuSystemHist__ = plotobjects.niceCurve("CPU Kernel History", 
                             1, QtGui.QColor(255,0,0),QtGui.QColor(170,0,0), 
                             plot)
                             
    self.__curveIoWaitHist__ = plotobjects.niceCurve("CPU IO wait history", 
                             1, QtGui.QColor(0,0,255),QtGui.QColor(0,0,127), 
                             plot)
    
    self.__curveIrqHist__ = plotobjects.niceCurve("CPU irq history", 
                             1, QtGui.QColor(0,255,255),QtGui.QColor(0,127,127), 
                             plot)
    
    scale = plotobjects.scaleObject()
    scale.min = 0
    scale.max = 100

    self.__adaptedplot__ = plotobjects.procExpPlot(plot, scale)  
    self.__plot__ = plot

    self.__depth__ = depth
    self.__reader__ = reader
    self.__cpu__ = cpu
    self.__cpuUsageHistory__ = [0] * int(self.__depth__)
    self.__cpuUsageSystemHistory__ = [0] * int(self.__depth__)
    self.__cpuUsageIoWaitHistory__ = [0] * int(self.__depth__)
    self.__cpuUsageIrqHistory__ = [0] * int(self.__depth__)
  def update(self):
    values = self.__reader__.getSingleCpuUsage(self.__cpu__)
    self.__cpuUsageHistory__.append(values[0]+values[1]+values[2]+values[3])
    self.__cpuUsageHistory__ = self.__cpuUsageHistory__[1:]
    
    
    self.__cpuUsageSystemHistory__.append(values[1]+values[2]+values[3])
    self.__cpuUsageSystemHistory__ = self.__cpuUsageSystemHistory__[1:]
    
    
    self.__cpuUsageIoWaitHistory__.append(values[2]+values[3])
    self.__cpuUsageIoWaitHistory__ = self.__cpuUsageIoWaitHistory__[1:]
    
    
    self.__cpuUsageIrqHistory__.append(values[3])
    self.__cpuUsageIrqHistory__ = self.__cpuUsageIrqHistory__[1:]
    


                                 
    self.__curveCpuHist__ .setData(range(self.__depth__), self.__cpuUsageHistory__)
    self.__curveCpuSystemHist__.setData(range(self.__depth__), self.__cpuUsageSystemHistory__)
    self.__curveIoWaitHist__.setData(range(self.__depth__), self.__cpuUsageIoWaitHistory__)
    self.__curveIrqHist__.setData(range(self.__depth__), self.__cpuUsageIrqHistory__)
    self.__plot__.replot()
    

class systemOverviewUi(object):
  def __init__(self, cpuCount, depth, reader):
    self.__reader__ = reader
    self.__depth__ = depth
    self.__dialog__ = QtGui.QDialog()
    self.__ui__ = ui.systeminformation.Ui_Dialog()
    self.__ui__.setupUi(self.__dialog__)
    self.__cpuCount__ = cpuCount
    self.__cpuPlotArray__ = []
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_01]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_02]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_03]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_04]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_05]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_06]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_07]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_08]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_09]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_10]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_11]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_12]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_13]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_14]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_15]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_16]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_17]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_18]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_19]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_20]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_21]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_22]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_23]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_24]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_25]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_26]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_27]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_28]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_29]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_30]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_31]]
    self.__cpuPlotArray__ += [[self.__ui__.qwtPlotCpuHist_32]]
    
    
    for cpu in xrange(32):
      if cpu+1 > self.__cpuCount__:
        self.__cpuPlotArray__[cpu][0].setVisible(False)
        self.__cpuPlotArray__[cpu].append(False)
      else:
        self.__cpuPlotArray__[cpu].append(True)
        
      if self.__cpuPlotArray__[cpu][1] == True:
        self.__cpuPlotArray__[cpu].append(cpuPlotObject(self.__cpuPlotArray__[cpu][0],
                                                         self.__depth__,
                                                         self.__reader__,
                                                         cpu))
                                                         
    self.__memPlot__ = memoryPlotObject(self.__ui__.qwtPlotMemoryHist,
                                                         self.__depth__,
                                                         self.__reader__)
  def show(self):
    self.__dialog__.show()
    self.__dialog__.setVisible(True)    
  
  def close(self):
    self.__dialog__.close()
    
  def setFontSize(self, fontSize):
    font = QtGui.QFont()
    font.setPointSize(fontSize)
    self.__dialog__.setFont(font)
    
    
  def update(self):
    for plot in xrange(32):
      if plot+1 <= self.__cpuCount__:
        self.__cpuPlotArray__[plot][2].update()
    memvalues = self.__reader__.getMemoryUsage()
    
    self.__ui__.memUsed.setText(str(memvalues[0]-memvalues[1]))
    self.__ui__.memTotal.setText(str(memvalues[0]))
    self.__ui__.memAvailable.setText(str(memvalues[1]))
    self.__ui__.memBuffers.setText(str(memvalues[2]))
    self.__ui__.memCached.setText(str(memvalues[3]))
    self.__ui__.swapUsed.setText(str(memvalues[4]))
    
    avg = self.__reader__.getLoadAvg()
    self.__ui__.last1minUtil.setText(str(avg[0][0]))
    self.__ui__.last5minUtil.setText(str(avg[0][1]))
    self.__ui__.last10minUtil.setText(str(avg[0][2]))
    self.__ui__.lastpid.setText(str(avg[3]))
    self.__ui__.procs.setText(str(avg[2])+"/"+str(avg[1]))
    self.__memPlot__.update(memvalues)
    
