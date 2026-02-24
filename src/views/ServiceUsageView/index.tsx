import React, { useEffect, useState } from 'react';
import { Button } from '../../components/common';
import { useCreditsStore } from '../../store/creditsStore';
import { TRANSACTION_TYPE_CONFIG, TransactionType, formatTransactionDescription } from '../../types/credits';
import type { CreditTransaction, PricingInfo } from '../../types/credits';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import { ChevronLeft, ChevronRight, ChevronDown, ChevronUp } from 'lucide-react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../../components/ui/select';

/** 前端极简兜底（仅在后端 API 完全未返回定价时使用，不含模型级别单价） */
const FALLBACK_PRICING = { input: 1.0, cachedInput: 0.5, output: 2.0, reasoning: 2.0, cacheCreation: 1.0 };

/** Token 明细展开卡片 */
const TokenDetailCard: React.FC<{
  transaction: CreditTransaction;
  pricingInfo: PricingInfo | null;
}> = ({ transaction, pricingInfo }) => {
  const d = transaction.tokenDetails;
  if (!d) return null;

  const modelPricing = pricingInfo?.modelPricing?.[d.modelName] ?? pricingInfo?.modelPricing?.['default'] ?? FALLBACK_PRICING;
  const creditsPerDollar = pricingInfo?.creditsPerDollar ?? 12400;

  // 计算 new input（排除 cache 部分）
  const newInput = Math.max(d.promptTokens - d.cacheReadTokens - d.cacheCreationTokens, 0);
  const newOutput = Math.max(d.completionTokens - d.reasoningTokens, 0);

  return (
    <div className="bg-gray-50 dark:bg-gray-800/50 px-6 py-4 text-sm">
      <div className="grid grid-cols-2 gap-6">
        {/* Token 用量 */}
        <div>
          <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Token 用量</h4>
          <div className="space-y-1 text-gray-600 dark:text-gray-400 font-mono text-xs">
            <div className="flex justify-between">
              <span>Input Tokens</span>
              <span className="text-gray-900 dark:text-gray-200">{d.promptTokens.toLocaleString()}</span>
            </div>
            {d.cacheReadTokens > 0 && (
              <div className="flex justify-between text-green-600 dark:text-green-400">
                <span>Cache Read</span>
                <span>{d.cacheReadTokens.toLocaleString()}</span>
              </div>
            )}
            {d.cacheCreationTokens > 0 && (
              <div className="flex justify-between text-blue-600 dark:text-blue-400">
                <span>Cache Create</span>
                <span>{d.cacheCreationTokens.toLocaleString()}</span>
              </div>
            )}
            <div className="flex justify-between">
              <span>Output Tokens</span>
              <span className="text-gray-900 dark:text-gray-200">{d.completionTokens.toLocaleString()}</span>
            </div>
            {d.reasoningTokens > 0 && (
              <div className="flex justify-between text-purple-600 dark:text-purple-400">
                <span>Reasoning</span>
                <span>{d.reasoningTokens.toLocaleString()}</span>
              </div>
            )}
            <div className="flex justify-between pt-1 font-medium">
              <span>Total</span>
              <span className="text-gray-900 dark:text-gray-200">{d.totalTokens.toLocaleString()}</span>
            </div>
          </div>
        </div>

        {/* 费用计算 */}
        <div>
          <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">
            费用计算
          </h4>
          <div className="space-y-1 text-gray-600 dark:text-gray-400 font-mono text-xs">
            <div className="flex justify-between">
              <span>New Input: {newInput.toLocaleString()} × ${modelPricing.input}/M</span>
              <span>${(newInput / 1_000_000 * modelPricing.input).toFixed(6)}</span>
            </div>
            {d.cacheReadTokens > 0 && (
              <div className="flex justify-between text-green-600 dark:text-green-400">
                <span>Cache Read: {d.cacheReadTokens.toLocaleString()} × ${modelPricing.cachedInput}/M</span>
                <span>${(d.cacheReadTokens / 1_000_000 * modelPricing.cachedInput).toFixed(6)}</span>
              </div>
            )}
            {d.cacheCreationTokens > 0 && (
              <div className="flex justify-between text-blue-600 dark:text-blue-400">
                <span>Cache Create: {d.cacheCreationTokens.toLocaleString()} × ${modelPricing.cacheCreation}/M</span>
                <span>${(d.cacheCreationTokens / 1_000_000 * modelPricing.cacheCreation).toFixed(6)}</span>
              </div>
            )}
            <div className="flex justify-between">
              <span>Output: {newOutput.toLocaleString()} × ${modelPricing.output}/M</span>
              <span>${(newOutput / 1_000_000 * modelPricing.output).toFixed(6)}</span>
            </div>
            {d.reasoningTokens > 0 && (
              <div className="flex justify-between text-purple-600 dark:text-purple-400">
                <span>Reasoning: {d.reasoningTokens.toLocaleString()} × ${modelPricing.reasoning}/M</span>
                <span>${(d.reasoningTokens / 1_000_000 * modelPricing.reasoning).toFixed(6)}</span>
              </div>
            )}
            <div className="flex justify-between pt-1 font-medium text-gray-900 dark:text-gray-200">
              <span>USD 合计</span>
              <span>${d.totalCost.toFixed(6)}</span>
            </div>
            <div className="flex justify-between text-gray-900 dark:text-gray-200">
              <span>积分换算</span>
              <span>${d.totalCost.toFixed(6)} × {creditsPerDollar.toLocaleString()} = {(d.totalCost * creditsPerDollar).toFixed(2)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const ServiceUsageView: React.FC = () => {
  const {
    transactions,
    transactionTotal,
    transactionPage,
    transactionPageSize,
    transactionTotalPages,
    pricingInfo,
    isLoading,
    fetchTransactions,
  } = useCreditsStore();

  const [selectedType, setSelectedType] = useState<TransactionType | 'all'>('all');
  const [expandedId, setExpandedId] = useState<string | null>(null);

  useEffect(() => {
    fetchTransactions(1, 20, selectedType === 'all' ? undefined : selectedType);
  }, [fetchTransactions, selectedType]);

  const handlePageChange = (page: number) => {
    setExpandedId(null);
    fetchTransactions(page, transactionPageSize, selectedType === 'all' ? undefined : selectedType);
  };

  const handleTypeChange = (type: TransactionType | 'all') => {
    setExpandedId(null);
    setSelectedType(type);
  };

  const toggleExpand = (transaction: CreditTransaction) => {
    if (transaction.tokenDetails) {
      setExpandedId(expandedId === transaction.id ? null : transaction.id);
    }
  };

  if (isLoading && transactions.length === 0) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-gray-500">加载中...</div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-white dark:bg-gray-900">
      {/* ── 固定页眉 ── */}
      <div className="flex-shrink-0 flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-slate-700">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">使用记录</h2>
        <div className="flex items-center space-x-2">
          <Select
            value={selectedType}
            onValueChange={(value) => handleTypeChange(value as TransactionType | 'all')}
          >
            <SelectTrigger className="w-[100px]" size="sm">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">全部</SelectItem>
              <SelectItem value="recharge">充值</SelectItem>
              <SelectItem value="consume">消费</SelectItem>
              <SelectItem value="gift">赠送</SelectItem>
              <SelectItem value="expire">过期</SelectItem>
              <SelectItem value="refund">退款</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* ── 可滚动表格 ── */}
      {transactions.length === 0 ? (
        <div className="flex-1 flex items-center justify-center text-gray-500">暂无交易记录</div>
      ) : (
        <div className="flex-1 overflow-y-auto min-h-0">
          <table className="w-full table-fixed">
            <thead className="sticky top-0 bg-white dark:bg-gray-900 z-10">
              <tr className="border-b border-gray-200 dark:border-slate-700">
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  详情
                </th>
                <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider w-32">
                  日期
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider w-32">
                  积分变更
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 dark:divide-slate-700/50">
              {transactions.map((transaction) => {
                const config = TRANSACTION_TYPE_CONFIG[transaction.type];
                const isExpanded = expandedId === transaction.id;
                const hasDetails = !!transaction.tokenDetails;

                return (
                  <React.Fragment key={transaction.id}>
                    <tr
                      className={`transition-colors ${hasDetails ? 'cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700/50' : ''}`}
                      onClick={() => toggleExpand(transaction)}
                    >
                      <td className="px-6 py-3.5">
                        <div className="flex items-center gap-2 min-w-0">
                          <span className="w-4 flex-shrink-0 text-gray-400">
                            {hasDetails ? (
                              isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />
                            ) : null}
                          </span>
                          <span className="text-sm text-gray-700 dark:text-gray-300">
                            {formatTransactionDescription(transaction.description, transaction.type) || '-'}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-3.5 text-center">
                        <span className="text-xs text-gray-500 dark:text-gray-400">
                          {formatDistanceToNow(new Date(transaction.createdAt), {
                            addSuffix: true,
                            locale: zhCN,
                          })}
                        </span>
                      </td>
                      <td className="px-6 py-3.5 text-right">
                        <span
                          className={`text-sm font-semibold tabular-nums ${
                            transaction.amount >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
                          }`}
                        >
                          {transaction.amount >= 0 ? '+' : ''}
                          {transaction.amount.toFixed(2)}
                        </span>
                      </td>
                    </tr>
                    {isExpanded && transaction.tokenDetails && (
                      <tr>
                        <td colSpan={3} className="p-0">
                          <TokenDetailCard transaction={transaction} pricingInfo={pricingInfo} />
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* ── 固定页脚 ── */}
      {transactions.length > 0 && (
        <div className="flex-shrink-0 flex items-center justify-between px-6 py-3 border-t border-gray-200 dark:border-slate-700">
          <div className="text-sm text-gray-600 dark:text-gray-400">
            共 {transactionTotal} 条记录，第 {transactionPage} / {transactionTotalPages} 页
          </div>
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => handlePageChange(transactionPage - 1)}
              disabled={transactionPage <= 1 || isLoading}
            >
              <ChevronLeft className="w-4 h-4" />
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => handlePageChange(transactionPage + 1)}
              disabled={transactionPage >= transactionTotalPages || isLoading}
            >
              <ChevronRight className="w-4 h-4" />
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ServiceUsageView;
