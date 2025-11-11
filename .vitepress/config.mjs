import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "小码奔腾",
  description: "记录一些和自动化测试、CI有关的想法",
  lang: 'zh-CN',
  
  // 站点根路径（GitHub Pages）
  base: '/',
  
  // 最后更新时间
  lastUpdated: true,
  
  // 清理 URL
  cleanUrls: true,
  
  // Head 配置
  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }],
    ['meta', { name: 'author', content: 'python012' }],
    ['meta', { name: 'keywords', content: '自动化测试,Python,CI,Jenkins,Java' }]
  ],
  
  // 主题配置
  themeConfig: {
    // 导航栏
    nav: [
      { text: '首页', link: '/' },
      { text: '归档', link: '/archives' },
      { text: '标签', link: '/tags' },
      { text: '关于', link: '/about' }
    ],

    // 侧边栏
    sidebar: [
      {
        text: '最近文章',
        items: [
          // 将会动态生成
        ]
      }
    ],

    // 社交链接
    socialLinks: [
      { icon: 'github', link: 'https://github.com/python012' }
    ],

    // 页脚
    footer: {
      message: '基于 VitePress 构建',
      copyright: 'Copyright © 2016-2025 python012'
    },

    // 搜索
    search: {
      provider: 'local'
    },

    // 文档页脚
    docFooter: {
      prev: '上一篇',
      next: '下一篇'
    },

    // 大纲
    outline: {
      label: '目录',
      level: [2, 3]
    },

    // 最后更新时间文本
    lastUpdated: {
      text: '最后更新于',
      formatOptions: {
        dateStyle: 'full',
        timeStyle: 'short'
      }
    }
  },

  // Markdown 配置
  markdown: {
    lineNumbers: true,
    theme: {
      light: 'github-light',
      dark: 'github-dark'
    }
  }
})
