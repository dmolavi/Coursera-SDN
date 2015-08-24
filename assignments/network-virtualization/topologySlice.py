'''
Coursera:
- Software Defined Networking (SDN) course
-- Network Virtualization

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
from collections import defaultdict

import pox.openflow.libopenflow_01 as of
import pox.openflow.discovery
import pox.openflow.spanning_tree

from pox.lib.revent import *
from pox.lib.util import dpid_to_str
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
from collections import namedtuple
import os

log = core.getLogger()


class TopologySlice (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Slicing Module")


    """This event will be raised each time a switch will connect to the controller"""
    def _handle_ConnectionUp(self, event):

        # Use dpid to differentiate between switches (datapath-id)
        # Each switch has its own flow table. As we'll see in this
        # example we need to write different rules in different tables.
        dpid = dpidToStr(event.dpid)
        log.debug("Switch %s has come up.", dpid)

        """ Add your logic here """
        if dpid == '00-00-00-00-00-01':
            # h1 -> h3
            in_port = 3
            out_port = 1
           
            s1s2 = of.ofp_flow_mod()
            s1s2.match.in_port = in_port
            s1s2.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(s1s2)
           
            # h3 -> h1
            in_port = 1
            out_port = 3
           
            s2s1 = of.ofp_flow_mod()
            s2s1.match.in_port = in_port
            s2s1.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(s2s1)
           
            # h2 -> h4
            in_port = 4
            out_port = 2
           
            s1s3 = of.ofp_flow_mod()
            s1s3.match.in_port = in_port
            s1s3.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(s1s3)
           
            # h4 -> h2
            in_port = 2
            out_port =4
           
            s3s1 = of.ofp_flow_mod()
            s3s1.match.in_port = in_port
            s3s1.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(s3s1)
       
        elif dpid == '00-00-00-00-00-02' or dpid == '00-00-00-00-00-03':
           
            # Update switch 2 and 3
            in_port = 1
            out_port = 2
           
            s2s3 = of.ofp_flow_mod()
            s2s3.match.in_port = in_port
            s2s3.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(s2s3)
           
            # Update switch 2 and 3
            in_port = 2
            out_port = 1
           
            s3s2 = of.ofp_flow_mod()
            s3s2.match.in_port = in_port
            s3s2.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(s3s2)
       
        elif dpid == '00-00-00-00-00-04':
           
            # h3 -> h1
            in_port = 3
            out_port = 1
           
            s4s2 = of.ofp_flow_mod()
            s4s2.match.in_port = in_port
            s4s2.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(s4s2)
           
            # h1 -> h3
            in_port = 1
            out_port = 3
           
            s2s4 = of.ofp_flow_mod()
            s2s4.match.in_port = in_port
            s2s4.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(s2s4)
           
            # h4 -> h2
            in_port = 4
            out_port = 2
           
            s4s3 = of.ofp_flow_mod()
            s4s3.match.in_port = in_port
            s4s3.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(s4s3)
           
            # h2 -> h4
            in_port = 2
            out_port =4
           
            s3s4 = of.ofp_flow_mod()
            s3s4.match.in_port = in_port
            s3s4.actions.append(of.ofp_action_output(port=out_port))
            event.connection.send(s3s4)



def launch():
    # Run spanning tree so that we can deal with topologies with loops
    pox.openflow.discovery.launch()
    pox.openflow.spanning_tree.launch()

    '''
    Starting the Topology Slicing module
    '''
    core.registerNew(TopologySlice)
