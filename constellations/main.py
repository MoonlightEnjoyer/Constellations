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
    constellation_image = cv2.imread("./user_images_cleared/6.jpg", cv2.IMREAD_UNCHANGED)
    constellations = compare_images.identify_constellation_c(constellation_image)
    print("After identify_constellations call inside main.py")
    print(type(constellations))
    for item in constellations.items():
        result_image = compare_images.mark_constellation(item[1], constellation_image)
        cv2.imwrite(f'./results/{item[0]}.png', result_image)
        
def clear_user():
    dir = fr"./user_images"
    cleared_dir = fr"./user_images_cleared"
    for filename in os.listdir(dir):
        user_image = cv2.imread(f"{dir}\{filename}", cv2.IMREAD_UNCHANGED)
        user_image = clear_user_images.clear_image(user_image)
        cv2.imwrite(fr"{cleared_dir}\{filename}", user_image)


identify()