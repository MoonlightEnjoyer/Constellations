from constellations_geometry import *
import constellations_database
    
def identify_constellation(source_image):
    stars = calculate_angles.create_stars_list(source_image)
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