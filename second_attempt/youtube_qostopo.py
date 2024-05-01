from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import RemoteController, OVSKernelSwitch
from time import sleep

scenario = 3

class QoStopo (Topo):
  "6 switch connected to n hosts."
  
  def build(self):
    s1 = self.addSwitch('s1')
    s2 = self.addSwitch('s2')
    s3 = self.addSwitch('s3')
    s4 = self.addSwitch('s4')
    s5 = self.addSwitch('s5')
    s6 = self.addSwitch('s6')
    
    h1 = self.addHost('hl', mac="00:00:00:00:00:01", ip="10.1.1.1/24")
    h2 = self.addHost('h2', mac="00:00:00:00:00:02", ip="10.1.1.2/24")
    h3 = self.addHost('h3', mac="00:00:00:00:00:03", ip="10.1.1.3/24")
    h4 = self.addHost('h4', mac="00:00:00:00:00:04", ip="10.1.1.4/24")
    h5 = self.addHost('h4', mac="00:00:00:00:00:05", ip="10.1.1.5/24")
    h6 = self.addHost('h4', mac="00:00:00:00:00:06", ip="10.1.1.6/24")
    h7 = self.addHost('h7', mac="00:00:00:00:00:07", ip="10.1.1.7/24")
    h8 = self.addHost('h8', mac="00:00:00:00:00:08", ip="10.1.1.8/24")
    h9 = self.addHost('h9', mac="00:00:00:00:00:09", ip="10.1.1.9/24")
    h10 = self.addHost('h10', mac="00:00:00:00:00:10", ip="10.1.1.10/24")
    
    self.addLink(s1, s2, cls=TCLink, bw=10)
    self.addLink(s3, s2, cls=TCLink, bw=10)
    self.addLink(s2, s4, cls=TCLink, bw=10)
    self.addLink(s4, s5, cls=TCLink, bw=10)
    self.addLink(s4, s6, cls=TCLink, bw=10)
    #self.addLink(54, h6, cls=TCLink, bw=5, delay='11ms' )
    
    self.addLink(h1, s1, cls=TCLink, bw=10)
    self.addLink(h2, s1, cls=TCLink, bw=10)
    self.addLink(h3, s1, cls=TCLink, bw=10)
    self.addLink(h4, s3, cls=TCLink, bw=10)
    self.addLink(h5, s3, cls=TCLink, bw=10)
    self.addLink(h6, s5, cls=TCLink, bw=10)
    self.addLink(h7, s5, cls=TCLink, bw=10)
    self.addLink(h8, s5, cls=TCLink, bw=10)
    self.addLink(h9, s6, cls=TCLink, bw=10)
    self.addLink(h10, s6, cls=TCLink, bw=10)
    

setLogLevel('info')
topo = QoStopo()
c1 = RemoteController('c1', ip='127.0.0.1')
net = Mininet (topo-topo, controller=cl)
net.start()
print("Waiting for 10 seconds to start the traffic test....")
sleep (1)
net.pingAll()

print("Starting the servers in h4, h5, h6")
h6 = net.get('h6')
h7 = net.get('h7')
h8 = net.get('h8')
h9 = net.get('h9')
h10 = net.get('h10')
#qosl
h6.cmd('iperf -u -s -p 5000 -1 10 > h6qos1_server.log &')
h7.cmd('iperf -u -s -p 6000 -i 10 > h7qos2_server.log &')
h10.cmd('iperf -u -s -p 7000 - -i 10 > h10be_server.log &')

if scenario == 0:
  #demo static Q0S(5,5,5)
  h1 = net.get('h1').cmd('iperf -u -c 10.1.1.6 -p 5000 -b 5M -1 10 -t 120 > hl_iperf_qosl_client.log &')
  #qos2 traffic
  h4 = net.get('h4').cmd('iperf -u -c 10.1.1.7 -p 6000 -b 5M -1 10 -t 120 > h4_1perf_qos2_client.log &')
  #be traffic
  h3 = net.get('h3').cmd('iperf -u -c 10.1.1.10 -p 7000 -b 5M -i 10 -t 120 > h3_iperf_be_client.log &')
  """   if scenario == 1:
  #demol for static qos (5,1,4)
  #qos1 traffic
  hl=net.get('h1').cmd('iperfu -c 10.1.1.6 -p 5000 -b 5M -1 10 -t 120 > h1_iperf_qos1_client.log &' )
  I
  #qos2 traffic
  h4 = net.get('h4').cmd('iperf -u -c 10.1.1.7 -p 6000 -b 1M -1 10 -t 120 > h4_iperf_qos2_client.log &')
  # be traffic
  h3 = net.get('h3').cmd('iperf -u -c 10.1.1.10 -p 7000 -b 4M -1 10 -t 120 > h3_iperf_be_client.log &')
  elif scenario ==  2:
  """
  if scenario == 1:
    #demol for static qos (5,1,4)
    #qos1 traffic
    h1 = net.get('h1').cmd('iperf -u -c 10.1.1.6 -p 5000 -b 5M -i 10 t 120 > h1_iperf_qos1_client.log &' ) #qos2 traffic
    h4 = net.get('h4').cmd('iperf -u -c 10.1.1.7 -p 6000 b 1M i 10 t 120 > h4_iperf_qos2_client.log &')
    #be traffic
    h3 = net.get('h3').cmd('iperf -u -c 10.1.1.10 -p 7000 b 4M -i 10 t 120 > h3_iperf_be_client.log &')
  elif scenario == 2:
    #demo2 for static gos (1,7,2)
    #qos1 traffic
    h1 = net.get('h1').cmd('iperf -u -c 10.1.1.6 -p 5000 -b 1M -i 10 t 120 > h1_iperf_qosl_client.log&') #qos2 traffic
    h4 = net.get('h4').cmd('iperf -u -c 10.1.1.7 -p 6000 -b 7M - 10 -t 120 > h4_iperf_qos2_client.log &')
    #be traffic
    h3 = net.get('h3').cmd('iperf -u -c 10.1.1.10 -p 7000 -b 2M -i 10 - 120 > h3_iperf_be_client.log&')
  elif scenario == 3:
    #demo2 for static gos (8,1,1)
    #qos1 traffic
    h1 = net.get('h1').cmd('iperf -u -c 10.1.1.6 -p 5000 -b 8M -i 10 t 120 > h1_iperf_qosl_client.log&') #qos2 traffic
    h4 = net.get('h4').cmd('iperf -u -c 10.1.1.7 -p 6000 -b 1M - 10 -t 120 > h4_iperf_qos2_client.log &')
    #be traffic
    h3 = net.get('h3').cmd('iperf -u -c 10.1.1.10 -p 7000 -b 1M -i 10 - 120 > h3_iperf_be_client.log&')
  else:
    print("Invalid scenario")
  CLI(net)
  net.stop()
    
    