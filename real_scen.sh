px print('Realistic Scenario')

px print('Cleaning previous implementations of iperf')
h4 pkill iperf
h4 pkill iperf
px time.sleep(1)

px print('Begining servers')
h4 iperf -s -u -i 1 -p 5001 -e > outputs/realistic/h4_server_h1 & 
h4 iperf -s -u -i 1 -p 5002 -e > outputs/realistic/h4_server_h2 & 
h4 iperf -s -u -i 1 -p 5003 -e > outputs/realistic/h4_server_h3 & 
px time.sleep(1)

px print('Begining clients')
h1 iperf -c 10.0.0.4 -p 5001 -u -b 10M -t 15 -e &
px time.sleep(5)
h2 iperf -c 10.0.0.4 -p 5002 -u -b 10M -t 35 -e &
px time.sleep(15)                                
h3 iperf -c 10.0.0.4 -p 5003 -u -b 10M -t 35 -e &
px time.sleep(10)
h1 iperf -c 10.0.0.4 -p 5001 -u -b 10M -t 20 -e &