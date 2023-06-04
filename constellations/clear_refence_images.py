import cv2
import numpy as np
import os

src_dir = 'visualization(named stars)'
dest_dir = 'visualization(cleared)'

def clear_constellation_image(filename):
    img = cv2.imread(fr'{src_dir}\{filename}',cv2.IMREAD_UNCHANGED)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            avg = int(img[i][j][0]) + int(img[i][j][1]) + int(img[i][j][2])
            avg /= 3
            if avg < 215:
                img[i][j][0] = 0
                img[i][j][1] = 0
                img[i][j][2] = 0

    kernel = np.ones((4, 4), np.uint8)

    img = cv2.dilate(img, kernel)

    cv2.imwrite(fr"{dest_dir}\{filename}", img)


for file in os.listdir(src_dir):
    clear_constellation_image(file)