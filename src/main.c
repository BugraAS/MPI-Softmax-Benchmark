#include "macros.h"
#include "mpi.h"
#include "utils.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char *argv[]) {
  MPI_Init(&argc, &argv);
  int myId;
  int numProcs;
  double start; // start time

  MPI_Comm_size(MPI_COMM_WORLD, &numProcs);
  MPI_Comm_rank(MPI_COMM_WORLD, &myId);
  if(ISROOT) DEBUGLOG("There are %d processes", numProcs)

  if (argc < 4)
    ABORT("insufficent parameters.\n"
          "Usage: %s [benchmark-file] [size-of-vector] [number-of-iterations]",
          argv[0])
  
  float* locvec; // local vector
  float* bigvec = NULL;
  int* sendcounts = NULL;
  int* displs = NULL;
  int bigvsize = 0;
  int locvsize = 0;

  if (ISROOT) {
    float *bmark = read_benchmark(argv[1]);
    for (int i = 0; i < numProcs; i++)
      bmark[i] = 1 / bmark[i];
    DEBUGLOG("found and read benchmark")

    bigvsize = atoi(argv[2]);
    if (bigvsize <= 0)
      ABORT("illegal vector size %d", bigvsize);
    bigvec = malloc(sizeof(float) * bigvsize);
    DEBUGLOG("created big vector of size %d",bigvsize)

    sendcounts = malloc(sizeof(int)*numProcs);
    calc_sendcounts(bmark, sendcounts, bigvsize);
    DEBUGLOG("calculated sendcounts successfully")

    displs = malloc(sizeof(int)*numProcs);
    displs[0] = 0;
    for (int i = 1; i < numProcs; i++)
      displs[i] = displs[i-1] + sendcounts[i-1];
    DEBUGLOG("created displs successfully")
  }

  MPI_Scatter(sendcounts, 1, MPI_INT, &locvsize, 1, MPI_INT, 0, MPI_COMM_WORLD);
  locvec = malloc(sizeof(float)*locvsize);
  if(ISROOT) DEBUGLOG("successfully created local vectors")

  double total = 0;
  int num_iter = atoi(argv[3]);
  if(num_iter < 1) ABORT("invalid iteration count: %d", num_iter);

  for(int iter =0; iter < num_iter; iter++){
    if(ISROOT){
      // create random numbers in (-1000, 1000)
      srand(time(NULL));
      for (int i = 0; i < bigvsize; i++)
        bigvec[i] = 2000.0f * rand() / (float)RAND_MAX - 1000.0f;
      DEBUGLOG("randomized the bigvector")
    }

    MPI_Scatterv(bigvec, sendcounts, displs, MPI_FLOAT, locvec, locvsize, MPI_FLOAT, 0, MPI_COMM_WORLD);
    DEBUGLOG("scatterv successful at id: %d",myId)

    double t1 = MPI_Wtime();

    float locsum = 0;
    for (int i = 0; i < locvsize; i++)
      locsum += expf(locvec[i]);

    float bigsum = 0;
    MPI_Allreduce(&locsum, &bigsum, 1, MPI_FLOAT, MPI_SUM, MPI_COMM_WORLD);

    for (int i = 0; i < locvsize; i++)
      locvec[i] = expf(locvec[i])/bigsum;

    double t2 = MPI_Wtime();

    // MPI_Gatherv(locvec, locvsize, MPI_FLOAT, bigvec, sendcounts, displs, MPI_FLOAT, 0, MPI_COMM_WORLD);

    total += t2-t1;
  }

  double bigtotal = 0;
  MPI_Reduce(&total, &bigtotal, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

  DEBUGLOG("finished calculations at %d",myId)
  if(ISROOT){
    printf("Avg. time: %16lf, benchmark: %32s\n",bigtotal/numProcs,argv[1]);
  }


  DEBUGLOG("finalizing id: %d", myId)
  MPI_Finalize();

  //BUG: This causes a crash for seemingly no good reason
  free(locvec);

  if(ISROOT){
    free(bigvec);
    free(displs);
    free(sendcounts);
  }
}