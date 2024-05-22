#/bin/bash

iperf -c 10.0.0.4 -p 5001 -u -b 10M -t 30 &
iperf -c 10.0.0.4 -p 5002 -u -b 10M -t 30 &
iperf -c 10.0.0.4 -p 5003 -u -b 10M -t 30 &
