<template>
  <div class="md-body" v-html="rendered" />
</template>

<script setup lang="ts">
import { computed, watch, onMounted, onUnmounted } from "vue";
import MarkdownIt from "markdown-it";
import hljs from "highlight.js";

// 预加载主题 CSS（vite ?inline 返回字符串，不自动注入 DOM）
import atomOneDark from "highlight.js/styles/atom-one-dark.css?inline";
import githubDark from "highlight.js/styles/github-dark.css?inline";
import monokai from "highlight.js/styles/monokai.css?inline";
import github from "highlight.js/styles/github.css?inline";

const THEME_MAP: Record<string, string> = {
  "atom-one-dark": atomOneDark,
  "github-dark": githubDark,
  monokai,
  github,
};

const THEME_NAMES = { "atom-one-dark": "Atom One Dark", "github-dark": "GitHub Dark", monokai: "Monokai", github: "GitHub Light" };

const md: MarkdownIt = new MarkdownIt({
  breaks: true,
  linkify: true,
  highlight(str: string, lang: string): string {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return `<pre class="hljs"><code>${hljs.highlight(str, { language: lang, ignoreIllegals: true }).value}</code></pre>`;
      } catch { /* fall through */ }
    }
    return `<pre class="hljs"><code>${md.utils.escapeHtml(str)}</code></pre>`;
  },
});

const props = withDefaults(
  defineProps<{ content: string; final?: boolean; theme?: string }>(),
  { final: true, theme: "atom-one-dark" },
);

const rendered = computed(() => md.render(props.content));

// 动态切换 highlight.js 主题
let styleEl: HTMLStyleElement | null = null;

function applyTheme(name: string) {
  const css = THEME_MAP[name] || THEME_MAP["atom-one-dark"];
  if (!styleEl) {
    styleEl = document.createElement("style");
    styleEl.id = "hljs-theme";
    document.head.appendChild(styleEl);
  }
  styleEl.textContent = css;
}

onMounted(() => applyTheme(props.theme));

watch(() => props.theme, applyTheme);

onUnmounted(() => {
  if (styleEl) { styleEl.remove(); styleEl = null; }
});

defineExpose({ THEME_MAP, THEME_NAMES });
</script>

<style scoped>
.md-body :deep(p) { margin: 0 0 8px; line-height: 1.65; }
.md-body :deep(p:last-child) { margin-bottom: 0; }

/* 内联代码 */
.md-body :deep(code) {
  font-size: 12px;
  background: var(--el-fill-color-dark);
  color: var(--el-color-danger-light-3);
  padding: 2px 6px;
  border-radius: 4px;
}

/* 代码块容器 */
.md-body :deep(pre) {
  margin: 10px 0;
  border-radius: 8px;
  overflow-x: auto;
  position: relative;
}
.md-body :deep(pre code) {
  background: none;
  padding: 0;
  font-size: 12.5px;
  line-height: 1.6;
  color: inherit;
}

/* highlight.js 代码块 */
.md-body :deep(pre.hljs) {
  background: #282c34;
  border: 1px solid #3e4452;
  padding: 14px 16px;
}

/* 语言标签 */
.md-body :deep(pre[class*="language-"])::before {
  content: attr(data-lang);
  position: absolute;
  top: 0;
  right: 0;
  font-size: 11px;
  color: #abb2bf;
  background: #21252b;
  padding: 2px 10px;
  border-radius: 0 8px 0 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.md-body :deep(ul),
.md-body :deep(ol) { padding-left: 20px; margin: 4px 0 8px; }
.md-body :deep(li) { margin-bottom: 2px; }
.md-body :deep(blockquote) {
  border-left: 3px solid var(--el-color-primary-light-5);
  padding-left: 12px;
  margin: 8px 0;
  color: var(--el-text-color-secondary);
}
.md-body :deep(a) {
  color: var(--el-color-primary);
  text-decoration: underline;
}
.md-body :deep(table) {
  border-collapse: collapse;
  margin: 8px 0;
  width: 100%;
}
.md-body :deep(th),
.md-body :deep(td) {
  border: 1px solid var(--el-border-color);
  padding: 6px 10px;
  text-align: left;
  font-size: 12px;
}
.md-body :deep(th) { background: var(--el-fill-color); font-weight: 600; }
.md-body :deep(hr) {
  border: none;
  border-top: 1px solid var(--el-border-color-light);
  margin: 12px 0;
}
.md-body :deep(img) { max-width: 100%; border-radius: 6px; }
</style>
