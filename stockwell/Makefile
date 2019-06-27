
CFLAGS = $(shell python-config --includes) $(shell python -c "import numpy; print('-I' + numpy.get_include())") -fPIC
LDFLAGS = -L .

all:	_stockwell.so

_stockwell.so: sine.o st.o
	swig -python ./stockwell.i
	$(CC) -shared -fPIC $(CFLAGS) $(LDFLAGS) -o _stockwell.so sine.c st.c stockwell_wrap.c -lfftw3

clean:
	find . -name "*.o" | xargs rm -rf
	find . -name "*.so" | xargs rm -rf
	find . -name "*.pyc" | xargs rm -rf
	rm -rf stockwell_wrap.c
	rm -rf stockwell.py
