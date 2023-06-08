import clear_user_images
import constellations_geometry
import os
import cv2
from constellations_geometry import Triangle, PreciseTriangle, Star

ref_dir = './reference_images'
stars_database_path = './stars_database.txt'

def load_database():
    triangles = []
    with open("./stars_database.txt", "r") as stars_database:
        for raw_triangle_data in stars_database.readlines():
            triangles.append(Triangle(raw_triangle_data))
    return triangles

def load_constellation_database(constellation_name):
    triangles = []
    with open(fr"./constellations_database/{constellation_name}.txt", "r") as constellation_database:
        for raw_triangle_data in constellation_database.readlines():
            triangles.append(Triangle(f'{constellation_name},{raw_triangle_data}'))
    return triangles 

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
                        ang1, ang2, ang3 = constellations_geometry.calculate_angles(stars[i], stars[j], stars[k])
                        if ang1 != None:
                            stars_database.write(f'{filename[:-4]},{ang1},{ang2},{ang3}\n')
                            database.append(Triangle(filename[:-4], ang1, ang2, ang3))
                            counter += 1
                        if counter == 3:
                            stop = True
    return database

def get_precise_triangles(image) -> list[PreciseTriangle]:
    stars = constellations_geometry.create_stars_list(image)
    triangles = []
    for i in range(len(stars)):
        for j in range(i + 1, len(stars)):
            for k in range(j + 1, len(stars)):
                ang1, ang2, ang3 = constellations_geometry.calculate_angles(stars[i], stars[j], stars[k])
                if ang1 != None:
                    triangles.append(PreciseTriangle((ang1, stars[i]), (ang2, stars[j]), (ang3, stars[k])))
    return triangles

def get_triangles(image) -> list[Triangle]:
    stars = constellations_geometry.create_stars_list(image)
    triangles = []
    for i in range(len(stars)):
        for j in range(i + 1, len(stars)):
            for k in range(j + 1, len(stars)):
                ang1, ang2, ang3 = constellations_geometry.calculate_angles(stars[i], stars[j], stars[k])
                if ang1 != None:
                    triangles.append(Triangle('unknown', ang1, ang2, ang3))
    return triangles

def write_constellation_triangles(triangles: list[Triangle], destination):
    with open(destination, "w") as database:
        for triangle in triangles:
            database.write(f'{triangle.ang1},{triangle.ang2},{triangle.ang3}\n')


def create_constellations_database(source_dir, destination_dir):
    for filename in os.listdir(source_dir):
        image = cv2.imread(fr"{source_dir}/{filename}", cv2.IMREAD_UNCHANGED)
        triangles = get_triangles(image)
        write_constellation_triangles(triangles, fr"{destination_dir}/{filename[:-3]}txt")
