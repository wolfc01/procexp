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


from PyQt6 import QtCore, QtGui
import pyqtgraph

class scaleObject:
  pass

class niceCurve(object):
  def __init__(self, name, penWidth, lineColor, fillColor, plot, depth):
    self.__plot = plot
    self.__lineColor = lineColor
    self.__fillColor = fillColor
    self.__name = name
    self.__penWidth = penWidth
    self.__depth = depth

    self.__line = plot.plot(
      range(self.__depth), 
      [0]*self.__depth,
      pen=pyqtgraph.mkPen(color=lineColor, width=penWidth),
      fillLevel=0, 
      brush=pyqtgraph.mkBrush(color=fillColor))
    
    plot.setBackground("w")
    plot.hideAxis("bottom")
    plot.hideAxis("left")

  def setData(self, x, y):
    self.__line.setData(x, y)

class procExpPlot(object):
  def __init__(self, qwtPlot, scale=None, hasGrid=True):
    return
    self.__plot__ = qwtPlot
    if hasGrid:
      self.__curveCpuPlotGrid= Qwt.QwtPlotGrid()
      self.__curveCpuPlotGrid.setMajPen(QtGui.QPen(QtGui.QColor(0,100,0), 0, QtCore.Qt.SolidLine))
      self.__curveCpuPlotGrid.setMinPen(QtGui.QPen(QtGui.QColor(0,100,0), 0, QtCore.Qt.SolidLine))
      self.__curveCpuPlotGrid.enableXMin(True)
      self.__curveCpuPlotGrid.attach(self.__plot__)  
    self.__plot__.setCanvasBackground(QtGui.QColor(0,0,0))
    self.__plot__.enableAxis(0, False )
    self.__plot__.enableAxis(2, False )
    if scale is None:
      #self.__plot__.setAxisScale(0,0,100,20)    
      pass
    else:
      self.__plot__.setAxisScale(0, scale.min, scale.max, (scale.max - scale.min) / 10.0)
  
