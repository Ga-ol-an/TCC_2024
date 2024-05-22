from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

def customTopology():
    # Configuração básica do log
    setLogLevel('info')

    # Criação da rede, especificando o uso do controle remoto e do switch Open vSwitch Kernel
    net = Mininet(controller=RemoteController, switch=OVSKernelSwitch, link=TCLink)


    
    # Adiciona o controlador RYU
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    # Criação do switch com protocolo OpenFlow 1.3
    s1 = net.addSwitch('s1', protocols='OpenFlow13')

    # Criação dos hosts com configuração de MAC e IP automáticos
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    h4 = net.addHost('h4')

    # Criação dos links
    # loss em %
    # bw em Mbps
    net.addLink(h1, s1)#, cls=TCLink, bw=10, delay='150ms', loss=1)#, jitter='30ms')
    net.addLink(h2, s1)#, cls=TCLink, bw=10, delay='150ms', loss=1)#, jitter='30ms')
    net.addLink(h3, s1)#, cls=TCLink, bw=10, delay='150ms', loss=1)#, jitter='30ms')
    link4=net.addLink(h4, s1)#, cls=TCLink, bw=10, delay='150ms', loss=1)#, jitter='30ms')


    #tentando implementar bw no link 
    link4.intf1.config( loss=1, bw=10, delay='150ms')

    # Inicialização e configuração da rede
    net.start()
    h1.cmd('ifconfig h1-eth0 10.0.0.1')
    h2.cmd('ifconfig h2-eth0 10.0.0.2')
    h3.cmd('ifconfig h3-eth0 10.0.0.3')
    h4.cmd('ifconfig h4-eth0 10.0.0.4')

    #Configura o QoS
    s1.cmd('ovs-vsctl set-manager ptcp:6632')
    s1.cmd('xterm -e "ovs-vsctl set Bridge s1 protocols=OpenFlow13"')
    
    #h4:
    # h4.cmd('iperf -s -u -i 1 -p 5001 > outputs/h4_server_h1 &')
    # h4.cmd('iperf -s -u -i 1 -p 5002 > outputs/h4_server_h2 &')
    # h4.cmd('iperf -s -u -i 1 -p 5003 > outputs/h4_server_h3 &')


    #h1 to h3 (clients):

    # h1.cmd('iperf -c 10.1.1.4 -p 5001 -u -b 1M &')
    # h2.cmd('iperf -c 10.1.1.4 -p 5002 -u -b 1M &')
    # h3.cmd('iperf -c 10.1.1.4 -p 5003 -u -b 1M &')

    # Abre a interface CLI do Mininet para interação
    CLI(net)

    # Finalização e limpeza da rede
    net.stop()


if __name__ == '__main__':
    customTopology()