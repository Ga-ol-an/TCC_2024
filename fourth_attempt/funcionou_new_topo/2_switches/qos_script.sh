#!/bin/bash

## Add switch address to the app
curl -X PUT -d '"tcp:127.0.0.1:6632"' http://localhost:8080/v1.0/conf/switches/0000000000000001/ovsdb_addr 
sleep .5 # Waits 0.5 second.
curl -X PUT -d '"tcp:127.0.0.1:6632"' http://localhost:8080/v1.0/conf/switches/0000000000000002/ovsdb_addr 
echo 
sleep .5 # Waits 0.5 second.

#! ###################### S1  ###################### 
# ## Add the queues
# curl -X POST -d '{"port_name": "s1-eth4", "type": "linux-htb","max_rate": "10000000", "queues":[{"min_rate": "1000000" },{"min_rate": "3000000"},{"min_rate": "5000000"}]}' http://localhost:8080/qos/queue/0000000000000001
# echo 
# sleep .5 # Waits 0.5 second.
# ##A Add the QoS -- Port
# curl -X POST -d '{"priority": "1","match": { "tp_dst": "5001" ,"nw_proto": "UDP", "dl_type":"IPv4"}, "actions": {"queue": "0"}}' http://localhost:8080/qos/rules/0000000000000001 
# echo 
# sleep .5 # Waits 0.5 second.
# curl -X POST -d '{"priority": "1","match": { "tp_dst": "5002" ,"nw_proto": "UDP", "dl_type":"IPv4"}, "actions": {"queue": "1"}}' http://localhost:8080/qos/rules/0000000000000001 
# echo 
# sleep .5 # Waits 0.5 second.
# curl -X POST -d '{"priority": "1","match": { "tp_dst": "5003" ,"nw_proto": "UDP", "dl_type":"IPv4"}, "actions": {"queue": "2"}}' http://localhost:8080/qos/rules/0000000000000001 
# echo

#! ###################### S2  ###################### 

## Add the queues
curl -X POST -d '{"port_name": "s3-eth1", "type": "linux-htb","max_rate": "10000000", "queues":[{"min_rate": "1000000" },{"min_rate": "3000000"},{"min_rate": "5000000"}]}' http://localhost:8080/qos/queue/0000000000000002
echo 
sleep .5 # Waits 0.5 second.
##A Add the QoS -- Port
curl -X POST -d '{"priority": "1","match": { "tp_dst": "5001" ,"nw_proto": "UDP", "dl_type":"IPv4"}, "actions": {"queue": "0"}}' http://localhost:8080/qos/rules/0000000000000002 
echo 
sleep .5 # Waits 0.5 second.
curl -X POST -d '{"priority": "1","match": { "tp_dst": "5002" ,"nw_proto": "UDP", "dl_type":"IPv4"}, "actions": {"queue": "1"}}' http://localhost:8080/qos/rules/0000000000000002 
echo 
sleep .5 # Waits 0.5 second.
curl -X POST -d '{"priority": "1","match": { "tp_dst": "5003" ,"nw_proto": "UDP", "dl_type":"IPv4"}, "actions": {"queue": "2"}}' http://localhost:8080/qos/rules/0000000000000002 
echo