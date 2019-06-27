import sys
import numpy as npy
from numpy import arange, sin, sqrt, pi

from st import st

from math import sqrt


def calcK(bw, N, srate):
	"""Calculate K for a given bandwidth, length, and sampling rate.
	bw = 2p * fr, where fr = srate / N (frequency resolution).
	p specifies the half bandwidth in bins (fr units).
	K = 2p - 1"""

	K = int(bw * float(N) / srate + .5) - 1
	if K < 1: K = 1
	return K

def calcbw(K, N, srate):
	"""Calculate the bandwidth given K."""

	return float(K + 1) * srate / N

# Precompute the tapers.

def calc_tapers(K, N):
	return list(map(lambda k, N = N: sine_taper(k, N), npy.arange(K)))

# Multitaper Stockwell transform.

def mtst(K, tapers, x, lo, hi):
	N = len(x)
	K2 = float(K * K)
	s = 0.
	n = 0.
	for k in range(K):
		X = st(tapers[k] * x, int(lo), int(hi))
		mu = 1. - k * k / K2
		s += mu * abs(X)**2
		n += mu
	s *= N / n
	return s

# Riedel & Sidorenko sine tapers.
def sine_taper(k, N):
	"Compute the kth sine taper of length N"

	s = sqrt(2. / (N + 1))
	d = arange(N, dtype = 'd')
	return s * sin(pi * (k + 1) * (d + 1.) / (N + 1))

