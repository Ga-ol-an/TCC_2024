#Testa o QoS:

#h4 - Sem QoS:
h4 iperf -s -u -i 1 -p 5001 > outputs/h4_server_h1_sem_qos &
h4 iperf -s -u -i 1 -p 5002 > outputs/h4_server_h2_sem_qos &
h4 iperf -s -u -i 1 -p 5003 > outputs/h4_server_h3_sem_qos &


#h4 - Com QoS:

h4 iperf -s -u -i 1 -p 5001 > outputs/h4_server_h1 &
h4 iperf -s -u -i 1 -p 5002 > outputs/h4_server_h2 &
h4 iperf -s -u -i 1 -p 5003 > outputs/h4_server_h3 &

#h1 to h3 (clients):

h1 iperf -c 10.0.0.4 -p 5001 -u -b 10M -t 30 &
h2 iperf -c 10.0.0.4 -p 5002 -u -b 10M -t 30 &
h3 iperf -c 10.0.0.4 -p 5003 -u -b 10M -t 30 &