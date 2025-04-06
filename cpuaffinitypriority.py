from PyQt5 import QtGui, uic, QtWidgets
import subprocess
import os
import utils.procutils as procutils


def doAffinityPriority(cpuCount, process):
  """ setup and handle the cpu affinity menu.
  """
  dialog = QtWidgets.QDialog()
  gui = uic.loadUi(os.path.join(os.path.dirname(__file__), "./ui/cpuaffinity.ui"), baseinstance=dialog)
  
  #get affinity of process
  affinityHexStr =subprocess.Popen(["taskset", "-p", str(process)], \
                                   stdout=subprocess.PIPE).communicate()[0].strip().split(b"affinity mask: ")[1]
  
  affinity = int(affinityHexStr, 16)

  priority = subprocess.Popen(["ps", "-o", 'pri', "-p", str(process)], \
                                   stdout=subprocess.PIPE).communicate()[0].strip().split(b"\n")[1].strip().decode()
  gui.lineEditPriority.setText(priority)

  #fill the grid with checkboxes
  grid = gui.__dict__["gridLayout"]
  row = 0
  col = 0

  if cpuCount <= 8:
    rowMax = 4
  elif cpuCount <= 32:
    rowMax = 8
  elif cpuCount <= 128:
    rowMax = 16
  else:
    rowMax = 24

  for cpu in range(cpuCount):
    cb = QtWidgets.QCheckBox("checkBox_%s" %cpu)
    cb.setText("CPU_%s" %cpu)
    grid.addWidget(cb, row, col)
    row += 1
    if row > rowMax-1:
      row = 0
      col += 1

  #check CPU checkboxes
  for cpu in range(cpuCount):
    for w in gui.findChildren(QtWidgets.QCheckBox):
      objName = w.text()
      if objName == "CPU_%s" %cpu:
        if affinity & 2**cpu == 2**cpu:
          w.setChecked(True)
        else:
          w.setChecked(False)
          
  dialog.setModal(True)
  dialog.exec_()

  #apply new affinity
  newAff = 0
  for cpu in range(cpuCount):
    for w in gui.findChildren(QtWidgets.QCheckBox):
      objName = w.text()
      if objName == "CPU_%s" %cpu:
        if w.isChecked():
          newAff = newAff | 2**cpu

  if affinity != newAff:
    proc = subprocess.Popen(["taskset", "-p", hex(newAff).replace("0x",""), str(process)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()
    result = proc.returncode
    if result != 0:
      procutils.message("Setting process %s affinity value to %s failed" %(process, hex(newAff).replace("0x","")))

  newPrio = gui.lineEditPriority.text()
  if newPrio != priority:
    proc = subprocess.Popen(["renice", "-n", newPrio, "-p", str(process)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data = proc.communicate()
    result = proc.returncode
    if result != 0:
      procutils.message("Setting process %s priority value to %s failed. \n\nmessage=%s" %(process, newPrio, data[1].decode()))

  
  
  