
# Trabalho de Conclusão Final - Gabriel de Oliveira Andrade - 2024

## Este trabalho foi realizado como o Trabalho de Conclusão Final do curso de Engenharia Elétrica, na Universidade Federal de Minas Gerais.

### Orientador: Prof. Luciano de Errico

### Passos para reproduzir o trabalho:

Primeiro, certifique-se de que você possui a pasta outputs e as subpastas criadas. Se não tiver, execute o seguinte script, para Linux Ubuntu:

```
> ./create_outputs_folder.sh
```

Para executar o sistema, você precisará de 3 terminais. Mantenha os três terminais abertos e execute os seguintes comandos:

#### Terminal 1:

```
> sudo python3 topologia.py
```

#### Terminal 2:

```
> ryu-manager ryu.app.rest_qos qos_simple_switch_13.py ryu.app.rest_conf_switch
```

#### Terminal 3:

\# Testando com QoS:

```
> ./qos_script.sh
```

\# Testando sem QoS:

```
> ./no_qos_script.sh
```

Depois, vá para o Terminal 1 e execute o teste desejado na CLI do mininet. Você pode escolher uma ou mais das seguintes opções:

```
mininet> source ./real_scen.sh
mininet> source ./var_scen.sh
mininet> source ./stab_scen.sh
mininet> source ./realist_latency_evaluation.sh
mininet> source ./stable_latency_evaluation.sh
```

No final dos testes, as saídas desejadas serão armazenadas na pasta "outputs", na subpasta especificada.

Parte deste trabalho foi baseada no tutorial disponível no seguinte link: https://osrg.github.io/ryu-book/en/html/rest_qos.html