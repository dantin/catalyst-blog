title: 银行家算法
date: 2016-02-05 14:18:03
categories: 学术
tags: Algorithm
toc: true
---

银行家算法（Banker's Algorithm）是一个避免死锁（Deadlock）的著名算法,它以银行借贷系统的分配策略为基础，判断并保证系统的安全运行。

### 背景

在银行中，客户申请贷款的数量是有限的，每个客户在第一次申请贷款时要声明完成该项目所需的最大资金量，在满足所有贷款要求时，客户应及时归还。银行家在客户申请的贷款数量不超过自己拥有的最大值时，都应尽量满足客户的需要。在这样的描述中，银行家就好比操作系统，资金就是资源，客户就相当于要申请资源的进程。

### 进程

```bash
 Allocation　　　Max　　　Available
 　　ＡＢＣＤ　　ＡＢＣＤ　　ＡＢＣＤ
 P1　００１４　　０６５６　　１５２０　
 P2　１４３２　　１９４２　
 P3　１３５４　　１３５６
 P4　１０００　　１７５０
```

我们会看到一个资源分配表，要判断是否为安全状态，首先先找出它的Need，Need即Max(最多需要多少资源)减去Allocation(原本已经分配出去的资源)，计算结果如下：

```bash
NEED
 ＡＢＣＤ
 ０６４２　
 ０５１０
 ０００２
 ０７５０
 ```

然后加一个全都为false的字段

```bash
FINISH
 false
 false
 false
 false
```

接下来找出need比available小的(千万不能把它当成4位数 他是4个不同的数)

```bash
   NEED　　Available
 ＡＢＣＤ　　ＡＢＣＤ
 ０６４２　　１５２０
 ０５１０<-
 ０００２
 ０７５０
```

P2的需求小于能用的，所以配置给他再回收

```bash
  NEED　　Available
 ＡＢＣＤ　　ＡＢＣＤ
 ０６４２　　１５２０
 ００００　＋１４３２
 ０００２－－－－－－－
 ０７５０　　２９５２
```

此时P2 FINISH的false要改成true(己完成)

```bash
 FINISH
 false
 true
 false
 false
```

接下来继续往下找，发现P3的需求为0002，小于能用的2952，所以资源配置给他再回收

```bash
 　NEED　　Available
 ＡＢＣＤ　　Ａ　Ｂ　Ｃ　Ｄ
 ０６４２　　２　９　５　２
 ００００　＋１　３　５　４
 ０００２－－－－－－－－－－
 ０７５０　　３　12　10　6
```

同样的将P3的false改成true

```bash
 FINISH
 false
 true
 true
 false
```

依此类推，做完P4→P1，当全部的FINISH都变成true时，就是安全状态。

### 安全和不安全的状态

如果所有过程有可能完成执行（终止），则一个状态（如上述范例）被认为是安全的。由于系统无法知道什么时候一个过程将终止，或者之后它需要多少资源，系统假定所有进程将最终试图获取其声明的最大资源并在不久之后终止。在大多数情况下，这是一个合理的假设，因为系统不是特别关注每个进程运行了多久（至少不是从避免死锁的角度）。此外，如果一个进程终止前没有获取其它能获取的最多的资源，它只是让系统更容易处理。

基于这一假设，该算法通过尝试寻找允许每个进程获得的最大资源并结束（把资源返还给系统）的进程请求的一个理想集合，来决定一个状态是否是安全的。不存在这个集合的状态都是不安全的。

### 实现

#### 伪代码

* P - 进程的集合
* Mp - 进程p的最大的请求数目
* Cp - 进程p当前被分配的资源
* A - 当前可用的资源

```c
while (P != ∅) {
    found = FALSE;
    foreach (p ∈ P) {
        if (Mp − Cp ≤ A) {
             /* p可以獲得他所需的資源。假設他得到資源後執行；執行終止，並釋放所擁有的資源。*/
             A = A + Cp ;
             P = P − {p};
             found = TRUE;
        }
    }
    if (! found) return FAIL;
}
return OK;
```

#### C

