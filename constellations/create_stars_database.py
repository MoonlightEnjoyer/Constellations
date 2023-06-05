import clear_user_images
import calculate_angles
import os
import cv2
import compare_images
from compare_images import Triangle

ref_dir = './reference_images'
stars_database_path = './stars_database.txt'

def create_stars_database():
    database = []
    with open(stars_database_path, "w") as stars_database:
        for filename in os.listdir(ref_dir):
            image = cv2.imread(f'{ref_dir}/{filename}', cv2.IMREAD_UNCHANGED)
            stars = clear_user_images.create_stars_list(image)
            counter = 0
            stop = False
            for i in range(len(stars)):
                if stop:
                    break
                for j in range(i + 1, len(stars)):
                    if stop:
                        break
                    for k in range(j + 1, len(stars)):
                        if stop:
                            break
                        ang1, ang2, ang3 = calculate_angles.calculate_angles(stars[i], stars[j], stars[k])
                        if ang1 != None:
                            stars_database.write(f'{filename[:-4]},{ang1},{ang2},{ang3}\n')
                            database.append(Triangle(filename[:-4], ang1, ang2, ang3))
                            counter += 1
                        if counter == 3:
                            stop = True
    return database

create_stars_database()
