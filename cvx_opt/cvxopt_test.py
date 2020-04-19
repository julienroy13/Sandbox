# LINKS to documentation:
# - https://cvxopt.org/
# - https://cvxopt.org/examples/tutorial/lp.html
# - https://cvxopt.org/userguide/coneprog.html#linear-programming
# example mdp: https://github.com/pierrelux/vfpolytope/blob/master/polytope.ipynb

# Goal: put the LP presented in p.18 of Pierre-Luc's notes so that it can be solved by cvxopt solvers

from cvxopt import matrix, solvers
import numpy as np
from cvx_opt.mdp_example import mdp_fig2d

# =======================================
# EXAMPLE
#
#Procedure:
# 1. Put objective in the form: minimize c.T @ x
# 2. Put constraint set is form Ax <= b  with A.shape=(n_constraints, n_variables)
#
#Maths:
#    minimize    2*x1 + x2
#
#       s.t.     -x1 + x2   <= 1
#                -x1 - x2   <= -2
#                    - x2   <= 0
#                 x1 - 2*x2 <= 4
#Code:
# A = matrix(np.array([[-1.,  1.],
#                      [-1., -1.],
#                      [ 0., -1.],
#                      [ 1., -2.]]))
#
# b = matrix([1.0, -2.0, 0.0, 4.0])
# c = matrix([2.0, 1.0])
#
# sol = solvers.lp(c, A, b)
# print([f"{x:.2f}" for x in sol['x']])


# =======================================
# LP for Value Iteration

P, R, discount = mdp_fig2d()

# P is of shape (2,2,2): 1st dim = states, 2nd dim = actions, 3rd dim = next states
# R is of shape (2,2): 1st dim = states, 2nd dim = actions

# We want to solve this MDP by finding the optimal value function
# This problem can be formulated as a Linear Program of the form:
#
#    minimize    c @ v
#
#       s.t.     -v(s) + gamma * \sum_s' p(s'|s,a)v(s')  <=  - r(s,a)
#

LL = np.array([[-1.0, -1.0, 0.0, 1.0], [1.0, -1.0, -1.0, -2.0]])

c = matrix([0.5, 0.5])
b = matrix(R.flatten()) * -1.

A1 = np.array([discount * P[0, :, 0] - 1, discount * P[0, :, 1]])
A2 = np.array([discount * P[0, :, 0], discount * P[0, :, 1] - 1])

A = np.concatenate([A1, A2], axis=1).T

sol = solvers.lp(c=c, G=matrix(A), h=b)
print([f"v(s={i})={v:.2f}" for i, v in enumerate(sol['x'])])

# solution: (1.0272725,)