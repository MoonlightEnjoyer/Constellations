import os
import clear_reference_images
import constellations_database
import cv2
import compare_images
import clear_user_images

def clear_reference():
        src_dir = './visualization(named stars)'
        for file in os.listdir(src_dir):
                clear_reference_images.clear_constellation_image(file)

def create_database():
        constellations_database.create_stars_database()

def identify():
        constellation = cv2.imread(fr"D:\Work tools\Concepts\Constellations\constellations\user_images_cleared\2.jpg", cv2.IMREAD_UNCHANGED)
        compare_images.identify_constellation(constellation)

def clear_user():
        dir = fr"D:\Work tools\Concepts\Constellations\constellations\user_images"
        cleared_dir = fr"D:\Work tools\Concepts\Constellations\constellations\user_images_cleared"
        for filename in os.listdir(dir):
                user_image = cv2.imread(f"{dir}\{filename}", cv2.IMREAD_UNCHANGED)
                user_image = clear_user_images.clear_image(user_image)
                cv2.imwrite(fr"{cleared_dir}\{filename}", user_image)

identify()