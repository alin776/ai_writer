/**
 * FileTreePanel — 基于 react-arborist 的 VS Code 风格文件树
 *
 * 将后端 FileNode[] 转为 arborist 数据格式，自定义节点渲染，
 * chapters/ 下的文件生成 fs-{num} ID，其他文件生成 doc:{path} ID。
 */
import React, { useMemo, useCallback, useRef, useState, useEffect } from 'react';
import { Tree, NodeRendererProps } from 'react-arborist';
import { Plus, ChevronRight, ChevronDown, Folder, FolderOpen, FileText } from 'lucide-react';
import type { FileNode } from '../../services/docsFs';

interface FileTreePanelProps {
  workId: string;
  fileTree: FileNode[];
  activeFileId: string | null;
  onFileSelect: (fileId: string) => void;
  onAddChapter: () => void;
}

/** react-arborist 节点数据格式 */
interface TreeNodeData {
  id: string;
  name: string;
  path: string;
  type: 'file' | 'dir';
  children?: TreeNodeData[];
}

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

/** 自定义节点渲染 */
function Node({ node, style, dragHandle }: NodeRendererProps<TreeNodeData>) {
  const data = node.data;
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
        // 文件点击不阻止冒泡，让 Tree 的 onActivate 回调处理
      }}
    >
      {/* 展开/折叠图标 */}
      {isDir ? (
        node.isOpen
          ? <ChevronDown className="h-3.5 w-3.5 flex-shrink-0 opacity-50" />
          : <ChevronRight className="h-3.5 w-3.5 flex-shrink-0 opacity-50" />
      ) : (
        <span className="w-3.5 flex-shrink-0" /> /* 占位对齐 */
      )}

      {/* 图标 */}
      {isDir ? (
        node.isOpen
          ? <FolderOpen className="h-3.5 w-3.5 flex-shrink-0 text-amber-500 dark:text-amber-400" />
          : <Folder className="h-3.5 w-3.5 flex-shrink-0 text-amber-500 dark:text-amber-400" />
      ) : (
        <FileText className="h-3.5 w-3.5 flex-shrink-0 opacity-50" />
      )}

      {/* 名称 */}
      <span className="truncate">{data.name}</span>
    </div>
  );
}

export const FileTreePanel: React.FC<FileTreePanelProps> = ({
  fileTree,
  activeFileId,
  onFileSelect,
  onAddChapter,
}) => {
  const treeData = useMemo(() => toTreeData(fileTree), [fileTree]);

  // 动态测量容器高度，传给 react-arborist
  const treeContainerRef = useRef<HTMLDivElement>(null);
  const [treeHeight, setTreeHeight] = useState(400);

  useEffect(() => {
    const el = treeContainerRef.current;
    if (!el) return;
    const ro = new ResizeObserver(([entry]) => {
      setTreeHeight(Math.floor(entry.contentRect.height));
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  /** 从 activeFileId 反推 arborist 的 selection（用 path 作为 node id） */
  const selectedPath = useMemo(() => {
    if (!activeFileId) return undefined;
    // fs-N → chapters/NN-*.md — 需要在 treeData 中查找
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
    // doc:path → path
    if (activeFileId.startsWith('doc:')) return activeFileId.slice(4);
    return undefined;
  }, [activeFileId, treeData]);

  const handleActivate = useCallback(
    (node: { data: TreeNodeData }) => {
      if (node.data.type === 'file') {
        onFileSelect(pathToFileId(node.data.path));
      }
    },
    [onFileSelect],
  );

  return (
    <div className="flex-1 flex flex-col min-h-0">
      {/* 标题区域 */}
      <div className="px-3 py-1.5 flex items-center justify-between flex-shrink-0">
        <h2 className="text-[15px] text-zinc-800 dark:text-slate-100 tracking-tight">文件</h2>
        <button
          type="button"
          onClick={() => onAddChapter()}
          className="h-7 w-7 p-0 flex items-center justify-center text-zinc-500 hover:text-zinc-900 hover:bg-white hover:shadow-sm rounded-lg transition-all dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-800"
          title="新建章节"
        >
          <Plus className="h-5 w-5" />
        </button>
      </div>

      {/* 文件树 */}
      <div className="flex-1 overflow-hidden px-1" ref={treeContainerRef}>
        <Tree<TreeNodeData>
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
          {Node}
        </Tree>
      </div>
    </div>
  );
};
