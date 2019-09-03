*************************************************************
Monte-Carlo Uncertainty Quantification for Keane/Wolpin(1994)
*************************************************************

.. image:: https://travis-ci.org/OpenSourceEconomics/numerical-toolbox-uncertainty-quantification.svg?branch=master
    :target: https://travis-ci.org/OpenSourceEconomics/numerical-toolbox-uncertainty-quantification

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black

This repository conducts a Monte-Carlo Uncertainty Quantification for 
Quantities of Interests in *Keane/Wolpin(1994)*. Thereby, these Quantities
are computed.



Replication
###########

To solve and simulate the model, I rely on the open-source software [*respy*](https://github.com/OpenSourceEconomics/respy) and [*estimagic*](https://github.com/OpenSourceEconomics/estimagic).
Because the Monte-Carlo simulations require a long computation time, the relevant data
is stored as pickles in `auxiliary\results`.
To illustrate the program, the programs are run for a small number of iterations in the jupyter notebook


Reference
*********
Keane, M. P. & Wolpin, W. I. (1994). [The Solution and Estimation of 
Discrete Choice Dynamic Pogramming Models by Simulation and Interpolation: Monte Carlo
Evidence](http://research.economics.unsw.edu.au/mkeane/Solution_Estimation_DP.pdf), 
*Review of Economics and Statistics*, 76(4): 648-672.




