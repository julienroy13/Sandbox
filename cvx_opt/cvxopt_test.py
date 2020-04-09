# LINKS to documentation:
# - https://cvxopt.org/
# - https://cvxopt.org/examples/tutorial/lp.html
# - https://cvxopt.org/userguide/coneprog.html#linear-programming
# example mdp: https://github.com/pierrelux/vfpolytope/blob/master/polytope.ipynb

# Goal: put the LP presented in p.18 of Pierre-Luc's notes so that it can be solved by cvxopt solvers

from cvxopt import matrix, solvers
import numpy as np
from cvx_opt.mdp_example import mdp_fig2d

A = matrix([[-1.0, -1.0, 0.0, 1.0], [1.0, -1.0, -1.0, -2.0]])
b = matrix([1.0, -2.0, 0.0, 4.0])
c = matrix([2.0, 1.0])

sol = solvers.lp(c, A, b)
print(sol['x'])


P, R, discount = mdp_fig2d()

alpha = np.array([0.5, 0.5])
h = np.flatten(R)


# solution: (1.0272725,)