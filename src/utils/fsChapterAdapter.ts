/**
 * 文件系统章节适配器
 *
 * 将 FSChapter（后端文件系统格式）转换为 Chapter（前端已有格式），
 * 使 WorkDetailView 中 50+ 处 chapter.id 引用无需修改。
 */
import type { FSChapter } from '../types/novel';
import type { Chapter } from '../types';

/**
 * 将 FSChapter 转换为前端 Chapter 格式
 * 生成合成 ID "fs-{num}"，兼容已有的 chapter.id 引用
 */
export function fsToChapter(fs: FSChapter, workId: string): Chapter {
  const now = new Date().toISOString();
  return {
    id: `fs-${fs.num}`,
    workId,
    title: fs.title,
    content: fs.content || '',
    wordCount: fs.wordCount,
    viewCount: 0,
    isPublished: fs.status === 'published',
    order: fs.num,
    publishedAt: null,
    createdAt: now,
    updatedAt: now,
    status: fs.status,
  };
}

/**
 * 从合成 ID 提取章节序号
 * "fs-3" → 3，无效 ID 返回 null
 */
export function chapterIdToNum(id: string): number | null {
  const match = id.match(/^fs-(\d+)$/);
  if (!match) return null;
  return parseInt(match[1], 10);
}

// ─── doc: ID 辅助函数 ───

export function isDocId(id: string): boolean {
  return id.startsWith('doc:');
}

export function docIdToPath(id: string): string {
  const raw = id.slice(4);
  // Agent 路径可能带前导斜杠（如 doc:/knowledge/...），需去除以避免 URL 双斜杠
  return raw.startsWith('/') ? raw.slice(1) : raw;
}

export function pathToDocId(path: string): string {
  const normalized = path.startsWith('/') ? path.slice(1) : path;
  return `doc:${normalized}`;
}

/**
 * 前端防御：清除正文中意外残留的 YAML frontmatter 元数据。
 *
 * 处理以下情况：
 * 1. 带 --- 分隔符的完整 frontmatter
 * 2. Milkdown 损坏的 frontmatter：编辑器将 --- 转为 ***、___、--------- 等
 *    thematic break，导致 frontmatter 无法被正常解析
 * 3. 不带前导分隔符的 YAML 元数据 + 关闭分隔符
 * 4. 不带分隔符的裸 YAML 元数据（同时包含 status: 和 title:）
 *
 * 通常后端已处理，此函数作为前端最后的安全网。
 */
export function stripLeakedFrontmatter(content: string): string {
  let text = content;
  // eslint-disable-next-line no-constant-condition
  while (true) {
    const stripped = text.replace(/^\n+/, '');

    // 情况 1：完整 frontmatter（---\n...\n---）
    const fmMatch = stripped.match(/^---\n([\s\S]*?)\n---\n*/);
    if (fmMatch) {
      const meta = fmMatch[1];
      if (/(?:^|\n)\s*(?:title|status)\s*:/.test(meta)) {
        text = stripped.slice(fmMatch[0].length);
        continue;
      }
    }

    // 情况 2：Milkdown 损坏的 frontmatter
    // 编辑器将 --- 转换为 ***、___、--------- 等 Markdown thematic break
    // 模式：thematic_break \n+ YAML行 \n thematic_break（可选）
    const corruptedMatch = stripped.match(
      /^[*_-]{3,}[ \t]*\n+((?:(?:title|status):[^\n]*\n)+)(?:[*_-]{3,}[ \t]*\n?)?/
    );
    if (corruptedMatch) {
      const yamlText = corruptedMatch[1];
      const hasTitle = /title\s*:/.test(yamlText);
      const hasKnownStatus = /status\s*:\s*(?:draft|completed|published|archived)/.test(yamlText);
      if (hasTitle || hasKnownStatus) {
        text = stripped.slice(corruptedMatch[0].length).replace(/^\n+/, '');
        continue;
      }
    }

    // 情况 3：YAML 行 + 关闭分隔符（无开头分隔符）
    const fmMatch2 = stripped.match(
      /^((?:(?:title|status):[^\n]*\n)+)[*_-]{3,}[ \t]*\n?/
    );
    if (fmMatch2) {
      text = stripped.slice(fmMatch2[0].length).replace(/^\n+/, '');
      continue;
    }

    // 情况 4：裸 YAML 残留（status: draft\ntitle: xxx，无任何分隔符包裹）
    // 必须同时包含 title: 和已知 status 值才视为残留
    const bareMatch = stripped.match(
      /^((?:(?:title|status):[^\n]*\n?)+)/
    );
    if (bareMatch) {
      const matched = bareMatch[1];
      const hasTitle = /title\s*:/.test(matched);
      const hasKnownStatus = /status\s*:\s*(?:draft|completed|published|archived)\s*(?:\n|$)/.test(matched);
      if (hasTitle && hasKnownStatus) {
        text = stripped.slice(bareMatch[0].length).replace(/^\n+/, '');
        continue;
      }
    }

    break;
  }
  return text;
}
