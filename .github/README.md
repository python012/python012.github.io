# 小码奔腾 (Python012's Blog)

[![Blog Status](https://img.shields.io/badge/status-archived-yellow.svg)](https://python012.github.io)
[![Last Update](https://img.shields.io/badge/last%20update-2018--08--21-blue.svg)](https://github.com/python012/python012.github.io)
[![Hexo](https://img.shields.io/badge/hexo-v3.x-blue.svg)](https://hexo.io)
[![NexT Theme](https://img.shields.io/badge/theme-NexT%20v5.1.4-orange.svg)](https://github.com/theme-next/hexo-theme-next)

## 📖 项目简介

这是一个基于 **Hexo** 静态网站生成器创建的个人技术博客，主题为 **NexT v5.1.4**（Muse 风格）。博客专注于自动化测试、Python、Java、CI/CD 等技术领域的内容分享。

**⚠️ 重要提示：** 当前仓库存储的是 Hexo 生成后的静态网站文件（public 文件夹内容），并非源代码。如需继续更新博客，需要找到原始的 Hexo 源码项目。

## 🏗️ 项目结构

```
python012.github.io/
├── 2016/                    # 2016年博客文章
├── 2017/                    # 2017年博客文章
├── 2018/                    # 2018年博客文章（最后更新）
├── archives/                # 归档页面
├── tags/                    # 标签页面
│   ├── python/
│   ├── Java/
│   ├── Jenkins/
│   ├── Docker/
│   ├── Django/
│   └── ...
├── css/                     # 样式文件
├── js/                      # JavaScript 文件
├── lib/                     # 第三方库
│   ├── jquery/             # jQuery 2.1.3
│   ├── font-awesome/       # Font Awesome 4.6.2
│   ├── fancybox/
│   └── ...
├── images/                  # 图片资源
├── fancybox/               # 图片灯箱插件
└── index.html              # 首页

```

## 🛠️ 技术栈

### 核心框架
- **Hexo**: v3.x（静态网站生成器）
- **NexT Theme**: v5.1.4（主题）
- **Node.js**: 需要 Node.js 环境来运行 Hexo

### 前端依赖
- **jQuery**: v2.1.3
- **Font Awesome**: v4.6.2
- **Fancybox**: v2.1.5（图片灯箱效果）
- **Canvas Nest/Canvas Ribbon**: 背景动画效果
- **Velocity.js**: 动画库

### 博客主题配置
- 主题方案：Muse
- 侧边栏位置：左侧
- 支持的功能：
  - 文章归档
  - 标签分类
  - Fancybox 图片查看
  - 响应式设计
  - SEO 优化

## 📝 博客内容主题

根据标签分类，博客涵盖以下技术领域：

- **自动化测试**: Selenium, pytest, unittest, TestNG, Junit4
- **编程语言**: Python, Java
- **测试框架**: Django-Rest-Framework, Mockito
- **CI/CD**: Jenkins, DevOps
- **容器技术**: Docker
- **版本控制**: Git
- **Linux**: Shell, Xvfb
- **其他**: virtualenv, Maven, Json

## 🚀 如何继续使用这个博客

### 方案一：找回 Hexo 源码（推荐）

1. **寻找源码仓库**
   - 检查你的本地计算机是否还保留有 Hexo 源码目录
   - 通常源码目录包含：
     ```
     source/           # Markdown 文章源文件
     themes/           # 主题文件
     _config.yml       # Hexo 配置文件
     package.json      # Node.js 依赖
     ```
   - 可能的位置：`~/blog/`, `~/hexo-blog/`, 或其他自定义目录

2. **如果找到源码，继续写作**
   ```bash
   # 进入源码目录
   cd <hexo-source-directory>
   
   # 安装依赖
   npm install
   
   # 创建新文章
   hexo new "My New Post"
   
   # 本地预览
   hexo server
   
   # 生成并部署
   hexo clean
   hexo generate
   hexo deploy
   ```

### 方案二：重建 Hexo 项目

如果找不到源码，可以重新搭建 Hexo 环境：

1. **安装 Hexo**
   ```bash
   npm install -g hexo-cli
   ```

2. **创建新博客**
   ```bash
   hexo init my-blog
   cd my-blog
   npm install
   ```

3. **安装 NexT 主题**
   ```bash
   # NexT v5.1.4 已经较老，建议使用最新版本
   git clone https://github.com/theme-next/hexo-theme-next themes/next
   ```

4. **配置 _config.yml**
   ```yaml
   # 站点配置
   title: 小码奔腾
   subtitle: 记录一些和自动化测试、CI有关的想法
   author: python012
   language: zh
   timezone: Asia/Shanghai
   
   # URL
   url: https://python012.github.io
   
   # 主题
   theme: next
   
   # 部署
   deploy:
     type: git
     repo: https://github.com/python012/python012.github.io.git
     branch: master
   ```

5. **迁移旧文章**
   - 如果你有旧文章的备份（Markdown 文件），将它们复制到 `source/_posts/` 目录
   - 如果没有，可以从当前静态网站的 HTML 中提取内容（较为繁琐）

## ⚠️ 当前项目状态评估

### ✅ 优点
1. **网站仍然可访问**：静态文件完整，可以正常浏览
2. **结构清晰**：文件组织良好，易于维护
3. **内容有价值**：技术文章具有参考价值

### ❌ 存在的问题

1. **缺少源码**：只有编译后的静态文件，无法直接编辑文章
2. **技术栈过时**：
   - jQuery 2.1.3（2014年发布）→ 当前最新 3.7.x
   - Font Awesome 4.6.2（2016年）→ 当前最新 6.x
   - Hexo 3.x → 当前最新 7.x
   - NexT 5.1.4 → 当前最新 8.x
   
3. **安全隐患**：旧版本库可能存在已知的安全漏洞

4. **最后更新时间**：2018年8月21日（已经超过7年未更新）

### 🔄 是否需要更新

#### 如果只是展示现有内容
- **不需要更新**：静态网站可以继续使用，浏览器仍能正常渲染
- **优点**：零成本维护
- **缺点**：无法添加新文章，存在安全风险

#### 如果要继续写博客
- **强烈建议更新**：
  1. 使用最新版本的 Hexo（v7.x）
  2. 升级 NexT 主题到 v8.x
  3. 更新所有前端依赖库
  4. 考虑使用 GitHub Actions 自动化部署

#### 现代化替代方案

如果想完全重构，可以考虑：

1. **Hugo**：比 Hexo 更快的静态网站生成器（Go 语言编写）
2. **VitePress**：基于 Vite 的静态网站生成器（Vue 生态）
3. **Docusaurus**：Facebook 开源的文档网站生成器（React 生态）
4. **Astro**：现代化的静态网站框架

## 📋 迁移检查清单

如果决定继续使用此博客，建议按以下步骤操作：

- [ ] 寻找原始 Hexo 源码
- [ ] 备份当前静态网站
- [ ] 安装 Node.js LTS 版本
- [ ] 安装最新版 Hexo CLI
- [ ] 创建新的 Hexo 项目
- [ ] 安装并配置 NexT 主题
- [ ] 迁移旧文章（如果有源文件）
- [ ] 更新站点配置
- [ ] 测试本地运行
- [ ] 配置 GitHub Actions 自动部署
- [ ] 推送到 GitHub

## 🔗 相关链接

- **博客地址**: https://python012.github.io
- **GitHub 仓库**: https://github.com/python012/python012.github.io
- **Hexo 官方文档**: https://hexo.io/zh-cn/
- **NexT 主题文档**: https://theme-next.js.org/

## 📄 License

本项目内容遵循原作者的版权声明。

---

**最后更新时间**: 2018-08-21  
**最后提交**: Site updated: 2018-08-21 21:31:53

