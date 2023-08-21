import math
import numpy as np
from multipledispatch import dispatch
from typing import Tuple
from numba import njit
from numba.experimental import jitclass
from numba import int32
from common_types import Star



      
@njit
def calculate_distance(point1: Star, point2: Star) -> float:
    return math.sqrt(((point1.x - point2.x) ** 2) + ((point1.y - point2.y) ** 2))

@njit
def calculate_angle(point1: Star, point2: Star, point3: Star) -> float:
    try:
        a = calculate_distance(point1, point2)
        b = calculate_distance(point2, point3)
        c = calculate_distance(point1, point3)
        b_cos = (a ** 2 + c ** 2 - b ** 2) / (2 * a * c)

        b_angle = np.rad2deg(math.acos(b_cos))
        
        return b_angle
    except Exception:
        return None

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
