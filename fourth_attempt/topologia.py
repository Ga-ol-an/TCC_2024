from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

def simpleTopology():
    "Create and test a simple network"
    net = Mininet(controller=RemoteController, link=TCLink, switch=OVSKernelSwitch)

    print("Criando nós.")
    h1 = net.addHost('h1', mac='00:00:00:00:00:01')
    h2 = net.addHost('h2', mac='00:00:00:00:00:02')
    s1 = net.addSwitch('s1')

    print("Criando links.")
    net.addLink(h1, s1)
    net.addLink(h2, s1)

    print("Configurando controlador remoto.")
    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    print("Iniciando rede.")
    net.start()

    print("Abrindo xterm para cada host.")
    h1.cmd('xterm -e bash &')
    h2.cmd('xterm -e bash &')

    print("Executando CLI.")
    CLI(net)

    print("Parando rede.")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    simpleTopology()
 