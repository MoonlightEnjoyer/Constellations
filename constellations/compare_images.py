from constellations_geometry import *
import constellations_database
import numpy as np

def identify_constellation(source_image):
    stars = create_stars_list(source_image)
    database = constellations_database.load_database()
    constellations = {}
    length = len(stars)
    for i in range(length):
        for j in range(i + 1, length):
            for k in range(j + 1, length):
                ang1, ang2, ang3 = calculate_angles(stars[i], stars[j], stars[k])
                if ang1 != None:
                    new_triangle = Triangle("unknown", ang1, ang2, ang3)
                    for database_triangle in database:
                        if new_triangle == database_triangle:
                            if not constellations.__contains__(database_triangle.constellation_name):
                                constellations[database_triangle.constellation_name] = []
                                print(database_triangle.constellation_name)
                            constellations[database_triangle.constellation_name].append(stars[i])
                            constellations[database_triangle.constellation_name].append(stars[j])
                            constellations[database_triangle.constellation_name].append(stars[k])
                            

    return constellations

def mark_constellation(stars, image):
    result_image = np.zeros((image.shape[0], image.shape[1]), np.uint8)

    for star in stars:
        result_image[star.y][star.x] = 255

    return result_image



