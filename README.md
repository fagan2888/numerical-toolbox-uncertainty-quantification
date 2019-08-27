### Caution: Please make sure to download my notebook and to view it via jupyter!
The notebook version in the browser is not updating. Thus an old, incomplete version is shown. <br>
(See: https://github.com/jupyter/notebook/issues/3035)

# Monte-Carlo Uncertainty Quantification for Keane/Wolpin(1997)

## Abstract

This repository conducts a Monte-Carlo Uncertainty Quantification for statistics
in *Keane/Wolpin(1997)*. Thereby, the statistics are computed.

**Section 1** sketches the concept of Uncertainty Quantification and gives a 
short, illustrative example. **Section 2** presents the Extended Discrete Dynamic Occupation Choice Model developed by *Keane/Wolpin(1997)*. **Section 3** and **Section 4** compute the Quantities of Interest. **Section 5** presents the results of the Uncertainty Quantification. **Section 6** concludes.


## Replication

To solve and simulate the model, I rely on the open-source software [*respy*](https://github.com/OpenSourceEconomics/respy) and [*estimagic*](https://github.com/OpenSourceEconomics/estimagic).
Because the Monte-Carlo simulations require a long computation time, the relevant data
is stored as pickles in `auxiliary\results`. If you still want to run a replication, follow these steps:

1. Make sure to install the right version of *respy* by executing
`pip install git+git://github.com/OpenSourceEconomics/respy.git@7d035c0dcd1ea1d17cd02741408411e7eec5c5b8`
2. Run `auxiliary\kw97_replication.py` and `auxiliary\monte_carlo_uncertainty.py`
3. Run `auxiliary\visualize.py`


## Reference

Keane, M. P. & Wolpin, W. I. (1997). [The career Decisions of Young Men.](https://www.jstor.org/stable/10.1086/262080), 
*Journal of Political Economy, 105(3): 473-552.*105(3): 473-552.


[![Build Status](https://travis-ci.org/HumanCapitalAnalysis/student-project-tostenzel.svg?branch=master)](https://travis-ci.org/HumanCapitalAnalysis/student-project-tostenzel)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](HumanCapitalAnalysis/student-project-template/blob/master/LICENSE)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HumanCapitalAnalysis/student-project-tostenzel/master?urlpath=https%3A%2F%2Fgithub.com%2FHumanCapitalAnalysis%2Fstudent-project-tostenzel%2Fblob%2Fmaster%2Fstudent_project.ipynb)



