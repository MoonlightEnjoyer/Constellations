import cv2
import numpy as np
import constellations_geometry

def clear_constellation_image(source_path, destination_path):
    img = cv2.imread(source_path,cv2.IMREAD_UNCHANGED)
    cleared_image = np.zeros((img.shape[0], img.shape[1]), np.uint8)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            avg = int(img[i][j][0]) + int(img[i][j][1]) + int(img[i][j][2])
            avg /= 3
            if avg < 30:
                cleared_image[i][j] = 255

    kernel = np.ones((5,5), np.uint8)
    cleared_image = cv2.erode(cleared_image, kernel=kernel, iterations=1)

    stars = constellations_geometry.create_stars_list(cleared_image)
    cleared_image = np.zeros((img.shape[0], img.shape[1]), np.uint8)

    for star in stars:
        cleared_image[star.y][star.x] = 255

    cv2.imwrite(destination_path, cleared_image)