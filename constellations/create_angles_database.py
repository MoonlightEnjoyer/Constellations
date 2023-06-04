import clear_user_images
import calculate_angles
import os
import cv2

ref_dir = './reference_images'
stars_database_path = './stars_database.txt'

with open(stars_database_path, "w") as stars_database:
    for filename in os.listdir(ref_dir):
        image = cv2.imread(f'{ref_dir}/{filename}', cv2.IMREAD_UNCHANGED)
        stars = clear_user_images.create_stars_list(image)
        for i in range(len(stars)):
            for j in range(i, len(stars)):
                for k in range(j, len(stars)):
                    ang1, ang2, ang3 = calculate_angles.calculate_angles(stars[i], stars[j], stars[k])
                    stars_database.write(f'{filename}: {ang1}')
                    stars_database.write(f'{filename}: {ang2}')
                    stars_database.write(f'{filename}: {ang3}')
