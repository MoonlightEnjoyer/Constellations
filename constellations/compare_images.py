from constellations_geometry import *
import constellations_database
import cv2
import numpy as np

def identify_constellation(source_image) -> list[str]:
    stars = create_stars_list(source_image)
    triangles = []
    for i in range(len(stars)):
        for j in range(i + 1, len(stars)):
            for k in range(j + 1, len(stars)):
                ang1, ang2, ang3 = calculate_angles(stars[i], stars[j], stars[k])
                if ang1 != None:
                    triangles.append(Triangle("unknown", ang1, ang2, ang3))
    constellations = []
    database = constellations_database.load_database()
    for database_triangle in database:
        if database_triangle in triangles and not database_triangle.constellation_name in constellations:
            constellations.append(database_triangle.constellation_name)

    for constellation in constellations:
        print(constellation)

    return constellations

def mark_constellation(constellation_name, image):
    """
    1. Get all precise triangles from image.
    2. Load all triangles of constellation from database.
    3. Create new empty image.
    4. Compare every triangle obtained from the image with triangles from the database.
    5. Add points of the triangle to the empty image in triangle match the database.
    6. Return constructed image.
    """

    precise_triangles = constellations_database.get_precise_triangles(image)
    database_triangles = constellations_database.load_constellation_database(constellation_name)

    result_image = np.zeros((image.shape[0], image.shape[1]), np.uint8)

    for precise_triangle in precise_triangles:
        for database_triangle in database_triangles:
            if precise_triangle.are_similar(database_triangle):
                for vertex in precise_triangle.vertices:
                    result_image[vertex[1].y][vertex[1].x] = 255

    return result_image



