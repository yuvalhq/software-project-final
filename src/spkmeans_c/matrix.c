#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#define COMMA ','
#define LINE_FEED '\n'
#define CARRIAGE_RETURN '\r'

#include <stdlib.h>
#include <stdio.h>
#include "matrix.h"
#include "strutils.h"

Matrix build_matrix(size_t n, size_t m) {
    size_t i;
    Matrix mat = (Matrix) malloc(n * sizeof(Vector));

    for (i = 0; i < n; i++) {
        mat[i] = (Vector) calloc(m, sizeof(double));
    }
    return mat;
}

Matrix build_identity_matrix(size_t n) {
    size_t i;
    Matrix mat = build_matrix(n, n);

    for (i = 0; i < n; i++) {
        mat[i][i] = 1;
    }
    return mat;
}

Matrix build_matrix_from_file(char *filename, size_t *n, size_t *m) {
    size_t i, line_len;
    char *line = NULL;
    char *line_idx = NULL;
    Vector vector = NULL;
    Matrix mat = NULL;
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        return NULL;
    }

    *m = 0;
    *n = 0;
    mat = (Matrix) malloc(sizeof(Vector));

    while (getline(&line, &line_len, file) != -1) {
        if (*m == 0) {
           *m = strcount(line, COMMA) + 1;
        }

        vector = (Vector) calloc(*m, sizeof(double));
        line_idx = line;

        for (i = 0; i < (*m); i++) {
            vector[i] = strtod(line_idx, &line_idx);
            if (*line_idx != COMMA && *line_idx != LINE_FEED &&
                *line_idx != CARRIAGE_RETURN) {
                    free(line);
                    free(vector);
                    free_matrix(mat, *n);
                    fclose(file);
                    return NULL;
            }
            line_idx++;
            if (*line_idx == LINE_FEED) {
                line_idx++;
            }
        }

        mat = (Matrix) realloc(mat, (++(*n)) * sizeof(Vector));
        mat[(*n) - 1] = vector;
    }

    free(line);
    fclose(file);
    return mat;
}

Matrix copy_matrix(Matrix mat, size_t n, size_t m) {
    size_t i, j;
    Matrix copy = build_matrix(n, m);

    for (i = 0; i < n; i++) {
        for (j = 0; j < m; j++) {
            copy[i][j] = mat[i][j];
        }
    }
    return copy;
}

Matrix matrix_sub(Matrix left, Matrix right, size_t n, size_t m) {
    size_t i, j;
    Matrix sub = build_matrix(n, m);

    for (i = 0; i < n; i++) {
        for (j = 0; j < m; j++){
            sub[i][j] = left[i][j] - right[i][j];
        }
    }
    return sub;
}

Matrix matrix_mul(Matrix left, Matrix right, size_t n) {
    size_t i, j, k;
    Matrix res = build_matrix(n, n);

    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
            for (k = 0; k < n; k++) {
                res[i][j] += left[i][k] * right[k][j];
            }
        }
    }
    return res;
}

Matrix transpose(Matrix mat, size_t n, size_t m) {
    size_t i, j;
    Matrix res = build_matrix(n, m);

    for (i = 0; i < n; i++) {
        for (j = 0; j < m; j++) {
            res[i][j] = mat[j][i];
        }
    }
    return res;
}

Vector matrix_diagonal_values(Matrix mat, size_t n){
    size_t i;
    Vector eigenvalues = (Vector) calloc(n, sizeof(double));

    for (i = 0; i < n; i++) {
        eigenvalues[i] = mat[i][i];
    }
    return eigenvalues;
}

void print_matrix(Matrix mat, size_t n, size_t m) {
    size_t i;
    for (i = 0; i < n; i++) {
        print_vector(mat[i], m);
    }
}

void print_transposed_matrix(Matrix mat, size_t n, size_t m) {
    size_t i, j;
    for (j = 0; j < m; j++) {
        for (i = 0; i < n; i++) {
            printf("%.4f", mat[i][j]);
            if (i < n - 1) {
                printf(",");
            }
        }
        printf("\n");
    }
}

void free_matrix(Matrix mat, size_t n) {
    size_t i;
    for (i = 0; i < n; i++) {
        free(mat[i]);
    }
    free(mat);
}
