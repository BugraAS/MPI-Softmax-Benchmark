#pragma once

float* read_benchmark(const char* fname);
void calc_sendcounts(float* weights, int* out, int vsize);
char* to_str_vector(int* arr, int size);