import React, { useEffect, useState } from 'react';
import { Card, Button } from '../../components/common';
import { useCreditsStore } from '../../store/creditsStore';
import { TRANSACTION_TYPE_CONFIG, TransactionType, formatTransactionDescription } from '../../types/credits';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const ServiceUsageView: React.FC = () => {
  const {
    transactions,
    transactionTotal,
    transactionPage,
    transactionPageSize,
    transactionTotalPages,
    isLoading,
    fetchTransactions,
  } = useCreditsStore();

  const [selectedType, setSelectedType] = useState<TransactionType | 'all'>('all');

  useEffect(() => {
    fetchTransactions(1, 20, selectedType === 'all' ? undefined : selectedType);
  }, [fetchTransactions, selectedType]);

  const handlePageChange = (page: number) => {
    fetchTransactions(page, transactionPageSize, selectedType === 'all' ? undefined : selectedType);
  };

  const handleTypeChange = (type: TransactionType | 'all') => {
    setSelectedType(type);
  };

  if (isLoading && transactions.length === 0) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-gray-500">加载中...</div>
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto overflow-x-hidden bg-gray-50 dark:bg-gray-900">
      <div className="w-[1152px] mx-auto p-6 space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">使用记录</h1>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">查看您的积分交易流水</p>
        </div>

        <Card padding="lg">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">积分流水</h2>
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-600 dark:text-gray-400">筛选类型:</span>
                <select
                  value={selectedType}
                  onChange={(e) => handleTypeChange(e.target.value as TransactionType | 'all')}
                  className="px-3 py-1.5 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="all">全部</option>
                  <option value="recharge">充值</option>
                  <option value="consume">消费</option>
                  <option value="gift">赠送</option>
                  <option value="expire">过期</option>
                  <option value="refund">退款</option>
                </select>
              </div>
            </div>

            {transactions.length === 0 ? (
              <div className="text-center py-12 text-gray-500">暂无交易记录</div>
            ) : (
              <>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-gray-200 dark:border-gray-700">
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                          类型
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                          积分
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                          描述
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                          交易前
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                          交易后
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                          时间
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                      {transactions.map((transaction) => {
                        const config = TRANSACTION_TYPE_CONFIG[transaction.type];
                        return (
                          <tr key={transaction.id} className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                            <td className="px-4 py-4 whitespace-nowrap">
                              <div className={`inline-flex px-2 py-1 rounded text-xs font-medium ${config.color}`}>
                                {config.icon} {config.label}
                              </div>
                            </td>
                            <td className="px-4 py-4 whitespace-nowrap">
                              <span
                                className={`text-sm font-semibold ${
                                  transaction.amount >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
                                }`}
                              >
                                {transaction.amount >= 0 ? '+' : ''}
                                {transaction.amount.toFixed(2)}
                              </span>
                            </td>
                            <td className="px-4 py-4">
                              <span className="text-sm text-gray-700 dark:text-gray-300">{formatTransactionDescription(transaction.description)}</span>
                            </td>
                            <td className="px-4 py-4 whitespace-nowrap">
                              <span className="text-sm text-gray-600 dark:text-gray-400">
                                {transaction.balanceBefore.toFixed(2)}
                              </span>
                            </td>
                            <td className="px-4 py-4 whitespace-nowrap">
                              <span className="text-sm text-gray-600 dark:text-gray-400">
                                {transaction.balanceAfter.toFixed(2)}
                              </span>
                            </td>
                            <td className="px-4 py-4 whitespace-nowrap">
                              <span className="text-xs text-gray-500 dark:text-gray-400">
                                {formatDistanceToNow(new Date(transaction.createdAt), {
                                  addSuffix: true,
                                  locale: zhCN,
                                })}
                              </span>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>

                <div className="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
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
              </>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
};

export default ServiceUsageView;
