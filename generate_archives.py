"""
生成文章列表和归档页面
"""

import os
from pathlib import Path
import re

def parse_frontmatter(md_file):
    """解析 Markdown 文件的 frontmatter"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None
    
    frontmatter = {}
    current_key = None
    
    for line in match.group(1).split('\n'):
        line = line.rstrip()
        
        # 检查是否是列表项
        if line.startswith('  - '):
            if current_key == 'tags':
                tag = line.strip('  -').strip()
                if tag:
                    frontmatter['tags'].append(tag)
        elif ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            if key == 'tags':
                frontmatter['tags'] = []
                current_key = 'tags'
            elif key == 'title':
                # 移除引号
                value = value.strip('"').strip("'")
                frontmatter[key] = value
                current_key = key
            else:
                frontmatter[key] = value
                current_key = key
    
    return frontmatter

def collect_articles(base_dir):
    """收集所有文章信息"""
    articles = []
    base_path = Path(base_dir)
    
    for year_dir in ['2016', '2017', '2018', '2025']:
        year_path = base_path / year_dir
        if not year_path.exists():
            continue
        
        for md_file in year_path.rglob('*.md'):
            try:
                frontmatter = parse_frontmatter(md_file)
                if frontmatter and 'title' in frontmatter:
                    # 构建相对路径
                    rel_path = md_file.relative_to(base_path)
                    url_path = '/' + str(rel_path).replace('\\', '/').replace('.md', '')
                    
                    articles.append({
                        'title': frontmatter.get('title', ''),
                        'date': frontmatter.get('date', ''),
                        'tags': frontmatter.get('tags', []),
                        'path': url_path,
                        'year': year_dir,
                        'file': md_file
                    })
            except Exception as e:
                print(f"处理文件出错 {md_file}: {e}")
    
    # 按日期排序（最新在前）
    articles.sort(key=lambda x: x['date'], reverse=True)
    return articles

def generate_archives_page(articles, output_file):
    """生成归档页面"""
    content = """# 文章归档

## 📚 全部文章

"""
    
    # 按年份分组
    articles_by_year = {}
    for article in articles:
        year = article['year']
        if year not in articles_by_year:
            articles_by_year[year] = []
        articles_by_year[year].append(article)
    
    # 生成内容
    for year in sorted(articles_by_year.keys(), reverse=True):
        content += f"\n### {year}年\n\n"
        for article in articles_by_year[year]:
            date = article['date']
            title = article['title']
            path = article['path']
            content += f"- **{date}** - [{title}]({path})\n"
    
    content += f"\n\n---\n\n> 共 {len(articles)} 篇文章\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ 已生成归档页面: {output_file}")

def generate_tags_page(articles, output_file):
    """生成标签页面"""
    # 收集所有标签
    tags_dict = {}
    for article in articles:
        for tag in article['tags']:
            if tag not in tags_dict:
                tags_dict[tag] = []
            tags_dict[tag].append(article)
    
    content = """# 标签

## 🏷️ 所有标签

"""
    
    # 按标签字母顺序排序
    for tag in sorted(tags_dict.keys()):
        articles_with_tag = tags_dict[tag]
        # 创建锚点 ID（转小写，去除空格）
        tag_id = tag.lower().replace(' ', '-')
        content += f"\n### <span id=\"{tag_id}\">{tag}</span> ({len(articles_with_tag)})\n\n"
        for article in articles_with_tag:
            content += f"- [{article['title']}]({article['path']}) - {article['date']}\n"
    
    content += f"\n\n---\n\n> 共 {len(tags_dict)} 个标签\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ 已生成标签页面: {output_file}")

def generate_index_recent_posts(articles, output_file):
    """更新首页的最近文章"""
    # 读取现有首页
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 生成最近文章列表（前10篇）
    recent_posts = "\n## 📝 最近更新\n\n"
    for article in articles[:10]:
        recent_posts += f"- **{article['date']}** - [{article['title']}]({article['path']})\n"
    
    recent_posts += f"\n[查看全部 {len(articles)} 篇文章 →](/archives)\n"
    
    # 替换内容
    new_content = re.sub(
        r'## 最近更新.*?(?=##|$)', 
        recent_posts + '\n',
        content,
        flags=re.DOTALL
    )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ 已更新首页: {output_file}")

def main():
    print("=" * 60)
    print("生成文章列表和归档页面")
    print("=" * 60)
    print()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 收集文章
    print("正在收集文章信息...")
    articles = collect_articles(base_dir)
    print(f"找到 {len(articles)} 篇文章")
    print()
    
    # 生成归档页面
    generate_archives_page(articles, os.path.join(base_dir, 'archives.md'))
    
    # 生成标签页面
    generate_tags_page(articles, os.path.join(base_dir, 'tags.md'))
    
    # 更新首页
    generate_index_recent_posts(articles, os.path.join(base_dir, 'index.md'))
    
    print()
    print("=" * 60)
    print("完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
