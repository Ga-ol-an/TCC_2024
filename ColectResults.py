from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

class SRTestTopo( Topo ):
    "Simple topology for testing segment routing"

    def __init__( self, **opts ):
        Topo.__init__( self, **opts )

        # Add hosts and switches
        h1 = self.addHost( 'h1', ip='10.0.0.1/24' )
        h2 = self.addHost( 'h2', ip='10.0.0.2/24' )
        h3 = self.addHost( 'h3', ip='10.0.0.3/24' )
        h4 = self.addHost( 'h4', ip='10.0.0.4/24' )
        s1 = self.addSwitch( 's1', cls=OVSSwitch )
        s2 = self.addSwitch( 's2', cls=OVSSwitch )
        s3 = self.addSwitch( 's3', cls=OVSSwitch )
        s4 = self.addSwitch( 's4', cls=OVSSwitch )

        # Add links
        for h, s in [ ( h1, s1 ), ( h2, s2 ), ( h3, s3 ), ( h4, s4 ) ]:
            self.addLink( h, s )

        self.addLink( s1, s2 )
        self.addLink( s2, s3 )
        self.addLink( s3, s4 )

def run_SRTest():
    topo = SRTestTopo()
    net = Mininet( topo=topo, \
      #controller=RemoteController,
      switch=OVSSwitch )
    # net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=6633 )
    net.start()

    h1, h2, h3, h4 = net.get( 'h1', 'h2', 'h3', 'h4' )

    print("Testing network connectivity")
    net.pingAll()

    print("Testing bandwidth between h1 and h2 (h3 and h4) with iperf")
    h2.sendCmd( 'iperf -s -u -i 1 > iperf_server_h2.log &' )
    h1.sendCmd( 'iperf -c %s -t 200 -i 1 > iperf_client_h1.log &' % h2.IP() )
    h4.sendCmd( 'iperf -s -u -i 1 > iperf_server_h4.log &' )
    h3.sendCmd( 'iperf -c %s -t 200 -i 1 > iperf_client_h3.log &' % h4.IP() )

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run_SRTest()