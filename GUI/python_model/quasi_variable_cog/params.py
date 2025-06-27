from sympy import *
import numpy as np

from dataclasses import dataclass
from typing import ClassVar

@dataclass
class BoatParams:
    mass: float = 60000
    length: float = 15.0
    width: float = 8.5
    height: float = 4.5
    k_roll: int = 4e5
    k_pitch: int = 5e5
    d_roll: int = 800000 
    d_pitch: int = 800000 
    d_yaw: int = 1500000 
    d_x: int = 4500
    d_y: int = 8500
    d_z: int = 33700
    rho: int = 1000
    r:          ClassVar[Matrix] = Matrix([0, 0, height/2]) # Vector from CO to CG
    num_of_ballast_tanks: int = 4
    shape: str = "prism"
    

@dataclass
class Gravity:
    g: float = 9.81

@dataclass
class CraneBase:
    # Frame has z-axis pointing down
    x: int = 2 # relative to CO
    y: int = 2 # relative to CO
    mass: int = 100
    height: int = 1 
    radius: float = 0.5
    shape: str = "cylinder"

@dataclass
class Joint1Params:
    # Rotating about z-axis
    mass: float = 200
    k: int = 90000
    d: int = 200000
    radius: float = 0.2
    length: int = 2
    shape: str = "cylinder"

@dataclass
class Joint2Params:
    # Rotating about y-axis (I think)
    mass: float = 150
    k: int = 90000
    d: int = 200000
    radius: float = 0.2
    length: int = 2
    shape: str = "cylinder"

@dataclass
class Joint3Params:
    # Rotating about y-axis
    mass: float = 100
    k: int = 90000
    d: int = 200000
    radius: float = 0.2
    length: float =0.2
    shape: str = "cylinder"

@dataclass
class Joint4Params:
    # Translating along x-axis
    mass: float = 200
    k: int = 90000
    d: int = 200000
    radius: float = 0.2
    length: float = 1
    shape: str = "cylinder"

@dataclass(frozen=True)
class UnitVectors:
    i:        ClassVar[Matrix] = Matrix([1, 0, 0])
    j:        ClassVar[Matrix] = Matrix([0, 1, 0])
    k:        ClassVar[Matrix] = Matrix([0, 0, 1])

    i_jac_w:  ClassVar[Matrix] = Matrix([0, 0, 0, 1, 0, 0])
    j_jac_w:  ClassVar[Matrix] = Matrix([0, 0, 0, 0, 1, 0])
    k_jac_w:  ClassVar[Matrix] = Matrix([0, 0, 0, 0, 0, 1])

    i_jac_v:  ClassVar[Matrix] = Matrix([1, 0, 0, 0, 0, 0])
    j_jac_v:  ClassVar[Matrix] = Matrix([0, 1, 0, 0, 0, 0])
    k_jac_v:  ClassVar[Matrix] = Matrix([0, 0, 1, 0, 0, 0])

@dataclass(frozen=True)
class TanksAftStarboard:
    length:     float = 1.0
    width:      float = 1.0
    height:     float = 2.0
    # r is the vector from body-fixed frame to CG of tank. The z-coordinate must be added
    # in main code, as this depends on the mass in the tank. The body-fixed frame has z-axis pointing down
    # so z is given as: z = - (mass/(2*rho*length*width)) 
    r:          ClassVar[Matrix] = Matrix([-(BoatParams.length/2-length/2),
                                           (BoatParams.width/2 - width/2),
                                           0])
    shape:      str = "cube"
    max_capacity:   str = "2000 litres"

@dataclass(frozen=True)
class TanksAftPortside:
    length:     float = 1.0
    width:      float = 1.0
    height:     float = 2.0
    # r is the vector from body-fixed frame to CG of tank. The z-coordinate must be added
    # in main code, as this depends on the mass in the tank. The body-fixed frame has z-axis pointing down
    # so z is given as: z = - (mass/(2*rho*length*width)) 
    r:          ClassVar[Matrix] = Matrix([-(BoatParams.length/2-length/2),
                                           -(BoatParams.width/2 - width/2),
                                           0])
    shape:      str = "cube"
    max_capacity:   str = "2000 litres"

@dataclass(frozen=True)
class TanksForepeakStarboard:
    length:     float = 1.0
    width:      float = 1.0
    height:     float = 2.0
    # r is the vector from body-fixed frame to CG of tank. The z-coordinate must be added
    # in main code, as this depends on the mass in the tank. The body-fixed frame has z-axis pointing down
    # so z is given as: z = - (mass/(2*rho*length*width)) 
    r:          ClassVar[Matrix] = Matrix([(BoatParams.length/2-length/2),
                                           (BoatParams.width/2 - width/2),
                                           0])
    shape:      str = "cube"
    max_capacity:   str = "2000 litres"

@dataclass(frozen=True)
class TanksForepeakPortside:
    length:     float = 1.0
    width:      float = 1.0
    height:     float = 2.0
    # r is the vector from body-fixed frame to CG of tank. The z-coordinate must be added
    # in main code, as this depends on the mass in the tank. The body-fixed frame has z-axis pointing down
    # so z is given as: z = - (mass/(2*rho*length*width)) 
    r:          ClassVar[Matrix] = Matrix([(BoatParams.length/2-length/2),
                                           -(BoatParams.width/2 - width/2),
                                           0])
    shape:      str = "cube"
    max_capacity:   str = "2000 litres"