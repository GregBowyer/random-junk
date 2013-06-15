#include <stdio.h>
#include <sys/mman.h>
#include <string.h>
#include <errno.h>

#include <fcntl.h>
#include <stdlib.h>
#include <sys/time.h>

int main(int argc, char** argv) {
    off_t offset;

    offset = 0;

    int fd;
    fd = open("/datasets/dictionary-deduped.txt", O_CREAT | O_RDWR, 0755);

    if (fd < 0) {
        perror("fuckit it");
        exit(1);
    }

    int prot = PROT_READ | PROT_WRITE;
    int flags = MAP_PRIVATE | MAP_HUGETLB;
    size_t len = 4 * 1024 * 1024;
    void *addr = mmap(NULL, len, prot, flags, fd, offset);

    if (addr == MAP_FAILED) {
        printf("Fuckit: %s\n", strerror(errno));
        return 1;
    } else {
        while (1 == 1) {
            // Dont chew the CPU
            struct timeval tv;
            tv.tv_sec = 1000;
            tv.tv_usec = 0;
            select(0, NULL, NULL, NULL, &tv);
        }
    }
    return 0;
}
