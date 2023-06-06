import cv2
import numpy as np
import constellations_geometry

src_dir = './visualization(named stars)'
dest_dir = './reference_images'

def clear_constellation_image(self, filename):
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

    stars = constellations_geometry.create_stars_list(cleared_image)
    cleared_image = np.zeros((img.shape[0], img.shape[1]), np.uint8)
    for star in stars:
        cleared_image[star.y][star.x] = 255

    cv2.imwrite(fr"{dest_dir}\{filename}", cleared_image)