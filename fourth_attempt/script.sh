#Comandos:

#!Inicia a topologia: 
#xterm -hold -e "sudo python3 topologia.py" 
sudo python3 topologia.py

#!Inicia a API
#xterm -hold -e "ryu-manager ryu.app.rest_qos qos_simple_switch_13.py ryu.app.rest_conf_switch"
ryu-manager ryu.app.rest_qos qos_simple_switch_13.py ryu.app.rest_conf_switch


#Adiciona o OVSDB address
curl -X PUT -d '"tcp:127.0.0.1:6632"' http://localhost:8080/v1.0/conf/switches/0000000000000001/ovsdb_addr

#Adiciona as Queues 
#! O max_rate ali limita a BW da porta

Opcoes abaixo: #! Max rate tá 100MB pra usar o link do mininet
  1 - Ninguem briga
    curl -X POST -d '{"port_name": "s1-eth4", "type": "linux-htb","max_rate": "100000000", "queues": [{"max_rate": "1000000", "min_rate": "0000000" },{"max_rate": "2000000","min_rate": "1000000"},{"max_rate": "3000000","min_rate": "2000000"}]}' http://localhost:8080/qos/queue/0000000000000001
  2 - Testa min rate de 1 e 2 e 0 será despriorizado
    curl -X POST -d '{"port_name": "s1-eth4", "type": "linux-htb","max_rate": "100000000", "queues": [{ "max_rate": "5000000" },{"min_rate": "4000000"},{"min_rate": "4000000"}]}' http://localhost:8080/qos/queue/0000000000000001

#Adiciona o QoS

# Antigos #! Aqui o nw_dst não faz sentido, já que todos são o mesmo. nw_src pode ajudar. MUDEI AQUI
        curl -X POST -d '{"match": {"nw_src": "10.0.0.1", "nw_proto": "UDP", "tp_dst": "5001"}, "actions":{"queue": "0"}}' http://localhost:8080/qos/rules/0000000000000001
        curl -X POST -d '{"match": {"nw_src": "10.0.0.2", "nw_proto": "UDP", "tp_dst": "5002"}, "actions":{"queue": "1"}}' http://localhost:8080/qos/rules/0000000000000001
        curl -X POST -d '{"match": {"nw_src": "10.0.0.3", "nw_proto": "UDP", "tp_dst": "5003"}, "actions":{"queue": "2"}}' http://localhost:8080/qos/rules/0000000000000001

#! Novos -- IP: Testar

curl -X POST -d '{"match": {"nw_src": "10.0.0.1/32" }, "actions": {"queue": "0"}}' http://localhost:8080/qos/rules/0000000000000001
curl -X POST -d '{"match": {"nw_src": "10.0.0.2/32" }, "actions": {"queue": "1"}}' http://localhost:8080/qos/rules/0000000000000001
curl -X POST -d '{"match": {"nw_src": "10.0.0.3/32" }, "actions": {"queue": "2"}}' http://localhost:8080/qos/rules/0000000000000001

#! Novos -- Porta -- Rever esse:

curl -X POST -d '{"match": {"in_port": "5001" ,"nw_proto": "UDP", "dl_type":"IPv4"}, "actions": {"queue": "0"}}' http://localhost:8080/qos/rules/0000000000000001
curl -X POST -d '{"match": {"in_port": "5002" ,"nw_proto": "UDP", "dl_type":"IPv4"}, "actions": {"queue": "1"}}' http://localhost:8080/qos/rules/0000000000000001
curl -X POST -d '{"match": {"in_port": "5003" ,"nw_proto": "UDP", "dl_type":"IPv4"}, "actions": {"queue": "2"}}' http://localhost:8080/qos/rules/0000000000000001

# No mininet:#h4:
h4 iperf -s -u -i 1 -p 5001 > outputs/h4_server_h1 &
h4 iperf -s -u -i 1 -p 5002 > outputs/h4_server_h2 &
h4 iperf -s -u -i 1 -p 5003 > outputs/h4_server_h3 &

iperf -s -u -i 1 -p 5001 > outputs/h4_server_h1
iperf -s -u -i 1 -p 5002 > outputs/h4_server_h2
iperf -s -u -i 1 -p 5003 > outputs/h4_server_h3


 h4 xterm -e 'iperf -s -u -i 1 -p 5001 > outputs/h4_server_h1'

#h1 to h3 (clients):

h1 iperf -c 10.0.0.4 -p 5001 -u -b 10M -t 30 &
h2 iperf -c 10.0.0.4 -p 5002 -u -b 10M -t 20 &
h3 iperf -c 10.0.0.4 -p 5003 -u -b 10M -t 10 &