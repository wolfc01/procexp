"""automatic test suite for process explorer
   Run this on a quad cpu machine
"""
import subprocess

try:
  subprocess.Popen(["killall", "python"])
except: 
  pass

def start_processexplorer():
    p = subprocess.Popen(["python","/home/cpwolff/procexp/code/trunk/procexp.py"])
    #p = subprocess.Popen("procexp.sh")
     
    wait("1388491619153.png", 20)
    type(Pattern("1388491661459.png").targetOffset(-175,-21), "test")
    click("1388435311540.png")   
    click("1388436794512.png")

def maximize_process_explorer():
    #process explorer full size
    type(Key.SPACE, KEY_ALT)
    type("x") 
    click(Pattern("1388478858825.png").similar(0.98).targetOffset(-40,14)) 
    doubleClick(Pattern("1388436274469.png").similar(0.90))    
    doubleClick(Pattern("1388436357270.png").similar(0.96))

def startproperties_25process():
    
    maximize_process_explorer()    
    wait("1388436426300.png", 20)
    rightClick("1388436426300.png")

def test_cpu25percent():
    """test a cpu bound process to take 25% CPU at a 4 core machine"""
    #start CPU bound process
    proc = subprocess.Popen(["python", "-c", "while True:  pass"])    
    start_processexplorer()
    startproperties_25process()
     
    #show process detail screen 
    type(Key.DOWN)
    type(Key.DOWN)
    type(Key.DOWN)
    type(Key.DOWN)
    type(Key.DOWN)
    type(Key.DOWN)
    type(Key.ENTER)

    #wait until we see usage of about 25%
    wait(Pattern("1388480252501.png").similar(0.86), 60)
    wait("1388437097963.png", 90)
    p = subprocess.Popen(["killall", "python"])

def test_affinity():
    """test affinity settings of a process"""
    #start CPU bound process
    proc = subprocess.Popen(["python", "-c", "while True:  pass"])
    start_processexplorer()
    startproperties_25process()   
    type(Key.DOWN)
    type(Key.ENTER)
    click(Pattern("1388483186882.png").exact())
    click(Pattern("1388483198383.png").exact())
    click(Pattern("1388483211934.png").exact())
    click("1388483235141.png")
    type(Key.F4, KEY_ALT)
    start_processexplorer()
    startproperties_25process()   
    type(Key.DOWN)
    type(Key.ENTER)
    wait(Pattern("1388483627687.png").similar(0.86))
    wait(Pattern("1388483637679.png").similar(0.95))
    wait(Pattern("1388483647911.png").similar(0.98))
    wait(Pattern("1388483656564.png").similar(0.98))
    p = subprocess.Popen(["killall", "python"])

def testdeadprocess():
    start_processexplorer() 
    maximize_process_explorer() 
    proc = subprocess.Popen(["python", "-c", "import time; time.sleep(10)"])
    wait("1388494525665.png", 20)
    rightClick("1388494525665.png")
    type(Key.DOWN)
    type(Key.DOWN)
    type(Key.DOWN)
    type(Key.DOWN)
    type(Key.DOWN)
    type(Key.DOWN)
    type(Key.ENTER)
    wait(Pattern("1388495924849.png").similar(0.93), 60) 
    subprocess.Popen(["killall", "python"])    
    
if __name__ == "__main__":
   test_cpu25percent()
   test_affinity()
   testdeadprocess()
   print "************************"
   print "* all tests succeeded  *"
   print "************************"
