/**
 * UniqueID 扩展
 * 给块级节点（段落、标题等）分配唯一 ID，用于精确定位
 *
 * 功能：
 * 1. 自动给新节点分配短 ID（如 "p-a1b2c3"）
 * 2. ID 持久化到 HTML 的 data-id 属性
 * 3. 提供通过 ID 查找节点的方法
 */
import { Extension } from '@tiptap/core';
import { Plugin, PluginKey } from '@tiptap/pm/state';

export interface UniqueIDOptions {
  /** 需要添加 ID 的节点类型 */
  types: string[];
  /** HTML 属性名 */
  attributeName: string;
  /** ID 生成函数 */
  generateID: () => string;
}

/** 节点查找结果 */
export interface NodeFindResult {
  /** 节点在文档中的位置 */
  pos: number;
  /** ProseMirror 节点对象 */
  node: any;
  /** 节点文本内容 */
  text: string;
}

/** 段落信息（用于列表展示） */
export interface ParagraphInfo {
  /** 唯一 ID */
  id: string;
  /** 节点类型 */
  type: string;
  /** 内容预览（前50字） */
  preview: string;
  /** 完整文本 */
  text: string;
  /** 在文档中的位置 */
  pos: number;
}

// 简单的短 ID 生成器（不依赖 nanoid）
function generateShortID(): string {
  const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let id = '';
  for (let i = 0; i < 8; i++) {
    id += chars[Math.floor(Math.random() * chars.length)];
  }
  return id;
}

declare module '@tiptap/core' {
  interface Commands<ReturnType> {
    uniqueID: {
      /** 手动给当前节点设置 ID */
      setNodeID: (id: string) => ReturnType;
    };
  }
}

