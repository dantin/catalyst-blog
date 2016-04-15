title: Java中线程的同步与等待
date: 2016-04-14 21:06:11
categories: 工程
tags: Java
toc: true
---

多线程设计过程中，经常会遇到需要等待其它线程结束以后再做其他事情的情况，本文以此为场景，介绍线程间的同步与等待问题。

### 示例线程

首先是一个线程，它执行完毕需要5秒。

```java
public class TestThread implements Runnable {

    private int id;
    
    public TestThread(int id) {
        this.id = id;
    }
    @Override
    public void run() {
        System.out.printf("Task %d begin\n", id);
        try {
            Thread.sleep(WAITING_TIME);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.printf("Task %d end\n", id);
    }
}
```

### 并发不同步

在主线程中，计划等待子线程执行完成。

```java
public void testWait() {
    long start = System.currentTimeMillis();

    Thread thread = new Thread(new TestThread(1));
    thread.start();

    long end = System.currentTimeMillis();
    System.out.printf("main stop in %d ms", end - start);
}
```

但是执行上面的main发现并不是想要的结果：

```bash
Task 1 begin
main stop in 8 ms
```

很明显主线程和子线程是并发执行的，主线程并没有等待。

### 并发同步

对于只有一个子线程，如果主线程需要等待子线程执行完成，再继续向下执行，可以使用Thread的join()方法。join()方法会阻塞主线程继续向下执行。

```java
public void testJoin() {
    long start = System.currentTimeMillis();

    Thread thread = new Thread(new TestThread(1));
    thread.start();

    try {
        thread.join();
    } catch (InterruptedException e) {
        e.printStackTrace();
    }

    long end = System.currentTimeMillis();
    System.out.printf("main stop in %d ms", end - start);
}
```

执行结果：

```bash
Task 1 begin
Task 1 end
main stop in 5023 ms
```

_注意：join()要在start()方法之后调用。_

### 等待多个子线程顺序执行

比如主线程需要等待4个子线程。这4个线程之间是串行执行。

```java
public void testSyncWait() {
    long start = System.currentTimeMillis();

    for(int i = 0; i < TOTAL_NUMBER_OF_TASKS; i++) {
        Thread thread = new Thread(new TestThread(i));
        thread.start();

        try {
            thread.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    long end = System.currentTimeMillis();
    System.out.printf("main stop in %d ms", end - start);
}
```

在上面的代码套上一个for循环，执行结果：

```bash
Task 0 begin
Task 0 end
Task 1 begin
Task 1 end
Task 2 begin
Task 2 end
Task 3 begin
Task 3 end
main stop in 20020 ms
```

由于thread.join()阻塞了主线程继续执行，导致for循环一次就需要等待一个子线程执行完成，而下一个子线程不能立即start()，5个子线程不能并发。

### 等待子进程并发执行

要想子线程之间能并发执行，那么需要在所有子线程start()后，在执行所有子线程的join()方法。

```java
public void testAsyncWait() {
    long start = System.currentTimeMillis();

    List<Thread> threads = new ArrayList<>(TOTAL_NUMBER_OF_TASKS);
    for(int i = 0; i < TOTAL_NUMBER_OF_TASKS; i++) {
        Thread thread = new Thread(new TestThread(i));
        thread.start();
        threads.add(thread);

    }

    try {
        for(Thread thread : threads) {
            thread.join();
        }
    } catch (InterruptedException e) {
        e.printStackTrace();
    }

    long end = System.currentTimeMillis();
    System.out.printf("main stop in %d ms", end - start);
}
```

执行结果：

```bash
Task 0 begin
Task 1 begin
Task 2 begin
Task 3 begin
Task 1 end
Task 0 end
Task 3 end
Task 2 end
main stop in 5010 ms
```

### CountDownLatch进行同步等待

CountDownLatch是java.util.concurrent中的一个同步辅助类，可以把它看做一个倒数计数器。初始化时先设置一个倒数计数初始值，每调用一次countDown()方法，倒数值减一，await()方法会阻塞当前进程，直到倒数至0。

同样还是主线程等待5个并发的子线程。修改上面的代码，在主线程中，创建一个初始值为5的CountDownLatch，并传给每个子线程，在每个子线程最后调用countDown()方法对倒数器减1，当5个子线程等执行完成，那么CountDownLatch也就倒数完成，主线程调用await()方法等待5个子线程执行完成。

修改MyThread接收传入的CountDownLatch

```java
public void testCountDownLatch() {
    long start = System.currentTimeMillis();

    // 创建一个初始值为5的倒数计数器
    CountDownLatch countDownLatch = new CountDownLatch(TOTAL_NUMBER_OF_TASKS);
    for(int i = 0; i < TOTAL_NUMBER_OF_TASKS; i++) {
        final int id = i;
        Thread thread = new Thread(() -> {
            try {
                System.out.printf("task %d start\n", id);
                Thread.sleep(WAITING_TIME);
                System.out.printf("task %d stop\n", id);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            countDownLatch.countDown();
        });
        thread.start();
    }

    try {
        // 阻塞当前线程，直到倒数计数器倒数到0
        countDownLatch.await();
    } catch (InterruptedException e) {
        e.printStackTrace();
    }

    long end = System.currentTimeMillis();
    System.out.println("子线程执行时长：" + (end - start));
}
```

