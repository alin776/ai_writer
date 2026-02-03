import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Wallet, TrendingUp, TrendingDown, Gift, ArrowRight } from 'lucide-react';
import { Card } from '../../components/common';
import { useCreditsStore } from '../../store/creditsStore';
import { TRANSACTION_TYPE_CONFIG, formatTransactionDescription } from '../../types/credits';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale';

const ServiceCreditsView: React.FC = () => {
  const { balance, transactions, isLoading, fetchBalance, fetchTransactions } = useCreditsStore();

  useEffect(() => {
    fetchBalance();
    fetchTransactions(1, 5);
  }, [fetchBalance, fetchTransactions]);

  if (isLoading && !balance) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-gray-500">加载中...</div>
      </div>
    );
  }

  return (
    <div className="h-full overflow-auto bg-gray-50 dark:bg-gray-900">
      <div className="max-w-5xl mx-auto p-6 space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">我的积分</h1>
          <p className="mt-1 text-sm text-gray-500">查看您的积分余额和使用情况</p>
        </div>

        <Card padding="lg">
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Wallet className="w-5 h-5 text-amber-600 dark:text-amber-500" />
              <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">当前余额</h2>
            </div>

            <div className="flex items-baseline space-x-2">
              <span className="text-4xl font-bold text-amber-600">
                {balance?.balance.toFixed(2) || '0.00'}
              </span>
              <span className="text-lg text-gray-500">积分</span>
            </div>

            <div className="text-sm text-gray-500">
              {balance?.expiresAt ? (
                <span>到期时间: {new Date(balance.expiresAt).toLocaleDateString()}</span>
              ) : (
                <span>永不过期</span>
              )}
            </div>

            <div>
              <Link
                to="/service/obtain"
                className="inline-flex items-center px-4 py-2 bg-amber-600 text-white hover:text-white rounded hover:bg-amber-700 transition-colors text-sm font-semibold"
                style={{ color: 'white' }}
              >
                <Gift className="w-4 h-4 mr-2 text-white" />
                兑换积分
              </Link>
            </div>
          </div>
        </Card>

        <Card padding="lg">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">积分统计</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-green-50 dark:bg-green-900/30 rounded-lg">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600 dark:text-gray-400">累计充值</span>
                <TrendingUp className="w-4 h-4 text-green-600" />
              </div>
              <div className="mt-2 text-2xl font-bold text-green-600">
                {balance?.totalRecharged.toFixed(2) || '0.00'}
              </div>
            </div>

            <div className="p-4 bg-red-50 dark:bg-red-900/30 rounded-lg">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600 dark:text-gray-400">累计消耗</span>
                <TrendingDown className="w-4 h-4 text-red-600" />
              </div>
              <div className="mt-2 text-2xl font-bold text-red-600">
                {balance?.totalConsumed.toFixed(2) || '0.00'}
              </div>
            </div>

            <div className="p-4 bg-blue-50 dark:bg-blue-900/30 rounded-lg">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600 dark:text-gray-400">累计赠送</span>
                <Gift className="w-4 h-4 text-blue-600" />
              </div>
              <div className="mt-2 text-2xl font-bold text-blue-600">
                {balance?.totalGifted.toFixed(2) || '0.00'}
              </div>
            </div>
          </div>
        </Card>

        <Card padding="lg">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">最近交易</h2>
            <Link
              to="/service/usage"
              className="flex items-center text-sm text-blue-600 hover:text-blue-700"
            >
              查看全部
              <ArrowRight className="w-4 h-4 ml-1" />
            </Link>
          </div>

          {transactions.length === 0 ? (
            <div className="text-center py-8 text-gray-500">暂无交易记录</div>
          ) : (
            <div className="space-y-3">
              {transactions.slice(0, 5).map((transaction) => {
                const config = TRANSACTION_TYPE_CONFIG[transaction.type];
                return (
                  <div
                    key={transaction.id}
                    className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                  >
                    <div className="flex items-center space-x-3">
                      <div className={`px-2 py-1 rounded text-xs font-medium ${config.color}`}>
                        {config.icon} {config.label}
                      </div>
                      <span className="text-sm text-gray-700 dark:text-gray-300">{formatTransactionDescription(transaction.description)}</span>
                    </div>

                    <div className="flex items-center space-x-4">
                      <span
                        className={`text-sm font-semibold ${
                          transaction.amount >= 0 ? 'text-green-600' : 'text-red-600'
                        }`}
                      >
                        {transaction.amount >= 0 ? '+' : ''}
                        {transaction.amount.toFixed(2)}
                      </span>
                      <span className="text-xs text-gray-500">
                        {formatDistanceToNow(new Date(transaction.createdAt), {
                          addSuffix: true,
                          locale: zhCN,
                        })}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default ServiceCreditsView;
