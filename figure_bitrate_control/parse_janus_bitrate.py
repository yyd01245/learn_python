 #!/usr/bin/python2
import sys
import os
import re
import time
import matplotlib.pyplot as plt

global bitrate
global ytime
global index
global max_avg
global avg_big
global lost_data
global delay_data
global delay_pkt
global frame_delay_big
global frame_delay_little

global current_bitrate

current_bitrate = []
frame_delay_big = []
frame_delay_little = []
delay_pkt = []
delay_data = []
lost_data = []
avg_big = []
max_avg = []
bitrate = []
ytime = []
index = 0

global delay_tol
delay_tol = 0
global delay_index
delay_index = 0


def list_bitrate():
  global bitrate
  xticks = []
#  for b in bitrate:
#    print b
  for d in range(0,len(bitrate),1):
#    print d
    data = d*1
    xticks.append(int(data))
  
  avg_x = []
  for x in range(0,len(avg_big),1):
    data = x*2
    avg_x.append(int(data))
  #xticks.append(len(bitrate))
  #print type(xticks)
  #print xticks
  print len(bitrate),len(xticks)
  print "max_avg len",len(max_avg)
  # ax = plt.subplots()
  # ax.set_xticks(xticks)
  #plt.plot(xticks,bitrate)
  plt.figure(1,figsize=(8,6))
#   plt.plot(xticks,bitrate,label="bitrate current",color="red",linewidth=2)
#   plt.plot(avg_x,max_avg,label="bitrate avg 30",color="blue",linewidth=2)
#   plt.plot(avg_x,avg_big,label="bitrate avg 6",color="yellow",linewidth=2)
#   plt.plot(xticks,lost_data,label="lost_rate value*100000",color="green",linewidth=2)
#   #plt.title("lost rate")
#   #plt.plot(xticks,delay_pkt,label="packet delay value*1000",color="grey",linewidth=2)
#   # plt.plot(avg_x,frame_delay_big,label="frame delay avg 30 value*2000",color="purple",linewidth=2)
#   # plt.plot(avg_x,frame_delay_little,label="frame delay avg 6 value*2000",color="c",linewidth=2)
#   plt.title("bitrate avg avg_big; lost rate; package delay; frame delay")
#   #plt.grid()
#   plt.legend(loc='upper left')
#   #plt.figure(2)

#   plt.grid()

#   plt.figure(2)
#   xdata = []
#   for d in range(0,len(delay_data),1):
# #    print d
#     data = d*1
#     xdata.append(int(data))
#   plt.plot(xdata,delay_data,label="delay sample",color="black",linewidth=2)
#   plt.title("frame delay")
#   plt.grid()

  # plt.figure(3,figsize=(8,6))
  print len(lost_data)
  print len(current_bitrate)
  plt.plot(range(0,len(lost_data),1),lost_data,label="packet lost rate \*1000000",color="red",linewidth=2)
  plt.plot(range(0,len(current_bitrate),1),current_bitrate,label="current bitrate",color="green",linewidth=2)
  plt.title("new plan lost and bitrate x scale 0.2ms")
  #plt.ylabel("bitrate bps")
  plt.legend(loc='upper left')
  #plt.figure(2)

  plt.grid()

  # plt.figure(4)
  # delay_pkt[0] = 0
  # print delay_pkt
  # plt.plot(range(0,len(delay_pkt),1),delay_pkt,label="packet delay sample",color="grey",linewidth=2)
  # plt.title("package for perid avg delay")
  # #plt.ylabel("bitrate bps")
  # plt.grid()

  plt.show()

def func_read_bitrate(filename):

  lines = open(filename).readlines()
  for line in lines:
  #  print line
 #   p = re.compile(line)
 #   m = p.search("rtcp send semb bitrate=")
    m = line.find("rtcp send semb bitrate=")
    if m != -1:
      global bitrate
      l = line.split("rtcp send semb bitrate=")
  #    print l[0]
  #    print("%s" % l[len(l)-1])
      bitrate.append(int(l[len(l)-1]))
    elif line.find("calculate_bitrate max_avg=") != -1:
      global max_avg
      global avg_big
      t = line.split("calculate_bitrate ")
      #print t[1]
      npos = t[1].index(", bitrate=")
      l = t[1][:npos]
      #print l
      data = l.split(", ")
      #print data
      max_data = data[0].split("=")
      max_avg.append(float(max_data[1]))
      avg = data[1].split("=")
      avg_big.append(float(avg[1]))

      # delay_big = data[2].split("=")
      # print delay_big
      # frame_delay_big.append(float(delay_big[1])*2000)
      # delay_little = data[3].split("=")
      # print delay_little
      # frame_delay_little.append(float(delay_little[1])*2000)

      #l = t[1].split(", avg_6=")
    elif line.find("====broadcast in 1s get lost") != -1:
      global lost_data
      global delay_data
      global current_bitrate
      t = line.split("====broadcast in 1s get ")
      print t[1]
  #    npos = t[1].index("lost=")
  #    l = t[1][:npos]
   #   print l
      data = t[1].split(" ")
    #  print "get lost ="
   #   print data[0]
      max_data = data[0].split("=")
   #   print max_data
      lost_data.append(float(max_data[1])*1000000)

      #delay
      delay = data[1].split("=")
      #print delay
     # print delay[1]
      delay_pkt.append(float(delay[1])*1000)
      #print data[2]
      #current bitrate
      cur_bitrate = data[2].split("=")
      print cur_bitrate
      if cur_bitrate[0]=="bitrate":
        current_bitrate.append(float(cur_bitrate[1]))

    elif line.find("--currenttim =") != -1:
      global delay_data
      global delay_tol
      global delay_index
      t = line.split("compute deltas timestamp")
   #   print t[1]
  #    npos = t[1].index("lost=")
  #    l = t[1][:npos]
   #   print l
      data = t[1].split(", ")
   #   print "get delay ="
    #  print data[0]
      max_data = data[1].split("=")
      #print max_data
      real_dat = data[2].split("=")
      #print real_dat
      value = abs(float(real_dat[1]))
      delay_index += 1
      delay_tol += value
      #if value < 150:
      if delay_index >= 15:
        value = float(delay_tol) / float(delay_index)
        delay_data.append(value)
        delay_index = 0
        delay_tol = 0
        
   #   print max_data
  #    print real_dat
      #h = abs(float(max_data[1]) - float(real_dat[1]))
  #    print h
  #    if h > 50 :
   #     print max_data
    #    print real_dat
   #   delay_data.append(int(abs(h)))

    
if __name__ == "__main__":

  if len(sys.argv) == 2:
    src_data = (sys.argv[1])
    func_read_bitrate(src_data)
    list_bitrate()
  