#pragma once

float* read_benchmark(const char* fname);
void calc_sendcounts(float* weights, int* out, int vsize);