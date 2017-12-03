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

from PyQt4 import QtGui
import ui.about
import os
g_dialog = None

def doAboutWindow():
  """Make a log window"""
  global g_dialog
  icon = os.path.dirname(__file__) + "/ui/icon.png"
  g_dialog = QtGui.QDialog()
  about = ui.about.Ui_Dialog()
  about.setupUi(g_dialog)
  about.label.setPixmap(QtGui.QPixmap(icon))
  g_dialog.exec_()

  
