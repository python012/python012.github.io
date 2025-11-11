# Hexo 博客恢复操作指南

## 🎯 目标

帮助你快速恢复这个 Hexo 博客的编辑和发布能力。

## 📋 前置准备

### 1. 检查本地是否有源码

在你的电脑上搜索以下文件/文件夹：

```bash
# Windows 搜索
dir /s /b _config.yml 2>nul | findstr hexo
dir /s /b package.json 2>nul | findstr hexo

# 或者在文件资源管理器中搜索
_config.yml
package.json
```

**可能的位置**:
- `C:\Users\你的用户名\blog\`
- `C:\Users\你的用户名\hexo-blog\`
- `C:\Users\你的用户名\Documents\blog\`
- `D:\blog\`
- 桌面
- 其他开发目录

### 2. 源码目录的特征

一个完整的 Hexo 源码目录应该包含：

```
hexo-blog/
├── _config.yml          # 主配置文件 ✓
├── package.json         # Node.js 依赖 ✓
├── scaffolds/           # 文章模板
├── source/              # 源文件目录 ✓✓✓
│   ├── _posts/         # Markdown 文章 ✓✓✓
│   └── about/          # 关于页面
├── themes/              # 主题目录 ✓✓
│   └── next/           # NexT 主题
└── node_modules/       # 依赖包
```

**最重要的是 `source/_posts/` 目录，里面应该有 `.md` 文件！**

## 🔍 情况 A: 找到了源码

恭喜！按照以下步骤操作：

### 步骤 1: 安装 Node.js

1. 下载 Node.js LTS 版本：https://nodejs.org/
2. 安装（一路下一步）
3. 验证安装：
   ```cmd
   node -v
   npm -v
   ```

### 步骤 2: 进入源码目录

```cmd
cd "你的源码目录路径"
# 例如: cd C:\Users\YourName\hexo-blog
```

### 步骤 3: 安装依赖

```cmd
npm install
```

如果遇到错误，尝试：
```cmd
npm install --legacy-peer-deps
```

### 步骤 4: 测试本地运行

```cmd
hexo clean
hexo generate
hexo server
```

然后打开浏览器访问：http://localhost:4000

### 步骤 5: 写新文章

```cmd
# 创建新文章
hexo new "我的新文章"

# 这会在 source/_posts/ 目录下创建 "我的新文章.md"
# 用任何文本编辑器打开它，开始写作！
```

### 步骤 6: 发布

```cmd
# 生成静态文件
hexo clean
hexo generate

# 部署到 GitHub
hexo deploy
```

如果 deploy 失败，检查 `_config.yml` 中的 deploy 配置：

```yaml
deploy:
  type: git
  repo: https://github.com/python012/python012.github.io.git
  branch: master
```

可能需要安装部署插件：
```cmd
npm install hexo-deployer-git --save
```

---

## 🔨 情况 B: 没有找到源码

### 方案 B1: 从零开始重建（推荐）

#### 第1步: 安装环境

1. 安装 Node.js（同上）
2. 安装 Hexo：
   ```cmd
   npm install -g hexo-cli
   ```

#### 第2步: 创建新博客

```cmd
# 创建博客目录
hexo init my-blog
cd my-blog

# 安装依赖
npm install

# 测试
hexo server
```

#### 第3步: 安装 NexT 主题

```cmd
# 方法1: 使用 npm（推荐）
npm install hexo-theme-next

# 方法2: 使用 git
git clone https://github.com/theme-next/hexo-theme-next themes/next
```

#### 第4步: 配置主题

编辑 `_config.yml`（博客根目录）：

```yaml
# 网站设置
title: 小码奔腾
subtitle: 记录一些和自动化测试、CI有关的想法
description: 记录一些和自动化测试、CI有关的想法
keywords: 自动化测试 Python CI Jenkins Java
author: python012
language: zh-CN
timezone: Asia/Shanghai

# URL
url: https://python012.github.io
root: /
permalink: :year/:month/:day/:title/
permalink_defaults:
pretty_urls:
  trailing_index: true
  trailing_html: true

# 主题
theme: next

# 部署
deploy:
  type: git
  repo: https://github.com/python012/python012.github.io.git
  branch: master
```

编辑 `themes/next/_config.yml` 或 `_config.next.yml`（根目录）：

```yaml
# 主题方案
scheme: Muse

# 侧边栏
sidebar:
  position: left
  display: post
```

#### 第5步: 手动迁移旧文章（可选）

如果你想保留旧文章，可以尝试从 HTML 中提取：

1. 打开旧文章的 HTML 文件
2. 找到文章内容部分
3. 复制到新的 Markdown 文件
4. 添加 Front Matter：

```markdown
---
title: 文章标题
date: 2018-05-20 17:37:17
tags:
  - Python
  - 测试
categories:
  - 技术
---

文章内容...
```

#### 第6步: 配置自动部署（GitHub Actions）

创建 `.github/workflows/deploy.yml`：

```yaml
name: Deploy Hexo to GitHub Pages

on:
  push:
    branches:
      - source  # 或你的源码分支名

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          submodules: true
          
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          
      - name: Install Dependencies
        run: |
          npm install
          npm install hexo-cli -g
          
      - name: Build
        run: |
          hexo clean
          hexo generate
          
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
          publish_branch: master
