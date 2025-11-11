---
title: "使用Git制作patch文件"
date: 2018-05-27
tags:
  - Git
description: "项目中是用Review board来做code review，用Git来管理代码，所以每次提交之前，需要把修改的代码做成patch文件，上传到Review board里去，再发给相关同事检查。 这里简单记录下制作patch文件的过程。 假设大家一直工作在master分支上，现在当前目录下的repo已经git pull到最新，同时需要提交的代码已经完成，检查git status。 123456789"
---

# 使用Git制作patch文件

<div class="article-meta">
  <span class="date">📅 发布于：2018年05月27日</span>
  <span class="tags">🏷️ 标签：<span class="tag">Git</span></span>
</div>

项目中是用[Review board]来做code review，用Git来管理代码，所以每次提交之前，需要把修改的代码做成patch文件，上传到Review board里去，再发给相关同事检查。

这里简单记录下制作patch文件的过程。

假设大家一直工作在master分支上，现在当前目录下的repo已经`git pull`到最新，同时需要提交的代码已经完成，检查`git status`。

```text
rx:pytest_proj reed$ git status
On branch master
Your branch is up-to-date with'origin/master'.
Untracked files:
(use"git add <file>..."to includeinwhat will be committed)

change.txt

nothing added to commit but untracked files present (use"git add"to track)

```

执行`git branch patch`生成一个名为patch的分支，再`git checkout patch`切换到patch分支。

在patch分支上`git add .`，继续`git commit`，完成commit后再执行`git format-patch -M master`生成patch文件，其含义是将当前分支上的，所有的，更加新的提交（和master分支相比）打包成patch文件，然后可见当前目录下会生成一个`.patch`文件。

然后这个patch文件即可上交了，最后需要把当前repo拆回原状，注意当前分支还是patch分支，需要先`get reset --soft 上次commit的hash`，再继续`git reset HEAD .`，最后切回最开始工作的master分支即可。