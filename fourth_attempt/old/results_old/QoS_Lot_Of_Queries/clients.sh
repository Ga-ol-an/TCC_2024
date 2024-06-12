h1 iperf -c 10.0.0.4 -p 5001 -u -b 10M -t 10 -e &
px import time
px time.sleep(5)
h2 iperf -c 10.0.0.4 -p 5002 -u -b 10M -t 30 -e &
px time.sleep(10)
h3 iperf -c 10.0.0.4 -p 5003 -u -b 10M -t 40 -e &
px time.sleep(20)
h1 iperf -c 10.0.0.4 -p 5001 -u -b 10M -t 20 -e &
px time.sleep(10)
h2 iperf -c 10.0.0.4 -p 5002 -u -b 10M -t 10 -e &
