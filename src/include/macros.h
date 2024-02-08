#pragma once

#include "stdio.h"
#include "mpi.h"

#define ISROOT myId == 0

#define ABORT( message, args... ) {fprintf(stderr, "ERROR: " message "\n" ,##args ); MPI_Abort(MPI_COMM_WORLD, EXIT_FAILURE);}

#ifndef NDEBUG
#define DEBUGLOG( message, args...) {fprintf(stderr, "DEBUG: " message "\n" ,##args );}
#else
#define DEBUGLOG( message, args...) {}
#endif // !NDEBUG