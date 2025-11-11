import DefaultTheme from 'vitepress/theme'
import ArticleMetadata from './components/ArticleMetadata.vue'
import PageViews from './components/PageViews.vue'
import './custom.css'
import { onMounted, h } from 'vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('ArticleMetadata', ArticleMetadata)
    app.component('PageViews', PageViews)
  },
  setup() {
    onMounted(() => {
      // Load busuanzi script for page view counter
      const script = document.createElement('script')
      script.async = true
      script.src = '//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js'
      document.body.appendChild(script)
    })
  },
  Layout() {
    return h(DefaultTheme.Layout, null, {
      'doc-after': () => h(PageViews)
    })
  }
}
