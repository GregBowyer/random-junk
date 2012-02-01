#!/bin/bash

PID=$1
SIG=$2
TIME=$3
HOST=$4
EXE=$5
TRUE_EXE=`readlink -f /proc/${PID}/exe`

REPORT_DIR=/tmp/crash-${PID}-${TIME}-${EXE}

mkdir ${REPORT_DIR}

lsof -p ${PID} >> ${REPORT_DIR}/open-files
lsof -p -i ${PID} >> ${REPORT_DIR}/open-ports
uptime >> ${REPORT_DIR}/uptime
top -b -n 1 >> ${REPORT_DIR}/process-table

cat /proc/${PID}/maps >> ${REPORT_DIR}/maps
cat /proc/${PID}/stat >> ${REPORT_DIR}/stat     
cat /proc/${PID}/cmdline >> ${REPORT_DIR}/cmdline          
cat /proc/${PID}/cwd >> ${REPORT_DIR}/cwd      
cat /proc/${PID}/environ >> ${REPORT_DIR}/environ  
cat /proc/${PID}/limits >> ${REPORT_DIR}/limits  

# Remember once the core is dumped the process goes from being a 
# member of the walking dead to a real bonafide corpse
# if you want to do anything special on the OS
# do it before you consume the core-file from STDIN
cp /dev/stdin ${REPORT_DIR}/core

gdb --batch-silent \
    -ex 'set logging overwrite on' \
    -ex "set logging file ${REPORT_DIR}/backtrace" \
    -ex 'set logging on' \
    -ex 'handle SIG33 pass nostop noprint' \
    -ex "file ${TRUE_EXE}" \
    -ex "core-file ${REPORT_DIR}/core" \
    -ex 'set pagination 0' \
    -ex 'echo backtrace::\n' \
    -ex 'backtrace full' \
    -ex 'echo \nregisters::\n' \
    -ex 'info registers' \
    -ex 'echo \nprogram-counters::\n' \
    -ex 'x/16i $pc' \
    -ex 'echo \nfull-backtrace\n' \
    -ex 'thread apply all backtrace' \
    -ex 'quit'

chmod 755 ${REPORT_DIR}/*

cat ${REPORT_DIR}/backtrace | mailx -s "Core dump occured on ${HOST}. Look in ${REPORT_DIR}" gbowyer@shopzilla.com
