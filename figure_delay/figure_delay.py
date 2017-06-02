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
  sumValue = 0
  less10ms = 0
  greater10ms = 0
  greater25ms = 0
  greater50ms = 0
  greater100ms = 0
  greater150ms = 0
  for x in dataChannelDelay:
    print x
    if x > 150000:
      greater150ms += 1
    elif x > 100000:
      greater100ms += 1
    elif x > 50000:
      greater50ms += 1
    elif x > 25000:
      greater25ms += 1
    elif x > 10000:
      greater10ms += 1
    else:
      less10ms += 1
  print "delay time >150ms count=%d" % greater150ms
  print "delay time >100ms < 150ms count=%d" % greater100ms
  print "delay time >50ms < 100ms count=%d" % greater50ms
  print "delay time >25ms < 50ms count=%d" % greater25ms
  print "delay time >10ms <25ms count=%d" % greater10ms
  print "delay time <=10ms count=%d" % less10ms
  # avg = sumValue / len(dataChannelDelay)

  avg = sum(dataChannelDelay) / float(len(dataChannelDelay))
  print "diff  len=%d avg=%d" % (len(dataChannelDelay),avg)
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
      #print t[1]
      dataChannelDelay.append(int(t[1]))
    
if __name__ == "__main__":

  if len(sys.argv) == 2:
    src_data = (sys.argv[1])
    func_read_httpDelay(src_data)
    list_Delay()
  