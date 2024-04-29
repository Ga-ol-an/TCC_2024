from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel

def simpleTopology():
    net = Mininet(controller=RemoteController, switch=OVSKernelSwitch)

    # Adicionando o controlador RYU
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    # Adicionando switches e hosts
    s1 = net.addSwitch('s1')
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')

    # Criando links
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)

    # Iniciando a rede
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    simpleTopology()
