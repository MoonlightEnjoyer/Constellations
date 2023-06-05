import cv2
import numpy as np
import os
import calculate_angles

src_dir = './visualization(named stars)'
dest_dir = './reference_images'

def clear_constellation_image(filename):
    img = cv2.imread(fr'{src_dir}\{filename}',cv2.IMREAD_UNCHANGED)
    cleared_image = np.zeros((img.shape[0], img.shape[1]), np.uint8)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            avg = int(img[i][j][0]) + int(img[i][j][1]) + int(img[i][j][2])
            avg /= 3
            if avg < 215:
                cleared_image[i][j] = 0
            else:
                cleared_image[i][j] = 255

    stars = calculate_angles.create_stars_list(cleared_image)
    cleared_image = np.zeros((img.shape[0], img.shape[1]), np.uint8)
    for star in stars:
        cleared_image[star.y][star.x] = 255
    # kernel = np.ones((2, 2), np.uint8)

    # cleared_image = cv2.dilate(cleared_image, kernel)

    cv2.imwrite(fr"{dest_dir}\{filename}", cleared_image)

for file in os.listdir(src_dir):
    clear_constellation_image(file)