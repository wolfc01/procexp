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

  #disable cpu checkboxes of the cpu's.
  for objName in gui.__dict__:
    if objName.find("checkBox_") != -1:
      cpuNr = int(objName.split("_")[1])
      if cpuNr < cpuCount:
        gui.__dict__[objName].setEnabled(True)
      else:
        gui.__dict__[objName].setEnabled(False)
  
  #check CPU checkboxes
  for cpu in range(cpuCount):
    for objName in gui.__dict__:
      if objName == "checkBox_%s" %cpu:
        if affinity & 2**cpu == 2**cpu:
          gui.__dict__[objName].setChecked(True)
        else:
          gui.__dict__[objName].setChecked(False)
          
  dialog.setModal(True)
  dialog.exec_()

  #apply new affinity
  newAff = 0
  for cpu in range(cpuCount):
    for objName in gui.__dict__:
      if objName == "checkBox_%s" %cpu:
        if gui.__dict__[objName].isChecked():
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

  
  
  