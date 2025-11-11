---
title: "博客重启：从 Hexo 到 VitePress 的迁移之旅"
date: 2025-11-11
description: "记录7年后重启博客的完整迁移过程，从旧的 Hexo 静态站点迁移到现代化的 VitePress，包括技术选型、迁移步骤和后续维护指南"
tags: ["VitePress", "博客迁移", "GitHub Pages", "CI/CD"]
---

<div class="article-metadata">
  <span class="article-date">📅 2025-11-11</span>
  <span class="article-tags">
    🏷️ <a href="/tags#VitePress">VitePress</a> / 
    <a href="/tags#博客迁移">博客迁移</a> / 
    <a href="/tags#GitHub-Pages">GitHub Pages</a> / 
    <a href="/tags#CI-CD">CI/CD</a>
  </span>
</div>

# 博客重启：从 Hexo 到 VitePress 的迁移之旅

## 背景

时隔7年，重新发现了自己在 GitHub Pages 上的技术博客（最后更新于 2018-08-21）。然而发现原始仓库只保留了编译后的静态 HTML 文件，Hexo 源代码已经遗失。面对这种情况，决定借此机会将博客迁移到更现代化的技术栈。

## 技术选型

### 为什么选择 VitePress？

经过调研，最终选择了 **VitePress 1.6.4** 作为新的静态站点生成器，主要原因：

1. **现代化技术栈**：基于 Vue 3 + Vite，构建速度快，开发体验好
2. **简洁高效**：配置简单，开箱即用
3. **Markdown 友好**：原生支持 Markdown，适合技术写作
4. **主题可定制**：可以轻松扩展默认主题
5. **活跃维护**：VitePress 是 Vue 团队维护的项目，生态活跃

对比旧的 Hexo 3.x：
- Hexo 基于 Node.js 但构建较慢
- VitePress 使用 Vite 构建，速度更快
- VitePress 对 TypeScript 和现代化工具链支持更好

## 迁移过程

### 1. 内容提取与转换

**挑战**：只有编译后的 HTML 文件，需要还原为 Markdown 格式

**解决方案**：
```python
# 使用 BeautifulSoup 解析 HTML 并提取内容
from bs4 import BeautifulSoup

# 提取文章元数据
title = soup.find('h1', class_='post-title').text.strip()
date = soup.find('time', class_='post-time')['datetime'][:10]
tags = [a.text for a in soup.select('.post-tags a')]

# 提取文章正文
content = soup.find('div', class_='post-body')
```

**成果**：成功提取了 33 篇文章及 31 张图片

### 2. VitePress 项目搭建

#### 初始化项目
```bash
npm init
npm add -D vitepress
```

#### 核心配置文件：`.vitepress/config.mjs`
```javascript
export default {
  title: '小码奔腾',
  description: '测试开发、自动化、CI/CD',
  lang: 'zh-CN',
  cleanUrls: true,
  
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '归档', link: '/archives' },
      { text: '标签', link: '/tags' },
      { text: '关于', link: '/about' }
    ],
    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: { buttonText: '搜索文档' },
              modal: { noResultsText: '无法找到相关结果' }
            }
          }
        }
      }
    }
  },
  
  // 处理开发环境中的死链
  ignoreDeadLinks: [
    /^https?:\/\/localhost/,
    'favicon.ico'
  ]
}
```

### 3. 内容格式修复

迁移过程中遇到并解决了多个格式问题：

#### 问题1：YAML Frontmatter 解析错误
```yaml
# 错误：描述中包含冒号但未引号包裹
description: Error: spawn Xvfb ENOENT

# 修复：添加引号
description: "Error: spawn Xvfb ENOENT"
```

**解决脚本**：自动为所有 description 字段添加引号

#### 问题2：代码块中的行号干扰
```markdown
# 问题：从 HTML 提取时带入了行号
1 public class Example {
2     // code
3 }

# 修复：移除行号
public class Example {
    // code
}
```

#### 问题3：文章元数据展示
在每篇文章中添加了元数据展示区块：
```html
<div class="article-metadata">
  <span class="article-date">📅 2025-11-11</span>
  <span class="article-tags">
    🏷️ <a href="/tags#VitePress">VitePress</a>
  </span>
</div>
```

配合自定义 CSS 样式：
```css
.article-metadata {
  margin: 1.5rem 0;
  padding: 1rem;
  background: var(--vp-c-bg-soft);
  border-radius: 8px;
}
```

### 4. 自动化部署配置

#### Git 分支策略
- **vitepress-source**：存放 VitePress 源代码
- **master**：存放编译后的静态文件（GitHub Pages 部署分支）

#### GitHub Actions 工作流

创建 `.github/workflows/deploy.yml`：

```yaml
name: Deploy VitePress to GitHub Pages

on:
  push:
    branches: [vitepress-source]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run docs:build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: .vitepress/dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/deploy-pages@v4
```

#### 配置要点

1. **GitHub Pages 设置**：
   - 进入仓库 Settings → Pages
   - Source 选择 "GitHub Actions"

2. **权限配置**：
   ```yaml
   permissions:
     contents: read
     pages: write
     id-token: write
   ```

3. **避免的坑**：
   - ❌ 不要在 deploy job 中添加 `environment: github-pages`
   - ✅ 直接使用 `actions/deploy-pages@v4` 即可
   - 原因：environment 配置会触发保护规则，导致部署失败

### 5. 辅助工具

#### 归档和标签页生成器：`generate_archives.py`

自动生成归档页面和标签页面的 Python 脚本：

