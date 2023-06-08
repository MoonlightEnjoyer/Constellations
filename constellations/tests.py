from constellations_geometry import Star
import constellations_database
import constellations_geometry
import clear_reference_images
import clear_user_images
import cv2

def test_load_stars_database():
    database_from_file = constellations_database.load_database()
    original_database = constellations_database.create_stars_database()
    assert database_from_file == original_database

def test_clear_constellation_image():
    clear_reference_images.clear_constellation_image(fr"D:\Work tools\Concepts\Constellations\constellations\visualization(named stars)\Andromeda.png",
                                                      fr"D:\Work tools\Concepts\Constellations\constellations\test_files\Andromeda_cleared.png")
    
def test_clear_image():
    image = cv2.imread(fr"D:\Work tools\Concepts\Constellations\constellations\user_images\2.jpg")
    clear_user_images.clear_image(image)

def test_calculate_distance():
    distance = constellations_geometry.calculate_distance(Star(123, 33), Star(555, 142))
    assert abs(distance - 445.538999) < 0.000001

def test_calculate_angles():
    ang1, ang2, ang3 = constellations_geometry.calculate_angles(Star(20, 9), Star(45, 70), Star(80, 31))
    assert (47.5781089249191, 64.19152958791565, 68.23036148716524) == (ang1, ang2, ang3)

def test_create_stars_list():
    image = cv2.imread(fr"D:\Work tools\Concepts\Constellations\constellations\reference_images\Andromeda.png", cv2.IMREAD_UNCHANGED)
    constellations_geometry.create_stars_list(image)

def test_write_constellation_triangles():
    image = cv2.imread(fr"D:\Work tools\Concepts\Constellations\constellations\reference_images\Andromeda.png", cv2.IMREAD_UNCHANGED)
    triangles = constellations_database.get_triangles(image)
    constellations_database.write_constellation_triangles(triangles, fr'./test_files/andromeda_database.txt')

def test_create_constellations_database():
    constellations_database.create_constellations_database("./reference_images/", "./test_files/constellations_database/")