#include <string.h>
#include <iostream>
#include <map>
#include <list>
#include <algorithm>
#include <chrono>
#include <cmath>
#include <vector>

#ifndef  M_PI
#define  M_PI  3.141592653589793238
#endif


#define RAD2DEG_COEF 180 / M_PI

using namespace std;

struct Star
{
    int x;
    int y;
};

struct DatabaseStar
{
    char* constellation;
    float* angles;
};

struct Triangle
{
    char* constellation_name;
    float* angles;
};

struct MyList
{
    struct MyNode* head;
    struct MyNode* tail;
};

struct MyNode
{
    struct Star value;
    struct MyNode* next;
};


struct Constellation
{
    char* name;
    struct Star* stars;
    int stars_length;
};

bool isclose(float value1, float value2, float precision)
{
    return abs(value1 - value2) <= precision;
}

float calculate_distance(Star star1, Star star2)
{
    int diff_x = star1.x - star2.x;
    int diff_y = star1.y - star2.y;
    return sqrt(diff_x * diff_x + diff_y * diff_y);
}

inline float calculate_angle(Star star1, Star star2, Star star3)
{
    float a = calculate_distance(star1, star2);
    float b = calculate_distance(star2, star3);
    float c = calculate_distance(star1, star3);

    float b_cos = (a * a + c * c - b * b) / (2 * a * c);

    float b_angle = RAD2DEG_COEF * acos(b_cos);

    return b_angle;
}

bool triangles_are_equal(Triangle tr1, Triangle tr2)
{
    float precision = 0.5;

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
Constellation* identify_constellation(int stars_length, Star stars[], int database_length, DatabaseStar database[])
{
    using namespace std::chrono;
    auto t1_s = high_resolution_clock::now();
    Constellation* result_constellations;
    map<std::string, std::list<Star>> constellations_map;

    float new_angle;

    DatabaseStar* stars_calculated = new DatabaseStar[stars_length]; 


    for (int i = 0; i < stars_length; i++)
    {
        vector<float> new_angles;

        for (int j = 0; j < stars_length; j++)
        { 
            if (i == j)
            {
                continue;
            }

            for (int k = 0; k < stars_length; k++)
            {
                if (i == j || j == k)
                {
                    continue;
                }

                new_angle = calculate_angle(stars[i], stars[j], stars[k]);

                new_angles.push_back(new_angle);
            }
        }

        stars_calculated[i].angles = new_angles.data();

        //TODO
        //find star with similar angles list in database.
        //stars_calculated[i].constellation = constellation_name from database
        //constellations_map[stars_calculated[i].constellation].insert(stars[i])
        //TODO
    }

    // no changes after this line

    result_constellations = (Constellation*)malloc(sizeof(Constellation) * (constellations_map.size() + 1));
    int i = 0;
    int j;
    struct Star temp_star;

    auto iterator_end = constellations_map.end();

    for (auto it = constellations_map.begin(); it != iterator_end; ++it, i++)
    {
        result_constellations[i].name = (char*)malloc(it->first.size() + 1);
        strcpy(result_constellations[i].name, (char*)it->first.c_str());
        result_constellations[i].stars = (Star*)malloc(sizeof(Star) * it->second.size());
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

    result_constellations[i].stars_length = 0;

    auto t1_e = high_resolution_clock::now();

    auto time_1 = duration_cast<duration<double>>(t1_e - t1_s);
    std::cout << "identify_constellation execution time: " << time_1.count() << " seconds." << endl; 

    return result_constellations;
}
