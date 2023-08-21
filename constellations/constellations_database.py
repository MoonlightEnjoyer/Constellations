import clear_user_images
import constellations_geometry
import os
import cv2
from common_types import Triangle, DatabaseStar

ref_dir = './reference_images'
stars_database_path = './stars_database.txt'

def load_database() -> list[DatabaseStar]:
    triangles = []
    with open("./stars_database.txt", "r") as stars_database:
        for raw_triangle_data in stars_database.readlines():
            triangles.append(Triangle(raw_triangle_data))
    return triangles

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