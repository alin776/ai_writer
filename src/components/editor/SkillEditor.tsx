/**
 * SkillEditor — Markdown 渲染组件（只读）
 *
 * 用 react-markdown + react-syntax-highlighter 实现 Typora 风格的渲染效果：
 * - 代码块：语言标签 + 复制按钮 + 语法高亮（含无语言标记的代码块）
 * - 标题 / 列表 / 引用 / 分割线等完整 GFM 支持
 * - 深浅模式自动切换
 */
import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark, oneLight } from 'react-syntax-highlighter/dist/esm/styles/prism';
import remarkGfm from 'remark-gfm';
import remarkBreaks from 'remark-breaks';
import { Copy, Check } from 'lucide-react';

interface SkillEditorProps {
  content: string;
  placeholder?: string;
  onChange?: (md: string) => void;
}

/* ── 暗色模式检测 hook ────────────────────────────────────────────────── */
function useDarkMode() {
  const [dark, setDark] = useState(() =>
    document.documentElement.classList.contains('dark'),
  );
  useEffect(() => {
    const check = () => setDark(document.documentElement.classList.contains('dark'));
    const obs = new MutationObserver(check);
    obs.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
    return () => obs.disconnect();
  }, []);
  return dark;
}

/* ── CodeBlock 头部：语言标签 + 复制按钮 ──────────────────────────────── */
function CodeBlockHeader({ language, code }: { language: string; code: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 1800);
  };

  return (
    <div className="flex items-center justify-between px-4 py-1.5
                    bg-gray-100 dark:bg-[#2a2a3c] border-b border-gray-200 dark:border-gray-700/60">
      <span className="text-[11px] font-medium tracking-wide text-gray-500 dark:text-gray-400 uppercase select-none">
        {language}
      </span>
      <button
        onClick={handleCopy}
        className="flex items-center gap-1 text-[11px] text-gray-400 dark:text-gray-500
                   hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
      >
        {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
      </button>
    </div>
  );
}

/* ── 块级代码块渲染 ───────────────────────────────────────────────────── */
function CodeBlock({ language, code, isDark }: { language: string; code: string; isDark: boolean }) {
  return (
    <div className="skill-codeblock-wrapper my-4 rounded-xl overflow-hidden
                    border border-gray-200 dark:border-gray-700/60">
      <CodeBlockHeader language={language} code={code} />
      <SyntaxHighlighter
        style={isDark ? oneDark : oneLight}
        language={language}
        PreTag="div"
        customStyle={{
          margin: 0,
          borderRadius: 0,
          padding: '16px 20px',
          fontSize: '13px',
          lineHeight: '1.7',
          background: isDark ? '#1e1e2e' : '#fafafa',
        }}
        codeTagProps={{ style: { background: 'transparent' } }}
      >
        {code}
      </SyntaxHighlighter>
    </div>
  );
}

/* ── 主组件 ───────────────────────────────────────────────────────────── */
export default function SkillEditor({ content, placeholder }: SkillEditorProps) {
  const isDark = useDarkMode();

  if (!content) {
    return (
      <div className="h-full flex items-center justify-center text-sm text-gray-400 dark:text-gray-600">
        {placeholder || '在此编写技能文档…'}
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto bg-white dark:bg-gray-950">
      <article className="skill-md-body px-8 py-6 max-w-none">
        <ReactMarkdown
          remarkPlugins={[remarkGfm, remarkBreaks]}
          components={{
            /* ── pre: 统一处理所有块级代码 ─────────────────────────── */
            pre({ children, ...props }: any) {
              // 从 <pre><code class="language-xxx">...</code></pre> 结构中提取信息
              const child = React.Children.toArray(children)[0];
              if (React.isValidElement(child)) {
                const { className, children: codeChildren } = child.props as any;
                const match = /language-(\w+)/.exec(className || '');
                const lang = match?.[1] || 'text';
                const codeStr = String(codeChildren).replace(/\n$/, '');
                return <CodeBlock language={lang} code={codeStr} isDark={isDark} />;
              }
              // fallback: 原生 pre
              return <pre className="whitespace-pre-wrap text-sm text-gray-700 dark:text-gray-300 my-4" {...props}>{children}</pre>;
            },

            /* ── code: 只处理行内代码 ─────────────────────────────── */
            code({ children, ...props }: any) {
              return (
                <code
                  className="bg-gray-100 dark:bg-slate-800 text-gray-700 dark:text-gray-200
                             px-1.5 py-0.5 rounded text-[13px] font-mono"
                  {...props}
                >
                  {children}
                </code>
              );
            },

            /* ── 排版元素 ─────────────────────────────────────────── */
            h1: ({ children }) => (
              <h1 className="text-xl font-bold mt-0 mb-4 pb-2 border-b border-gray-200 dark:border-gray-700
                             text-gray-900 dark:text-gray-100">
                {children}
              </h1>
            ),
            h2: ({ children }) => (
              <h2 className="text-base font-semibold mt-6 mb-3 text-gray-800 dark:text-gray-200">
                {children}
              </h2>
            ),
            h3: ({ children }) => (
              <h3 className="text-sm font-semibold mt-5 mb-2 text-gray-700 dark:text-gray-300">
                {children}
              </h3>
            ),
            p: ({ children }) => (
              <p className="mb-3 leading-relaxed text-gray-700 dark:text-gray-300">{children}</p>
            ),
            ul: ({ children }) => (
              <ul className="list-disc pl-6 mb-3 space-y-1 text-gray-700 dark:text-gray-300">{children}</ul>
            ),
            ol: ({ children }) => (
              <ol className="list-decimal pl-6 mb-3 space-y-1 text-gray-700 dark:text-gray-300">{children}</ol>
            ),
            blockquote: ({ children }) => (
              <blockquote className="border-l-[3px] border-blue-500 dark:border-blue-400 pl-4 my-3
                                     text-gray-500 dark:text-gray-400 italic">
                {children}
              </blockquote>
            ),
            hr: () => <hr className="my-5 border-gray-200 dark:border-gray-700" />,
            strong: ({ children }) => (
              <strong className="font-semibold text-gray-900 dark:text-gray-100">{children}</strong>
            ),
            a: ({ href, children }) => (
              <a href={href} className="text-blue-600 dark:text-blue-400 hover:underline" target="_blank" rel="noreferrer">
                {children}
              </a>
            ),
            table: ({ children }) => (
              <div className="overflow-x-auto my-4">
                <table className="min-w-full text-sm border-collapse border border-gray-200 dark:border-gray-700">
                  {children}
                </table>
              </div>
            ),
            th: ({ children }) => (
              <th className="px-3 py-2 text-left font-semibold bg-gray-50 dark:bg-gray-800
                             border border-gray-200 dark:border-gray-700 text-gray-800 dark:text-gray-200">
                {children}
              </th>
            ),
            td: ({ children }) => (
              <td className="px-3 py-2 border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300">
                {children}
              </td>
            ),
          }}
        >
          {content}
        </ReactMarkdown>
      </article>
    </div>
  );
}
