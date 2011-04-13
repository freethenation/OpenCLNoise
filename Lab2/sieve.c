#include <stdio.h>
#include <stdlib.h>
#define ARRSIZE 1073741824

long findsmallest(char* primes, long idx) {
	for(long i=idx; i < ARRSIZE; ++i)
	  if(primes[i] == 1)
		return i;
}

long sieve() {
	char* primes = malloc(ARRSIZE);
	printf("Allocating array... ");
	for(long i=0; i < ARRSIZE; ++i)
		primes[i] = 1;
	printf("done.\n");
	primes[0] = 0;
	primes[1] = 0;
	long k = 2, mult;
	while(k*k <= ARRSIZE) {
	  printf("Testing value %ld.\n",k);
		mult = k * k;
		while(mult <= ARRSIZE) {
			primes[mult] = 0;
			mult += k;
		}
		k = findsmallest(primes,k+1);
	}
	
	printf("Summing... ");
	long n = 0;
	for(long i=0; i < ARRSIZE; ++i)
		n += primes[i];
	printf("done.\n");
	free(primes);
	return n;
}

int main() {
  printf("Primes < %d: %ld\n",ARRSIZE,sieve());
  return 0;
}
