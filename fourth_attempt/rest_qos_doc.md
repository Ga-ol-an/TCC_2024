
# =============================
#          REST API
# =============================
#
#  Note: specify switch and vlan group, as follows.
#   {switch-id} : 'all' or switchID
#   {vlan-id}   : 'all' or vlanID
#
# about queue status
#
# get status of queue
# GET /qos/queue/status/{switch-id}
#
# about queues
# get a queue configurations
# GET /qos/queue/{switch-id}
#
# set a queue to the switches
# POST /qos/queue/{switch-id}
#
# request body format:
#  {"port_name":"<name of port>",
#   "type": "<linux-htb or linux-other>",
#   "max-rate": "<int>",
#   "queues":[{"max_rate": "<int>", "min_rate": "<int>"},...]}
#
#   Note: This operation override
#         previous configurations.
#   Note: Queue configurations are available for
#         OpenvSwitch.
#   Note: port_name is optional argument.
#         If does not pass the port_name argument,
#         all ports are target for configuration.
#
# delete queue
# DELETE /qos/queue/{swtich-id}
#
#   Note: This operation delete relation of qos record from
#         qos colum in Port table. Therefore,
#         QoS records and Queue records will remain.
#
# about qos rules
#
# get rules of qos
# * for no vlan
# GET /qos/rules/{switch-id}
#
# * for specific vlan group
# GET /qos/rules/{switch-id}/{vlan-id}
#
# set a qos rules
#
#   QoS rules will do the processing pipeline,
#   which entries are register the first table (by default table id 0)
#   and process will apply and go to next table.
#
# * for no vlan
# POST /qos/{switch-id}
#
# * for specific vlan group
# POST /qos/{switch-id}/{vlan-id}
#
#  request body format:
#   {"priority": "<value>",
#    "match": {"<field1>": "<value1>", "<field2>": "<value2>",...},
#    "actions": {"<action1>": "<value1>", "<action2>": "<value2>",...}
#   }
#
#  Description
#    * priority field
#     <value>
#    "0 to 65533"
#
#   Note: When "priority" has not been set up,
#         "priority: 1" is set to "priority".
#
#! Abaixo tem-se o que cada um significa
#    * match field
#     <field> : <value>
#    "in_port" : "<int>"
#    "dl_src"  : "<xx:xx:xx:xx:xx:xx>"
#    "dl_dst"  : "<xx:xx:xx:xx:xx:xx>"
#    "dl_type" : "<ARP or IPv4 or IPv6>"
#    "nw_src"  : "<A.B.C.D/M>"
#    "nw_dst"  : "<A.B.C.D/M>"
#    "ipv6_src": "<xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx/M>"
#    "ipv6_dst": "<xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx/M>"
#    "nw_proto": "<TCP or UDP or ICMP or ICMPv6>"
#    "tp_src"  : "<int>"
#    "tp_dst"  : "<int>"
#    "ip_dscp" : "<int>"
#
#    * actions field
#     <field> : <value>
#    "mark": <dscp-value>
#    sets the IPv4 ToS/DSCP field to tos.
#    "meter": <meter-id>
#    apply meter entry
#    "queue": <queue-id>
#    register queue specified by queue-id
#
#   Note: When "actions" has not been set up,
#         "queue: 0" is set to "actions".
#
# delete a qos rules
# * for no vlan
# DELETE /qos/rule/{switch-id}
#
# * for specific vlan group
# DELETE /qos/{switch-id}/{vlan-id}
#
#  request body format:
#   {"<field>":"<value>"}
#
#     <field>  : <value>
#    "qos_id" : "<int>" or "all"
#
# about meter entries
#
# set a meter entry
# POST /qos/meter/{switch-id}
#
#  request body format:
#   {"meter_id": <int>,
#    "bands":[{"action": "<DROP or DSCP_REMARK>",
#              "flag": "<KBPS or PKTPS or BURST or STATS"
#              "burst_size": <int>,
#              "rate": <int>,
#              "prec_level": <int>},...]}
#
# delete a meter entry
# DELETE /qos/meter/{switch-id}
#
#  request body format:
#   {"<field>":"<value>"}
#
#     <field>  : <value>
#    "meter_id" : "<int>"
#




"in_port": The input port number where the packet was received. It's important for the switch to know where the packet came from to make forwarding decisions.

"dl_src": The source MAC address of the Ethernet frame.

"dl_dst": The destination MAC address of the Ethernet frame.

"dl_type": The type of Ethernet frame, which could be ARP, IPv4, or IPv6. This field helps the switch understand how to process the packet.

"nw_src": The source IP address for the packet, which can be specified with a subnet mask (e.g., A.B.C.D/M). This is used for layer 3 (network layer) forwarding decisions.

"nw_dst": The destination IP address for the packet, also potentially with a subnet mask.

"ipv6_src": The source IPv6 address, specified similarly with a subnet mask for network layer decisions in IPv6 networks.

"ipv6_dst": The destination IPv6 address with an optional subnet mask.

"nw_proto": The network protocol used (e.g., TCP, UDP, ICMP for IPv4, and ICMPv6 for IPv6). This field is crucial for determining how to process the packet at the transport layer.

"tp_src": The source port of the transport layer (e.g., for TCP or UDP). This helps in filtering and forwarding decisions, especially for service differentiation or security functions.

"tp_dst": The destination port of the transport layer. Like the source port, it's used for determining the destination service or application.

"ip_dscp": The Differentiated Services Code Point, which is used for Quality of Service (QoS) in IP networks. This field tells network equipment what kind of forwarding precedence to give the packet.

