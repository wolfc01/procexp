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

from PyQt5 import uic, QtWidgets
import os
dialog = None
import configobj

g_settings = {}

def _loadMsgSettings():
  """ load messages earlier shown
  """
  global g_settings
  settingsPath = os.path.expanduser("~/.procexp/questions")
  if os.path.exists(settingsPath):
    f = open(settingsPath,"rb")
    settingsObj = configobj.ConfigObj(infile=f)
    g_settings=settingsObj.dict()

def _saveMsgSettings():
  """ save messages we dont want to see anymore
  """
  settingsPath = os.path.expanduser("~/.procexp")
  if not(os.path.exists(settingsPath)):
    os.makedirs(settingsPath)
  f = open(settingsPath + "/questions","wb")
  cfg = configobj.ConfigObj(g_settings)
  cfg.write(f)
  f.close()

def clearAllMessages():
  """ clear persisted messages we dont want to see
  """
  settingsPath = os.path.expanduser("~/.procexp/questions")
  if os.path.exists(settingsPath):
    os.remove(settingsPath)
  global g_settings
  g_settings = {}
  
def doMessageWindow(msg):
  """Make a message window"""
  _loadMsgSettings()
  if g_settings.has_key(msg):
    return
  global dialog
  dialog = QtWidgets.QDialog()
  msgDialog = uic.loadUi(os.path.join(os.path.dirname(__file__), "./ui/message.ui"), baseinstance=dialog)
  msgDialog.messageLabel.setText(msg)
  dialog.exec_()
  if msgDialog.showAgainCheckBox.isChecked():
    g_settings[msg] = True
    _saveMsgSettings()
