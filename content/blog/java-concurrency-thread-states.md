+++
date = "2016-06-28T13:56:30+08:00"
title = "Java线程的状态及切换"
categories = ["Engineering"]
tags = ["Java", "Concurrency"]
description = "本文介绍Java中线程的状态"
slug = "java-concurrency-thread-states"
+++

线程是Java编程中绕不开的槛，Java线程一共有六个状态。

### 线程状态

#### NEW

_新建尚未运行/启动_

还没调用start，或者调用了start()方法，不一定立即改变线程状态，中间可能需要一些步骤才完成一个线程的启动。

#### RUNNABLE

_处于可运行状态：正在运行或准备运行_

start调用结束，线程由NEW变成RUNNABLE，存活着，并尝试占用CPU资源，yield操作时，线程还是Runnable状态，只是它有一个细节的内部变化，做一个简单的让步。在Java层面是Runnable的状态，并不代表一定处于运行中的状态，比如BIO中，线程正阻塞在网络等待的时候，看到的状态依然是Runnable状态，而底层线程已经被阻塞住了。

#### BLOCKED

_等待获取锁时进入的状态_

线程被挂起了，原因通常是因为它在等待一个锁，当某个synchronized正好有线程在使用时，一个线程尝试进入这个临界区，就会被阻塞，直到另一个线程走完临界区或发生了相应锁对象的wait操作后，它才有机会去争夺进入临界区的权利。当抢到锁之后，才会从blocked状态恢复到runnable状态。这个状态它好像什么也不做一样。

#### WAITING

_通过wait方法进入的等待_

当wait，join，park方法调用时，进入WAITING状态。前提是这个线程已经拥有锁了。

> blocked和waiting状态的区别是：
> 
> * blocked是虚拟机认为程序还不能进入某个区域，因为同时进去就会有问题，这是一块临界区。
> * 发生wait等操作的先决条件是要进入临界区，也就是线程已经拿到锁了，自己可能进去做了一些事情，但此时通过判定业务上的参数，发现还有一些其他配合的资源没有准备充分，那么自己就等等再做其他事情。

在waiting状态下，如果发生了interrupt操作，则处于该状态的线程在内部会抛出一个InterruptedException，这个异常应当在run方法内捕获，使得run方法正常地执行完成，当然捕获异常后，是决定让线程继续运行，还是结束等要根据业务场景才处理。

如果发生了notify动作，则会从等待池当中唤醒一个线程重新恢复到Runnable状态，如果是notifyall操作，则唤醒所有等待线程。

#### TIMED_WAITING

_通过sleep或wait timeout方法进入的限期等待的状态_

通过wait(t),sleep(t),join(t),parkNanos,parkUntil等方法进入此状态。当时间达到时触发线程回到工作状态Runnable。

interrupt只对处于waiting或timed_waiting状态的线程起作用，对其他状态不起作用。

#### TERMINATED

_线程终止状态_

线程结束了，就处于这种状态，也就是run方法运行完了。这只是Java语言级别的一种状态，在操作系统内部可能已经注销了相应的线程，或者将它复用给其他需要使用线程的请求。

### 线程状态切换

<img src="/images/java_thread_states.png" alt="Java线程状态" style="width: 500px;"/>

<img src="/images/java_thread_states_exchange.png" alt="Java线程状态切换" style="width: 500px;"/>

### 状态表

| 状态名称      | 说明      |
| ------------ |:--------:|
| NEW          | 初始状态，线程被构建，但是还没有调用start()方法 |
| RUNNABLE     | 运行状态，Java线程将操作系统中的就绪和运行两种状态笼统地称为“运行中” |
| BLOCKED      | 阻塞状态，表示线程阻塞于锁 |
| WAITING      | 等待状态，表示线程进入等待状态，进入该状态表示当前线程需要等待其他线程做出一些特定动作（通知或中断） |
| TIME_WAITING | 超时等待状态，该状态不同于WAITING，它是可以在指定的时间自行返回的 |
| TERMINATED   | 终止状态，表示当前线程已经执行完毕 |

### 线程状态源码

```java
/**
 * A thread state.  A thread can be in one of the following states:
 * <ul>
 * <li>{@link #NEW}<br>
 *     A thread that has not yet started is in this state.
 *     </li>
 * <li>{@link #RUNNABLE}<br>
 *     A thread executing in the Java virtual machine is in this state.
 *     </li>
 * <li>{@link #BLOCKED}<br>
 *     A thread that is blocked waiting for a monitor lock
 *     is in this state.
 *     </li>
 * <li>{@link #WAITING}<br>
 *     A thread that is waiting indefinitely for another thread to
 *     perform a particular action is in this state.
 *     </li>
 * <li>{@link #TIMED_WAITING}<br>
 *     A thread that is waiting for another thread to perform an action
 *     for up to a specified waiting time is in this state.
 *     </li>
 * <li>{@link #TERMINATED}<br>
 *     A thread that has exited is in this state.
 *     </li>
 * </ul>
 *
 * <p>
 * A thread can be in only one state at a given point in time.
 * These states are virtual machine states which do not reflect
 * any operating system thread states.
 *
 * @since   1.5
 * @see #getState
 */
public enum State {
    /**
     * Thread state for a thread which has not yet started.
     */
    NEW,
    /**
     * Thread state for a runnable thread.  A thread in the runnable
     * state is executing in the Java virtual machine but it may
     * be waiting for other resources from the operating system
     * such as processor.
     */
    RUNNABLE,
    /**
     * Thread state for a thread blocked waiting for a monitor lock.
     * A thread in the blocked state is waiting for a monitor lock
     * to enter a synchronized block/method or
     * reenter a synchronized block/method after calling
     * {@link Object#wait() Object.wait}.
     */
    BLOCKED,
    /**
     * Thread state for a waiting thread.
     * A thread is in the waiting state due to calling one of the
     * following methods:
     * <ul>
     *   <li>{@link Object#wait() Object.wait} with no timeout</li>
     *   <li>{@link #join() Thread.join} with no timeout</li>
     *   <li>{@link LockSupport#park() LockSupport.park}</li>
     * </ul>
     *
     * <p>A thread in the waiting state is waiting for another thread to
     * perform a particular action.
     *
     * For example, a thread that has called <tt>Object.wait()</tt>
     * on an object is waiting for another thread to call
     * <tt>Object.notify()</tt> or <tt>Object.notifyAll()</tt> on
     * that object. A thread that has called <tt>Thread.join()</tt>
     * is waiting for a specified thread to terminate.
     */
    WAITING,
    /**
     * Thread state for a waiting thread with a specified waiting time.
     * A thread is in the timed waiting state due to calling one of
     * the following methods with a specified positive waiting time:
     * <ul>
     *   <li>{@link #sleep Thread.sleep}</li>
     *   <li>{@link Object#wait(long) Object.wait} with timeout</li>
     *   <li>{@link #join(long) Thread.join} with timeout</li>
     *   <li>{@link LockSupport#parkNanos LockSupport.parkNanos}</li>
     *   <li>{@link LockSupport#parkUntil LockSupport.parkUntil}</li>
     * </ul>
     */
    TIMED_WAITING,
    /**
     * Thread state for a terminated thread.
     * The thread has completed execution.
     */
    TERMINATED;
}
```
