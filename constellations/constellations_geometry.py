import math
import numpy as np
from multipledispatch import dispatch
from typing import Tuple


class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Triangle:
    @dispatch(str, float, float, float)
    def __init__(self, constellation_name: str, ang1: float, ang2: float, ang3: float):
        self.constellation_name = constellation_name
        self.ang1 = ang1
        self.ang2 = ang2
        self.ang3 = ang3
    
    @dispatch(str)
    def __init__(self, raw_triangle_data: str):
        tr_data = raw_triangle_data.split(",")
        self.constellation_name = tr_data[0]
        self.ang1 = float(tr_data[1])
        self.ang2 = float(tr_data[2])
        self.ang3 = float(tr_data[3])
        
    def __eq__(self, __value: object):
        angles = [__value.ang1, __value.ang2, __value.ang3]
        angles_self = [self.ang1, self.ang2, self.ang3]
        
        for angle in angles:
            equal = False
            for angle_self in angles_self:
                if math.isclose(angle, angle_self, abs_tol=0.0000001):
                    equal = True
            if not equal:
                return False

        return True

class PreciseTriangle:
    def __init__(self, ang1: Tuple[float, Star], ang2: Tuple[float, Star], ang3: Tuple[float, Star]):
        self.vertices = [ang1, ang2, ang3]
    
    def are_similar(self, triangle: Triangle) -> bool:
        angles = [triangle.ang1, triangle.ang2, triangle.ang3]
        angles_self = [self.vertices[0][0], self.vertices[1][0], self.vertices[2][0]]
        
        for angle in angles:
            equal = False
            for angle_self in angles_self:
                if math.isclose(angle, angle_self, abs_tol=0.0000001):
                    equal = True
            if not equal:
                return False

        return True
        

def calculate_distance(point1: Star, point2: Star) -> float:
    return math.sqrt(((point1.x - point2.x) ** 2) + ((point1.y - point2.y) ** 2))

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
    
def create_stars_list(image) -> list[Star]:
    stars = []
    block_size = 5
    block_size_half = int(block_size / 2)
    image = np.append(np.zeros((image.shape[0], block_size_half), np.uint8), image, axis=1)
    image = np.append(image, np.zeros((image.shape[0], block_size_half), np.uint8), axis=1)

    image = np.append(np.zeros((block_size_half, image.shape[1]), np.uint8), image, axis=0)
    image = np.append(image, np.zeros((block_size_half, image.shape[1]), np.uint8), axis=0)
    for i in range(block_size_half, image.shape[0] - (block_size_half + 1)):
        for j in range(block_size_half, image.shape[1] - (block_size_half + 1)):
            if image[i][j] != 0:
                new_star = Star(j - block_size_half, i - block_size_half)
                stars.append(new_star)
    return stars
