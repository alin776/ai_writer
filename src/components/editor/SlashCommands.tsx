/**
 * Slash 命令菜单
 * 输入 / 触发快速插入命令
 */
import React from 'react';
import { Editor } from '@tiptap/core';
import {
  Heading1,
  Heading2,
  Heading3,
  List,
  ListOrdered,
  CheckSquare,
  Quote,
  Code,
  Image,
  Minus,
  FileCode,
  Type,
  Wand2,
  Sparkles,
  FileText,
  Minimize2,
} from 'lucide-react';

export interface CommandItem {
  title: string;
  description: string;
  icon: React.ReactNode;
  command: (editor: Editor) => void;
  searchTerms?: string[];
}

/**
 * Slash 命令列表
 */
export const slashCommands: CommandItem[] = [
  {
    title: '正文',
    description: '普通段落文本',
    icon: <Type className="w-5 h-5" />,
    searchTerms: ['p', 'paragraph', 'text', '段落', 'zhengwen'],
    command: (editor) => {
      editor.chain().focus().setParagraph().run();
    },
  },
  {
    title: '一级标题',
    description: '最大的标题',
    icon: <Heading1 className="w-5 h-5" />,
    searchTerms: ['h1', 'heading1', 'title', '标题', 'yiji'],
    command: (editor) => {
      editor.chain().focus().toggleHeading({ level: 1 }).run();
    },
  },
  {
    title: '二级标题',
    description: '中等大小的标题',
    icon: <Heading2 className="w-5 h-5" />,
    searchTerms: ['h2', 'heading2', 'subtitle', '标题', 'erji'],
    command: (editor) => {
      editor.chain().focus().toggleHeading({ level: 2 }).run();
    },
  },
  {
    title: '三级标题',
    description: '小标题',
    icon: <Heading3 className="w-5 h-5" />,
    searchTerms: ['h3', 'heading3', '标题', 'sanji'],
    command: (editor) => {
      editor.chain().focus().toggleHeading({ level: 3 }).run();
    },
  },
  {
    title: '无序列表',
    description: '创建一个简单的列表',
    icon: <List className="w-5 h-5" />,
    searchTerms: ['ul', 'bullet', 'list', '列表', 'wuxu'],
    command: (editor) => {
      editor.chain().focus().toggleBulletList().run();
    },
  },
  {
    title: '有序列表',
    description: '创建一个数字列表',
    icon: <ListOrdered className="w-5 h-5" />,
    searchTerms: ['ol', 'number', 'list', '列表', 'youxu'],
    command: (editor) => {
      editor.chain().focus().toggleOrderedList().run();
    },
  },
  {
    title: '任务列表',
    description: '创建一个带复选框的列表',
    icon: <CheckSquare className="w-5 h-5" />,
    searchTerms: ['todo', 'task', 'checkbox', '任务', 'renwu'],
    command: (editor) => {
      editor.chain().focus().toggleTaskList().run();
    },
  },
  {
    title: '引用',
    description: '插入引用块',
    icon: <Quote className="w-5 h-5" />,
    searchTerms: ['quote', 'blockquote', '引用', 'yinyong'],
    command: (editor) => {
      editor.chain().focus().toggleBlockquote().run();
    },
  },
  {
    title: '代码块',
    description: '插入代码块',
    icon: <FileCode className="w-5 h-5" />,
    searchTerms: ['code', 'codeblock', '代码', 'daima'],
    command: (editor) => {
      editor.chain().focus().toggleCodeBlock().run();
    },
  },
  {
    title: '分割线',
    description: '插入水平分割线',
    icon: <Minus className="w-5 h-5" />,
    searchTerms: ['hr', 'horizontal', 'line', '分割', 'fenge'],
    command: (editor) => {
      editor.chain().focus().setHorizontalRule().run();
    },
  },
  {
    title: '图片',
    description: '插入图片',
    icon: <Image className="w-5 h-5" />,
    searchTerms: ['image', 'img', 'photo', '图片', 'tupian'],
    command: (editor) => {
      const url = window.prompt('请输入图片地址:');
      if (url) {
        editor.chain().focus().setImage({ src: url }).run();
      }
    },
  },
  {
    title: 'AI 续写',
    description: '使用 AI 继续写作',
    icon: <Wand2 className="w-5 h-5" />,
    searchTerms: ['ai', 'continue', 'write', '续写', 'xuxie', 'ai续写'],
    command: (editor) => {
      // 触发 AI 续写
      const event = new CustomEvent('ai-continue', {
        detail: { editor },
      });
      window.dispatchEvent(event);
    },
  },
  {
    title: 'AI 扩写',
    description: '扩展选中的内容',
    icon: <FileText className="w-5 h-5" />,
    searchTerms: ['ai', 'expand', '扩写', 'kuoxie', 'ai扩写'],
    command: (editor) => {
      const event = new CustomEvent('ai-expand', {
        detail: { editor },
      });
      window.dispatchEvent(event);
    },
  },
  {
    title: 'AI 总结',
    description: '总结选中的内容',
    icon: <Minimize2 className="w-5 h-5" />,
    searchTerms: ['ai', 'summarize', 'summary', '总结', 'zongjie', 'ai总结'],
    command: (editor) => {
      const event = new CustomEvent('ai-summarize', {
        detail: { editor },
      });
      window.dispatchEvent(event);
    },
  },
  {
    title: 'AI 润色',
    description: '润色选中的内容',
    icon: <Sparkles className="w-5 h-5" />,
    searchTerms: ['ai', 'polish', 'improve', '润色', 'runse', 'ai润色'],
    command: (editor) => {
      const event = new CustomEvent('ai-polish', {
        detail: { editor },
      });
      window.dispatchEvent(event);
    },
  },
];

/**
 * 过滤命令
 */
export const filterCommands = (query: string): CommandItem[] => {
  const lowerQuery = query.toLowerCase();

  if (!lowerQuery) {
    return slashCommands;
  }

  return slashCommands.filter((item) => {
    const titleMatch = item.title.toLowerCase().includes(lowerQuery);
    const descMatch = item.description.toLowerCase().includes(lowerQuery);
    const searchMatch = item.searchTerms?.some((term) =>
      term.toLowerCase().includes(lowerQuery)
    );

    return titleMatch || descMatch || searchMatch;
  });
};

interface SlashCommandsMenuProps {
  items: CommandItem[];
  selectedIndex: number;
  onSelect: (index: number) => void;
}

/**
 * Slash 命令菜单 UI
 */
export const SlashCommandsMenu: React.FC<SlashCommandsMenuProps> = ({
  items,
  selectedIndex,
  onSelect,
}) => {
  if (items.length === 0) {
    return (
      <div className="slash-commands-menu">
        <div className="px-4 py-3 text-sm text-gray-500">没有找到匹配的命令</div>
      </div>
    );
  }

  return (
    <div className="slash-commands-menu">
      {items.map((item, index) => (
        <button
          key={item.title}
          className={`slash-command-item ${
            index === selectedIndex ? 'selected' : ''
          }`}
          onClick={() => onSelect(index)}
          onMouseEnter={() => onSelect(index)}
        >
          <div className="slash-command-icon">{item.icon}</div>
          <div className="slash-command-content">
            <div className="slash-command-title">{item.title}</div>
            <div className="slash-command-description">{item.description}</div>
          </div>
        </button>
      ))}
    </div>
  );
};
