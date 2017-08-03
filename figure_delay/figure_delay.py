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
global tcpPingDelay

dataChannelDelay = []
httpDelay = []
ytime = []
index = 0
tcpPingDelay = []

global delay_tol
delay_tol = 0
global delay_index
delay_index = 0


def list_Delay():

  # xticks = []

  # for d in range(0,len(httpDelay),1):
  #   data = d*1
  #   xticks.append(int(data))
  
  # avg_x = []
  sumValue = 0
  less10ms = 0

  # avg = sumValue / len(dataChannelDelay)
  if(len(tcpPingDelay) > 0):
    greater10ms = 0
    greater25ms = 0
    greater50ms = 0
    greater100ms = 0
    greater150ms = 0
    for x in tcpPingDelay:
      # print x
      if x > 150:
        greater150ms += 1
      elif x > 100:
        greater100ms += 1
      elif x > 50:
        greater50ms += 1
      elif x > 25:
        greater25ms += 1
      elif x > 10:
        greater10ms += 1
      else:
        less10ms += 1
    print "delay time >150ms count=%d rate=%f" % (greater150ms,greater150ms/float(len(tcpPingDelay)));
    print "delay time >100ms < 150ms count=%d rate=%f" % (greater100ms,greater100ms/float(len(tcpPingDelay)))
    print "delay time >50ms < 100ms count=%d rate=%f" % (greater50ms,greater50ms/float(len(tcpPingDelay)));
    print "delay time >25ms < 50ms count=%d rate=%f" % (greater25ms,greater25ms/float(len(tcpPingDelay)));
    print "delay time >10ms <25ms count=%d rate=%f" % (greater10ms,greater10ms/float(len(tcpPingDelay)));
    print "delay time <=10ms count=%d" % less10ms
    avg = sum(tcpPingDelay) / float(len(tcpPingDelay))
    print "diff  len=%d avg=%d" % (len(tcpPingDelay),avg)
  if(len(dataChannelDelay) > 0):
    greater10ms = 0
    greater25ms = 0
    greater50ms = 0
    greater100ms = 0
    greater150ms = 0
    for x in dataChannelDelay:
      # print x
      if x > 150:
        greater150ms += 1
      elif x > 100:
        greater100ms += 1
      elif x > 50:
        greater50ms += 1
      elif x > 25:
        greater25ms += 1
      elif x > 10:
        greater10ms += 1
      else:
        less10ms += 1
    print "delay time >150ms count=%d rate=%f" % (greater150ms,greater150ms/float(len(dataChannelDelay)));
    print "delay time >100ms < 150ms count=%d rate=%f" % (greater100ms,greater100ms/float(len(dataChannelDelay)))
    print "delay time >50ms < 100ms count=%d rate=%f" % (greater50ms,greater50ms/float(len(dataChannelDelay)));
    print "delay time >25ms < 50ms count=%d rate=%f" % (greater25ms,greater25ms/float(len(dataChannelDelay)));
    print "delay time >10ms <25ms count=%d rate=%f" % (greater10ms,greater10ms/float(len(dataChannelDelay)));
    print "delay time <=10ms count=%d" % less10ms
    avg = sum(dataChannelDelay) / float(len(dataChannelDelay))
    print "diff  len=%d avg=%d" % (len(dataChannelDelay),avg)
  plt.figure(1,figsize=(8,6))

  print len(tcpPingDelay)
  plt.plot(range(0,len(tcpPingDelay),1),tcpPingDelay,label="icmp ping delay ",color="red",linewidth=2)
  plt.plot(range(0,len(dataChannelDelay),1),dataChannelDelay,label="data channel Delay",color="green",linewidth=2)
  plt.title("datachannel delay and ping ms")
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
      if int(t[1]) > 500:
        print t[1]
      dataChannelDelay.append(int(t[1]))
    elif line.find("packets transmitted") != -1:
      global tcpPingDelay
      l = line.split("time ")
      # print l[1]
      #print("%s" % l[1])
      data = l[1].split("ms")
      print data[0]
      tcpPingDelay.append(float(data[0]));
    elif line.find(" time") != -1:
      global tcpPingDelay
      l = line.split("time=")
      # print l[1]
      #print("%s" % l[1])
      data = l[1].split(" ")
      print data[0]
      tcpPingDelay.append(float(data[0]));

    
if __name__ == "__main__":

  if len(sys.argv) == 2:
    src_data = (sys.argv[1])
    func_read_httpDelay(src_data)
    list_Delay()
  