

[![DOI](https://zenodo.org/badge/442139626.svg)](https://zenodo.org/badge/latestdoi/442139626)


There have been many attempts at orchestrating single or multiple instruments; even laboratories exist that are automated but the real questions are: 

> What really constitutes a materials platform?
> Why accelerate?

We seek to answer the "why" part with the fact that we need electrochemical energy storage systems (read: batteries) like yesterday but researching batteries cannot be done by a single lab or even modality. Enter the materials acceleration platform! We believe that a real "platform" needs to transcend the lab and involve more than one method from more than one modality (i.e. experiment, theory, manufacturing) that are likely spatially distributed across different countries. In this repo we have our alpha version of *finales* which helped us to orchestrate many partners from different labs in europe at the same time.

# finales
**f**ast **in**tention **a**gnostic **le**arning **s**erver

The basic idea is that we no longer have entities, called tenants, talk to each other but everyone talks to a central server by putting empty or filled out posts. Currently we allow users to ask/submit measurements for denisty, viscosity, conductivity or 1D spectral data.

The exact layout is described in **link to chemRxiv** and is being submitted to **journal of choice**

# to do

There is still lots of things to do that we currently consider to be work in progress

1. :no_entry_sign: 100% complete adoption of BattINFO i.e. everything that is not yet covered
2. :no_entry_sign: Sign up form (no hardcoded users)
3. :no_entry_sign: Tenants can post their capabilities and uptime
4. :no_entry_sign: Implementation of GraphDB

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

Then from some other computer you can run

```console
foo@bar:~$ python3 mock_init.py
foo
```

From the experiment computer you can run

```console
foo@bar:~$ python3 mock_experiment.py
foo
```

From the simulation computer you can run

```console
foo@bar:~$ python3 mock_simulation.py
foo
```

From the optimizer computer you can run

```console
foo@bar:~$ python3 mock_optimizer.py
foo
```


## Acknowledgements

This project has received funding from the European Union’s [Horizon 2020 research and innovation programme](https://ec.europa.eu/programmes/horizon2020/en) under grant agreement [No 957189](https://cordis.europa.eu/project/id/957189).
