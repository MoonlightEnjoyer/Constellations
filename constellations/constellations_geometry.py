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
        
@njit
def calculate_distance(point1: Star, point2: Star) -> float:
    return math.sqrt(((point1.x - point2.x) ** 2) + ((point1.y - point2.y) ** 2))

@njit
def calculate_angles(point1: Star, point2: Star, point3: Star) -> Tuple[float, float, float]:
    try:
        a = calculate_distance(point1, point2)
        b = calculate_distance(point2, point3)
        c = calculate_distance(point1, point3)
        a_cos = (b ** 2 + c ** 2 - a ** 2) / (2 * c * b)
        b_cos = (a ** 2 + c ** 2 - b ** 2) / (2 * a * c)
        c_cos = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)

        a_angle = np.rad2deg(math.acos(a_cos))
        b_angle = np.rad2deg(math.acos(b_cos))
        c_angle = np.rad2deg(math.acos(c_cos))
        
        return b_angle, c_angle, a_angle
    except Exception:
        return None, None, None

@njit
def create_stars_list(image) -> list[Star]:
    stars = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i][j] != 0:
                stars.append(Star(j, i))

    
    cleared_stars = []
    for star in stars:
        ok = True
        for star_1 in cleared_stars:
            if calculate_distance(star, star_1) < 20:
                ok = False
        if ok:
            cleared_stars.append(star)

    return cleared_stars
