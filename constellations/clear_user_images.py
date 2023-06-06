import numpy as np
from constellations_geometry import *

src_dir = './user_images'
dest_dir = './user_images_cleared'

def clear_image(image):
    cleared_image = np.zeros((image.shape[0],image.shape[1]), np.uint8)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            avg = int(image[i][j][0]) + int(image[i][j][1]) + int(image[i][j][2])
            avg /= 3
            if avg < 135:
                cleared_image[i][j] = 0
            else:
                cleared_image[i][j] = 255

    stars = create_stars_list(cleared_image)
    cleared_image = np.zeros((image.shape[0],image.shape[1]), np.uint8)
    for star in stars:
        cleared_image[star.y][star.x] = 255
    return cleared_image
