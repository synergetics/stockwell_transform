

void sine_taper(int k, int N, double *d);

void set_wisfile(void);
int st_freq(double f, int len, double srate);

void st(int len, int lo, int hi, double *data, double *result);
void ist(int len, int lo, int hi, double *data, double *result);
void hilbert(int len, double *data, double *result);
