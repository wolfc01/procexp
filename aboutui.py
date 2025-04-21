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

from PyQt6 import QtGui, uic, QtWidgets
import os

def doAboutWindow():
  """Make an about window"""
  icon = os.path.dirname(__file__) + "/ui/icon.png"
  dialog = QtWidgets.QDialog()
  about = uic.loadUi(os.path.join(os.path.dirname(__file__), "./ui/about.ui"), baseinstance=dialog)
  about.label.setPixmap(QtGui.QPixmap(icon))
  dialog.exec()

