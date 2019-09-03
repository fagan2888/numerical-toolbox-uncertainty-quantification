**************************************
Exploration Uncertainty Quantification
**************************************

.. image:: https://travis-ci.org/OpenSourceEconomics/numerical-toolbox-uncertainty-quantification.svg?branch=master
    :target: https://travis-ci.org/OpenSourceEconomics/numerical-toolbox-uncertainty-quantification

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
     :target: https://github.com/OpenSourceEconomics/numerical-toolbox-uncertainty-quantification/blob/master/LICENSE

.. image:: https://static.mybinder.org/badge_logo.svg
     :target: https://hub.gke.mybinder.org/user/opensourceecono--quantification-r5b326rz/notebooks/uncertainty-quantification/uq-exploration.ipynb

.. image:: https://github.com/jupyter/design/blob/master/logos/Badges/nbviewer_badge.svg
     :target: https://nbviewer.jupyter.org/github/OpenSourceEconomics/numerical-toolbox-uncertainty-quantification/blob/master/uncertainty-quantification/uq-exploration.ipynb

|

This repository conducts a explorative Monte-Carlo Uncertainty Quantification for 
Quantities of Interests of the Discrete Occupation Choice Dynamic Programming Model
in *Keane and Wolpin (1994)*. Our exploration is described in this `notebook <https://github.com/OpenSourceEconomics/numerical-toolbox-uncertainty-quantification/blob/master/uncertainty-quantification/uq-exploration.ipynb>`_.


Implementation
##############

To solve and simulate the model, we use the open-source software `respy <https://github.com/OpenSourceEconomics/respy>`_ and `estimagic <https://github.com/OpenSourceEconomics/estimagic>`_.
Because the Monte-Carlo simulations require a long computation time, the relevant data
is stored as json in folder``uncertainty-quantification/json``.
To illustrate the program, it is run for a small number of iterations in the
jupyter notebook 
``uncertainty-quantification/uq-exploration.ipynb``.


Reference
#########

Keane, M. P. & Wolpin, W. I. (1994). `The Solution and Estimation of 
Discrete Choice Dynamic Pogramming Models by Simulation and Interpolation: Monte Carlo
Evidence <http://research.economics.unsw.edu.au/mkeane/Solution_Estimation_DP.pdf>`_, 
*Review of Economics and Statistics*, 76(4): 648-672.




