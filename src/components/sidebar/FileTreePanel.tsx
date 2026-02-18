/**
 * FileTreePanel — 基于 react-arborist 的 VS Code 风格文件树
 *
 * 将后端 FileNode[] 转为 arborist 数据格式，自定义节点渲染，
 * chapters/ 下的文件生成 fs-{num} ID，其他文件生成 doc:{path} ID。
 */
import React, { useMemo, useCallback, useRef, useState, useEffect } from 'react';
import { Tree, TreeApi, NodeRendererProps } from 'react-arborist';
import {
  ChevronRight, ChevronDown, Folder, FolderOpen,
  FileText, FilePlus, FolderPlus, Trash2, Pencil,
} from 'lucide-react';
import type { FileNode } from '../../services/docsFs';
import { docsFs } from '../../services/docsFs';
import ConfirmDialog from '../common/ConfirmDialog';

interface FileTreePanelProps {
  workId: string;
  fileTree: FileNode[];
  activeFileId: string | null;
  onFileSelect: (fileId: string) => void;
  onChapterCreate: (title: string) => Promise<FileNode[]>;
  onTreeChange: (tree: FileNode[]) => void;
}

/** react-arborist 节点数据格式 */
interface TreeNodeData {
  id: string;
  name: string;
  path: string;
  type: 'file' | 'dir';
  children?: TreeNodeData[];
}

/** 右键菜单状态 */
interface CtxMenuState {
  x: number;
  y: number;
  node: TreeNodeData;
}

/** 内联重命名状态 */
interface EditingNodeState {
  path: string;
  originalName: string;
}

/** Inline 创建状态 */
interface InlineCreateState {
  type: 'file' | 'dir';
  parentPath: string;
}

const PHANTOM_ID = '__inline_new__';

/** 从 chapters/ 下的文件名提取章节号 */
function chapterNumFromPath(path: string): number | null {
  const m = path.match(/^chapters\/(\d+)-[^/]+\.md$/);
  return m ? parseInt(m[1], 10) : null;
}

/** 将文件路径转为编辑器可用的 ID */
function pathToFileId(path: string): string {
  const num = chapterNumFromPath(path);
  if (num !== null) return `fs-${num}`;
  return `doc:${path}`;
}

/** 将后端 FileNode[] 递归转为 arborist TreeNodeData[] */
function toTreeData(nodes: FileNode[]): TreeNodeData[] {
  return nodes.map(n => ({
    id: n.path,
    name: n.name,
    path: n.path,
    type: n.type,
    ...(n.type === 'dir' && n.children
      ? { children: toTreeData(n.children) }
      : {}),
  }));
}

/** 判断路径是否在 chapters/ 目录下 */
function isChapterPath(path: string): boolean {
  return path === 'chapters' || path.startsWith('chapters/');
}

/** 从节点推导父目录路径 */
function getParentPath(node: TreeNodeData): string {
  if (node.type === 'dir') return node.path;
  const lastSlash = node.path.lastIndexOf('/');
  return lastSlash > 0 ? node.path.substring(0, lastSlash) : '';
}

/** 在树中递归查找节点 */
function findNode(nodes: TreeNodeData[], path: string): TreeNodeData | undefined {
  for (const n of nodes) {
    if (n.path === path) return n;
    if (n.children) {
      const found = findNode(n.children, path);
      if (found) return found;
    }
  }
  return undefined;
}

const toolbarBtnClass =
  'h-7 w-7 p-0 flex items-center justify-center text-zinc-500 hover:text-zinc-900 hover:bg-white hover:shadow-sm rounded-lg transition-all dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-800';

