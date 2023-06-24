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
    float* angles;
};


struct Constellation
{
    char* name;
    int name_length;
    struct Star* stars;
    int stars_length;
};

bool isclose(float value1, float value2, float precision)
{
    return abs(value1 - value2) <= precision;
}

float calculate_distance(struct Star star1, struct Star star2)
{
    return sqrt(pow(star1.x - star2.x, 2) + pow(star1.y - star2.y, 2));
}

struct Triangle calculate_angles(struct Star star1, struct Star star2, struct Star star3)
{
    float a = calculate_distance(star1, star2);
    float b = calculate_distance(star2, star3);
    float c = calculate_distance(star1, star3);

    float a_cos = (b * b + c * c - a * a) / (2 * c * b);
    float b_cos = (a * a + c * c - b * b) / (2 * a * c);
    float c_cos = (a * a + b * b - c * c) / (2 * a * b);

    float a_angle = (180 / M_PI) * acos(a_cos);
    float b_angle = (180 / M_PI) * acos(b_cos);
    float c_angle = (180 / M_PI) * acos(c_cos);

    struct Triangle triangle;
    triangle.angles = new float[3];
    triangle.angles[0] = a_angle;
    triangle.angles[1] = b_angle;
    triangle.angles[2] = c_angle;

    sort(triangle.angles, triangle.angles + 3);

    triangle.constellation_name = "";

    return triangle;
}

bool triangles_are_equal(struct Triangle tr1, struct Triangle tr2)
{
    float precision = 0.00001;

    return isclose(tr1.angles[0], tr2.angles[0], precision) && isclose(tr1.angles[1], tr2.angles[1], precision) && isclose(tr1.angles[2], tr2.angles[2], precision);
}

char* triangles_binary_search(Triangle triangle, Triangle* array, int start, int end)
{
    int middle = (start + end) / 2;

    if (middle == start)
    {
        if (triangles_are_equal(triangle, array[middle]))
        {
            return array[middle].constellation_name;
        }
        else
        {
            return nullptr;
        }
    }

    char* triangle_name;

    if (triangle.angles[0] < array[middle].angles[0])
    {
        triangle_name = triangles_binary_search(triangle, array, start, middle);
    }
    else
    {
        triangle_name = triangles_binary_search(triangle, array, middle, end);
    }

    return triangle_name;
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

                char* cons_name = triangles_binary_search(new_triangle, database, 0, database_length);

                if (cons_name != nullptr)
                {
                    if (constellations_map.count(cons_name) == 0)
                    {
                        list<struct Star> new_list;
                        constellations_map.insert({cons_name, new_list});
                    }

                    constellations_map[cons_name].insert(constellations_map[cons_name].end(), stars[i]);
                    constellations_map[cons_name].insert(constellations_map[cons_name].end(), stars[j]);
                    constellations_map[cons_name].insert(constellations_map[cons_name].end(), stars[k]);
                }

                delete[] new_triangle.angles;
            }
        } 
    }

    result_constellations = (struct Constellation*)malloc(sizeof(struct Constellation) * (constellations_map.size() + 1));
    int i = 0;
    int j;
    struct Star temp_star;

    auto iterator_end = constellations_map.end();

    for (auto it = constellations_map.begin(); it != iterator_end; ++it, i++)
    {
        result_constellations[i].name = (char*)malloc(it->first.size());
        strcpy(result_constellations[i].name, (char*)it->first.c_str());
        result_constellations[i].name_length = it->first.size();
        result_constellations[i].stars = (struct Star*)malloc(sizeof(struct Star) * it->second.size());
        j = 0;

        auto stars_iterator_end = it->second.end();

        for (auto st_it = it->second.begin(); st_it != stars_iterator_end; ++st_it, j++)
        {
            temp_star.x = st_it->x;
            temp_star.y = st_it->y;
            result_constellations[i].stars[j] = temp_star;
        }

        result_constellations[i].stars_length = it->second.size();
    }

    result_constellations[i].name_length = 0;

    return result_constellations;
}
