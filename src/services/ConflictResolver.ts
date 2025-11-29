/**
 * 冲突解决服务 - 处理用户和Agent同时编辑时的冲突
 *
 * 策略:
 * - 乐观锁冲突：重试机制 + 用户确认
 * - 内容合并：智能三方合并
 */

export interface ConflictResolution {
  strategy: 'user_wins' | 'agent_wins' | 'merge' | 'manual';
  resolved_content: string;
  conflict_regions?: Array<{
    start: number;
    end: number;
    user_version: string;
    agent_version: string;
  }>;
}

export interface ConflictInfo {
  chapter_id: string;
  base_version: number;
  user_content: string;
  agent_content: string;
  base_content: string;
}

class ConflictResolver {
  /**
   * 自动解决冲突
   *
   * 策略优先级：
   * 1. 无冲突 -> 直接合并
   * 2. 非重叠编辑 -> 三方合并
   * 3. 重叠编辑 -> 标记冲突区域，提示用户手动解决
   */
  async resolveConflict(conflict: ConflictInfo): Promise<ConflictResolution> {
    const {
      user_content,
      agent_content,
      base_content
    } = conflict;

    // 1. 检查是否完全相同（无冲突）
    if (user_content === agent_content) {
      return {
        strategy: 'user_wins', // 或 'agent_wins'，无所谓
        resolved_content: user_content
      };
    }

    // 2. 检查用户是否未修改（Agent wins）
    if (user_content === base_content) {
      return {
        strategy: 'agent_wins',
        resolved_content: agent_content
      };
    }

    // 3. 检查Agent是否未修改（User wins）
    if (agent_content === base_content) {
      return {
        strategy: 'user_wins',
        resolved_content: user_content
      };
    }

    // 4. 尝试智能合并（非重叠编辑）
    const mergeResult = await this.attemptMerge(
      base_content,
      user_content,
      agent_content
    );

    if (mergeResult.success) {
      return {
        strategy: 'merge',
        resolved_content: mergeResult.content
      };
    }

    // 5. 存在冲突，需要手动解决
    return {
      strategy: 'manual',
      resolved_content: user_content, // 默认保留用户版本
      conflict_regions: mergeResult.conflicts
    };
  }

  /**
   * 尝试三方合并
   *
   * 算法：
   * - 基于 diff-match-patch 的三方合并
   * - 检测非重叠编辑区域
   */
  private async attemptMerge(
    base: string,
    user: string,
    agent: string
  ): Promise<{
    success: boolean;
    content: string;
    conflicts?: Array<{
      start: number;
      end: number;
      user_version: string;
      agent_version: string;
    }>;
  }> {
    // 简化实现：使用启发式判断
    // 如果用户和Agent修改的区域不重叠，可以合并

    const baseLines = base.split('\n');
    const userLines = user.split('\n');
    const agentLines = agent.split('\n');

    // 计算用户和Agent相对于base的diff
    const userDiff = this.computeLineDiff(baseLines, userLines);
    const agentDiff = this.computeLineDiff(baseLines, agentLines);

    // 检查是否有重叠编辑
    const hasOverlap = this.checkOverlap(userDiff.changed, agentDiff.changed);

    if (!hasOverlap) {
      // 无重叠，可以自动合并
      const merged = this.applyBothDiffs(baseLines, userDiff, agentDiff);
      return {
        success: true,
        content: merged.join('\n')
      };
    }

    // 有重叠，标记冲突区域
    const conflicts = this.findConflictRegions(
      base,
      user,
      agent,
      userDiff.changed,
      agentDiff.changed
    );

    return {
      success: false,
      content: user, // 默认返回用户版本
      conflicts
    };
  }

  /**
   * 计算行级别的diff
   */
  private computeLineDiff(
    base: string[],
    modified: string[]
  ): {
    changed: Set<number>; // 被修改的行号（基于base）
  } {
    const changed = new Set<number>();

    // 简化：逐行比较
    const minLen = Math.min(base.length, modified.length);
    for (let i = 0; i < minLen; i++) {
      if (base[i] !== modified[i]) {
        changed.add(i);
      }
    }

    // 处理长度变化
    if (base.length !== modified.length) {
      for (let i = minLen; i < Math.max(base.length, modified.length); i++) {
        changed.add(i);
      }
    }

    return { changed };
  }

