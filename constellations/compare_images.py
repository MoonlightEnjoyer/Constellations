from multipledispatch import dispatch
import calculate_angles
import cv2

class Triangle:
    @dispatch(str, float, float, float)
    def __init__(self, constellation_name: str, ang1: float, ang2: float, ang3: float):
        self.constellation_name = constellation_name
        self.ang1 = ang1
        self.ang2 = ang2
        self.ang3 = ang3
    
    @dispatch(str)
    def __init__(self, raw_triangle_data: str):
        tr_data = raw_triangle_data.split(",")
        self.constellation_name = tr_data[0]
        self.ang1 = float(tr_data[1])
        self.ang2 = float(tr_data[2])
        self.ang3 = float(tr_data[3])
        

    def __eq__(self, __value: object):
        angles = [__value.ang1, __value.ang2, __value.ang3]
        return self.ang1 in angles and self.ang2 in angles and self.ang3 in angles

def load_stars_database():
    triangles = []
    with open("./stars_database.txt", "r") as stars_database:
        for raw_triangle_data in stars_database.readlines():
            triangles.append(Triangle(raw_triangle_data))
    return triangles
    
def identify_constellation(source_image):
    stars = calculate_angles.create_stars_list(source_image)
    triangles = []
    for i in range(len(stars)):
        for j in range(i + 1, len(stars)):
            for k in range(j + 1, len(stars)):
                ang1, ang2, ang3 = calculate_angles.calculate_angles(stars[i], stars[j], stars[k])
                if ang1 != None:
                    triangles.append(Triangle("unknown", ang1, ang2, ang3))
    constellations = []
    database = load_stars_database()
    for database_triangle in database:
        if database_triangle in triangles and not database_triangle.constellation_name in constellations:
            constellations.append(database_triangle.constellation_name)

    for constellation in constellations:
        print(constellation)

constellation = cv2.imread("./reference_images/Cancer.png", cv2.IMREAD_UNCHANGED)
identify_constellation(constellation)
    
