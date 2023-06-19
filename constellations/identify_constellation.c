#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>

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

struct Star* identify_constellation(int stars_length, struct Star stars[], int database_length, struct Triangle database[])
{
    printf("Inside c code: identify_constellation\n");
    return NULL;
}

// struct Star* identify_constellation()
// {
//     printf("Inside c code: identify_constellation\n");
//     return NULL;
// }
