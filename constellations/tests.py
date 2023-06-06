from constellations_geometry import Star
import constellations_database
import constellations_geometry

def test_calculate_angles():
    ang1, ang2, ang3 = constellations_geometry.calculate_angles(Star(20, 9), Star(45, 70), Star(80, 31))
    assert (68.23036148716524, 47.5781089249191, 64.19152958791565) == (ang1, ang2, ang3)

def test_load_stars_database():
    database_from_file = constellations_database.load_database()
    original_database = constellations_database.create_stars_database()
    assert database_from_file == original_database