
from ryu.ofproto import ofproto_v1_3 as ofp
from ryu.ofproto import ofproto_v1_3_parser as ofp_parser

match = ofp_parser.OFPMatch(in_port=1, eth_dst='ff:ff:ff:ff:ff:ff')

actions = [ofp_parser.OFPActionSetQueue(queue_id=3), ofp_parser.OFPActionOutput(port=ofp.OFPP_NORMAL)]

instructions = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
datapath.send_msg(ofp_parser.OFPFlowMod(datapath, match=match, instructions=instructions))
