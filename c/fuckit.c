#include <stdio.h>
#include <sys/mman.h>
#include <string.h>
#include <errno.h>

#include <fcntl.h>
#include <stdlib.h>
#include <sys/time.h>

/* Would like a semi-open interval [min, max) */
int random_in_range (unsigned int min, unsigned int max)
{
  int base_random = rand(); /* in [0, RAND_MAX] */
  if (RAND_MAX == base_random) return random_in_range(min, max);
  /* now guaranteed to be in [0, RAND_MAX) */
  int range       = max - min,
      remainder   = RAND_MAX % range,
      bucket      = RAND_MAX / range;
  /* There are range buckets, plus one smaller interval
     within remainder of RAND_MAX */
  if (base_random < RAND_MAX - remainder) {
    return min + base_random/bucket;
  } else {
    return random_in_range (min, max);
  }
}

int main(int argc, char** argv) {
    off_t offset;

    offset = 0;

    int fd;
    fd = open("/datasets/lucene-benchmarking/data/enwiki-20120502-lines-1k.txt", O_CREAT | O_RDWR, 0755);

    if (fd < 0) {
        perror("fuckit it");
        exit(1);
    }

    int prot = PROT_READ | PROT_WRITE;
    int flags = MAP_SHARED;

    // Map in 24 GB of the file, we just need something huge
    size_t len = 24L * 1024 * 1024 * 1024;
    void *addr = mmap(NULL, len, prot, flags, fd, offset);

    if (addr == MAP_FAILED) {
        printf("Fuckit: %s\n", strerror(errno));
        return 1;
    } else {

        int good_advise = madvise(addr, len, MADV_WILLNEED);
        if (!good_advise) {
            printf("The kernel does not like our advise %s\n", strerror(errno));
            return 1;
        }

        while (1 == 1) {
            // Dont chew the CPU
            struct timeval tv;
            tv.tv_sec = 0;
            tv.tv_usec = atoi(argv[1]);
            select(0, NULL, NULL, NULL, &tv);

            // pick a random page
            int hunk_o_ram = random_in_range(0, 1024*1024*1024);
            int offset = random_in_range(1, 23);

            long page = (long) hunk_o_ram * (long) offset;
            char something = ((char*)addr)[page];
        }
    }
    return 0;
}
