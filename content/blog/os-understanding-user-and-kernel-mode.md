+++
date = "2016-03-16T14:44:49+08:00"
title = "用户态和内核态"
categories = ["Scholar"]
tags = ["OS"]
description = "操作系统中关于用户态和内核态的概念"
slug = "os-understanding-user-and-kernel-mode"
+++

类似Redis、Memcached之类的缓存系统，需要频繁申请与释放内存，为了确保效率，一般都提供了用户态的内存管理。原因是，直接调用malloc/free会导致用户态到内核态的切换，较为耗时。那么，两者的区别到底是什么呢？

### 内核态与用户态的定义

CPU只会运行在以下两种状态：

* __Kernel Mode__

    In Kernel mode, the executing code has complete and unrestricted access to the underlying hardware. It can execute any CPU instruction and reference any memory address. Kernel mode is generally reserved for the lowest-level, most trusted functions of the operating system. Crashes in kernel mode are catastrophic; they will halt the entire PC.

* __User Mode__

    In User mode, the executing code has no ability to *directly* access hardware or reference memory. Code running in user mode must delegate to system APIs to access hardware or memory. Due to the protection afforded by this sort of isolation, crashes in user mode are always recoverable. Most of the code running on your computer will execute in user mode.

不同硬件的实现方式可能也不同，x86是通过0-3的4层protection rings硬件来划分的。据称Linux仅使用ring 0作为内核态，ring 3作为用户态，未涉及ring 1-2；而windows中部分drivers会使用ring 1-2。

### 何时会切换

Typically, there are 2 points of switching:

* __When calling a System Call__

    after calling a System Call, the task voluntary calls pieces of code living in Kernel Mode

* __When an IRQ (or exception) comes__

    after the IRQ an IRQ handler (or exception handler) is called, then control returns back to the task that was interrupted like nothing was happened.

    IRQ全称为Interrupt Request，即是“中断请求”的意思，IRQ的作用就是在我们所用的电脑中，执行硬件中断请求的动作。

一般而言，系统调用是用户主动发起的，例如调用`fork`函数，会间接调用系统函数`sys_fork`，从而陷入内核态。而IRQ的发生也有用户“主动”和“被动”两种形式：例如用户调用`malloc`申请内存，可能会导致缺页异常，引发IRQ陷入内核态；或者我们需要读取硬盘中的一段数据时，当数据读取完毕，硬盘就通过IRQ来通知系统，相应的数据已经写到指定的内存中了。

### 切换成本

从用户态到内核态，本质上都是响应中断。因为系统调用实际上最终是中断机制实现的，而异常和中断的处理机制基本上也是一致的。其切换过程如下：

1. 从当前进程的描述符中提取其内核栈的ss0及esp0信息。
2. 使用ss0和esp0指向的内核栈将当前进程的cs,eip,eflags,ss,esp信息保存起来，这个过程也完成了由用户栈到内核栈的切换过程，同时保存了被暂停执行的程序的下一条指令。
3. 将先前由中断向量检索得到的中断处理程序的cs,eip信息装入相应的寄存器，开始执行中断处理程序，这时就转到了内核态的程序执行了。
内核态到用户态需要将保存的进程信息予以恢复。

从上面的步骤可以看到，模式切换涉及大量数据的复制，还需要硬件配合，故耗时较大。而在不发生模式切换时，CPU只需顺序执行指令即可。所以应该尽量减少切换次数！

参考资料

1. [codinghorror](http://blog.codinghorror.com/understanding-user-and-kernel-mode/)
2. [TLDP](http://www.tldp.org/HOWTO/KernelAnalysis-HOWTO-3.html)
3. [Redis和Memcached的区别](http://www.biaodianfu.com/redis-vs-memcached.html)
4. [Linux的内核态和用户态](http://flykobe.com/index.php/2015/03/03/linux%E7%9A%84%E5%86%85%E6%A0%B8%E6%80%81%E5%92%8C%E7%94%A8%E6%88%B7%E6%80%81/)