```python
def collect_articles(root_dir):
    """Collect all markdown articles with metadata"""
    articles = []
    for year_dir in ['2016', '2017', '2018', '2025']:
        year_path = os.path.join(root_dir, year_dir)
        if not os.path.exists(year_path):
            continue
        for root, dirs, files in os.walk(year_path):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    metadata = parse_frontmatter(file_path)
                    if metadata:
                        articles.append(metadata)
    return sorted(articles, key=lambda x: x['date'], reverse=True)
```

每次新增文章后运行此脚本，自动更新归档和标签索引。

## 最终成果

### 项目结构
```
python012.github.io/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions 部署配置
├── .vitepress/
│   ├── config.mjs              # VitePress 主配置
│   ├── theme/
│   │   ├── index.js            # 主题扩展
│   │   ├── custom.css          # 自定义样式
│   │   └── components/         # 自定义组件
│   └── dist/                   # 构建输出（自动生成）
├── public/
│   └── images/                 # 图片资源
├── 2016/, 2017/, 2018/, 2025/  # 按年份组织的文章
├── archives.md                 # 归档页面
├── tags.md                     # 标签页面
├── about.md                    # 关于页面
├── generate_archives.py        # 归档生成脚本
└── package.json                # 项目依赖
```

### 统计数据
- ✅ 迁移文章：33 篇
- ✅ 迁移图片：31 张
- ✅ 时间跨度：2016-2018
- ✅ 标签数量：24 个
- ✅ 自动部署：完全自动化

### 在线访问
- 📝 博客地址：https://python012.github.io/
- 💻 源码仓库：https://github.com/python012/python012.github.io

## 后续发布新文章的步骤

### 快速指南（5步完成）

#### 1. 创建文章文件
```bash
# 按日期创建目录和文章
mkdir -p 2025/11/12
code 2025/11/12/my-new-article.md
```

#### 2. 编写文章内容
```markdown
---
title: "文章标题"
date: "2025-11-12"
description: "文章描述"
tags: ["标签1", "标签2"]
---

<div class="article-metadata">
  <span class="article-date">📅 2025-11-12</span>
  <span class="article-tags">
    🏷️ <a href="/tags#标签1">标签1</a> / 
    <a href="/tags#标签2">标签2</a>
  </span>
</div>

# 文章标题

正文内容...
```

#### 3. 更新归档和标签索引
```bash
python generate_archives.py
```

#### 4. 本地预览（可选）
```bash
npm run docs:dev
# 访问 http://localhost:5173/
```

#### 5. 提交并推送
```bash
git add .
git commit -m "新增文章：文章标题"
git push origin vitepress-source
```

**自动部署**：推送后，GitHub Actions 会自动构建并部署，约 2-3 分钟后即可在线访问。

### 图片处理

如果文章包含图片：
```bash
# 将图片放入 public/images/ 目录
cp my-image.png public/images/

# 在 Markdown 中引用
![图片描述](/images/my-image.png)
```

### 本地开发命令

```bash
# 安装依赖（首次或更新依赖时）
npm install

# 启动开发服务器
npm run docs:dev

# 构建生产版本
npm run docs:build

# 预览构建结果
npm run docs:preview
```

## 技术栈总结

### 核心技术
- **VitePress 1.6.4**：静态站点生成器
- **Node.js 20**：运行环境
- **Vue 3**：VitePress 基础框架
- **Vite**：构建工具

### 部署技术
- **GitHub Actions**：CI/CD 自动化
- **GitHub Pages**：静态站点托管
- **Git**：版本控制

### 开发工具
- **Python 3**：内容迁移脚本
- **BeautifulSoup**：HTML 解析
- **Markdown**：内容格式

## 经验总结

### 成功经验

1. **选择现代化工具链**：VitePress 的开发体验和构建速度远超旧的静态站点生成器
2. **自动化优先**：GitHub Actions 实现了推送即部署，无需手动构建
3. **结构化组织**：按年/月/日组织文章，清晰易维护
4. **保留原始数据**：成功恢复了所有文章的发布日期和标签

### 踩过的坑

1. **Environment 配置导致部署失败**
   - 问题：在 workflow 中配置了 `environment: github-pages`
   - 影响：触发了环境保护规则，阻止部署
   - 解决：移除 environment 配置，直接使用 deploy-pages action

2. **死链检查过于严格**
   - 问题：开发环境中的 localhost 链接导致构建失败
   - 解决：配置 `ignoreDeadLinks` 忽略特定链接

3. **YAML 解析错误**
   - 问题：Frontmatter 中的冒号需要引号包裹
   - 解决：编写脚本批量修复所有文章

### 未来优化方向

1. **评论系统**：集成 Giscus 或类似评论系统
2. **访问统计**：添加 Google Analytics 或其他分析工具
3. **搜索优化**：改进本地搜索功能
4. **RSS 订阅**：生成 RSS feed
5. **自定义域名**：配置自定义域名（如果需要）

## 结语

这次博客迁移虽然遇到了一些挑战，但通过现代化的工具链和自动化流程，最终建立了一个更加高效、易维护的博客系统。希望这篇文章能够帮助有类似需求的朋友，也为自己未来的维护提供参考。

技术在不断进步，工具在不断更新，但记录和分享的热情不变。让我们继续在技术的道路上前行！

---

**相关链接**：
- VitePress 官方文档：https://vitepress.dev/
- GitHub Actions 文档：https://docs.github.com/en/actions
- 本博客源码：https://github.com/python012/python012.github.io

---

*本次博客迁移在 GitHub Copilot (Claude 3.5 Sonnet) 协助下完成。*
