'''Log window'''
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

from PyQt4.QtGui import QDialog
from PyQt4 import uic
from utils.procutils import getLog
import os

class _LogWindowWrapper(object):
  '''Manage the procexp log window.'''
  def __init__(self):
    self._dialog = None
    self._log_ui = None

  def createDialog(self):
    '''Create and show dialog window.'''
    if not self._dialog:
      self._dialog = QDialog()
      self._log_ui = uic.loadUi(os.path.join(os.path.dirname(__file__), "./ui/log.ui"), baseinstance=self._dialog)
    self._dialog.show()

  def update(self):
    '''Append latest log text.'''
    if self._log_ui:
      logs = getLog()
      oldText = str(self._log_ui.plainTextEdit.toPlainText())
      newText = oldText + logs
      self._log_ui.plainTextEdit.setPlainText(newText)

  def close(self):
    '''Close this dialog'''
    print("close")
    if self._dialog:
      self._dialog.close()

_inst = _LogWindowWrapper()
doLogWindow = _inst.createDialog
update = _inst.update
closeLogWindow = _inst.close