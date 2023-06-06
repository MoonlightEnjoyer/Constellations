import math
import numpy as np
from multipledispatch import dispatch


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
        return self.ang1 in angles and self.ang2 in angles and self.ang3 in angles

def calculate_distance(point1: Star, point2: Star):
    return math.sqrt(((point1.x - point2.x) ** 2) + ((point1.y - point2.y) ** 2))

def calculate_angles(point1: Star, point2: Star, point3: Star):
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
        
        return a_angle, b_angle, c_angle
    except Exception:
        return None, None, None
    
def create_stars_list(image):
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
                contains = False
                new_star = Star(j - block_size_half, i - block_size_half)
                for star in stars:
                    if calculate_distance(new_star, star) < 20:
                        contains = True
                        break
                if not contains:
                    stars.append(new_star)
    return stars