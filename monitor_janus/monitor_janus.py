1 #!/usr/bin/python2

import sys
import os 
import ConfigParser

global threadNameList
threadNameList = []
global proccess_name
proccess_name = ""
global timing_log
timing_log = 120
global log_path
log_path = ""


def get_command_param(configfile='monitor.conf'):
    global proccess_name
    global threadNameList
    global timing_log
    global log_path
    with open(configfile,'r') as cfgfile:
        cf = ConfigParser.ConfigParser()
        cf.readfp(cfgfile)
        secs = cf.sections()
#        print 'sections:',secs

        name = cf.get("info","name")
        proccess_name = cf.get("info",'target_proccess_name')
        gen_log = cf.get("info","generate_unnormal_log")
        print "streamnumber %s,gen_log %s" % (proccess_name,gen_log)

        timing_log = cf.get("info","timing_log_interval")
        thread_name = cf.get("info","target_thread_name")
        print thread_name
        threadNameList = thread_name.split(",")
        print type(thread_name)
        print type(threadNameList)
        print threadNameList
        log_path = cf.get("info","log_path")
        print "get log_path",log_path
        if not os.path.isabs(log_path):
            abs_path = os.path.abspath(".")
            log_path = os.path.join(abs_path,log_path)
            print "log_path",log_path
        if not ( os.path.isdir(log_path) and os.path.exists(log_path)):
            print "no log path,create"
            os.mkdir(log_path)
        # for th in thread_name:
        #     print th

def monitor_thread(proccessName,threadName):
    # cmdline = 'pstree -p $(pidof %s) |grep %s|wc -l' % proccessName , threadName
    # print cmdline   
    cmd = 'pstree -p $(pidof ',proccessName,') |grep ',threadName,'|wc -l' 
    print cmd
    # ret = os.popen(cmdline).readlines() 
def monitor():
    global proccess_name
    global threadNameList
    global timing_log
    global log_path
    print "begin"
    if proccess_name == "":
        print "proccess name error: ",proccess_name
        return
    for th in threadNameList:
        monitor_thread(proccess_name,th)


if __name__ == "__main__":
  print "*"*10
  print "capture janus thread"
  get_command_param()
  monitor()
  print "-"*10