export const FileTreePanel: React.FC<FileTreePanelProps> = ({
  workId,
  fileTree,
  activeFileId,
  onFileSelect,
  onChapterCreate,
  onTreeChange,
}) => {
  const baseTreeData = useMemo(() => toTreeData(fileTree), [fileTree]);

  // 动态测量容器高度
  const treeContainerRef = useRef<HTMLDivElement>(null);
  const treeRef = useRef<TreeApi<TreeNodeData>>(null);
  const [treeHeight, setTreeHeight] = useState(400);

  // 右键菜单
  const [ctxMenu, setCtxMenu] = useState<CtxMenuState | null>(null);
  // 内联重命名
  const [editingNode, setEditingNode] = useState<EditingNodeState | null>(null);
  // 删除确认弹窗
  const [deleteTarget, setDeleteTarget] = useState<TreeNodeData | null>(null);
  // Inline 创建（新建文件/文件夹在树中显示输入框）
  const [inlineCreate, setInlineCreate] = useState<InlineCreateState | null>(null);
  // 防止 onBlur + onKeyDown 双重触发
  const inlineHandledRef = useRef(false);
  const renameHandledRef = useRef(false);

  useEffect(() => {
    const el = treeContainerRef.current;
    if (!el) return;
    const ro = new ResizeObserver(([entry]) => {
      setTreeHeight(Math.floor(entry.contentRect.height));
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  // ─── 内联创建时自动展开父文件夹 ───
  useEffect(() => {
    if (inlineCreate?.parentPath && treeRef.current) {
      treeRef.current.open(inlineCreate.parentPath);
    }
  }, [inlineCreate]);

  // ─── 幻影节点注入 ───
  // 当 inlineCreate 激活时，在目标父目录下注入一个临时节点
  const treeData = useMemo(() => {
    if (!inlineCreate) return baseTreeData;

    const phantom: TreeNodeData = {
      id: PHANTOM_ID,
      name: '',
      path: PHANTOM_ID,
      type: inlineCreate.type,
    };

    if (!inlineCreate.parentPath) {
      return [...baseTreeData, phantom];
    }

    const inject = (nodes: TreeNodeData[]): TreeNodeData[] =>
      nodes.map(n => {
        if (n.path === inlineCreate.parentPath) {
          return { ...n, children: [...(n.children || []), phantom] };
        }
        return n.children ? { ...n, children: inject(n.children) } : n;
      });
    return inject(baseTreeData);
  }, [baseTreeData, inlineCreate]);

  /** 从 activeFileId 反推 arborist 的 selection */
  const selectedPath = useMemo(() => {
    if (!activeFileId) return undefined;
    if (activeFileId.startsWith('fs-')) {
      const num = parseInt(activeFileId.slice(3), 10);
      const findPath = (nodes: TreeNodeData[]): string | undefined => {
        for (const n of nodes) {
          if (n.type === 'file' && chapterNumFromPath(n.path) === num) return n.id;
          if (n.children) {
            const found = findPath(n.children);
            if (found) return found;
          }
        }
        return undefined;
      };
      return findPath(treeData);
    }
    if (activeFileId.startsWith('doc:')) return activeFileId.slice(4);
    return undefined;
  }, [activeFileId, treeData]);

  /** 工具栏按钮的目标目录：基于当前选中节点推导 */
  const activeParentPath = useMemo(() => {
    if (!selectedPath) return '';
    const node = findNode(treeData, selectedPath);
    if (!node) return '';
    return getParentPath(node);
  }, [selectedPath, treeData]);

  const handleActivate = useCallback(
    (node: { data: TreeNodeData }) => {
      if (node.data.type === 'file' && node.data.id !== PHANTOM_ID) {
        onFileSelect(pathToFileId(node.data.path));
      }
    },
    [onFileSelect],
  );

  // ─── 文件操作 ───

  /** inline 创建确认 */
  const handleInlineConfirm = useCallback(async (name: string) => {
    if (!inlineCreate || !workId || !name.trim()) {
      setInlineCreate(null);
      return;
    }
    try {
      let trimmed = name.trim();
      let newTree: FileNode[];

      if (inlineCreate.type === 'file' && isChapterPath(inlineCreate.parentPath)) {
        // chapters/ 下新建文件 → 走章节创建逻辑（自动编号 + frontmatter）
        newTree = await onChapterCreate(trimmed);
      } else if (inlineCreate.type === 'file') {
        if (!trimmed.endsWith('.md')) trimmed += '.md';
        const path = inlineCreate.parentPath ? `${inlineCreate.parentPath}/${trimmed}` : trimmed;
        newTree = await docsFs.createFile(workId, path);
      } else {
        const path = inlineCreate.parentPath ? `${inlineCreate.parentPath}/${trimmed}` : trimmed;
        newTree = await docsFs.createDir(workId, path);
      }
      onTreeChange(newTree);
    } catch (err) {
      console.error('Inline create failed:', err);
    }
    setInlineCreate(null);
  }, [inlineCreate, workId, onTreeChange, onChapterCreate]);

  // 用 ref 暴露给 memoized NodeRenderer
  const handleInlineConfirmRef = useRef(handleInlineConfirm);
  handleInlineConfirmRef.current = handleInlineConfirm;
  const setInlineCreateRef = useRef(setInlineCreate);
  setInlineCreateRef.current = setInlineCreate;
  const inlineTypeRef = useRef<'file' | 'dir'>('file');
  const inlineParentPathRef = useRef('');
  if (inlineCreate) {
    inlineTypeRef.current = inlineCreate.type;
    inlineParentPathRef.current = inlineCreate.parentPath;
  }

  /** 右键菜单：新建文件 */
  const handleCtxNewFile = useCallback((node: TreeNodeData) => {
    setInlineCreate({ type: 'file', parentPath: getParentPath(node) });
  }, []);

  /** 右键菜单：新建文件夹 */
  const handleCtxNewDir = useCallback((node: TreeNodeData) => {
    setInlineCreate({ type: 'dir', parentPath: getParentPath(node) });
  }, []);

  /** 内联重命名确认 */
  const handleRenameConfirm = useCallback(async (newName: string) => {
    if (!editingNode || !workId || !newName.trim()) {
      setEditingNode(null);
      return;
    }
    const trimmed = newName.trim();
    if (trimmed === editingNode.originalName) {
      setEditingNode(null);
      return;
    }
    try {
      const newTree = await docsFs.rename(workId, editingNode.path, trimmed);
      onTreeChange(newTree);
    } catch (err) {
      console.error('Rename failed:', err);
    }
    setEditingNode(null);
  }, [editingNode, workId, onTreeChange]);

  /** 删除（显示确认弹窗） */
  const handleDelete = useCallback((node: TreeNodeData) => {
    setDeleteTarget(node);
  }, []);

  /** 删除确认回调 */
  const handleDeleteConfirm = useCallback(async () => {
    if (!workId || !deleteTarget) return;
    try {
      const newTree = await docsFs.remove(workId, deleteTarget.path);
      onTreeChange(newTree);
    } catch (err) {
      console.error('Delete failed:', err);
    }
    setDeleteTarget(null);
  }, [workId, deleteTarget, onTreeChange]);

  // 内联重命名 refs（放在 handleRenameConfirm 之后避免 TDZ 错误）
  const handleRenameConfirmRef = useRef(handleRenameConfirm);
  handleRenameConfirmRef.current = handleRenameConfirm;
  const editingNodeRef = useRef(editingNode);
  editingNodeRef.current = editingNode;
  const setEditingNodeRef = useRef(setEditingNode);
  setEditingNodeRef.current = setEditingNode;

  // ─── 自定义节点渲染 ───

  const NodeRenderer = useCallback(({ node, style, dragHandle }: NodeRendererProps<TreeNodeData>) => {
    const data = node.data;

    // 幻影节点 → inline 输入框
    if (data.id === PHANTOM_ID) {
      return (
        <div ref={dragHandle} style={style} className="flex items-center gap-1.5 px-2 py-0.5">
          {inlineTypeRef.current === 'dir'
            ? <Folder className="h-3.5 w-3.5 flex-shrink-0 text-amber-500 dark:text-amber-400" />
            : <FileText className="h-3.5 w-3.5 flex-shrink-0 opacity-50" />
          }
          <input
            autoFocus
            type="text"
            className="flex-1 h-5 text-[13px] bg-transparent border-b border-blue-500 dark:border-blue-400 outline-none text-zinc-900 dark:text-slate-100 placeholder:text-zinc-400 dark:placeholder:text-slate-500"
            placeholder={inlineTypeRef.current === 'dir' ? '文件夹名称' : isChapterPath(inlineParentPathRef.current) ? '章节标题' : '文件名.md'}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                inlineHandledRef.current = true;
                handleInlineConfirmRef.current((e.target as HTMLInputElement).value);
              } else if (e.key === 'Escape') {
                inlineHandledRef.current = true;
                setInlineCreateRef.current(null);
              }
            }}
            onBlur={(e) => {
              if (inlineHandledRef.current) {
                inlineHandledRef.current = false;
                return;
              }
              const val = e.target.value.trim();
              if (val) {
                handleInlineConfirmRef.current(val);
              } else {
                setInlineCreateRef.current(null);
              }
            }}
          />
        </div>
      );
    }

    // 内联重命名模式
    const isEditing = editingNodeRef.current?.path === data.path;

    // 普通节点
    const isDir = data.type === 'dir';
    return (
      <div
        ref={dragHandle}
        style={style}
        className={`flex items-center gap-1.5 px-2 py-0.5 cursor-pointer select-none text-[13px] leading-relaxed rounded-md transition-colors ${
          node.isSelected
            ? 'bg-white shadow-sm ring-1 ring-zinc-900/5 text-zinc-900 dark:bg-slate-800 dark:ring-slate-700 dark:text-slate-100'
            : 'text-zinc-600 hover:bg-zinc-100/60 dark:text-slate-400 dark:hover:bg-slate-800/60'
        }`}
        onClick={(e) => {
          if (isDir) {
            e.stopPropagation();
            node.toggle();
          }
        }}
        onContextMenu={(e) => {
          e.preventDefault();
          e.stopPropagation();
          setCtxMenu({ x: e.clientX, y: e.clientY, node: data });
        }}
      >
        {isDir ? (
          node.isOpen
            ? <ChevronDown className="h-3.5 w-3.5 flex-shrink-0 opacity-50" />
            : <ChevronRight className="h-3.5 w-3.5 flex-shrink-0 opacity-50" />
        ) : (
          <span className="w-3.5 flex-shrink-0" />
        )}
        {isDir ? (
          node.isOpen
            ? <FolderOpen className="h-3.5 w-3.5 flex-shrink-0 text-amber-500 dark:text-amber-400" />
            : <Folder className="h-3.5 w-3.5 flex-shrink-0 text-amber-500 dark:text-amber-400" />
        ) : (
          <FileText className="h-3.5 w-3.5 flex-shrink-0 opacity-50" />
        )}
        {isEditing ? (
          <input
            autoFocus
            type="text"
            defaultValue={editingNodeRef.current!.originalName}
            className="flex-1 h-5 text-[13px] bg-transparent border-b border-blue-500 dark:border-blue-400 outline-none text-zinc-900 dark:text-slate-100"
            ref={(el) => {
              if (el) {
                // 选中文件名部分（不含后缀）
                const name = el.value;
                const dotIdx = name.lastIndexOf('.');
                el.setSelectionRange(0, dotIdx > 0 ? dotIdx : name.length);
              }
            }}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                renameHandledRef.current = true;
                handleRenameConfirmRef.current((e.target as HTMLInputElement).value);
              } else if (e.key === 'Escape') {
                renameHandledRef.current = true;
                setEditingNodeRef.current(null);
              }
            }}
            onBlur={(e) => {
              if (renameHandledRef.current) {
                renameHandledRef.current = false;
                return;
              }
              const val = e.target.value.trim();
              if (val && val !== editingNodeRef.current?.originalName) {
                handleRenameConfirmRef.current(val);
              } else {
                setEditingNodeRef.current(null);
              }
            }}
          />
        ) : (
          <span className="truncate">{data.name}</span>
        )}
      </div>
    );
  }, [editingNode]);

  return (
    <div className="flex-1 flex flex-col min-h-0">
      {/* 标题区域 + 工具栏 */}
      <div className="px-3 py-1.5 flex items-center justify-between flex-shrink-0">
        <h2 className="text-[15px] text-zinc-800 dark:text-slate-100 tracking-tight">文件</h2>
        <div className="flex items-center gap-0.5">
          <button type="button" onClick={() => setInlineCreate({ type: 'file', parentPath: activeParentPath })} className={toolbarBtnClass} title="新建文件">
            <FilePlus className="h-4 w-4" />
          </button>
          <button type="button" onClick={() => setInlineCreate({ type: 'dir', parentPath: activeParentPath })} className={toolbarBtnClass} title="新建文件夹">
            <FolderPlus className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* 文件树 */}
      <div className="flex-1 overflow-hidden px-1" ref={treeContainerRef}>
        <Tree<TreeNodeData>
          ref={treeRef}
          data={treeData}
          openByDefault
          disableDrag
          disableDrop
          disableEdit
          disableMultiSelection
          indent={16}
          rowHeight={28}
          selection={selectedPath}
          onActivate={handleActivate}
          width="100%"
          height={treeHeight}
          className="!overflow-y-auto custom-scrollbar"
        >
          {NodeRenderer}
        </Tree>
      </div>

      {/* 右键菜单 */}
      {ctxMenu && (
        <>
          <div className="fixed inset-0 z-40" onClick={() => setCtxMenu(null)} />
          <div
            className="fixed z-50 bg-white dark:bg-slate-800 rounded-lg p-1 min-w-[160px] shadow-lg border border-zinc-200 dark:border-slate-700"
            style={{ left: ctxMenu.x, top: ctxMenu.y }}
          >
            <button
              onClick={() => { handleCtxNewFile(ctxMenu.node); setCtxMenu(null); }}
              className="w-full flex items-center gap-2 px-3 py-1.5 text-sm text-zinc-700 dark:text-slate-300 rounded hover:bg-zinc-100 dark:hover:bg-slate-700"
            >
              <FilePlus className="h-3.5 w-3.5" /> 新建文件
            </button>
            <button
              onClick={() => { handleCtxNewDir(ctxMenu.node); setCtxMenu(null); }}
              className="w-full flex items-center gap-2 px-3 py-1.5 text-sm text-zinc-700 dark:text-slate-300 rounded hover:bg-zinc-100 dark:hover:bg-slate-700"
            >
              <FolderPlus className="h-3.5 w-3.5" /> 新建文件夹
            </button>
            <button
              onClick={() => { setEditingNode({ path: ctxMenu.node.path, originalName: ctxMenu.node.name }); setCtxMenu(null); }}
              className="w-full flex items-center gap-2 px-3 py-1.5 text-sm text-zinc-700 dark:text-slate-300 rounded hover:bg-zinc-100 dark:hover:bg-slate-700"
            >
              <Pencil className="h-3.5 w-3.5" /> 重命名
            </button>
            <div className="h-px bg-zinc-200 dark:bg-slate-700 my-1" />
            <button
              onClick={() => { handleDelete(ctxMenu.node); setCtxMenu(null); }}
              className="w-full flex items-center gap-2 px-3 py-1.5 text-sm text-red-600 dark:text-red-400 rounded hover:bg-red-50 dark:hover:bg-red-900/20"
            >
              <Trash2 className="h-3.5 w-3.5" /> 删除
            </button>
          </div>
        </>
      )}

      {/* 删除确认弹窗 */}
      <ConfirmDialog
        isOpen={deleteTarget !== null}
        title="确认删除"
        message={`确定删除「${deleteTarget?.name ?? ''}」吗？此操作不可撤销。`}
        confirmText="删除"
        cancelText="取消"
        variant="danger"
        onConfirm={handleDeleteConfirm}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  );
};
