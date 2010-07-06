#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#include <cutil.h>
#include "utils.h"

#define null NULL;

int main(int argc, char** argv) {

    bool if_quiet = false;
    unsigned int timer_compute = 0;

    int i, j;

    char *matrix_id = null, *input_fn = null, *gold_fn = null;
    int Mw = 0, Mh = 0, Nw = 0, Nh = 0, Pw = 0, Ph = 0;

    if(argc == 2) {
        matrix_id = strdup(argv[1]);
    } else {
        fprintf(stderr, "Error: Wring input parameter numbers \n");
        fprintf(stderr, "Usage: \n"
            "$> ./labl.l-matrixmul <8, 128, 512, 3072, 4096>\n"
            "Examples:\n"
            "$> ./labl.l-matrixmul 128\n");
        return 1;
    }

    Mw = Mh = Nw = Nh = Pw = Ph =  atoi(matrix_id);
    input_fn = (char *) malloc(30 * sizeof(char));
    gold_fn = (char *) malloc(30 * sizeof(char));

    sprintf(input_fn, "matrix_%s.bin", matrix_id);
    sprintf(gold_fn, "matrix_%s.gold", matrix_id);

    // You do not want to be displaying a matrix larger than 15 x 15
    if(Pw * Ph > 15 * 15) {
        if_quiet = true;
    }

    printf("Input Matrix Size: %d × %d\n", Mw, Mh);

    // Setup Host
    //------------------------------------------------------------------------------------------ 
    printf("Setup host side environment:\n");

    printf("Allocate host memory for matrices M and N\n");
    printf("\tM: %d × %d\n", Mw, Mh);
    printf("\tN: %d × %d\n", Nw, Nh);

    unsigned int size_M = Mw * Mh;
    unsigned int mem_size_M = sizeof(float) * size_M;
    float* hostM = (float*) malloc(mem_size_M);

    unsigned int size_N = Nw * (Nh);
    unsigned int mem_size_N = sizeof(float) * size_N;
    float* hostN = (float*) malloc(mem_size_N);

    // allocate mem for the result on the host
    printf("Allocate memory for the result on the host size\n");
    unsigned int size_P = Pw * Ph;
    unsigned int mem_size_P = sizeof(float) * size_P;
    float* hostP = (float*) malloc(mem_size_P);

    // Init inputs
    printf("Generating input matrix data for N and M\n");
    GenMatrixFile(input_fn, Pw, Ph, if_quiet);
    unsigned int* matrix = ReadMatrixFile(input_fn, Pw, Ph, true);

    for(i = 0; i< Mw; i++) {
        for(j = 0; j < Nw; j++) {
            hostM[i * Mw + j] = hostN[i * Mw + j] = 
                (float) matrix[i * Mw + j];
        }
    }

    free(matrix);
    matrix = null;

    printf("Computing matrix mult M × N: \n");

    if((Pw * Ph) > (512 * 512)) {
        printf(" ... This is going to take some time \n");
    }

    CUT_SAFE_CALL(cutCreateTimer(&timer_compute));
    CUT_SAFE_CALL(cutStartTimer(timer_compute));

    float* reference = (float*) malloc(mem_size_P);
    computeGold(reference, hostM, hostN, Mh, Mw, Nw);
    CUT_SAFE_CALL(cutStopTimer(timer_compute));

    printf("The CPU munged the matrix in : %f (ms) \n"
        cutGetTimerValue(timer_compute));
    CUT_SAFE_CALL(cutDeleteTimer(timer_compute));

    printf("Matrix chksum :%g\n", CheckSum(reference, Mw, Nw));

    if(!if_quiet) {
        printf("Matrix data contents: \n");
        printf(" ");
    }

    matrix = (unsigned int*) malloc(Pw*Ph*sizeof(unsigned int));

    for(i = 0; i < Ph; i++) {
        for(j = 0; j < pW; j++) {
            matrix[i * Pw + j] = (unsigned int) reference[i * Pw + j];
            if(!if_quiet) {
                printf("%u ", matrix[i * Pw + j]);
            }
        }
        if(!if_quiet) {
            printf("\n ");
        }
    }

    if(!if_quiet) {
        printf("\n");
    }

    writeMatrixFile(gold_fn, matrix, Pw, Ph, i);

    free(matrix);
    matrix = NULL;
    free(reference);

    free(hostM);
    free(hostN);
    free(hostP);
    free(input_fn);
    free(gold_fn);

    return 0;
}
