 #!/usr/bin/python2
import sys
import os
import re
import time
import matplotlib.pyplot as plt

global httpDelay
global ytime
global index
global dataChannelDelay


dataChannelDelay = []
httpDelay = []
ytime = []
index = 0

global delay_tol
delay_tol = 0
global delay_index
delay_index = 0


def list_Delay():
  global httpDelay
  # xticks = []

  # for d in range(0,len(httpDelay),1):
  #   data = d*1
  #   xticks.append(int(data))
  
  # avg_x = []
  # for x in range(0,len(avg_big),1):
  #   data = x*2
  #   avg_x.append(int(data))

  print "diff  len",len(dataChannelDelay)
  plt.figure(1,figsize=(8,6))

  print len(httpDelay)
  plt.plot(range(0,len(httpDelay),1),httpDelay,label="http delay ",color="red",linewidth=2)
  plt.plot(range(0,len(dataChannelDelay),1),dataChannelDelay,label="data channel Delay",color="green",linewidth=2)
  plt.title("datachannel delay and httpDelay x scale 0.2ms")
  plt.legend(loc='upper left')
  #plt.figure(2)

  plt.grid()

  plt.show()

def func_read_httpDelay(filename):

  lines = open(filename).readlines()
  for line in lines:
    m = line.find("diff_http = ")
    if m != -1:
      global httpDelay
      l = line.split("diff_http = ")
      #print l[0]
      #print("%s" % l[1])
      data = l[1].split(" i = ")
      print data[0]
      httpDelay.append(int(data[0]))
    elif line.find("diff = ") != -1:
      global dataChannelDelay
      global avg_big
      t = line.split("diff = ")
      print t[1]
      dataChannelDelay.append(int(t[1]))
    
if __name__ == "__main__":

  if len(sys.argv) == 2:
    src_data = (sys.argv[1])
    func_read_httpDelay(src_data)
    list_Delay()
  