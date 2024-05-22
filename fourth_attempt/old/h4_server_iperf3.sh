#/bin/bash

#pra iperf adicionar -u

iperf3 -s -i 1 -p 5001 > outputs/server_iperf3 &
iperf3 -s -i 1 -p 5002 > outputs/server_iperf3 &
iperf3 -s -i 1 -p 5003 > outputs/server_iperf3 &
