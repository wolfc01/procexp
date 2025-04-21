g_stateCtr = 0

def simGetProcessInfo():
  global g_stateCtr
  g_stateCtr+=1
  procs = {}
  if g_stateCtr == 1:
    procs[1] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 0, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[2] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[3] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[4] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    deleted = []
    added = [1,2,3,4]
  elif g_stateCtr == 2:
    procs[1] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 0, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[2] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[3] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[4] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    deleted = []
    added = []
  elif g_stateCtr == 3:
    procs[1] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 0, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[2] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[3] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[4] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[5] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 4, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    deleted = []
    added = [5]
  elif g_stateCtr == 4:
    procs[1] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 0, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[2] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[3] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[4] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[5] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 4, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[6] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 5, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    deleted = []
    added = [6]
  elif g_stateCtr == 5:
    procs[1] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 0, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[2] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[3] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[4] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[6] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    deleted = [5]
    added = []
  elif g_stateCtr == 6:
    procs[1] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 0, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[2] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[3] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[4] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[6] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    deleted = []
    added = []
  elif g_stateCtr == 7:
    procs[1] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 0, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[2] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[3] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[4] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    deleted = [6]
    added = []
  elif g_stateCtr == 8:
    procs[1] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 0, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[2] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[3] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[4] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    deleted = []
    added = []
  elif g_stateCtr == 9:
    procs[1] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 0, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[2] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[3] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[4] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[5] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[6] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 5, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[7] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 5, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[8] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 5, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    deleted = []
    added = [5,6,7,8]
  elif g_stateCtr == 10:
    procs[1] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 0, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[2] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[3] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[4] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[6] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[7] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[8] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    deleted = [5]
    added = []
  elif g_stateCtr == 11:
    procs[1] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 0, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[2] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[3] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[4] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[6] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[7] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[8] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    deleted = []
    added = []
  elif g_stateCtr == 12:
    procs[1] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 0, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[2] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[3] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[4] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[7] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[8] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    deleted = [6]
    added = []
  elif g_stateCtr == 13:
    procs[1] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 0, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[2] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[3] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[4] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[8] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    deleted = [7]
    added = []
  elif g_stateCtr == 14:
    procs[1] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 0, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[2] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[3] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[4] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    deleted = [8]
    added = []
  elif g_stateCtr == 15:
    procs[1] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 0, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[2] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[3] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    procs[4] = {'name': 'test', 'env': '---', 'prevJiffy': 620, 'prevJiffyKernel': 35, 'prevIO': 4868954, 'PPID': 1, 'cpuUsage': 0.0, 'cmdline': '', 'uid': 'carl', 'wchan': '---', 'nfThreads': '27','hasListener': False, 'cpuUsageKernel': 0.0, 'Rss': 178996}
    deleted = []
    added = []
  #errorbox = QtWidgets.QMessageBox()
  #errorbox.setText("wait %s:\n" %g_stateCtr)
  #errorbox.exec()sleep 30 &
  if g_stateCtr >= 15:
    g_stateCtr = 2

  return procs, deleted, added