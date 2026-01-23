/**
 * localStorage 配额问题验证工具
 * 用于确认刷新后退出登录的真实原因
 */

import { analyzeLocalStorage } from './storageDebug';

interface ValidationResult {
  issue: string;
  severity: 'critical' | 'warning' | 'info';
  description: string;
  solution?: string;
}

/**
 * 验证 localStorage 配额状态
 */
export function validateStorageQuota(): ValidationResult[] {
  const results: ValidationResult[] = [];
  const stats = analyzeLocalStorage();

  // 检查 1: 存储使用率
  if (stats.usage > 90) {
    results.push({
      issue: 'localStorage 使用率超过 90%',
      severity: 'critical',
      description: `当前使用: ${stats.totalFormatted} / ${stats.quotaFormatted} (${stats.usage.toFixed(2)}%)`,
      solution: '运行 storageDebug.cleanup() 清理旧数据',
    });
  } else if (stats.usage > 70) {
    results.push({
      issue: 'localStorage 使用率较高',
      severity: 'warning',
      description: `当前使用: ${stats.totalFormatted} / ${stats.quotaFormatted} (${stats.usage.toFixed(2)}%)`,
      solution: '建议定期清理旧会话',
    });
  } else {
    results.push({
      issue: 'localStorage 使用率正常',
      severity: 'info',
      description: `当前使用: ${stats.totalFormatted} / ${stats.quotaFormatted} (${stats.usage.toFixed(2)}%)`,
    });
  }

  // 检查 2: Agent 会话占用
  const sessionKeys = stats.items.filter((item) =>
    item.key.startsWith('agent_conversation_session_')
  );

  const totalSessionSize = sessionKeys.reduce((sum, item) => sum + item.size, 0);

  if (sessionKeys.length > 5) {
    results.push({
      issue: `检测到 ${sessionKeys.length} 个 Agent 会话`,
      severity: 'warning',
      description: `总占用: ${formatBytes(totalSessionSize)}`,
      solution: '建议减少到 3-5 个会话',
    });
  }

  // 检查 3: authStore 状态
  const authStorageKey = stats.items.find((item) => item.key === 'auth-storage');

  if (authStorageKey) {
    results.push({
      issue: 'authStore 状态',
      severity: 'info',
      description: `大小: ${authStorageKey.sizeFormatted}`,
    });

    // 尝试解析
    try {
      const authData = JSON.parse(localStorage.getItem('auth-storage') || '{}');
      const hasToken = !!authData.state?.token;
      const hasUser = !!authData.state?.user;
      const isAuthenticated = authData.state?.isAuthenticated;

      if (!hasToken || !hasUser || !isAuthenticated) {
        results.push({
          issue: 'authStore 状态异常',
          severity: 'critical',
          description: `token: ${hasToken}, user: ${hasUser}, isAuthenticated: ${isAuthenticated}`,
          solution: '可能是 localStorage 写入失败导致',
        });
      }
    } catch (error) {
      results.push({
        issue: 'authStore 解析失败',
        severity: 'critical',
        description: String(error),
        solution: '可能是数据损坏',
      });
    }
  } else {
    results.push({
      issue: 'authStore 不存在',
      severity: 'critical',
      description: '未找到 auth-storage 键',
      solution: '可能是从未登录，或 localStorage 被清除',
    });
  }

  // 检查 4: 最大的存储项
  if (stats.largestItems.length > 0) {
    const largest = stats.largestItems[0];
    if (largest.percentage > 30) {
      results.push({
        issue: `单个项目占用过大: ${largest.key}`,
        severity: 'warning',
        description: `占用: ${largest.sizeFormatted} (${largest.percentage.toFixed(1)}%)`,
        solution: '考虑压缩或迁移到 IndexedDB',
      });
    }
  }

  return results;
}

/**
 * 打印验证结果
 */
export function printValidationResults(): void {
  const results = validateStorageQuota();

  console.group('🔍 localStorage 配额问题验证');

  results.forEach((result) => {
    const emoji =
      result.severity === 'critical' ? '❌' : result.severity === 'warning' ? '⚠️' : '✅';

    console.log(`\n${emoji} ${result.issue}`);
    console.log(`   ${result.description}`);
    if (result.solution) {
      console.log(`   💡 解决方案: ${result.solution}`);
    }
  });

  console.groupEnd();

  // 总结
  const criticalCount = results.filter((r) => r.severity === 'critical').length;
  const warningCount = results.filter((r) => r.severity === 'warning').length;

  if (criticalCount > 0) {
    console.error(
      `\n🚨 发现 ${criticalCount} 个严重问题，${warningCount} 个警告`
    );
    console.error('建议立即处理严重问题');
  } else if (warningCount > 0) {
    console.warn(`\n⚠️ 发现 ${warningCount} 个警告`);
    console.warn('建议定期清理以避免问题');
  } else {
    console.log('\n✅ 未发现问题');
  }
}

/**
 * 测试写入 localStorage
 */
export async function testStorageWrite(): Promise<void> {
  console.group('🧪 测试 localStorage 写入');

  const testKey = 'storage_test_' + Date.now();
  const testSizes = [
    { size: 10, label: '10 KB' },
    { size: 100, label: '100 KB' },
    { size: 500, label: '500 KB' },
    { size: 1000, label: '1 MB' },
  ];

  for (const test of testSizes) {
    try {
      const data = 'x'.repeat(test.size * 1024);
      localStorage.setItem(testKey, data);
      localStorage.removeItem(testKey);
      console.log(`✅ ${test.label}: 写入成功`);
    } catch (error) {
      if (isQuotaExceeded(error)) {
        console.error(`❌ ${test.label}: 配额超限`);
        console.error('   当前存储无法容纳此大小的数据');
        break;
      } else {
        console.error(`❌ ${test.label}: 写入失败`, error);
      }
    }
  }

  console.groupEnd();
}

/**
 * 模拟刷新测试
 */
export function testRefreshPersistence(): void {
  console.group('🔄 测试刷新持久化');

  // 检查当前 authStore 状态
  try {
    const authData = JSON.parse(localStorage.getItem('auth-storage') || '{}');
    console.log('当前 authStore 状态:', {
      hasState: !!authData.state,
      hasToken: !!authData.state?.token,
      hasUser: !!authData.state?.user,
      isAuthenticated: authData.state?.isAuthenticated,
    });

    console.log('\n💡 提示：');
    console.log('1. 刷新页面（F5）');
    console.log('2. 再次运行此测试');
    console.log('3. 对比状态是否一致');
    console.log('4. 如果状态丢失，说明持久化失败');
  } catch (error) {
    console.error('❌ 读取 authStore 失败:', error);
  }

  console.groupEnd();
}

/**
 * 检查是否是配额超限错误
 */
function isQuotaExceeded(error: unknown): boolean {
  if (!error || typeof error !== 'object') return false;
  const name = (error as { name?: string }).name;
  return name === 'QuotaExceededError' || name === 'NS_ERROR_DOM_QUOTA_REACHED';
}

/**
 * 格式化字节
 */
function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`;
}

/**
 * 在开发模式下暴露到全局
 */
if (import.meta.env.DEV) {
  (window as any).storageValidation = {
    validate: printValidationResults,
    testWrite: testStorageWrite,
    testRefresh: testRefreshPersistence,
  };

  console.log(
    '💡 localStorage 验证工具已加载，使用方法：\n' +
      '  storageValidation.validate()     - 验证存储状态\n' +
      '  storageValidation.testWrite()    - 测试写入能力\n' +
      '  storageValidation.testRefresh()  - 测试刷新持久化'
  );
}
