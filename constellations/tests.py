import pytest

import calculate_angles
from calculate_angles import Point
import compare_images
from compare_images import Triangle
import create_stars_database

def test_calculate_angles():
    ang1, ang2, ang3 = calculate_angles.calculate_angles(Point(20, 9), Point(45, 70), Point(80, 31))
    assert (68.23036148716524, 47.5781089249191, 64.19152958791565) == (ang1, ang2, ang3)

def test_load_stars_database():
    database_from_file = compare_images.load_stars_database()
    original_database = create_stars_database.create_stars_database()
    assert database_from_file == original_database