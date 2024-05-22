#/bin/bash

iperf -s -u -i 1 -p 5001 > outputs/h4_server_h1_sem_qos &
iperf -s -u -i 1 -p 5002 > outputs/h4_server_h2_sem_qos &
iperf -s -u -i 1 -p 5003 > outputs/h4_server_h3_sem_qos &