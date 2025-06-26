import model_generation.models.model_1.quasi_variable_cog.params as pm
import model_generation.utils.utils as util
from sympy import *
"""Comparing model with variable CoG and constant CoG, transforming the coordinates from constant CoG,
to the frame of that with variable CoG"""

"""
C massesenter når tankene er tomme 0 0 H/2
D origo i den variable CoG modellen 0 0 0
r_DC = 0 0 H/2

X = x_constant_cg - R^b_n * r_DC
"""