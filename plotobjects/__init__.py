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


from PyQt4 import QtCore, QtGui
import PyQt4.Qwt5 as Qwt

class scaleObject:
  pass

class niceCurve(object):
  def __init__(self, name, penWidth, lineColor, fillColor, plot):
    self.__curve__ = Qwt.QwtPlotCurve(name)
    pen = QtGui.QPen(lineColor)
    pen.setWidth(penWidth)
    self.__curve__.setPen(pen)
    self.__curve__.setBrush(fillColor)
    self.__curve__.attach(plot)
    
    #work around to get nicer plotting.
    self.__curveExt__ = Qwt.QwtPlotCurve(name+" extra")
    self.__curveExt__.setPen(QtGui.QPen(lineColor))
    self.__curveExt__.attach(plot)
  def setData(self, x, y):
    self.__curve__.setData(x, y)
    self.__curveExt__.setData(x,y)



class procExpPlot(object):
  def __init__(self, qwtPlot, scale=None, hasGrid=True):
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
  
