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
# implements a message UI capable of supressing messages which the user already knows
#

from PyQt6 import uic, QtWidgets
import os
import configobj

class settingsDialog():
  def __init__(self):
    self._settings = {}

  def _loadMsgSettings(self):
    """ load messages earlier shown
    """
    settingsPath = os.path.expanduser("~/.procexp/questions")
    if os.path.exists(settingsPath):
      f = open(settingsPath,"rb")
      settingsObj = configobj.ConfigObj(infile=f)
      self._settings=settingsObj.dict()

  def _saveMsgSettings(self):
    """ save messages we dont want to see anymore
    """
    settingsPath = os.path.expanduser("~/.procexp")
    if not(os.path.exists(settingsPath)):
      os.makedirs(settingsPath)
    f = open(settingsPath + "/questions","wb")
    cfg = configobj.ConfigObj(self._settings)
    cfg.write(f)
    f.close()

  def clearAllMessages(self):
    """ clear persisted messages we dont want to see
    """
    settingsPath = os.path.expanduser("~/.procexp/questions")
    if os.path.exists(settingsPath):
      os.remove(settingsPath)
    self._settings = {}
    
  def doMessageWindow(self, msg):
    """Make a message window"""
    self._loadMsgSettings()
    if msg in self._settings:
      return
    dialog = QtWidgets.QDialog()
    msgDialog = uic.loadUi(os.path.join(os.path.dirname(__file__), "./ui/message.ui"), baseinstance=dialog)
    msgDialog.messageLabel.setText(msg)
    dialog.exec()
    if msgDialog.showAgainCheckBox.isChecked():
      self._settings[msg] = True
      self._saveMsgSettings()