```c
/*PROGRAM TO IMPLEMENT BANKER'S ALGORITHM
  *   --------------------------------------------*/
#include <stdio.h>
int curr[5][5], maxclaim[5][5], avl[5];
int alloc[5] = {0, 0, 0, 0, 0};
int maxres[5], running[5], safe=0;
int count = 0, i, j, exec, r, p, k = 1;

int main()
{
    printf("\nEnter the number of processes: ");
    scanf("%d", &p);

    for (i = 0; i < p; i++) {
        running[i] = 1;
        count++;
    }

    printf("\nEnter the number of resources: ");
    scanf("%d", &r);

    printf("\nEnter Claim Vector:");
    for (i = 0; i < r; i++) { 
        scanf("%d", &maxres[i]);
    }

    printf("\nEnter Allocated Resource Table:\n");
    for (i = 0; i < p; i++) {
        for(j = 0; j < r; j++) {
            scanf("%d", &curr[i][j]);
        }
    }

    printf("\nEnter Maximum Claim Table:\n");
    for (i = 0; i < p; i++) {
        for(j = 0; j < r; j++) {
            scanf("%d", &maxclaim[i][j]);
        }
    }

    printf("\nThe Claim Vector is: ");
    for (i = 0; i < r; i++) {
        printf("\t%d", maxres[i]);
    }

    printf("\nThe Allocated Resource Table:\n");
    for (i = 0; i < p; i++) {
        for (j = 0; j < r; j++) {
            printf("\t%d", curr[i][j]);
        }

        printf("\n");
    }

    printf("\nThe Maximum Claim Table:\n");
    for (i = 0; i < p; i++) {
        for (j = 0; j < r; j++) {
            printf("\t%d", maxclaim[i][j]);
        }

        printf("\n");
    }

    for (i = 0; i < p; i++) {
        for (j = 0; j < r; j++) {
            alloc[j] += curr[i][j];
        }
    }

    printf("\nAllocated resources:");
    for (i = 0; i < r; i++) {
        printf("\t%d", alloc[i]);
    }

    for (i = 0; i < r; i++) {
        avl[i] = maxres[i] - alloc[i];
    }

    printf("\nAvailable resources:");
    for (i = 0; i < r; i++) {
        printf("\t%d", avl[i]);
    }
    printf("\n");

    //Main procedure goes below to check for unsafe state.
    while (count != 0) {
        safe = 0;
        for (i = 0; i < p; i++) {
            if (running[i]) {
                exec = 1;
                for (j = 0; j < r; j++) {
                    if (maxclaim[i][j] - curr[i][j] > avl[j]) {
                        exec = 0;
                        break;
                    }
                }
                if (exec) {
                    printf("\nProcess%d is executing\n", i + 1);
                    running[i] = 0;
                    count--;
                    safe = 1;

                    for (j = 0; j < r; j++) {
                        avl[j] += curr[i][j];
                    }

                    break;
                }
            }
        }
        if (!safe) {
            printf("\nThe processes are in unsafe state.\n");
            break;
        } else {
            printf("\nThe process is in safe state");
            printf("\nAvailable vector:");

            for (i = 0; i < r; i++) {
                printf("\t%d", avl[i]);
            }

            printf("\n");
        }
    }
}
```

输出

```bash
/*SAMPLE  OUTPUT
-----------------
Enter the number of processes:5

Enter the number of resources:4

Enter Claim Vector:8 5 9 7

Enter Allocated Resource Table:
2 0 1 1
0 1 2 1
4 0 0 3
0 2 1 0
1 0 3 0

Enter Maximum Claim Table:
3 2 1 4
0 2 5 2
5 1 0 5
1 5 3 0
3 0 3 3

The Claim Vector is:    8   5   9   7
The Allocated Resource Table:
    2   0   1   1
    0   1   2   1
    4   0   0   3
    0   2   1   0
    1   0   3   0

The  Maximum Claim Table:
    3   2   1   4
    0   2   5   2
    5   1   0   5
    1   5   3   0
    3   0   3   3

 Allocated resources:   7   3   7   5
 Available resources:   1   2   2   2

Process3 is executing

 The process is in safe state
 Available vector:  5   2   2   5
Process1 is executing

 The process is in safe state
 Available vector:  7   2   3   6
Process2 is executing

 The process is in safe state
 Available vector:  7   3   5   7
Process4 is executing

 The process is in safe state
 Available vector:  7   5   6   7
Process5 is executing

 The process is in safe state
 Available vector:  8   5   9   7

 ---------------------------------------------------------*/
 ```

参考

__[Wikipedia](https://en.wikipedia.org/wiki/Banker%27s_algorithm)__