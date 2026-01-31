/**
 * 修订定位工具
 * 用于在文档内容变化后重新定位修订位置
 *
 * 定位策略优先级：
 * 1. nodeId 定位（最高优先级，99%+ 准确率）
 * 2. 精确位置匹配
 * 3. 锚点匹配
 * 4. 模糊匹配
 */

export interface LocateResult {
  success: boolean;
  position?: { from: number; to: number };
  method?: 'nodeId' | 'exact' | 'anchor' | 'fuzzy';
  error?: string;
}

/**
 * 通过 nodeId 定位（使用 window.__editorNodeAPI）
 * @param nodeId 节点唯一 ID
 * @returns 定位结果
 */
export function locateByNodeId(nodeId: string): LocateResult {
  const api = (window as any).__editorNodeAPI;
  if (!api || !api.findByNodeID) {
    return {
      success: false,
      error: 'Editor Node API 不可用'
    };
  }

  const result = api.findByNodeID(nodeId);
  if (result && result.success) {
    return {
      success: true,
      position: result.position,
      method: 'nodeId'
    };
  }

  return {
    success: false,
    error: `未找到节点: ${nodeId}`
  };
}

/**
 * 转义正则表达式特殊字符
 */
function escapeRegex(str: string): string {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * 计算两个字符串的相似度（Jaccard 系数简化版）
 */
function similarity(a: string, b: string): number {
  if (!a || !b) return 0;
  if (a === b) return 1;

  const setA = new Set(a.split(''));
  const setB = new Set(b.split(''));
  const intersection = new Set([...setA].filter(x => setB.has(x)));
  const union = new Set([...setA, ...setB]);

  return intersection.size / union.size;
}

/**
 * 在文档中定位修订位置
 *
 * 定位策略（按优先级）：
 * 0. nodeId 定位（最高优先级，99%+ 准确率）
 * 1. 精确位置匹配：检查 position 处的内容是否与 originalText 一致
 * 2. 锚点匹配：用 before_anchor + originalText + after_anchor 模式匹配
 * 3. 模糊匹配：在全文中搜索最相似的片段
 */
export function locateRevisionPosition(
  docText: string,
  options: {
    nodeId?: string;  // 🆕 节点唯一 ID（最高优先级）
    position?: { from: number; to: number };
    originalText?: string;
    beforeAnchor?: string;
    afterAnchor?: string;
  }
): LocateResult {
  const { nodeId, position, originalText, beforeAnchor, afterAnchor } = options;

  // 0. nodeId 定位（最高优先级）
  if (nodeId) {
    const nodeResult = locateByNodeId(nodeId);
    if (nodeResult.success) {
      return nodeResult;
    }
    // nodeId 定位失败，继续尝试其他方式
    console.warn(`[revisionLocator] nodeId 定位失败: ${nodeId}，尝试其他方式`);
  }

  // 1. 精确位置匹配
  if (position && originalText) {
    const textAtPosition = docText.slice(position.from, position.to);
    if (textAtPosition === originalText) {
      return {
        success: true,
        position,
        method: 'exact'
      };
    }
  }

  // 2. 锚点匹配
  if (beforeAnchor || afterAnchor) {
    const beforePattern = beforeAnchor ? escapeRegex(beforeAnchor) : '';
    const afterPattern = afterAnchor ? escapeRegex(afterAnchor) : '';
    const targetPattern = originalText ? escapeRegex(originalText) : '([\\s\\S]*?)';

    // 构建匹配模式：before + target + after
    let pattern: string;
    if (beforeAnchor && afterAnchor) {
      pattern = `${beforePattern}(${originalText ? escapeRegex(originalText) : '[\\s\\S]*?'})${afterPattern}`;
    } else if (beforeAnchor) {
      pattern = `${beforePattern}(${originalText ? escapeRegex(originalText) : '[\\s\\S]{0,200}'})`;
    } else {
      pattern = `(${originalText ? escapeRegex(originalText) : '[\\s\\S]{0,200}'})${afterPattern}`;
    }

    try {
      const regex = new RegExp(pattern, 's');
      const match = docText.match(regex);

      if (match && match.index !== undefined) {
        const beforeLen = beforeAnchor?.length || 0;
        const from = match.index + beforeLen;
        const matchedContent = match[1] || '';
        const to = from + matchedContent.length;

        return {
          success: true,
          position: { from, to },
          method: 'anchor'
        };
      }
    } catch (e) {
      console.warn('[revisionLocator] 锚点正则匹配失败:', e);
    }
  }

  // 3. 模糊匹配（仅当有 originalText 时）
  if (originalText && originalText.length > 10) {
    // 滑动窗口搜索最相似的片段
    const windowSize = originalText.length;
    let bestMatch = { index: -1, score: 0 };

    for (let i = 0; i <= docText.length - windowSize; i++) {
      const window = docText.slice(i, i + windowSize);
      const score = similarity(window, originalText);

      if (score > bestMatch.score && score > 0.7) { // 相似度阈值 70%
        bestMatch = { index: i, score };
      }
    }

    if (bestMatch.index >= 0) {
      return {
        success: true,
        position: { from: bestMatch.index, to: bestMatch.index + windowSize },
        method: 'fuzzy'
      };
    }
  }

  // 定位失败
  return {
    success: false,
    error: '无法定位修订位置，文档内容可能已变更'
  };
}

/**
 * 定位续写/插入位置（文档末尾或指定位置）
 */
export function locateInsertPosition(
  docText: string,
  options: {
    nodeId?: string;  // 🆕 节点唯一 ID（在该节点后插入）
    position?: { from: number; to: number };
    beforeAnchor?: string;
    afterAnchor?: string;
  }
): LocateResult {
  const { nodeId, position, beforeAnchor, afterAnchor } = options;

  // 0. nodeId 定位（在节点末尾插入）
  if (nodeId) {
    const nodeResult = locateByNodeId(nodeId);
    if (nodeResult.success && nodeResult.position) {
      // 在节点末尾插入
      return {
        success: true,
        position: { from: nodeResult.position.to, to: nodeResult.position.to },
        method: 'nodeId'
      };
    }
  }

  // 1. 如果有位置且在有效范围内
  if (position && position.to <= docText.length) {
    return {
      success: true,
      position: { from: position.to, to: position.to },
      method: 'exact'
    };
  }

  // 2. 用 beforeAnchor 定位（在锚点后面插入）
  if (beforeAnchor) {
    const index = docText.lastIndexOf(beforeAnchor);
    if (index >= 0) {
      const insertPos = index + beforeAnchor.length;
      return {
        success: true,
        position: { from: insertPos, to: insertPos },
        method: 'anchor'
      };
    }
  }

  // 3. 用 afterAnchor 定位（在锚点前面插入）
  if (afterAnchor) {
    const index = docText.indexOf(afterAnchor);
    if (index >= 0) {
      return {
        success: true,
        position: { from: index, to: index },
        method: 'anchor'
      };
    }
  }

  // 4. 默认插入到文档末尾
  return {
    success: true,
    position: { from: docText.length, to: docText.length },
    method: 'exact'
  };
}
