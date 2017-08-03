#!/usr/bin/env python

 
import re
import subprocess
import os
import time

global fp
fp = open("./tcpping_delay.log","w")

def check_alive(ip,count=1,timeout=1):

        # cmd = 'ping -c %d -w %d %s' % (count,timeout,ip)
        cmd = 'ping %s' % (ip)
        
        p = subprocess.Popen(cmd,
                # stdin=subprocess.PIPE,
                stdout=subprocess.PIPE
                # stderr=subprocess.PIPE,
                # shell=True
        )
        p.wait()
        out = p.communicate()
        print out
        result = p.stdout.read()
        print "type ",type(result)
        print "ping result %s " % result
        regex = re.findall('100% packet loss',result)

        if len(regex) == 0:
                print "\033[31m%s UP\033[0m" % (ip)
        else:
                print "\033[32m%s DOWN\033[0m" % (ip)
 
def log_result(result):
    # log to json
    global fp

    print result
    #print type(log_text)
    fp.write(result)
    fp.flush() 

def pingServer(ip):
        # cmdline = "".join(('ps -T -p $(pidof ',proccessName,') |grep ',threadName,'|wc -l'))
        cmdline = 'ping -c %d %s' % (1,ip)
        # print cmdline   
        # cmd = 'pstree -p $(pidof ',proccessName,') |grep ',threadName,'|wc -l' 
        # print cmd
        ret = os.popen(cmdline).readlines() 
        print ret;
        print ret[1];
        # print "timeout ",ret[4];
        # regex = re.findall('time=',ret[1]);
        # print regex
        line = ret[1];
        regex = re.findall('100.0% packet loss',ret[3]);
        if len(regex) != 0:
                line = "timeout time=3000 ms";

        log_result(line);
        # delay = line.split("time=");
        # print delay[1];



if __name__ == "__main__":
        while(True):
                begin_ms = time.time()*1000.0;
                pingServer("119.254.209.16") 
                # pingServer("10.0.2.68")   
                end_ms = time.time()*1000.0;
                diff = (1000.0 - (end_ms - begin_ms))/1000.0;
                print "--- ping time =",diff
                if diff > 0:            
                        time.sleep(diff);
 
        # with file('/root/ip.txt','r') as f:
        #         for line in f.readlines():
        #                 ip = line.strip()
        #                 check_alive(ip)      