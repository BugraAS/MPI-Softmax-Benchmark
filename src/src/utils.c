#include "utils.h"
#include "macros.h"
#include <math.h>
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

float *read_benchmark(const char *fname)
{
  const int init_cap = 2;

  FILE *fptr = fopen(fname, "r");
  if (fptr == NULL)
    ABORT("could not open %s", fname)
  float num;
  float *out = malloc(sizeof(float) * init_cap);
  int size = 0;
  int capacity = init_cap;
  while (fscanf(fptr, "%f", &num) == 1) {
    out[size++] = num;
    if (size == capacity) {
      capacity *= 2;
      out = realloc(out, sizeof(float) * capacity);
      if (out == NULL)
        ABORT("failure to allocate memory.")
    }
  }

  int numProcs;
  MPI_Comm_size(MPI_COMM_WORLD, &numProcs);

  if (numProcs > size)
    ABORT("the benchmark file doesnt' contain enough entries, needed: %d, got: "
          "%d",
          numProcs, size)

  out = realloc(out, sizeof(float) * size);
  return out;
}

void calc_sendcounts(float *weights, int* out, int vsize)
{
  int numProcs;
  MPI_Comm_size(MPI_COMM_WORLD, &numProcs);

  // assume weights are greater than 0
  float sum = 0;
  for (int i = 0; i < numProcs; i++)
    sum += weights[i];
  float shares[numProcs];
  for (int i = 0; i < numProcs; i++)
    shares[i] = weights[i] / sum;

  out[numProcs-1] = vsize - roundf(shares[numProcs-1]*vsize);
  out[0] = 0;
  for (int i = numProcs-2; i > 0; i--)
    out[i] = out[i+1] -  roundf(shares[i]*vsize);

  for (int i = 0; i < numProcs-1; i++)
    out[i] = out[i+1] - out[i];
  out[numProcs-1] = vsize - out[numProcs-1];
}

char* to_str_vector(int* arr, int size)
{
  static char buff[256] = {'\0'};
  buff[0] = '\0';
  for (int i = 0; i < size; i++)
  {
    sprintf(buff, "%s %d",buff,arr[i]);
  }
  return buff;
}