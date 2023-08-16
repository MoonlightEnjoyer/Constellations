import cv2
import numpy as np
import constellations_geometry

def clear_constellation_image(source_path, destination_path, file):
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

    #cv2.imwrite(f"./binarized_images/{file}", cleared_image)

    contours, hierarchies = cv2.findContours(cleared_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    blank = np.zeros((img.shape[0], img.shape[1]), dtype='uint8')
    cv2.drawContours(blank, contours, -1, (255, 0, 0), 1)
    #cv2.imwrite(f"./contours/{file}", blank)

    cleared_image = np.zeros((img.shape[0], img.shape[1]), np.uint8)

    for i in contours:
        M = cv2.moments(i)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cleared_image[cy][cx] = 255

    cv2.imwrite(destination_path, cleared_image)