# VitePress 快速开始指南

## 📦 当前已完成

✅ 项目结构已创建  
✅ VitePress 配置已完成  
✅ 基础页面已创建  
✅ 测试文章已准备

---

## 🚀 立即执行

### 第 1 步：安装依赖（5分钟）

```cmd
cd D:\dev3\python012.github.io
npm install
```

等待安装完成，你会看到 `node_modules` 目录。

---

### 第 2 步：启动开发服务器（1分钟）

```cmd
npm run docs:dev
```

你会看到类似输出：
```
  vitepress v1.x.x

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

---

### 第 3 步：打开浏览器（1分钟）

访问：http://localhost:5173

你应该看到：
- ✅ 精美的首页
- ✅ 导航栏（首页、归档、标签、关于）
- ✅ 博客介绍和特性卡片
- ✅ GitHub 链接

点击"查看文章" → 应该能看到归档页面  
点击"关于我" → 应该能看到关于页面

---

### 第 4 步：查看测试文章

访问：http://localhost:5173/posts/welcome

你应该看到：
- ✅ 文章标题
- ✅ 代码高亮
- ✅ 提示框样式
- ✅ 侧边目录导航

---

### 第 5 步：测试热更新

1. 保持服务器运行
2. 用记事本打开 `index.md`
3. 修改任何文字
4. 保存
5. 浏览器自动刷新，看到修改！✨

---

## ✅ 如果一切正常

恭喜！VitePress 已经成功运行了！

接下来：
1. 按 `Ctrl+C` 停止服务器
2. 告诉我结果
3. 我会继续帮你：
   - 从 master 分支提取旧文章
   - 批量转换 HTML 到 Markdown
   - 配置自动部署

---

## ❌ 如果遇到问题

### 问题 1：npm install 失败
```cmd
# 清理缓存重试
npm cache clean --force
npm install
```

### 问题 2：端口被占用
```cmd
# 指定其他端口
npm run docs:dev -- --port 5174
```

### 问题 3：Node.js 版本过低
需要 Node.js 16+ 版本
```cmd
node -v
```

---

## 📝 项目结构说明

```
python012.github.io/
├── .vitepress/              # VitePress 配置
│   └── config.mjs          # 主配置文件
├── posts/                   # 博客文章目录
│   └── welcome.md          # 测试文章
├── public/                  # 静态资源（图片等）
├── .github/                 # GitHub 相关配置
├── index.md                 # 首页
├── about.md                 # 关于页面
├── archives.md              # 归档页面
├── tags.md                  # 标签页面
├── package.json             # Node.js 配置
├── .gitignore              # Git 忽略配置
├── MIGRATION_LOG.md        # 迁移日志
└── QUICK_START.md          # 本文件

将会添加：
├── 2016/                    # 2016年文章（从 master 提取）
├── 2017/                    # 2017年文章
└── 2018/                    # 2018年文章
```

---

## 🎯 下一阶段预览

完成测试后，我们将：

1. **提取旧文章**（15分钟）
   - 从 master 分支获取 HTML 文件
   - 运行提取脚本
   - 自动生成 Markdown 文件

2. **迁移图片**（5分钟）
   - 复制图片到 `public/images/`
   - 更新文章中的图片路径

3. **配置自动部署**（10分钟）
   - 创建 GitHub Actions 工作流
   - 推送代码自动构建
   - 自动部署到 GitHub Pages

4. **写迁移总结**（30分钟）
   - 记录迁移过程
   - 分享经验心得
   - 发布到博客

---

**准备好了吗？执行上面的步骤，然后告诉我结果！** 🚀
