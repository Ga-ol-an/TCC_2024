from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

def create_topology():
    net = Mininet(controller=RemoteController, switch=OVSSwitch)

    #! Adicionando o controlador Ryu -> Ver como fazer
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)

    # Adicionando switches
    switches = []
    for i in range(1, 5):
        switch = net.addSwitch(f's{i}')
        switches.append(switch)

    # Adicionando hosts
    hosts = []
    for i in range(1, 9):
        host = net.addHost(f'h{i}')
        hosts.append(host)
        
        
    # Switch 1: Conecta no 2 e 3
    # Switch 3: Conecta no 4
    
    
    # Switch1:              Switch2:
    #   Host 1 e 2            Host 7 e 8
    # Switch3:               Switch4:
    #    Host 4 e 5          Host 7 e 8

    # Conectando switches e hosts
    for i, switch in enumerate(switches):
        net.addLink(switch, hosts[2*(i+1)-1])
        net.addLink(switch, hosts[2*(i+1)-2])
      
    
    net.addLink(switches[0],switches[1])
    net.addLink(switches[1],switches[2])
    net.addLink(switches[2],switches[3])
    
        # if i == 0:
        #     net.addLink(switch, hosts[0])
        #     net.addLink(switch, hosts[1])
        # elif i == 4:
        #     net.addLink(switch, hosts[2])
        #     net.addLink(switch, hosts[3])
        # else:
        #     net.addLink(switch, hosts[i])

  
    # Construindo a rede
    net.build()
    c0.start()
    for switch in switches:
        switch.start([c0])

    return net

if __name__ == '__main__':
    setLogLevel('info')
    topology = create_topology()
    CLI(topology)
