from sympy import*
import numpy as np

def pad_matrix(mat, target_rows, target_cols):
    padded = zeros(target_rows, target_cols)
    # Copy elements from mat to padded
    for i in range(mat.rows):
        for j in range(mat.cols):
            padded[i, j] = mat[i, j]
    return padded

def inverse_se3(mat):
    R = mat[:3,:3]
    p = mat[:3, 3]
    result = simplify(Matrix.vstack(
        Matrix.hstack(R.T, -R.T*p),
        Matrix([[0, 0, 0, 1]])
    ))
    return result


def coriolis_matrix_christoffel(B, n, q, q_dot):
    coriolis_matrix = zeros(n, n)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                c_ijk = 0.5 * (
                    B[i, j].diff(q[k]) +
                    B[i, k].diff(q[j]) -
                    B[j, k].diff(q[i])
                )
                coriolis_matrix[i, j] += c_ijk * q_dot[k]
    return coriolis_matrix


# Meant for 3D-plotting
def add_point_se3(T, vec):
    if T.shape != (4,4) or vec.shape != (3,1):
        raise ValueError("Matrix or vector has wrong dimensions!")

    T_new = T.copy()

    # Convert sympy-vec to numpy-array
    vec_np = np.array(vec).astype(float).reshape(3,)

    # Rotate vec
    rotated_vec = T[0:3, 0:3] @ vec_np

    # Add vec
    T_new[0:3, 3] += rotated_vec

    return T_new

def skew_matrix(T):
    mat = Matrix([[0, -T[2], T[1]],
                  [T[2], 0, -T[0]],
                  [-T[1], T[0], 0]])
    return mat