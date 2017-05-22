1 #!/usr/bin/python2

import sys
import os 
import ConfigParser
import json
import time

global threadNameList
threadNameList = []
global proccess_name
proccess_name = ""
global timing_log_interval
timing_log_interval = 120
global log_path
log_path = ""
global result_data
result_data = {}
global fp
fp = None

global lastDataTime
lastDataTime = 0


def get_command_param(configfile='monitor.conf'):
    global proccess_name
    global threadNameList
    global timing_log
    global log_path
    global timing_log_interval
    with open(configfile,'r') as cfgfile:
        cf = ConfigParser.ConfigParser()
        cf.readfp(cfgfile)
        secs = cf.sections()
#        print 'sections:',secs

        name = cf.get("info","name")
        proccess_name = cf.get("info",'target_proccess_name')
        print "proccess_name %s" % (proccess_name)

        timing_log = cf.get("info","timing_log_interval")
        thread_name = cf.get("info","target_thread_name")
        print thread_name
        threadNameList = thread_name.split(",")
        # print type(thread_name)
        # print type(threadNameList)
        # print threadNameList
        log_path = cf.get("info","log_path")
        print "get log_path",log_path
        if not os.path.isabs(log_path):
            abs_path = os.path.abspath(".")
            log_path = os.path.join(abs_path,log_path)
            print "log_path",log_path
        # if os.path.isdir(log_path) and not (os.path.exists(log_path)):
        #     print "no log path,create"
        #     os.mkdir(log_path)
        # for th in thread_name:
        #     print th
        timing_log_interval = int(timing_log)
        print "timing_log_interval=%d" % timing_log_interval

def monitor_thread(proccessName,threadName):
    # cmdline = "".join(('pstree -p $(pidof ',proccessName,') |grep ',threadName,'|wc -l'))
    cmdline = "".join(('ps -T -p $(pidof ',proccessName,') |grep ',threadName,'|wc -l'))
    print cmdline   
    # cmd = 'pstree -p $(pidof ',proccessName,') |grep ',threadName,'|wc -l' 
    # print cmd
    global result_data
    ret = os.popen(cmdline).readlines() 
    thread_number = ret[0]
    if thread_number == '0':
        return
    thread_number = int(thread_number)
    result_data[threadName] = thread_number

def log_result():
    # log to json
    global fp
    global result_data
    tmp = result_data
    tmp["time"]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    log_text = json.dumps(tmp)
    print log_text
    #print type(log_text)
    fp.write(log_text+'\n')
    fp.flush() 

def monitor():
    global proccess_name
    global threadNameList
    global timing_log
    global log_path
    global fp
    global timing_log_interval
    lastDataTime = 0
    fp = open(log_path,"a")
    while True:
        nowtm = time.time()
        #print "now time %d",nowtm
        #nowtm = time.mktime(time.localtime())  
        diff = int(nowtm - lastDataTime) 
        if diff >  timing_log_interval:
            lastDataTime = nowtm
            if proccess_name == "":
                print "proccess name error: ",proccess_name
                continue
            for th in threadNameList:
                monitor_thread(proccess_name,th)
            log_result()
        time.sleep(1)
    fp.close()

if __name__ == "__main__":
  print "*"*10
  print "capture janus thread"
  get_command_param()
  monitor()
  print "-"*10