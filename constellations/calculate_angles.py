import numpy as np
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def create_stars_list(image):
    stars = []
    block_size = 5
    block_size_half = int(block_size / 2)
    black_block = np.zeros((block_size, block_size), np.uint8)
    image = np.append(np.zeros((image.shape[0], block_size_half), np.uint8), image, axis=1)
    image = np.append(image, np.zeros((image.shape[0], block_size_half), np.uint8), axis=1)

    image = np.append(np.zeros((block_size_half, image.shape[1]), np.uint8), image, axis=0)
    image = np.append(image, np.zeros((block_size_half, image.shape[1]), np.uint8), axis=0)
    for i in range(block_size_half, image.shape[0] - (block_size_half + 1)):
        for j in range(block_size_half, image.shape[1] - (block_size_half + 1)):
            if image[i][j] != 0:
                stars.append(Point(j - block_size_half, i - block_size_half))
                image[i - block_size_half: i + block_size_half + 1, j - block_size_half: j + block_size_half + 1] = black_block
    return stars

def calculate_distance(point1: Point, point2: Point):
    return math.sqrt(((point1.x - point2.x) ** 2) + ((point1.y - point2.y) ** 2))



def calculate_angles(point1: Point, point2: Point, point3: Point):
    a = calculate_distance(point1, point2)
    b = calculate_distance(point2, point3)
    c = calculate_distance(point1, point3)
    a_angle = np.rad2deg(math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * c * b)))
    b_angle = np.rad2deg(math.acos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c)))
    c_angle = np.rad2deg(math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b)))
    return a_angle, b_angle, c_angle
