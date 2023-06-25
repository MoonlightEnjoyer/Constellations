from constellations_geometry import *
import constellations_database
import numpy as np
import ctypes
import platform
from numba import njit

class Star_struct(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_int16),
        ('y', ctypes.c_int16)
    ]

class Triangle_struct(ctypes.Structure):
    _fields_ = [
        ('constellation_name', ctypes.c_char_p),
        ('angles', ctypes.POINTER(ctypes.c_float))
    ]

class Constellation_struct(ctypes.Structure):
    _fields_ = [
        ('name', ctypes.POINTER(ctypes.c_char)),
        #('name_length', ctypes.c_int),
        ('stars', ctypes.POINTER(Star_struct)),
        ('stars_length', ctypes.c_int)
    ]

if platform.system() == 'Linux':
    _identify_constellations = ctypes.CDLL('./libconstellations.so')
elif platform.system() == 'Windows':
    _identify_constellations = ctypes.CDLL('./libconstellations.dll')
_identify_constellations.identify_constellation.restype = ctypes.POINTER(Constellation_struct)
_identify_constellations.identify_constellation.argtypes = (ctypes.c_int, ctypes.POINTER(Star_struct), ctypes.c_int, ctypes.POINTER(Triangle_struct))


# def identify_constellation(source_image):
#     stars = create_stars_list(source_image)
#     database = constellations_database.load_database()
#     constellations = {}
#     length = len(stars)
#     for i in range(length):
#         for j in range(i + 1, length):
#             for k in range(j + 1, length):
#                 ang1, ang2, ang3 = calculate_angles(stars[i], stars[j], stars[k])
#                 if ang1 != None:
#                     new_triangle = Triangle("unknown", ang1, ang2, ang3)
#                     for database_triangle in database:
#                         if new_triangle == database_triangle:
#                             if not constellations.__contains__(database_triangle.constellation_name):
#                                 constellations[database_triangle.constellation_name] = []
#                                 print(database_triangle.constellation_name)
#                             constellations[database_triangle.constellation_name].append(stars[i])
#                             constellations[database_triangle.constellation_name].append(stars[j])
#                             constellations[database_triangle.constellation_name].append(stars[k])
                            

#     return constellations

def identify_constellation(source_image):
    stars = create_stars_list(source_image)
    database = constellations_database.load_database()

    database.sort(key=lambda x : x.angles[0])

    global _identify_constellations

    stars_array_type = Star_struct * len(stars)
    database_array_type = Triangle_struct * len(database)

    stars_struct = stars_array_type()
    
    for i in range(len(stars)):
        stars_struct[i].x = stars[i].x
        stars_struct[i].y = stars[i].y

    stars_struct_pointer = ctypes.pointer(stars_struct)

    database_struct = database_array_type()
    
    for i in range(len(database)):
        database_struct[i].constellation_name = database[i].constellation_name.encode('utf-8')
        angles_array = ctypes.c_float * 3
        database_struct[i].angles = angles_array(*database[i].angles)

    database_struct_pointer = ctypes.cast(database_struct, ctypes.POINTER(Triangle_struct))

    constellations_array_type = Constellation_struct * 0
    constellations_struct = constellations_array_type()
    constellations_pointer = ctypes.pointer(constellations_struct)

    stars_struct_pointer = ctypes.cast(stars_struct_pointer, ctypes.POINTER(Star_struct))
    database_struct_pointer = ctypes.cast(database_struct_pointer, ctypes.POINTER(Triangle_struct))
    constellations_pointer = ctypes.cast(constellations_pointer, ctypes.POINTER(Constellation_struct))

    constellations_pointer = _identify_constellations.identify_constellation(ctypes.c_int(len(stars)), stars_struct_pointer, ctypes.c_int(len(database)), database_struct_pointer)

                            
    constellations = {}

    counter = 0
    null_terminator = '\0'.encode('utf-8')

    while True:
        if (constellations_pointer[counter].stars_length == 0):
            break

        name_iterator = 0
        while constellations_pointer[counter].name[name_iterator] != null_terminator:
            name_iterator += 1

        name = (constellations_pointer[counter].name[:name_iterator]).decode('utf-8')

        constellations[name] = []
        for j in range(constellations_pointer[counter].stars_length):
            constellations[name].append(Star(constellations_pointer[counter].stars[j].x, constellations_pointer[counter].stars[j].y))

        counter += 1

    return constellations

def mark_constellation(stars, image):
    result_image = np.zeros((image.shape[0], image.shape[1]), np.uint8)

    for star in stars:
        result_image[star.y][star.x] = 255

    return result_image



