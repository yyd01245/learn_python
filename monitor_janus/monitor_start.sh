#!/bin/bash - 
#===============================================================================
#
#          FILE:  monitor_start.sh
# 
#         USAGE:  ./monitor_start.sh 
# 
#   DESCRIPTION:  
# 
#       OPTIONS:  ---
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR: Yandong Yan (A program fan), yandong.yan@upai.com or (yydgame@163.com)
#       COMPANY: Upyun
#       CREATED: 2017年05月22日 16时42分52秒 CST
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

PID=`ps -ef|grep monitor_janus.py|grep -v "grep"|awk '{print $2}'`

if [ ! -z "${PID}"  ]; then
    echo "Stopping process with \"kill\""
    kill -9 ${PID}

fi
#nohup python monitor_janus.py >/dev/null 2>&1 &
nohup python monitor_janus.py >./monitor.log 2>&1 &
#echo "ok"
