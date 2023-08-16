import numpy as np
from constellations_geometry import *
import cv2
from numba import njit

src_dir = './user_images'
dest_dir = './user_images_cleared'

@njit
def get_brightness(image):
    cleared_image = np.zeros((image.shape[0],image.shape[1]), np.uint8)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (0.0722 * image[i][j][0] + 0.7152 * image[i][j][1] + 0.2126 * image[i][j][2]) > 100:
                cleared_image[i][j] = 255

    return cleared_image




def clear_image(image, filename):
    # cleared_image = np.zeros((image.shape[0],image.shape[1]), np.uint8)

    # for i in range(image.shape[0]):
    #     for j in range(image.shape[1]):
    #         if (0.0722 * image[i][j][0] + 0.7152 * image[i][j][1] + 0.2126 * image[i][j][2]) > 100:
    #             cleared_image[i][j] = 255
    
    cleared_image = get_brightness(image)

    kernel = np.ones((3,3), np.uint8)
    cleared_image = cv2.dilate(cleared_image, kernel=kernel, iterations=1)


    # cv2.imwrite(f"./binarized_images/{filename}", cleared_image)

    blank = np.zeros((image.shape[0], image.shape[1], 3), dtype='uint8')
    contours, hierarchies = cv2.findContours(cleared_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


    cleared_image = np.zeros((image.shape[0], image.shape[1]), np.uint8)

    for i in contours:
        M = cv2.moments(i)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cleared_image[cy][cx] = 255

    # cv2.imwrite(f"./circles/{filename}", cleared_image)

    

    # stars = create_stars_list(cleared_image)

    # cleared_image = np.zeros((image.shape[0], image.shape[1]), np.uint8)

    # for star in stars:
    #     cleared_image[star.y][star.x] = 255

    return cleared_image
