class ProcEntry(object):
  def __init__(self, startValue):
    self._fields = {}
    for _ in xrange(startValue.count("><")):
      start =  startValue.find("<")
      end   =  startValue.find(">")
      startValue = startValue[:start] + startValue[start+1:end] +startValue[end+1:]
      fieldNo =  int(startValue[startValue.find("<")+1  :startValue.find(">") ])
      self._fields[fieldNo] = (start, end-1)
      startValue = startValue[:startValue.find("<")] + startValue[startValue.find(">")+1:]
    self._raw = startValue
    self._rawOrig = startValue
  def modify(self, l):
    self._raw = self._rawOrig
    prevEnd = 0
    new = ""
    for modifications in l:
      f = modifications[0]
      newValue = modifications[1]
      start = self._fields[f][0]
      end   = self._fields[f][1]
      new += self._raw[prevEnd:start] + str(newValue)
      prevEnd = end
    new += self._raw[end:]
    self._raw = new 
    return(self._raw)   
  def __str__(self):
    return self._raw 
  def restore(self):
    self._raw = self._rawOrig



cpuInfo = ProcEntry("""
processor  : 0
vendor_id  : GenuineIntel
cpu family  : 6
model    : 42
model name  : Intel(R) Core(TM) i7-2720QM CPU @ 2.20GHz
stepping  : 7
cpu MHz    : 2195.089
cache size  : 6144 KB
fdiv_bug  : no
hlt_bug    : no
<f00f_bug  : no><1>
coma_bug  : no
fpu    : yes
fpu_exception  : yes
cpuid level  : 13
wp    : yes
flags    : fpu vme de pse tsc msr pae mce cx8 apic mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss nx rdtscp lm constant_tsc up arch_perfmon pebs bts xtopology tsc_reliable nonstop_tsc aperfmperf pni pclmulqdq ssse3 cx16 sse4_1 sse4_2 popcnt aes xsave avx hypervisor lahf_lm ida arat epb xsaveopt pln pts dts
bogomips  : 4390.17
clflush size  : 64
cache_alignment  : 64
address sizes  : 40 bits physical, 48 bits virtual
power management:
"""
)

loadavg = ProcEntry("""0.14 0.13 0.14 6/335 10051
""")

procnetdev=ProcEntry("""Inter-|   Receive                                                |  Transmit
 face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
    lo: 1000212     738    0    0    0     0          0         0  1000212     738    0    0    0     0       0          0
  eth0: 13421550   12992    0    0    0     0          0         0   996365    8726    0    0    0     0       0          0

""")

procNetTcp = ProcEntry("""
  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode                                                     
   0: 00000000:0016 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 7543 1 00000000 300 0 0 2 -1                              
   1: 0100007F:0277 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 16428 1 00000000 300 0 0 2 -1                             
   2: 0100007F:8D7A 0100007F:9357 01 00000000:00000000 00:00000000 00000000  1000        0 15314 1 00000000 20 4 28 10 -1                            
   3: 0100007F:E984 0100007F:A4FD 01 00000000:00000000 00:00000000 00000000  1000        0 15319 1 00000000 20 0 0 10 -1                             
""")

procNetUdp = ProcEntry("""
  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode ref pointer drops             
  124: 00000000:0044 00000000:0000 07 00000000:00000000 00:00000000 00000000     0        0 56620 2 00000000 0                 
  289: 00000000:14E9 00000000:0000 07 00000000:00000000 00:00000000 00000000   106        0 7674 2 00000000 0                  
  334: 00000000:9516 00000000:0000 07 00000000:00000000 00:00000000 00000000   106        0 7676 2 00000000 0                  
""")

memInfo = ProcEntry("""MemTotal:        2061904 kB
MemFree:          825428 kB
Buffers:          201072 kB
Cached:           437540 kB
SwapCached:            0 kB
Active:           888652 kB
Inactive:         258564 kB
Active(anon):     348988 kB
Inactive(anon):   164536 kB
Active(file):     539664 kB
Inactive(file):    94028 kB
Unevictable:          16 kB
Mlocked:              16 kB
HighTotal:       1187720 kB
HighFree:         322696 kB
LowTotal:         874184 kB
LowFree:          502732 kB
SwapTotal:       1046524 kB
SwapFree:        1046428 kB
Dirty:                20 kB
Writeback:             0 kB
AnonPages:        508640 kB
Mapped:           109516 kB
Shmem:              4920 kB
Slab:              70164 kB
SReclaimable:      58972 kB
SUnreclaim:        11192 kB
KernelStack:        2640 kB
PageTables:         6456 kB
NFS_Unstable:          0 kB
Bounce:                0 kB
WritebackTmp:          0 kB
CommitLimit:     2077476 kB
Committed_AS:    1991700 kB
VmallocTotal:     122880 kB
VmallocUsed:        6760 kB
VmallocChunk:     110544 kB
HardwareCorrupted:     0 kB
AnonHugePages:         0 kB
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       4096 kB
DirectMap4k:       16376 kB
DirectMap4M:      892928 kB
""")

proc10stat=ProcEntry("""5356 (bash) S 5353 5356 5356 34818 11889 4202496 11878 128443 0 31 32 14 227 56 20 0 1 0 1103941 8671232 1156 4294967295 134512640 135406788 3219366944 3219365732 4269078 0 65536 3686404 1266761467 3238311109 0 0 17 0 0 0 0 0 0
""")
proc20stat=ProcEntry("""5357 (bash) S 5353 5356 5356 34818 11889 4202496 11878 128443 0 31 32 14 227 56 20 0 1 0 1103941 8671232 1156 4294967295 134512640 135406788 3219366944 3219365732 4269078 0 65536 3686404 1266761467 3238311109 0 0 17 0 0 0 0 0 0
""")

procstat = ProcEntry("""cpu  <173357><1> <5980><2> <35238><3> <2866149><4> 24978 0 742 0 0 0
cpu0 173357 5980 35238 2866149 24978 0 742 0 0 0
intr 5268205 150 64436 0 0 0 0 3 0 1 0 0 0 1090723 0 0 93269 74734 102290 1449 32546 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
ctxt 17690761
btime 1333373449
processes 14122
procs_running 6
procs_blocked 0
softirq 2059979 0 770654 19909 33150 131765 0 41511 0 2196 1060794
""")
