#!/usr/bin/python
from mininet.topo import Topo
from mininet.node import RemoteController
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
		
	self.fanout = fanout
	agg_count = 0
	edge_count = 0
	host_count = 0

	core = self.addSwitch('c1')
	
	for i in irange(1,fanout):
		agg_count = agg_count + 1
		aggregation = self.addSwitch('a%s' % agg_count)
		self.addLink(aggregation,core)
		for j in irange(1,fanout):
			edge_count = edge_count + 1
			edge = self.addSwitch('e%s' % edge_count)
			self.addLink(edge,aggregation)
			for k in irange(1,fanout):
				host_count = host_count + 1
				host = self.addHost('h%s' % host_count)
				self.addLink(host,edge)
			
def simpleTest():
	topo = CustomTopo(fanout=3)
	net = Mininet(topo=topo, link=TCLink, controller=RemoteController)
	net.start()
	print "Dump host connections"
	dumpNodeConnections(net.hosts)
	print "Dump switch connections"
	dumpNodeConnections(net.switches)	
	#print "Testing network connectivity"
	#net.pingAll()
	#net.stop()		

if __name__ == '__main__':
	# Tell mininet to print useful information
	setLogLevel('info')
	simpleTest()

topos = { 'custom': ( lambda: CustomTopo() ) }
