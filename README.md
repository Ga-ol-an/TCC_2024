
#  Undergraduate Thesis - Gabriel de Oliveira Andrade - 2024

## This work as done as the final project of Electric Engeneering course, at the Federal University of Minas Gerais. 

### Advisor: Prof. Luciano de Errico

### Steps to reproduce the work:

At  first,  make  sure  you  have  the  outputs  and  sub  folders  created.  If  you  dont  have,  run  the  following  script,  for  Linux  Ubuntu:

```
> ./create_outputs_folder.sh
```
  

To  run  the  system,  you  will  need  3  terminals. Keep the three terminals opened and run the following commands:


#### Terminal  1:
```
> sudo  python3  topologia.py
```
  

#### Terminal  2:

```
> ryu-manager  ryu.app.rest_qos  qos_simple_switch_13.py  ryu.app.rest_conf_switch
```
  

#### Terminal  3:

\# Testing  with  QoS:
```
> ./qos_script.sh
```

\# Testing  without  QoS:
```
> ./no_qos_script.sh
  ```

Then go  to  the  Terminal  1  and  run  the  desired  test, on the mininet CLI.  You can choose  one  or  more  of  the  following  options:
```
mininet> source  ./real_scen.sh
mininet> source  ./var_scen.sh
mininet> source  ./stab_scen.sh
mininet> source  ./realist_latency_evaluation.sh
mininet> source  ./stable_latency_evaluation.sh
```

  
At  the  end  of  the  tests,  the  desired  outputs  will be  stored  in  the  "outputs"  folder, on the specified subfolder.

  
Part  of  this  work  was  based  on  the  tutorial  on  the  following  link:  https://osrg.github.io/ryu-book/en/html/rest_qos.html