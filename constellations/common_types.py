import math
import numpy as np
from multipledispatch import dispatch
from typing import Tuple
from numba import njit
from numba.experimental import jitclass
from numba import int32


precision = 0.0000001

spec_star = [
    ('x', int32),
    ('y', int32)
]

@jitclass(spec_star)
class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class DatabaseStar:
    def __init__(self, constellation : str, angles : list[float]) -> None:
        self.constellation = constellation
        self.angles = angles

class Triangle:
    @dispatch(str, float, float, float)
    def __init__(self, constellation_name: str, ang1: float, ang2: float, ang3: float):
        self.constellation_name = constellation_name
        self.angles = [ang1, ang2, ang3]
        self.angles.sort()
    
    @dispatch(str)
    def __init__(self, raw_triangle_data: str):
        tr_data = raw_triangle_data.split(",")
        self.constellation_name = tr_data[0]
        self.angles = [float(tr_data[1]), float(tr_data[2]), float(tr_data[3])]
        self.angles.sort()
        
    def __eq__(self, __value: object):
        return math.isclose(self.angles[0], __value.angles[0], abs_tol=precision) and math.isclose(self.angles[1], __value.angles[1], abs_tol=precision) and  math.isclose(self.angles[2], __value.angles[2], abs_tol=precision)
  