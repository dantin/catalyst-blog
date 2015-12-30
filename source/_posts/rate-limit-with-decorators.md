title: 简单的访问频次限制实现
date: 2015-12-29 15:08:30
categories: 经验分享
tags: Python
---

在访问Web API的过程中，常见的一个问题是外部系统对请求的频率有限制。

本文记录了通过Python的decorator实现访问频次限制的需求。

``` Python
# -*- coding: utf-8 -*-
import time


def rate_limited(max_per_second):
    min_interval = 1.0 / float(max_per_second)

    def decorate(func):
        last_time_called = [0.0]

        def rate_limited_function(*args, **kargs):
            elapsed = time.clock() - last_time_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kargs)
            last_time_called[0] = time.clock()
            return ret

        return rate_limited_function

    return decorate


@rate_limited(2)  # 2 per second at most
def print_number(num):
    print num


if __name__ == "__main__":
    print "This should print 1,2,3... at about 2 per second."
    for i in range(1, 100):
        print_number(i)
```

这个方法比使用队列系统方便，它适合于顺序任务。但是不支持多线程。