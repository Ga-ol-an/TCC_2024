import json
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet

class QoSSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(QoSSwitch, self).__init__(*args, **kwargs)
        self.traffic_classes = self.read_traffic_classes('params')

    def read_traffic_classes(self, file_name):
        # Leitura do arquivo de configuração de classes de tráfego
        with open(file_name, 'r') as file:
            return json.load(file)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

        # Configuração de QoS para cada classe de tráfego
        for tc in self.traffic_classes:
            self.setup_qos(datapath, ofproto, parser, tc)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, instructions=inst)
        datapath.send_msg(mod)

    def setup_qos(self, datapath, ofproto, parser, traffic_class):
        # Configuração das filas baseadas nas classes de tráfego lidas do arquivo
        min_rate = traffic_class['min_rate']
        max_rate = traffic_class['max_rate']
        port = traffic_class['port']
        queues = [{'port_name': port, 'properties': {'min_rate': min_rate, 'max_rate': max_rate}}]
        req = parser.OFPQueueGetConfigRequest(datapath, port, queues)
        datapath.send_msg(req)

if __name__ == '__main__':
    from ryu.cmd import manager
    manager.main()
