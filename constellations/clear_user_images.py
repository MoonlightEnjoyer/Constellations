import cv2
import numpy as np
import os

src_dir = './user_images'
dest_dir = './user_images_cleared'

class Star:
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
                stars.append(Star(j - block_size_half, i - block_size_half))
                image[i - block_size_half: i + block_size_half + 1, j - block_size_half: j + block_size_half + 1] = black_block
    return stars

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


for file in os.listdir(src_dir):
    image = cv2.imread(fr'{src_dir}/{file}',cv2.IMREAD_UNCHANGED)
    img = clear_image(image)
    cv2.imwrite(fr"{dest_dir}/{file}", img)

