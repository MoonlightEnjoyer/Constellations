#include <string.h>
#include <iostream>
#include <map>
#include <list>
#include <algorithm>
#include <chrono>
#include <cmath>
#include <vector>
#include <unordered_map>

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
    int angles_length;
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

inline bool isclose(float value1, float value2)
{
    float precision = 0.5;
    return abs(value1 - value2) <= precision;
}

inline bool angles_binary_search(float angle, float* array, int start, int end)
{
    int middle = (start + end) / 2;

    if (middle == start)
    {
        return isclose(angle, array[middle]);
    }

    bool triangle_name;

    if (angle < array[middle])
    {
        triangle_name = angles_binary_search(angle, array, start, middle);
    }
    else
    {
        triangle_name = angles_binary_search(angle, array, middle, end);
    }

    return true;
}

extern "C"
Constellation* identify_constellation(int stars_length, Star stars[], int database_length, DatabaseStar database[])
{
    std::cout << "Inside identify constellation." << endl;

    std::cout << "Database length : " << database_length << endl;
    using namespace std::chrono;
    auto t1_s = high_resolution_clock::now();
    Constellation* result_constellations;
    unordered_map<std::string, std::list<Star>> constellations_map;

    float new_angle;
    
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

        std::cout << "After angles calculation." << endl;

        int max_angles = 0;
        char* constellation_name = "no_constellation";

        auto na_end = new_angles.end();
        auto na_beg = new_angles.begin();
        auto na_size = new_angles.size();
        auto na_data = new_angles.data();
        int angles_counter;
        long debug_counter = 0;
        for (auto it = na_beg; it != na_end; ++it)
        {   
            //takes too long
            auto s_s = high_resolution_clock::now();
            for (int i = 0; i < database_length; i++)
            {
                angles_counter = 0;
                for (int j = 0; j < database[i].angles_length; j++)
                {
                    angles_counter += angles_binary_search(database->angles[j], na_data, 0, na_size);
                    debug_counter++;
                }

                if (angles_counter > max_angles)
                {
                    max_angles = angles_counter;
                    constellation_name = database[i].constellation;
                }
            }

            auto s_e = high_resolution_clock::now();
            auto s_time = duration_cast<duration<double>>(s_e- s_s);
            //std::cout << "step [" << debug_counter << "] execution time: " << s_time.count() << " seconds." << endl; 
            //

            angles_counter = debug_counter;

            if (constellations_map.find(constellation_name) == constellations_map.end())
            {
                list<Star> new_list;
                constellations_map.insert({constellation_name, new_list});
            }

            constellations_map[constellation_name].insert(constellations_map[constellation_name].end(), stars[i]);
        }

        std::cout << i << " step of " << stars_length << endl;
    }

    std::cout << "After constellations_map filling." << endl;

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