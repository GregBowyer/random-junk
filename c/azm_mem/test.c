#include <stdio.h>
#include <string.h>

#include <aznix/az_memory.h>
#include <aznix/az_pgroup.h>

#include <unistd.h>
#include <stdlib.h>

/**
 * Stupid ridiculous test to see if I can engineer
 * at least a hello-world C program that can use the azul
 * memory interfaces
 */
void os_setup_avm_launch_env() {

    unsigned long avm_process_id = (unsigned long) getpid();
    unsigned long avm_mem_max    = (unsigned long) 1000L;
    unsigned long avm_mem_commit = (unsigned long) 500L;

    printf("Process id %d\n", avm_process_id);

    int retcode = az_pmem_set_account_funds(avm_process_id, AZMM_DEFAULT_ACCOUNT,
            AZMM_COMMITTED_FUND, AZMM_OVERDRAFT_FUND);

    if (retcode) {
        printf("FUCK! [%lu] failed to set Account [%d] with funds %d\%d: %s\n",
                avm_process_id, AZMM_DEFAULT_ACCOUNT, AZMM_COMMITTED_FUND, 
                AZMM_OVERDRAFT_FUND, strerror(errno));
        abort();
    }

    retcode = az_pmem_set_account_funds(avm_process_id, AZMM_JHEAP_ACCOUNT,
                                    AZMM_COMMITTED_FUND, AZMM_OVERDRAFT_FUND);
    if (retcode) {
      printf("[%lu] Failed to set AC# %d with funds %d/%d: %s\n",
               avm_process_id,
               AZMM_JHEAP_ACCOUNT, AZMM_COMMITTED_FUND, AZMM_OVERDRAFT_FUND,
               strerror(errno));
        abort();
    }

    retcode = az_pmem_set_account_funds(avm_process_id, AZMM_GCPP_ACCOUNT,
                                    AZMM_GCPP_FUND, AZMM_GCPP_FUND);
    if (retcode) {
      printf("[%lu] Failed to set AC# %d with funds %d/%d: %s\n",
               avm_process_id,
               AZMM_JHEAP_ACCOUNT, AZMM_GCPP_FUND, AZMM_GCPP_FUND,
               strerror(errno));
        abort();
    }
    printf("[%lu] Associated accts with funds\n", avm_process_id);

    retcode = az_pmem_fund_account(avm_process_id, AZMM_DEFAULT_ACCOUNT, avm_mem_commit);
    if (retcode) {
      printf("[%lu] Failed to fund AC# %d with %lu: %s\n",
               avm_process_id, AZMM_DEFAULT_ACCOUNT, avm_mem_commit,
               strerror(errno));
        abort();
    }
    printf("[%lu] Funded AC# %d with %lu\n",
           avm_process_id, AZMM_DEFAULT_ACCOUNT, avm_mem_commit);

    retcode = az_pmem_set_maximum(avm_process_id, avm_mem_max);
    if (retcode) {
      printf("[%lu] Failed to set mem_rlimit with %lu: %s\n",
               avm_process_id, avm_mem_max,
               strerror(errno));
        abort();
    }
    printf("[%lu] Set mem_rlimit with %lu\n", avm_process_id, avm_mem_max);

    retcode = az_pmem_set_account_maximum(avm_process_id, AZMM_DEFAULT_ACCOUNT, avm_mem_max);
    if (retcode) {
      printf("[%lu] Failed to set AC# 0 mem_rlimit with %lu: %s\n",
               avm_process_id, avm_mem_max,
               strerror(errno));
        abort();
    }
    printf("[%lu] Set AC# 0 mem_rlimit with %lu\n",
           avm_process_id, avm_mem_max);

    // Reserve low memory upfront for VM structures
    int flags = AZMM_BATCHABLE;
    /*
    size_t len = __VM_STRUCTURES_END_ADDR__ - __VM_STRUCTURES_START_ADDR__; 
    retcode = az_mreserve((address_t)__VM_STRUCTURES_START_ADDR__, len, flags);
    if (retcode < 0) {
      printf("az_mreserve(VMSTRUCTS) failed: %s", strerror(errno));
    }
    */

}

int main(int argc, char** argv) {

    printf("First attempt to init some az mem\n");
    os_setup_avm_launch_env();

    return 0;

}
