/************************************************************\
 * Copyright 2021 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> 

#define N 3

// __attribute__((annotate("@critical_path(pointcut='around')")))
void *foo(void *threadid)
{
    long tid;
    tid = (long)threadid;
    printf("This is worker_thread() %ld \n", tid);
    usleep(5000000);

    int temp = 0;
    int temp1[10000] = {25};
    int temp2[10000] = {22};
    int temp3[10000] = {0};
    for (int i = 0; i < 10000; i++)
    {
        temp = temp + 1;
        temp3[i] = temp1[i] * temp2[i];
        for (int j = i + 1; j < 10000; j++)
        {
            temp3[j] = temp3[j] / 3;
        }
    }
    
    pthread_exit(NULL);
}

int main()
{
    pthread_t my_thread[N];

    long id;
    for (id = 1; id <= N; id++)
    {
        int ret =  pthread_create(&my_thread[id], NULL, &foo, (void *)id);
        if (ret != 0)
        {
            printf("Error: pthread_create() failed\n");
            exit(EXIT_FAILURE);
        }
    }

    pthread_exit(NULL);
}
