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
import ui.settings as settingsMenu


global ui

def onChange():
  global ui
  
  try:
    nfSamples = int(str(ui.lineEditNfSamples.displayText())) * 1.0
    timesSecond = float(str(ui.lineEditTimesSecond.displayText()))
  
    ui.lineEditMinutes.setText(str(round(nfSamples / timesSecond / 60.0,2)))
    ui.lineEditDays.setText(str(round((nfSamples / timesSecond) / (24.0*60.0*60.0),2)))
    ui.lineEditHours.setText(str(round((nfSamples / timesSecond) / (60.0*60.0),2)))
  except:
    ui.lineEditMinutes.setText("?")
    ui.lineEditDays.setText("?")
    ui.lineEditHours.setText("?")
  

def doSettings(millisecWait, depth, fontSize):
  global ui
  Dialog = QtGui.QDialog()
  settings = settingsMenu.Ui_Dialog()
  settings.setupUi(Dialog)
  ui = settings
  Dialog.setModal(True)
  QtCore.QObject.connect(settings.lineEditNfSamples,  QtCore.SIGNAL('textChanged (const QString&)'), onChange)
  QtCore.QObject.connect(settings.lineEditTimesSecond,  QtCore.SIGNAL('textChanged (const QString&)'), onChange)
  ui.lineEditTimesSecond.setText(str(float(1000.0 / (millisecWait * 1.0))))
  ui.lineEditNfSamples.setText(str(depth))
  ui.lineEditFontSize.setText(str(fontSize))
  Dialog.exec_()
  
  millisecWait = int(1000.0 / float(str(ui.lineEditTimesSecond.displayText())))
  depth = int(str(ui.lineEditNfSamples.displayText()))
  fontSize = int(str(ui.lineEditFontSize.displayText()))
  return(millisecWait, depth, fontSize)