export const UniqueID = Extension.create<UniqueIDOptions>({
  name: 'uniqueID',

  addOptions() {
    return {
      types: ['paragraph', 'heading', 'blockquote', 'codeBlock'],
      attributeName: 'data-id',
      generateID: generateShortID,
    };
  },

  addGlobalAttributes() {
    return [
      {
        types: this.options.types,
        attributes: {
          id: {
            default: null,
            parseHTML: (element) => element.getAttribute(this.options.attributeName),
            renderHTML: (attributes) => {
              if (!attributes.id) return {};
              return { [this.options.attributeName]: attributes.id };
            },
          },
        },
      },
    ];
  },

  addProseMirrorPlugins() {
    const { types, generateID } = this.options;

    return [
      new Plugin({
        key: new PluginKey('uniqueID'),

        // 在事务提交前，给没有 ID 的节点分配 ID，或给重复 ID 的节点分配新 ID
        appendTransaction(transactions, oldState, newState) {
          // 检查是否有文档变化
          const docChanged = transactions.some((tr) => tr.docChanged);
          if (!docChanged) return null;

          const { tr } = newState;
          let modified = false;

          // 收集已存在的 ID，用于检测重复
          const existingIDs = new Set<string>();
          const duplicatePositions: Array<{ pos: number; node: any }> = [];

          // 第一遍：收集所有 ID，找出重复的
          newState.doc.descendants((node, pos) => {
            if (!types.includes(node.type.name)) return;

            const nodeID = node.attrs.id;
            if (nodeID) {
              if (existingIDs.has(nodeID)) {
                // 发现重复 ID，记录下来稍后处理
                duplicatePositions.push({ pos, node });
              } else {
                existingIDs.add(nodeID);
              }
            }
          });

          // 第二遍：给没有 ID 或重复 ID 的节点分配新 ID
          newState.doc.descendants((node, pos) => {
            if (!types.includes(node.type.name)) return;

            const isDuplicate = duplicatePositions.some((d) => d.pos === pos);

            // 如果没有 ID 或 ID 重复，分配一个新的
            if (!node.attrs.id || isDuplicate) {
              let newID = generateID();
              // 确保新 ID 不重复
              while (existingIDs.has(newID)) {
                newID = generateID();
              }
              existingIDs.add(newID);

              tr.setNodeMarkup(pos, undefined, {
                ...node.attrs,
                id: newID,
              });
              modified = true;
            }
          });

          return modified ? tr : null;
        },
      }),
    ];
  },

  addStorage() {
    return {
      /**
       * 通过 ID 查找节点
       * @param id 节点 ID
       * @returns 节点信息或 null
       */
      findNodeByID: (id: string): NodeFindResult | null => null,

      /**
       * 获取所有带 ID 的节点列表
       * @returns 段落信息列表
       */
      getAllNodes: (): ParagraphInfo[] => [],

      /**
       * 通过 ID 选中节点
       * @param id 节点 ID
       * @returns 是否成功
       */
      selectNodeByID: (id: string): boolean => false,

      /**
       * 通过 ID 替换节点内容
       * @param id 节点 ID
       * @param content 新内容
       * @returns 是否成功
       */
      replaceNodeByID: (id: string, content: string): boolean => false,
    };
  },

  onCreate() {
    const editor = this.editor;
    const types = this.options.types;
    const generateID = this.options.generateID;

    // 🆕 初始化：给现有节点分配 ID
    const existingIDs = new Set<string>();
    const nodesToUpdate: Array<{ pos: number; node: any }> = [];

    // 收集需要分配 ID 的节点
    editor.state.doc.descendants((node, pos) => {
      if (!types.includes(node.type.name)) return;

      if (node.attrs.id) {
        if (existingIDs.has(node.attrs.id)) {
          // 重复 ID，需要重新分配
          nodesToUpdate.push({ pos, node });
        } else {
          existingIDs.add(node.attrs.id);
        }
      } else {
        // 没有 ID，需要分配
        nodesToUpdate.push({ pos, node });
      }
    });

    // 批量更新节点
    if (nodesToUpdate.length > 0) {
      const { tr } = editor.state;
      nodesToUpdate.forEach(({ pos, node }) => {
        let newID = generateID();
        while (existingIDs.has(newID)) {
          newID = generateID();
        }
        existingIDs.add(newID);
        tr.setNodeMarkup(pos, undefined, { ...node.attrs, id: newID });
      });
      editor.view.dispatch(tr);
    }

    // 通过 ID 查找节点
    this.storage.findNodeByID = (id: string): NodeFindResult | null => {
      let found: NodeFindResult | null = null;

      editor.state.doc.descendants((node, pos) => {
        if (node.attrs.id === id) {
          found = {
            pos,
            node,
            text: node.textContent,
          };
          return false; // 停止遍历
        }
      });

      return found;
    };

    // 获取所有带 ID 的节点
    this.storage.getAllNodes = (): ParagraphInfo[] => {
      const nodes: ParagraphInfo[] = [];

      editor.state.doc.descendants((node, pos) => {
        if (types.includes(node.type.name) && node.attrs.id) {
          const text = node.textContent;
          nodes.push({
            id: node.attrs.id,
            type: node.type.name,
            preview: text.length > 50 ? text.slice(0, 50) + '...' : text,
            text,
            pos,
          });
        }
      });

      return nodes;
    };

    // 通过 ID 选中节点
    this.storage.selectNodeByID = (id: string): boolean => {
      const result = this.storage.findNodeByID(id);
      if (!result) return false;

      const { pos, node } = result;
      editor.commands.setTextSelection({
        from: pos + 1, // 进入节点内部
        to: pos + node.nodeSize - 1,
      });
      return true;
    };

    // 通过 ID 替换节点内容（保留原节点类型）
    this.storage.replaceNodeByID = (id: string, content: string): boolean => {
      const result = this.storage.findNodeByID(id);
      if (!result) return false;

      const { pos, node } = result;
      const nodeType = node.type.name;

      // 根据节点类型生成正确的 HTML
      let html: string;
      const attrString = `data-id="${id}"`;

      switch (nodeType) {
        case 'heading':
          const level = node.attrs.level || 1;
          html = `<h${level} ${attrString}>${content}</h${level}>`;
          break;
        case 'blockquote':
          html = `<blockquote ${attrString}><p>${content}</p></blockquote>`;
          break;
        case 'codeBlock':
          html = `<pre ${attrString}><code>${content}</code></pre>`;
          break;
        case 'paragraph':
        default:
          html = `<p ${attrString}>${content}</p>`;
          break;
      }

      editor
        .chain()
        .focus()
        .insertContentAt({ from: pos, to: pos + node.nodeSize }, html)
        .run();
      return true;
    };
  },

  addCommands() {
    return {
      setNodeID:
        (id: string) =>
        ({ tr, state }) => {
          const { from } = state.selection;
          const node = state.doc.nodeAt(from);
          if (!node) return false;

          tr.setNodeMarkup(from, undefined, {
            ...node.attrs,
            id,
          });
          return true;
        },
    };
  },
});

export default UniqueID;
