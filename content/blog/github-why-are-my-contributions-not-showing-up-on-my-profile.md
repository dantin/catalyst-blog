+++
date = "2016-12-12T18:49:10+08:00"
title = "为什么Github没有记录Contributions"
categories = ["Engineering"]
tags = ["Git", "Github"]
description = "本文记录Github没有记录提交记录的解决办法"
slug = "github-why-are-my-contributions-not-showing-up-on-my-profile"
+++


近来发现Github没有记录提交记录，解决办法记录如下：

### 原因

Github官网上有这么一句话：

> Your profile contributions graph is a record of contributions you've made to GitHub repositories. Contributions are only counted if they meet certain criteria. In some cases, we may need to rebuild your graph in order for contributions to appear.

[记录规则](https://help.github.com/articles/why-are-my-contributions-not-showing-up-on-my-profile/)

### 记录条件

__Issues 和 pull requests__

* 这个操作是在一年之内
* 这个操作是针对一个独立的仓库，不能是fork

__Commits__

当你的commits满足以下条件时，它才会被展示出来：

* 一年之内提交的commits
* commits使用的email地址是与你的Github账号相关联的
* 这些commits是在一个独立的仓库而不是fork仓库
* 这些commits是在：
    * 在默认分支上（通常是master）
    * 在gh-pages分支(包含 Project Pages sites 的仓库)

此外，至少满足下面条件中的一个（主要针对你Commit的仓库不是你创建的）：

* 你是这个仓库的协作者，或者是这个版本库的拥有组织中的一员
* 你fork过这个仓库
* 你对这个仓库发起过pull request或者issue
* 你对这个仓库标记了Star

_注意：私有库的贡献仅仅对私有库成员显示_

__Contributions未被Github计入的几个常见原因__

* 进行Commits的用户没有被关联到你的Github帐号中。
* 不是在这个版本库的默认分支进行的Commit。
* 这个仓库是一个Fork仓库，而不是独立仓库。

### 如何排查

你可以在你的本地repo里用git log命令查看commit记录上的个人邮箱是否正确，像我就是因为之前切换到Mac平台开发之后用户名没有配置，所以我之后的commit记录上的邮箱一直是Leo@Leo-MacBook-Pro.local，所以Github就会认为这些commits都不是你提交的！

### 补救措施

然而这也并不是没有补救办法的，Github官网上就有给出详细的补救过程，[Changing author info](https://help.github.com/articles/changing-author-info/)

__使用脚本来改变某个repo的Git历史__

我们已经创建了一个脚本，使用正确的姓名和电子邮件地址提交后，你以前提交的所有的commits中的作者信息及提交者字段中的旧的用户名和邮箱地址都将被更正

_注意： 执行这段脚本会重写 repo 所有协作者的历史。完成以下操作后，任何 fork 或 clone 的人必须获取重写后的历史并把所有本地修改 rebase 入重写后的历史中。_

在执行这段脚本前，你需要准备的信息：

给你的repo创建一个全新的clone

```
git clone --bare https://github.com/user/repo.git
cd repo.git
```

复制粘贴脚本，并根据你的信息修改以下变量：旧的Email地址，正确的用户名，正确的邮件地址

```bash
#!/bin/sh
git filter-branch --env-filter '
OLD_EMAIL="旧的Email地址"
CORRECT_NAME="正确的用户名"
CORRECT_EMAIL="正确的邮件地址"
if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags
```

用git log命令看看新 Git 历史有没有错误

把正确历史 push 到 Github

```console
git push --force --tags origin 'refs/heads/*'
```

删掉刚刚临时创建的 clone

```console
cd ..
rm -rf repo.git
```

如何正确设置你的 git 个人信息

```console
git config --global user.email "你的邮件地址"
git config --global user.name "你的Github用户名"
```
