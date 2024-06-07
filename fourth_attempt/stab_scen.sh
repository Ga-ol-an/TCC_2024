px print('Stable Scenario')

px print('Cleaning previous implementations of iperf')
h4 pkill iperf
h4 pkill iperf
px time.sleep(1)

px print('Begining servers')
h4 iperf -s -u -i 1 -p 5001 -e > outputs/stable/h4_server_h1 & 
h4 iperf -s -u -i 1 -p 5002 -e > outputs/stable/h4_server_h2 & 
h4 iperf -s -u -i 1 -p 5003 -e > outputs/stable/h4_server_h3 & 
px time.sleep(1)

px print('Begining clients')
h1 iperf -c 10.0.0.4 -p 5001 -u -b 10M -t 30 -e &
h2 iperf -c 10.0.0.4 -p 5002 -u -b 10M -t 30 -e &
h3 iperf -c 10.0.0.4 -p 5003 -u -b 10M -t 30 -e &