```

**注意**: 这需要你创建一个新的分支（如 `source`）来存放源码，`master` 分支继续存放生成的静态文件。

#### 第7步: 调整仓库结构

```bash
# 克隆现有仓库
git clone https://github.com/python012/python012.github.io.git
cd python012.github.io

# 创建新分支保存源码
git checkout -b source

# 删除所有旧的静态文件（保留 .git）
# 注意：在删除前请确保已备份！
del /s /q 2016 2017 2018 archives css fancybox images js lib page tags index.html

# 复制新的 Hexo 源码到这个目录
# （从 my-blog 目录复制所有文件）

# 提交源码
git add .
git commit -m "Add Hexo source files"
git push origin source

# 设置 source 为默认分支（在 GitHub 网页上操作）
```

---

### 方案 B2: 使用工具从 HTML 提取内容

如果你想保留所有旧文章，可以使用工具：

```bash
# 安装 html-to-markdown 工具
npm install -g html-to-markdown

# 或使用 Python 工具
pip install html2text
```

然后批量转换旧文章：

```python
# convert_html.py
import os
import html2text
from bs4 import BeautifulSoup

h = html2text.HTML2Text()
h.ignore_links = False

# 遍历所有 HTML 文件
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html') and 'index' in file:
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()
                soup = BeautifulSoup(html, 'html.parser')
                
                # 提取标题和内容
                title = soup.find('title')
                content = soup.find('div', class_='post-body')
                
                if content:
                    markdown = h.handle(str(content))
                    # 保存为 .md 文件
                    print(f"Converted: {filepath}")
```

---

## 🚀 快速开始模板

如果你想快速开始，使用以下命令序列：

```cmd
:: 1. 创建博客
hexo init my-blog
cd my-blog
npm install

:: 2. 安装主题
npm install hexo-theme-next

:: 3. 安装部署插件
npm install hexo-deployer-git --save

:: 4. 创建配置文件
echo theme: next >> _config.yml

:: 5. 创建第一篇文章
hexo new "Hello World"

:: 6. 启动本地服务器
hexo server
```

---

## 📝 日常使用流程

### 写文章
```cmd
# 1. 创建新文章
hexo new "文章标题"

# 2. 编辑文章
# 打开 source/_posts/文章标题.md

# 3. 本地预览
hexo server

# 4. 发布
hexo clean
hexo generate
hexo deploy
```

### 常用命令

```cmd
# 创建新文章
hexo new "My New Post"
hexo new "My New Post" -p custom-path/my-post

# 创建草稿
hexo new draft "My Draft"

# 发布草稿
hexo publish draft "My Draft"

# 清理缓存
hexo clean

# 生成静态文件
hexo generate
hexo g  # 简写

# 启动本地服务器
hexo server
hexo s  # 简写
hexo s -p 5000  # 指定端口

# 部署
hexo deploy
hexo d  # 简写

# 一键生成并部署
hexo g -d
```

---

## 🔧 常见问题

### Q1: hexo 命令找不到
```cmd
# 全局安装 hexo-cli
npm install -g hexo-cli
```

### Q2: 部署失败，显示权限错误
```cmd
# 配置 Git 凭据
git config --global user.name "your-username"
git config --global user.email "your-email@example.com"

# 使用 SSH 而不是 HTTPS
# 修改 _config.yml 中的 repo 为 SSH 格式
repo: git@github.com:python012/python012.github.io.git
```

### Q3: npm install 很慢
```cmd
# 使用淘宝镜像
npm config set registry https://registry.npmmirror.com
npm install
```

### Q4: 主题显示不正常
```cmd
# 清理缓存并重新生成
hexo clean
hexo g
hexo s
```

### Q5: 旧文章日期如何保持？
在 Markdown 文件的 Front Matter 中指定：
```markdown
---
title: 旧文章标题
date: 2018-05-20 17:37:17  # 保持原始日期
---
```

---

## 📚 进阶功能

### 添加评论系统（Giscus）

1. 安装：参考 [Giscus 文档](https://giscus.app/)
2. 配置 `_config.next.yml`:
```yaml
comments:
  active: giscus
  
giscus:
  enable: true
  repo: python012/python012.github.io
  repo_id: your-repo-id
  category: Announcements
  category_id: your-category-id
```

### 添加搜索功能

```cmd
npm install hexo-generator-searchdb --save
```

配置 `_config.yml`:
```yaml
search:
  path: search.xml
  field: post
  content: true
```

### 添加站点统计

使用 Google Analytics 或 百度统计，在主题配置中添加：
```yaml
google_analytics: UA-XXXXXXXXX-X
```

---

## 🎓 学习资源

- **Hexo 官方文档**: https://hexo.io/zh-cn/docs/
- **NexT 主题文档**: https://theme-next.js.org/
- **Markdown 语法**: https://markdown.com.cn/
- **GitHub Pages 文档**: https://docs.github.com/pages

---

## 💾 备份建议

### 方法 1: Git 双分支
- `source` 分支：存放 Hexo 源码
- `master` 分支：存放生成的静态文件

### 方法 2: 定期导出
```cmd
# 导出所有 Markdown 文件
xcopy source\_posts\*.md backup\ /s /y

# 打包整个博客
tar -czf hexo-backup-%date:~0,10%.tar.gz *
```

### 方法 3: 云同步
将源码目录同步到：
- OneDrive
- Google Drive
- Dropbox

---

**祝你博客恢复顺利！有问题随时参考文档或在 GitHub 上提 Issue。**

