import numpy as np
from sympy import Matrix, cos, sin, pi

def dh_transform (theta, d, a, alpha):
    T = np.array([
        [np.cos(theta), -np.sin(theta) * np.cos(alpha), np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
        [np.sin(theta), np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
        [0, np.sin(alpha), np.cos(alpha), d],
        [0, 0, 0, 1]
    ])

    return T

def dh_theta (theta, d, a, alpha):
    T = lambda theta: dh_transform(theta, d, a, alpha)
    return T

def dh_d (theta, d, a, alpha):
    T = lambda d: dh_transform(theta, d, a, alpha)
    return T

def dh_a (theta, d, a, alpha):
    T = lambda a: dh_transform(theta, d, a, alpha)
    return T

def dh_alpha (theta, d, a, alpha):
    T = lambda alpha: dh_transform(theta, d, a, alpha)
    return T

def combine_dh_transformations(*transformations):
    def combined(**kwargs):
        result = np.eye(4)
        for transform_name, transform_func, param_key in transformations:
            transform_params = kwargs.get(transform_name, {})
            result = np.dot(result, transform_func(**transform_params))
        return result
    transform_names = [(name, key) for name, _, key in transformations]
    return return_combined_dh_transformation(combined, transform_names)

def return_combined_dh_transformation(combined_transform, transform_names):
    def positional_transform(*args):
        if len(args) != len(transform_names):
            raise ValueError(f"Expected {len(transform_names)} arguments, got {len(args)}")
        kwargs = {name: {key: arg} for (name,key), arg in zip(transform_names, args)}
        return combined_transform(**kwargs)
    return positional_transform


def add(a,b):
    return a+b

def dh_matrix(theta, d, a, alpha):
    """Generates DH-matrix"""
    return Matrix([
        [cos(theta), -sin(theta)*cos(alpha), sin(theta)*sin(alpha), a*cos(theta)],
        [sin(theta),  cos(theta)*cos(alpha), -cos(theta)*sin(alpha), a*sin(theta)],
        [0,           sin(alpha),            cos(alpha),            d],
        [0,           0,                     0,                     1]
    ])