#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <iostream>
#include <map>
#include <list>
#include <algorithm>

#ifndef  M_PI
#define  M_PI  3.141592653589793238
#endif

using namespace std;

struct Star
{
    int x;
    int y;
};

struct Triangle
{
    char* constellation_name;
    double* angles;
};


struct Constellation
{
    char* name;
    int name_length;
    struct Star* stars;
    int stars_length;
};

bool isclose(double value1, double value2, double precision)
{
    return abs(value1 - value2) <= precision;
}

double calculate_distance(struct Star star1, struct Star star2)
{
    return sqrt(pow(star1.x - star2.x, 2) + pow(star1.y - star2.y, 2));
}

struct Triangle calculate_angles(struct Star star1, struct Star star2, struct Star star3)
{
    double a = calculate_distance(star1, star2);
    double b = calculate_distance(star2, star3);
    double c = calculate_distance(star1, star3);

    double a_cos = (b * b + c * c - a * a) / (2 * c * b);
    double b_cos = (a * a + c * c - b * b) / (2 * a * c);
    double c_cos = (a * a + b * b - c * c) / (2 * a * b);

    double a_angle = (180 / M_PI) * acos(a_cos);
    double b_angle = (180 / M_PI) * acos(b_cos);
    double c_angle = (180 / M_PI) * acos(c_cos);

    struct Triangle triangle;
    triangle.angles = (double*)malloc(sizeof(double) * 3);
    triangle.angles[0] = a_angle;
    triangle.angles[1] = b_angle;
    triangle.angles[2] = c_angle;

    sort(triangle.angles, triangle.angles + 3);

    triangle.constellation_name = "unknown";

    return triangle;
}

bool triangles_are_equal(struct Triangle tr1, struct Triangle tr2)
{
    double precision = 0.0001;

    return isclose(tr1.angles[0], tr2.angles[0], precision) && isclose(tr1.angles[1], tr2.angles[1], precision) && isclose(tr1.angles[2], tr2.angles[2], precision);
}

extern "C"
struct Constellation* identify_constellation(int stars_length, struct Star stars[], int database_length, struct Triangle database[])
{
    struct Constellation* result_constellations;
    map<std::string, std::list<struct Star>> constellations_map;


    for (int i = 0; i < stars_length; i++)
    {
        for (int j = i + 1; j < stars_length; j++)
        {
            for (int k = j + 1; k < stars_length; k++)
            {
                struct Triangle new_triangle = calculate_angles(stars[i], stars[j], stars[k]);
                for (int r = 0; r < database_length; r++)
                {
                    if (triangles_are_equal(new_triangle, database[r]))
                    {
                        if (constellations_map.count(database[r].constellation_name) == 0)
                        {
                            list<struct Star> new_list;
                            constellations_map.insert({database[r].constellation_name, new_list});
                        }

                        constellations_map[database[r].constellation_name].insert(constellations_map[database[r].constellation_name].end(), stars[i]);
                        constellations_map[database[r].constellation_name].insert(constellations_map[database[r].constellation_name].end(), stars[j]);
                        constellations_map[database[r].constellation_name].insert(constellations_map[database[r].constellation_name].end(), stars[k]);
                    }
                }
            }
        } 
    }

    result_constellations = (struct Constellation*)malloc(sizeof(struct Constellation) * (constellations_map.size() + 1));
    int i = 0;
    for (auto it = constellations_map.begin(); it != constellations_map.end(); ++it, i++)
    {
        result_constellations[i].name = (char*)it->first.c_str();
        result_constellations[i].name_length = it->first.size();
        result_constellations[i].stars = (struct Star*)malloc(sizeof(struct Star) * it->second.size());
        int j = 0;
        for (auto st_it = it->second.begin(); st_it != it->second.end(); ++st_it, j++)
        {
            struct Star temp_star;
            temp_star.x = st_it->x;
            temp_star.y = st_it->y;
            result_constellations[i].stars[j] = temp_star;
        }

        result_constellations[i].stars_length = it->second.size();
    }

    result_constellations[i].name_length = 0;

    return result_constellations;
}
