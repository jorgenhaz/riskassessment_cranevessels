from sympy import *
from model_generation.kinematics.joint_type import JointType

def jacobian(transformList, rotAxList, jointTypeList, jointVec):
    n = len(transformList)
    jac = zeros(6, n) 
    T_n = transformList[-1]  
    O_n = Matrix([T_n[i, 3] for i in range(3)]) 

    for i in range(n):
        T_i = transformList[i]
        R_i = T_i[:3, :3]
        p_i = Matrix([T_i[j, 3] for j in range(3)])
        rot_axis_global = R_i * rotAxList[i] 

        if jointTypeList[i] == JointType.REVOLUTE:
            jac[:3, i] = rot_axis_global.cross(O_n - p_i) 
            jac[3:6, i] = rot_axis_global  
        else:  
            jac[:3, i] = rot_axis_global  
            jac[3:6, i] = Matrix([0, 0, 0]) 

    return jac