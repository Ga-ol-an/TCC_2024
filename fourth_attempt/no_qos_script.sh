#!/bin/bash
echo 'No QoS Script'
echo 
## Add switch address to the app
echo 'Adding switch address to the app'
curl -X PUT -d '"tcp:127.0.0.1:6632"' http://localhost:8080/v1.0/conf/switches/0000000000000001/ovsdb_addr 
sleep .5 # Waits 0.5 second.
curl -X PUT -d '"tcp:127.0.0.1:6632"' http://localhost:8080/v1.0/conf/switches/0000000000000002/ovsdb_addr 
sleep .5 # Waits 0.5 second.
curl -X PUT -d '"tcp:127.0.0.1:6632"' http://localhost:8080/v1.0/conf/switches/0000000000000003/ovsdb_addr 
echo 
sleep .5 # Waits 0.5 second.

echo 'Adding the queues'
curl -X POST -d '{"port_name": "s3-eth1", "type": "linux-htb","max_rate": "10000000", "queues":[{"max_rate": "10000000"}]}' http://localhost:8080/qos/queue/0000000000000003
echo