注意：如果子线程中会有异常，那么countDownLatch.countDown()应该写在finally里面，这样才能保证异常后也能对计数器减1，不会让主线程永远等待。

另外，await()方法还有一个实用的重载方法：public boolean await(long timeout, TimeUnit unit)，设置超时时间。
例如上面的代码，想要设置超时时间10秒，到了10秒无论是否倒数完成到0，都会不再阻塞主线程。返回值是boolean类型，如果是超时返回false，如果计数到达0没有超时返回true。

```java
// 设置超时时间为10秒
boolean timeoutFlag = countDownLatch.await(10,TimeUnit.SECONDS);
if(timeoutFlag) {
    System.out.println("所有子线程执行完成");
} else {
    System.out.println("超时");
}
```

### 等待线程池

Java线程池java.util.concurrent.ExecutorService是很好用的多线程管理方式。ExecutorService的一个方法boolean awaitTermination(long timeout, TimeUnit unit)，即阻塞主线程，等待线程池的所有线程执行完成，用法和上面所说的CountDownLatch的public boolean await(long timeout,TimeUnit unit)类似，参数设置一个超时时间，返回值是boolean类型，如果超时返回false，如果线程池中的线程全部执行完成，返回true。

由于ExecutorService没有类似CountDownLatch的无参数的await()方法，只能通过awaitTermination来实现主线程等待线程池。

```java
public void testSyncByTaskExecutor() {
    ExecutorService taskExecutor = Executors.newFixedThreadPool(TOTAL_NUMBER_OF_TASKS);
    for(int i = 0; i < TOTAL_NUMBER_OF_TASKS; i++) {
        final int id = i;
        taskExecutor.execute(() -> {
            try {
                System.out.printf("task %d start\n", id);
                Thread.sleep(1000L);
                System.out.printf("task %d stop\n", id);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });
    }
    // force shutdown executor
    taskExecutor.shutdown();
    try {
        // force wait for all thread stopping
        taskExecutor.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
}
```

注意：

while(!executor.isTerminated())也可以替代上面的while (!executor.awaitTermination(10,TimeUnit.SECONDS))

isTerminated()是用来判断线程池是否执行完成。但是二者比较，还是awaitTermination()更好，它有一个超时时间可以控制每隔多久循环一次，而不是一直在循环来消耗性能。

### 线程池结合CountDownLatch

当然，也可以将CountDownLatch与线程池结合使用，如下：

```java
public void testSyncByLatch() {
    System.out.println("main start");
    final CountDownLatch latch = new CountDownLatch(TOTAL_NUMBER_OF_TASKS);
    ExecutorService taskExecutor = Executors.newFixedThreadPool(TOTAL_NUMBER_OF_TASKS);
    for(int i = 0; i < TOTAL_NUMBER_OF_TASKS; i++) {
        final int id = i;
        taskExecutor.execute(() -> {
            try {
                System.out.printf("task %d start\n", id);
                Thread.sleep(1000L);
                
                System.out.printf("task %d stop\n", id);
            } catch (InterruptedException e) {
                e.printStackTrace();
            } finally {
                latch.countDown();
            }
        });
    }

    System.out.println("wait for tasks to finish");
    try {
        latch.await();
    } catch (InterruptedException E) {
        // handle
    }
    // force shutdown executor
    taskExecutor.shutdown();
    System.out.println("main stop");
}
```

### Future实现

最后，也可以通过Future来实现等待。

```java
public void testSyncByFuture() {
    ExecutorService taskExecutor = Executors.newFixedThreadPool(TOTAL_NUMBER_OF_TASKS);
    List<Callable<Integer>> tasks = new ArrayList<>();

    for (int i = 1; i <= TOTAL_NUMBER_OF_TASKS; i++) {
        final int id = i;
        tasks.add(() -> {
            try {
                System.out.printf("task %d start\n", id);
                Thread.sleep(1000L);
                System.out.printf("task %d stop\n", id);
                return 0;
            } catch (InterruptedException e) {
                e.printStackTrace();
                return 1;
            }
        });
    }

    try {
        List<Future<Integer>> futures = taskExecutor.invokeAll(tasks);
        int flag = 0;

        for (Future<Integer> f : futures) {
            Integer res = f.get();
            System.out.println("Status: " + res);
            if (!f.isDone())
                flag = 1;
        }

        if (flag == 0)
            System.out.println("SUCCESS");
        else
            System.out.println("FAILED");

    } catch (InterruptedException | ExecutionException e) {
        e.printStackTrace();
    }
}
```

参考

[stackoverflow](http://stackoverflow.com/questions/1250643/how-to-wait-for-all-threads-to-finish-using-executorservice)
