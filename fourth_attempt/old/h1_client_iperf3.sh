#/bin/bash

iperf3 -c 10.0.0.4 -p 5001 -u -b 10M -t 30 > outputs/h4_server_h1 &
iperf3 -c 10.0.0.4 -p 5002 -u -b 10M -t 30 > outputs/h4_server_h2 &
iperf3 -c 10.0.0.4 -p 5003 -u -b 10M -t 30 > outputs/h4_server_h3 &
