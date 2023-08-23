import clear_user_images
import constellations_geometry
import os
import cv2
from common_types import DatabaseStar

ref_dir = './reference_images'
stars_database_path = './stars_database.txt'

def load_database() -> list[DatabaseStar]:
    database = []
    with open("./stars_database.txt", "r") as stars_database:
        for raw_constellation_data in stars_database.readlines():
            splitted_data = raw_constellation_data.split(':')
            raw_stars = splitted_data[1].split(';')[:-1]
            for raw_star in raw_stars:
                raw_angles = raw_star.split(' ')[:-1]
                float_angles = []
                for raw_angle in raw_angles:
                    float_angles.append(float(raw_angle))
                    float_angles.sort()
                database.append(DatabaseStar(splitted_data[0], float_angles))
    return database

def create_stars_database_full():
    with open(stars_database_path, "w") as stars_database:
        for filename in os.listdir(ref_dir):
            image = cv2.imread(f'{ref_dir}/{filename}', cv2.IMREAD_UNCHANGED)
            stars = clear_user_images.create_stars_list(image)
            stars_database.write(f'{filename[:-4]}:')
            for i in range(len(stars)):
                for j in range(len(stars)):
                    if j == i:
                        continue
                    for k in range(len(stars)):
                        if k == i or k == j:
                            continue
                        ang = constellations_geometry.calculate_angle(stars[i], stars[j], stars[k])
                        if ang != None:
                            stars_database.write(f'{ang} ')
                stars_database.write(';')
            stars_database.write('\n')