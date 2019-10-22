**************************************
Exploration Uncertainty Quantification
**************************************

This repository conducts an explorative Monte-Carlo Uncertainty Quantification for 
Quantities of Interests of the Discrete Occupation Choice Dynamic Programming Model
in *Keane and Wolpin (1994)*. Our exploration is described in this `notebook <https://github.com/OpenSourceEconomics/numerical-toolbox-uncertainty-quantification/blob/master/uncertainty-quantification/uq-exploration.ipynb>`_. Its path is ``uncertainty-quantification/uq-exploration.ipynb``.

.. image:: https://github.com/jupyter/design/blob/master/logos/Badges/nbviewer_badge.svg
     :target: https://nbviewer.jupyter.org/github/OpenSourceEconomics/numerical-toolbox-uncertainty-quantification/blob/master/uncertainty-quantification/uq-exploration.ipynb
     
.. image:: https://static.mybinder.org/badge_logo.svg
     :target: https://mybinder.org/v2/gh/OpenSourceEconomics/numerical-toolbox-uncertainty-quantification/master?filepath=https%3A%2F%2Fgithub.com%2FOpenSourceEconomics%2Fnumerical-toolbox-uncertainty-quantification%2Fblob%2Fmaster%2Funcertainty-quantification%2Fuq-exploration.ipynb


Implementation
##############

To solve and simulate the showcase model, we use our research group's open-source software `respy <https://github.com/OpenSourceEconomics/respy>`_ and `estimagic <https://github.com/OpenSourceEconomics/estimagic>`_.
Because the Monte-Carlo simulations require a long computation time, the relevant data
is stored as json in folder ``uncertainty-quantification/json``.


Reference
#########

Keane, M. P. & Wolpin, W. I. (1994). `The Solution and Estimation of 
Discrete Choice Dynamic Pogramming Models by Simulation and Interpolation: Monte Carlo
Evidence <http://research.economics.unsw.edu.au/mkeane/Solution_Estimation_DP.pdf>`_, 
*Review of Economics and Statistics*, 76(4): 648-672.

----------------------------------------------------------------------------------------

.. image:: https://travis-ci.org/OpenSourceEconomics/numerical-toolbox-uncertainty-quantification.svg?branch=master
    :target: https://travis-ci.org/OpenSourceEconomics/numerical-toolbox-uncertainty-quantification

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
     :target: https://github.com/OpenSourceEconomics/numerical-toolbox-uncertainty-quantification/blob/master/LICENSE




