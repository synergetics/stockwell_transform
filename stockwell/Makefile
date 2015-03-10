#PYINCDIR = /usr/include/python2.4
PYINCDIR = /usr/include/python2.6
NUMPYDIR = /usr/lib/python2.6/dist-packages/numpy/core/include/numpy
CFLAGS = -O3 -I$(PYINCDIR) -I$(NUMPYDIR) -fPIC

all:	sinemodule.so stmodule.so

sinemodule.so:	sinemodule.o
	$(CC) -shared -o $@ sinemodule.o

stmodule.so:	stmodule.o st.o
	$(CC) -shared -o $@ stmodule.o st.o -lfftw3