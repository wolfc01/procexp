class Command(object):
  COMMAND = "cmd"
  END     = "end"
  CONTINUE= "cont"
  STOP    = "stop"
  LISTDIR = "listdir"
  READLINK = "readlink"
  READFILE = "readfile"

class Result(object):
  OK="ok"
  FAIL="fail"
