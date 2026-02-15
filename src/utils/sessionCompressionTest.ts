/**
 * Agent 会话压缩效果测试
 *
 * 使用方法：
 * 1. 在浏览器控制台运行
 * 2. 查看当前存储使用情况
 * 3. 测试压缩效果
 */

import { analyzeLocalStorage, autoCleanupStorage } from '@/utils/storageDebug';
import {
  compressSessionMessages,
  analyzeCompression
} from '@/utils/sessionCompression';

/**
 * 测试当前所有会话的压缩效果
 */
export async function testSessionCompression() {
  console.group('🧪 测试 Agent 会话压缩效果');

  // 1. 分析当前存储使用情况
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('📊 步骤 1: 分析当前存储使用情况');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  const beforeStats = analyzeLocalStorage();
  console.log(`总使用量: ${beforeStats.totalFormatted}`);
  console.log(`使用率: ${beforeStats.usage.toFixed(2)}%`);
  console.log(`存储项数量: ${beforeStats.items.length}`);
  console.log('');

  // 2. 找到所有 Agent 会话
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('📦 步骤 2: 查找 Agent 会话');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  const sessionKeys = Object.keys(localStorage).filter(
    (key) => key.startsWith('agent_conversation_session_')
  );
  console.log(`找到 ${sessionKeys.length} 个会话`);
  console.log('');

  if (sessionKeys.length === 0) {
    console.log('⚠️ 没有找到任何会话，测试结束');
    console.groupEnd();
    return;
  }

  // 3. 测试每个会话的压缩效果
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('🔬 步骤 3: 测试压缩效果');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  let totalOriginal = 0;
  let totalCompressed = 0;
  let totalFlowItemsRemoved = 0;

  for (const key of sessionKeys.slice(0, 5)) {
    // 只测试前 5 个会话
    try {
      const sessionStr = localStorage.getItem(key);
      if (!sessionStr) continue;

      const session = JSON.parse(sessionStr);
      const { messages, title } = session;

      if (!messages || messages.length === 0) continue;

      // 压缩会话
      const compressed = compressSessionMessages(
        messages,
        'current', // 假设是当前会话
        session.id
      );

      // 分析压缩效果
      const stats = analyzeCompression(messages, compressed);

      totalOriginal += stats.originalSize;
      totalCompressed += stats.compressedSize;
      totalFlowItemsRemoved += stats.itemsRemoved;

      console.log(`\n📄 会话: ${title || '未命名'}`);
      console.log(`  消息数: ${messages.length}`);
      console.log(
        `  原始大小: ${formatBytes(stats.originalSize)}`
      );
      console.log(
        `  压缩后: ${formatBytes(stats.compressedSize)} (节省 ${(
          (1 - stats.ratio) *
          100
        ).toFixed(1)}%)`
      );
      console.log(`  移除 flowItems: ${stats.itemsRemoved} 个`);
    } catch (error) {
      console.error(`处理会话 ${key} 时出错:`, error);
    }
  }

  // 4. 总结
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('📈 步骤 4: 压缩效果总结');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(
    `总原始大小: ${formatBytes(totalOriginal)}`
  );
  console.log(
    `总压缩后: ${formatBytes(totalCompressed)}`
  );
  console.log(
    `总节省: ${formatBytes(totalOriginal - totalCompressed)} (${(
      ((totalOriginal - totalCompressed) / totalOriginal) *
      100
    ).toFixed(1)}%)`
  );
  console.log(
    `移除 flowItems 总数: ${totalFlowItemsRemoved} 个`
  );

  // 5. 建议
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('💡 优化建议');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  const savedPercentage =
    ((totalOriginal - totalCompressed) / totalOriginal) * 100;

  if (savedPercentage > 70) {
    console.log(
      '✅ 压缩效果优秀！建议启用自动压缩功能'
    );
  } else if (savedPercentage > 50) {
    console.log(
      '✅ 压缩效果良好，可以显著减少存储占用'
    );
  } else {
    console.log(
      '⚠️ 压缩效果有限，建议：'
    );
    console.log('  1. 减少保留会话数量');
    console.log('  2. 考虑使用 LZ-String 文本压缩');
    console.log('  3. 迁移到 IndexedDB 或后端存储');
  }

  console.groupEnd();
}

/**
 * 应用压缩到所有会话（谨慎使用！）
 */
export async function applyCompressionToAllSessions() {
  const confirmed = confirm(
    '⚠️ 警告：这将压缩所有会话的 flowItems 数据。\n\n' +
      '压缩后的数据无法恢复到原始状态。\n\n' +
      '建议先运行 testSessionCompression() 查看效果。\n\n' +
      '确定要继续吗？'
  );

  if (!confirmed) {
    console.log('❌ 已取消');
    return;
  }

  console.group('🔧 应用压缩到所有会话');

  const sessionKeys = Object.keys(localStorage).filter(
    (key) => key.startsWith('agent_conversation_session_')
  );

  let successCount = 0;
  let failCount = 0;

  for (const key of sessionKeys) {
    try {
      const sessionStr = localStorage.getItem(key);
      if (!sessionStr) continue;

      const session = JSON.parse(sessionStr);
      const { messages } = session;

      if (!messages || messages.length === 0) continue;

      // 压缩会话
      const compressed = compressSessionMessages(
        messages,
        'current',
        session.id
      );

      // 更新会话
      session.messages = compressed;
      localStorage.setItem(key, JSON.stringify(session));

      successCount++;
      console.log(`✅ ${session.title || '未命名'}`);
    } catch (error) {
      failCount++;
      console.error(`❌ ${key}:`, error);
    }
  }

  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`成功: ${successCount} 个`);
  console.log(`失败: ${failCount} 个`);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  // 显示压缩后的存储使用情况
  const afterStats = analyzeLocalStorage();
  console.log(`\n压缩后使用量: ${afterStats.totalFormatted}`);
  console.log(`使用率: ${afterStats.usage.toFixed(2)}%`);

  console.groupEnd();

  console.log('\n💡 提示：刷新页面以查看效果');
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
  (window as any).sessionCompressionTest = {
    test: testSessionCompression,
    apply: applyCompressionToAllSessions,
  };

  console.log(
    '💡 会话压缩测试工具已加载，使用方法：\n' +
      '  sessionCompressionTest.test()  - 测试压缩效果\n' +
      '  sessionCompressionTest.apply() - 应用压缩（谨慎！）'
  );
}
