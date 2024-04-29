# Essa é o app puro do ryu

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types


class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        
    

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        #! Aqui chega
        print('parece que começou')
        
        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.7
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        print(parser.OFPFlowStatsRequest(datapath))

    ##########################
    # Adicionei aqui 
   ##########################
  
    @set_ev_cls(ofp_event.EventOFPDescStatsReply, MAIN_DISPATCHER)
    def desc_stats_reply_handler(self, ev):
      body = ev.msg.body
  
      
      print('Se isso aqui apareceu, deu bom')
      print(body)
      """ self.logger.debug('DescStats: mfr_desc=%s hw_desc=%s sw_desc=%s '
                        'serial_num=%s dp_desc=%s',
                        body.mfr_desc, body.hw_desc, body.sw_desc,
                        body.serial_num, body.dp_desc) """

    def send_port_stats_request(self, datapath):
      ofp = datapath.ofproto
      ofp_parser = datapath.ofproto_parser

      
      req = ofp_parser.OFPPortStatsRequest(datapath, 0, ofp.OFPP_ANY)
      datapath.send_msg(req)

    #! Ver como usar isso:
    #* Dǘuida: pra que eu consiga mudar a minha porta, que função eu devo pegar?
    #parser.OFPQueueGetConfigRequest(datapath, port)
    #ofp.parser.OFPQueueGetConfigReply -> classryu.ofproto.ofproto_v1_3_parser.OFPQueueGetConfigReply(datapath, queues=None, port=None)
    #ofp_parser.OFPPort -> https://ryu.readthedocs.io/en/latest/ofproto_v1_3_ref.html#ryu.ofproto.ofproto_v1_3_parser.OFPPort
    #ofp_parser.OFPActionSetQueue(queue_id) (https://ryu.readthedocs.io/en/latest/ofproto_v1_3_ref.html#ryu.ofproto.ofproto_v1_3_parser.OFPActionSetQueue)
    ####################################################
    
    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        print("packet_in")
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src

        dpid = format(datapath.id, "d").zfill(16)
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
        
        ## Acho que deu bom?????
      
        queue =  [
                {
                    "OFPPacketQueue": {
                      "len": 64, 
                      "port": 77, 
                      "properties": [
                          {
                            "OFPQueuePropMinRate": {
                                "len": 16, 
                                "property": 1, 
                                "rate": 10
                            }
                          }, 
                          {
                            "OFPQueuePropMaxRate": {
                                "len": 16, 
                                "property": 2, 
                                "rate": 900
                            }
                          },
                          {
                            "OFPQueuePropExperimenter": {
                                "data": [], 
                                "experimenter": 999, 
                                "len": 16, 
                                "property": 65535
                            }
                          }
                      ], 
                      "queue_id": 99
                    }
                }, 
                {
                    "OFPPacketQueue": {
                      "len": 65, 
                      "port": 77, 
                      "properties": [
                          {
                            "OFPQueuePropMinRate": {
                                "len": 16, 
                                "property": 1, 
                                "rate": 100
                            }
                          }, 
                          {
                            "OFPQueuePropMaxRate": {
                                "len": 16, 
                                "property": 2, 
                                "rate": 200
                            }
                          },
                          {
                            "OFPQueuePropExperimenter": {
                                "experimenter": 999, 
                                "data": [
                                  1
                                ], 
                                "len": 17, 
                                "property": 65535
                            }
                          }
                      ], 
                      "queue_id": 88
                    }
                },
                {
                    "OFPPacketQueue": {
                      "len": 66, 
                      "port": 77, 
                      "properties": [
                          {
                            "OFPQueuePropMinRate": {
                                "len": 16, 
                                "property": 1, 
                                "rate": 200
                            }
                          }, 
                          {
                            "OFPQueuePropMaxRate": {
                                "len": 16, 
                                "property": 2, 
                                "rate": 400
                            }
                          },
                          {
                            "OFPQueuePropExperimenter": {
                                "experimenter": 999, 
                                "data": [
                                  1, 
                                  2
                                ], 
                                "len": 18, 
                                "property": 65535
                            }
                          }
                      ], 
                      "queue_id": 77
                    }
                }
              ]
        
        #! Adicionei isso aqui tbm
        print(parser.OFPQueueGetConfigReply(datapath, port=4294967295, queues=queue))
        #! FAzer os seguintes testes amanha:
        # VEr se esse config que eu criei realmente funciona, testando com o iperf a largura de banda na porta
        # ver se adiciono ele em outro local (pra um codigo mais limpo)
        print(parser.OFPPort)
        
        
        