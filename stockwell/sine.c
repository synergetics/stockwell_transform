/* Riedel & Sidorenko sine tapers. */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "stockwell.h"

/* Compute the kth sine taper. d is an array of length N. */

void sine_taper(int k, int N, double *d)
{
	int i;
	double s;

	s = sqrt(2. / (N + 1));
	for (i = 0; i < N; i++) {
		d[i] = s * sin(M_PI * (k + 1) * (i + 1) / (N + 1));
	}
}
