<script setup>
import { useData } from 'vitepress'
import DefaultTheme from 'vitepress/theme'

const { frontmatter } = useData()
</script>

<template>
  <div class="article-metadata">
    <div v-if="frontmatter.date" class="publish-date">
      <span class="icon">📅</span>
      <time :datetime="frontmatter.date">{{ formatDate(frontmatter.date) }}</time>
    </div>
    <div v-if="frontmatter.tags && frontmatter.tags.length" class="tags">
      <span class="icon">🏷️</span>
      <span v-for="tag in frontmatter.tags" :key="tag" class="tag">{{ tag }}</span>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    formatDate(date) {
      const d = new Date(date)
      const year = d.getFullYear()
      const month = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      return `${year}年${month}月${day}日`
    }
  }
}
</script>

<style scoped>
.article-metadata {
  margin: 1rem 0 2rem;
  padding: 1rem;
  background-color: var(--vp-c-bg-soft);
  border-radius: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  font-size: 0.9rem;
}

.publish-date,
.tags {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.icon {
  font-size: 1rem;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  padding: 0.2rem 0.6rem;
  background-color: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-dark);
  border-radius: 4px;
  font-size: 0.85rem;
}
</style>