  /**
   * 检查两个修改集合是否有重叠
   */
  private checkOverlap(set1: Set<number>, set2: Set<number>): boolean {
    for (const line of set1) {
      if (set2.has(line)) {
        return true;
      }
    }
    return false;
  }

  /**
   * 应用两个不重叠的diff
   */
  private applyBothDiffs(
    base: string[],
    userDiff: { changed: Set<number> },
    agentDiff: { changed: Set<number> }
  ): string[] {
    // 简化实现：假设已经检查过无重叠
    // 直接应用agent的修改（因为user和agent修改不同的行）

    // TODO: 实现更复杂的合并逻辑
    // 这里只是占位实现
    return base;
  }

  /**
   * 找到冲突区域
   */
  private findConflictRegions(
    base: string,
    user: string,
    agent: string,
    userChanged: Set<number>,
    agentChanged: Set<number>
  ): Array<{
    start: number;
    end: number;
    user_version: string;
    agent_version: string;
  }> {
    const conflicts: Array<{
      start: number;
      end: number;
      user_version: string;
      agent_version: string;
    }> = [];

    // 找到重叠的行
    const overlapLines: number[] = [];
    for (const line of userChanged) {
      if (agentChanged.has(line)) {
        overlapLines.push(line);
      }
    }

    if (overlapLines.length === 0) {
      return conflicts;
    }

    // 合并连续的冲突行
    overlapLines.sort((a, b) => a - b);

    let start = overlapLines[0];
    let end = overlapLines[0];

    for (let i = 1; i < overlapLines.length; i++) {
      if (overlapLines[i] === end + 1) {
        end = overlapLines[i];
      } else {
        // 形成一个冲突区域
        conflicts.push({
          start,
          end,
          user_version: this.extractLines(user, start, end),
          agent_version: this.extractLines(agent, start, end)
        });
        start = overlapLines[i];
        end = overlapLines[i];
      }
    }

    // 添加最后一个区域
    conflicts.push({
      start,
      end,
      user_version: this.extractLines(user, start, end),
      agent_version: this.extractLines(agent, start, end)
    });

    return conflicts;
  }

  /**
   * 提取指定行范围的内容
   */
  private extractLines(content: string, start: number, end: number): string {
    const lines = content.split('\n');
    return lines.slice(start, end + 1).join('\n');
  }

  /**
   * 手动解决冲突
   *
   * @param conflict 冲突信息
   * @param resolution 用户选择的解决方案
   */
  async manualResolve(
    conflict: ConflictInfo,
    resolution: {
      strategy: 'user' | 'agent' | 'custom';
      custom_content?: string;
    }
  ): Promise<string> {
    switch (resolution.strategy) {
      case 'user':
        return conflict.user_content;
      case 'agent':
        return conflict.agent_content;
      case 'custom':
        return resolution.custom_content || conflict.user_content;
      default:
        return conflict.user_content;
    }
  }

  /**
   * 重试机制：当乐观锁失败时，自动重试
   *
   * @param maxRetries 最大重试次数
   * @param operation 要执行的操作（返回新的version）
   */
  async retryWithConflictResolution<T>(
    maxRetries: number,
    operation: (expectedVersion: number) => Promise<{
      success: boolean;
      result?: T;
      conflict?: ConflictInfo;
    }>
  ): Promise<{ success: boolean; result?: T; conflict?: ConflictInfo }> {
    let currentVersion = 0; // 初始版本（应该从外部获取）

    for (let attempt = 0; attempt < maxRetries; attempt++) {
      const result = await operation(currentVersion);

      if (result.success) {
        return result;
      }

      // 失败了，尝试解决冲突
      if (result.conflict) {
        const resolution = await this.resolveConflict(result.conflict);

        if (resolution.strategy === 'manual') {
          // 需要用户手动介入
          return {
            success: false,
            conflict: result.conflict
          };
        }

        // 自动解决成功，更新版本号并重试
        currentVersion = result.conflict.base_version + 1;
        continue;
      }

      // 其他错误，停止重试
      return result;
    }

    // 达到最大重试次数
    return {
      success: false
    };
  }
}

// 单例导出
export const conflictResolver = new ConflictResolver();
export default conflictResolver;
