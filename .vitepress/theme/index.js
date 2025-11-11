import DefaultTheme from 'vitepress/theme'
import ArticleMetadata from './components/ArticleMetadata.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('ArticleMetadata', ArticleMetadata)
  }
}
