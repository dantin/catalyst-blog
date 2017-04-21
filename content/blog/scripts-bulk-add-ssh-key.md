+++
date = "2017-04-21T10:48:34+08:00"
title = "批量增加SSH公钥"
categories = ["Misc"]
tags = ["Scripts"]
description = "更改Java项目包名的脚步"
slug = "scripts-bulk-add-ssh-key"
+++

公司用ansible管理台机器，但是使用时会出现SSH公钥认证问题。在不修改`StrictHostKeyChecking`的前提下写了个脚本，批量把共钥加到`~/.ssh/known_hosts`中。

### 获得待处理IP地址

线上ansible配置文件

```console
[app_api_active]
production-app-api-1          ansible_ssh_host=10.1.1.54    ansible_priIP=10.1.1.54
production-app-api-2          ansible_ssh_host=10.1.1.34    ansible_priIP=10.1.1.34
production-app-api-3          ansible_ssh_host=10.1.1.214   ansible_priIP=10.1.1.214
```

通过`awk`获取所有IP

```bash
awk -F' ' '{if(NF>=3) print $3}' ~/Documents/code/ansible/env/production | awk -F'=' '{print $2}' > hosts
```

### 批量处理每台服务器

对所有服务器机器，批量处理

```bash
#!/bin/bash

cat ./hosts | while read line
do
    echo "Login: $line"
    ./copy-id.sh $line
done
```

使用`expect`添加SSH Key

```bash
#!/usr/bin/expect

set timeout 5

spawn ssh -l root [lindex $argv 0]
expect {
    timeout {
        puts "Connection timed out"
        exit 1
    }

    "yes/no" {
        send "yes\r"
        exp_continue
    }


    "*# " {
        send "ls -la\r"
    }
}
```
