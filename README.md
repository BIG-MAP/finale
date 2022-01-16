# finale
_f_ast _in_tention _a_gnostic _l_earning _e_nvironment

# how to run
Copy this repo and run docker build
```console
foo@bar:~$ docker build -t finaledocker .
```
Then run the image
```console
foo@bar:~$ docker run -d --name finalecontainer -p 13371:13371 finaledocker
foo
```
# todo 

Prio 1:
3. PENDING: implement fidelity aware ML model from helge

Prio 2:
2. Write manuscript draft of the whole thing

Prio unimportant:
1. one could restructure database for more cross references to make it suitable for a graph database
2. implement better database 
