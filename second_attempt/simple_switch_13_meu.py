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
        ##########################
        #! Adicionei abaixo daqui 
        ##########################
        print('parece que começou')
        
        ## Acho que deu bom?????
      
        queue =  [
                {
                    "OFPPacketQueue": {
                      "len": 48, 
                      "port": 6000, 
                      "properties": [
                          {
                            "OFPQueuePropMinRate": {
                                "len": 16, 
                                "property": 1, 
                                "rate": 1
                            }
                          }, 
                          {
                            "OFPQueuePropMaxRate": {
                                "len": 16, 
                                "property": 2, 
                                "rate": 500
                            }
                          }
                      ], 
                      "queue_id": 99
                    }
                }, 
                {
                    "OFPPacketQueue": {
                      "len": 48, 
                      "port": 6001, 
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
                                "rate": 1000
                            }
                          }
                      ], 
                      "queue_id": 88
                    }
                },
                {
                    "OFPPacketQueue": {
                      "len": 48, 
                      "port": 6002, 
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
                                "rate": 2000
                            }
                          }], 
                      "queue_id": 77
                    }
                },
                {
                    "OFPPacketQueue": {
                      "len": 48, 
                      "port": 6003, 
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
                                "rate": 3000
                            }
                          }], 
                      "queue_id": 78
                    }
                }
              ]
        
        #! Adicionei isso aqui tbm
        # print(parser.OFPQueueGetConfigReply(datapath, port=4294967295, queues=queue))
        #! FAzer os seguintes testes amanha:
        # Ver se esse config que eu criei realmente funciona, testando com o iperf a largura de banda na porta
        # ver se adiciono ele em outro local (pra um codigo mais limpo)
        print(parser.OFPPort)
        
        ##########################
        #! Adicionei acima daqui
        ##########################
         
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
        # print(parser.OFPFlowStatsRequest(datapath))

    ##########################
    # Adicionei aqui 
   ##########################
   
   
    def send_queue_get_config_request(self, datapath):
      ofp = datapath.ofproto
      ofp_parser = datapath.ofproto_parser

      req = ofp_parser.OFPQueueGetConfigRequest(datapath, ofp.OFPP_ANY)
      datapath.send_msg(req)
   
  
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

    ##########################
    #! Ver como usar isso:
    ##########################
    #* Dúvida: pra que eu consiga mudar a minha porta, que função eu devo pegar (SET ou GET)?

    """ def set_queue(self, rest, vlan_id):
        if self.ovs_bridge is None:
            msg = {'result': 'failure',
                   'details': 'ovs_bridge is not exists'}
            return REST_COMMAND_RESULT, msg

        port_name = rest.get(REST_PORT_NAME, None)
        vif_ports = self.ovs_bridge.get_port_name_list()

        if port_name is not None:
            if port_name not in vif_ports:
                raise ValueError('%s port is not exists' % port_name)
            vif_ports = [port_name]

        queue_list = {}
        queue_type = rest.get(REST_QUEUE_TYPE, 'linux-htb')
        parent_max_rate = rest.get(REST_QUEUE_MAX_RATE, None)
        queues = rest.get(REST_QUEUES, [])
        queue_id = 0
        queue_config = []
        for queue in queues:
            max_rate = queue.get(REST_QUEUE_MAX_RATE, None)
            min_rate = queue.get(REST_QUEUE_MIN_RATE, None)
            if max_rate is None and min_rate is None:
                raise ValueError('Required to specify max_rate or min_rate')
            config = {}
            if max_rate is not None:
                config['max-rate'] = max_rate
            if min_rate is not None:
                config['min-rate'] = min_rate
            if len(config):
                queue_config.append(config)
            queue_list[queue_id] = {'config': config}
            queue_id += 1

        for port_name in vif_ports:
            try:
                self.ovs_bridge.set_qos(port_name, type=queue_type,
                                        max_rate=parent_max_rate,
                                        queues=queue_config)
            except Exception as msg:
                raise ValueError(msg)
            self.queue_list[port_name] = queue_list

        msg = {'result': 'success',
               'details': queue_list}

        return REST_COMMAND_RESULT, msg"""

      
      
      """ do arq rest_qos   
      def set_qos(self, port_name, type='linux-htb', max_rate=None, queues=None):
        
        Sets a Qos rule and creates Queues on the given port.
        
        queues = queues if queues else []
        command_qos = ovs_vsctl.VSCtlCommand(
            'set-qos',
            [port_name, type, max_rate])
        command_queue = ovs_vsctl.VSCtlCommand(
            'set-queue',
            [port_name, queues])
        self.run_command([command_qos, command_queue])
        if command_qos.result and command_queue.result:
            return command_qos.result + command_queue.result
        return None 
        
      def del_qos(self, port_name):
        
        Deletes the Qos rule on the given port.
        
        command = ovs_vsctl.VSCtlCommand(
            'del-qos',
            [port_name])
        self.run_command([command])
        """

    # self.ovs_bridge.get_port_name_list()
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
        

        