/* Solution for the input problem. */

#include <assert.h>
#include <stdio.h>

#include "execute.c"

#define NUMLEN ((size_t) 14)
typedef long long number_t[NUMLEN];

#define SEQLEN ((size_t) 9)
typedef long long sequence_t[SEQLEN];

static long long (*const programs[NUMLEN])(
    const long long* const restrict, const size_t, const long long) = {
    execute00, execute01, execute02, execute03, execute04, execute05, execute06,
    execute07, execute08, execute09, execute10, execute11, execute12, execute13
};

static long long integer(const number_t num)
{
    long long res = 0;
    for (size_t i = 0; i < NUMLEN; ++i)
        res = res * 10 + num[i];
    return res;
}

static int solve(number_t result, const long long z0,
                 const size_t index, const sequence_t sequence)
{
    static const unsigned long long prime = 100000037;
    static unsigned long long counter = 0;

    assert(index < NUMLEN);
    if (index == 0)
        counter = 0;

    long long zval[SEQLEN];
    for (int i = 0; i < SEQLEN; ++i)
    {
        const long long z = programs[index](&sequence[i], 1, z0);
        if (index == NUMLEN - 1 && (z == 0 || counter++ % prime == 0))
        {
            result[index] = sequence[i];
            printf(" %15lld   %lld\r", z, integer(result));
            fflush(stdout);
        }
        if (z == 0 && index == NUMLEN - 1)
            return 0;
        zval[i] = z;
    }

    if (index < NUMLEN - 1)
    {
        for (int i = 0; i < SEQLEN; ++i)
        {
            result[index] = sequence[i];
            if (!solve(result, zval[i], index + 1, sequence))
                return 0;
        }
    }

    return 1;
}

static void one()
{
    number_t result = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    const sequence_t sequence = {9, 8, 7, 6, 5, 4, 3, 2, 1};
    if (!solve(result, 0, 0, sequence))
        printf("\nSolution: %lld\n", integer(result));
    else
        printf("\nNo solution\n");
}

static void two()
{
    number_t result = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    const sequence_t sequence = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    if (!solve(result, 0, 0, sequence))
        printf("\nSolution: %lld\n", integer(result));
    else
        printf("\nNo solution\n");
}

int main(int argc, const char* argv[])
{
    one();
    two();
    return 0;
}
