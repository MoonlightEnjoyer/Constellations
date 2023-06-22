import clear_user_images
import constellations_geometry
import os
import cv2
from constellations_geometry import Triangle, Star

ref_dir = './reference_images'
stars_database_path = './stars_database.txt'

def load_database() -> list[Triangle]:
    triangles = []
    with open("./stars_database.txt", "r") as stars_database:
        for raw_triangle_data in stars_database.readlines():
            triangles.append(Triangle(raw_triangle_data))
    return triangles

def create_stars_database():
    database = []
    with open(stars_database_path, "w") as stars_database:
        for filename in os.listdir(ref_dir):
            image = cv2.imread(f'{ref_dir}/{filename}', cv2.IMREAD_UNCHANGED)
            stars = clear_user_images.create_stars_list(image)
            for i in range(0, len(stars), 3):

                j = i + 1
                k = j + 1

                if i + 1 >= len(stars):
                    j = 0
                if i + 2 >= len(stars):
                    k = 1

                ang1, ang2, ang3 = constellations_geometry.calculate_angles(stars[i], stars[j], stars[k])
                if ang1 != None:
                    stars_database.write(f'{filename[:-4]},{ang1},{ang2},{ang3}\n')
                    database.append(Triangle(filename[:-4], ang1, ang2, ang3))
    return database

def create_stars_database_full():
    with open(stars_database_path, "w") as stars_database:
        for filename in os.listdir(ref_dir):
            image = cv2.imread(f'{ref_dir}/{filename}', cv2.IMREAD_UNCHANGED)
            stars = clear_user_images.create_stars_list(image)
            for i in range(len(stars)):
                for j in range(i, len(stars)):
                    for k in range(j, len(stars)):
                        ang1, ang2, ang3 = constellations_geometry.calculate_angles(stars[i], stars[j], stars[k])
                        if ang1 != None:
                            stars_database.write(f'{filename[:-4]},{ang1},{ang2},{ang3}\n')