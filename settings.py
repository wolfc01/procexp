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


from PyQt6 import QtCore, QtGui, uic, QtWidgets
import os

ui = None

def onChange():
  try:
    nfSamples = int(str(ui.lineEditNfSamples.displayText())) * 1.0
    timesSecond = float(str(ui.lineEditTimesSecond.displayText()))
    fontSize = int(str(ui.lineEditFontSize.displayText()))
  except: 
    pass

def doSettings(millisecWait, depth, fontSize):
  global ui
  Dialog = QtWidgets.QDialog()
  settings = uic.loadUi(os.path.join(os.path.dirname(__file__), "./ui/settings.ui"), baseinstance=Dialog)
  settings.lineEditNfSamples.setText(str(depth))
  settings.lineEditTimesSecond.setText(str(1/(millisecWait/1000)))
  settings.lineEditFontSize.setText(str(fontSize))
  ui = settings
  Dialog.setModal(True)

  settings.lineEditNfSamples.textChanged.connect(onChange)
  settings.lineEditTimesSecond.textChanged.connect(onChange)
  settings.lineEditFontSize.textChanged.connect(onChange)

  Dialog.exec()
  
  millisecWait = int(1000.0 / float(str(ui.lineEditTimesSecond.displayText())))
  depth = int(str(ui.lineEditNfSamples.displayText()))
  fontSize = int(str(ui.lineEditFontSize.displayText()))
  return(millisecWait, depth, fontSize)
