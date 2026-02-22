import React, { useState, useEffect, useCallback } from 'react';
import { Save, Plus, Trash2, AlertCircle, Loader2, Settings } from 'lucide-react';
import { Card, Button } from '../../components/common';
import { ApiAdapter } from '@/services/ApiAdapter';

const api = new ApiAdapter();

interface ModelPriceEntry {
  input: number;
  cachedInput: number;
  output: number;
  reasoning: number;
  cacheCreation: number;
}

type ModelPricing = Record<string, ModelPriceEntry>;

const PRICE_FIELDS: { key: keyof ModelPriceEntry; label: string }[] = [
  { key: 'input', label: 'Input' },
  { key: 'cachedInput', label: 'Cached Input' },
  { key: 'output', label: 'Output' },
  { key: 'reasoning', label: 'Reasoning' },
  { key: 'cacheCreation', label: 'Cache Creation' },
];

const AdminPricingView: React.FC = () => {
  const [creditsPerDollar, setCreditsPerDollar] = useState<number>(12400);
  const [modelPricing, setModelPricing] = useState<ModelPricing>({});
  const [newModelName, setNewModelName] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const loadConfig = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const [rateRes, pricingRes] = await Promise.all([
        api.get<{ key: string; value: any }>('/admin/config/credits_per_dollar'),
        api.get<{ key: string; value: any }>('/admin/config/model_pricing'),
      ]);
      setCreditsPerDollar(typeof rateRes.value === 'number' ? rateRes.value : parseInt(rateRes.value));
      setModelPricing(pricingRes.value as ModelPricing);
    } catch (err: any) {
      setError(err.message || '加载配置失败');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadConfig();
  }, [loadConfig]);

  const showSuccess = (msg: string) => {
    setSuccessMsg(msg);
    setTimeout(() => setSuccessMsg(null), 3000);
  };

  // 保存积分汇率
  const handleSaveRate = async () => {
    if (!creditsPerDollar || creditsPerDollar < 1) {
      setError('积分汇率必须为正整数（最小值 1）');
      return;
    }
    try {
      setSaving('rate');
      await api.put('/admin/config/credits_per_dollar', { value: creditsPerDollar });
      showSuccess(`积分汇率已更新为 ${creditsPerDollar.toLocaleString()}`);
    } catch (err: any) {
      setError(err.message || '保存汇率失败');
    } finally {
      setSaving(null);
    }
  };

  const handleSavePricing = async () => {
    try {
      setSaving('pricing');
      await api.put('/admin/config/model_pricing', { value: modelPricing });
      showSuccess('模型定价已保存');
    } catch (err: any) {
      setError(err.message || '保存定价失败');
    } finally {
      setSaving(null);
    }
  };

  const handlePriceChange = (model: string, field: keyof ModelPriceEntry, value: string) => {
    const num = parseFloat(value) || 0;
    setModelPricing(prev => ({
      ...prev,
      [model]: { ...prev[model], [field]: num },
    }));
  };

  const handleAddModel = () => {
    const name = newModelName.trim();
    if (!name || modelPricing[name]) return;
    setModelPricing(prev => ({
      ...prev,
      [name]: { input: 1.0, cachedInput: 0.5, output: 2.0, reasoning: 2.0, cacheCreation: 1.0 },
    }));
    setNewModelName('');
  };

  const handleDeleteModel = (model: string) => {
    if (model === 'default') return;
    setModelPricing(prev => {
      const next = { ...prev };
      delete next[model];
      return next;
    });
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">定价设置</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">管理模型定价和积分汇率</p>
        </div>
        <Card>
          <div className="p-12 text-center">
            <Settings className="w-16 h-16 mx-auto mb-4 text-gray-300 dark:text-gray-600 animate-pulse" />
            <p className="text-gray-500 dark:text-gray-400">加载配置中...</p>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">定价设置</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">管理模型定价和积分汇率，保存后立即生效</p>
      </div>

      {/* 全局提示 */}
      {error && (
        <div className="flex items-center gap-2 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-400 text-sm">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          {error}
          <button onClick={() => setError(null)} className="ml-auto text-red-500 hover:text-red-700">×</button>
        </div>
      )}
      {successMsg && (
        <div className="p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg text-green-700 dark:text-green-400 text-sm">
          ✓ {successMsg}
        </div>
      )}

      {/* 积分汇率 */}
      <Card background="blue">
        <div className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">积分汇率</h3>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600 dark:text-gray-400">1 USD =</span>
            <input
              type="number"
              value={creditsPerDollar}
              onChange={(e) => setCreditsPerDollar(parseInt(e.target.value) || 0)}
              className="w-32 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 text-right font-mono"
            />
            <span className="text-sm text-gray-600 dark:text-gray-400">积分</span>
            <Button
              size="sm"
              onClick={handleSaveRate}
              disabled={saving === 'rate'}
            >
              {saving === 'rate' ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4 mr-1" />}
              保存
            </Button>
          </div>
        </div>
      </Card>

      {/* 模型定价 */}
      <Card background="blue">
        <div className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">模型定价 ($/M tokens)</h3>
            <Button size="sm" onClick={handleSavePricing} disabled={saving === 'pricing'}>
              {saving === 'pricing' ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4 mr-1" />}
              保存定价
            </Button>
          </div>

          <div className="space-y-6">
            {Object.entries(modelPricing).map(([modelName, prices]) => (
              <div key={modelName} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-gray-900 dark:text-gray-100">● {modelName}</span>
                    {modelName === 'default' && (
                      <span className="text-xs px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 rounded">兜底</span>
                    )}
                  </div>
                  {modelName !== 'default' && (
                    <button
                      onClick={() => handleDeleteModel(modelName)}
                      className="text-red-400 hover:text-red-600 dark:hover:text-red-300 transition-colors"
                      title="删除模型"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  )}
                </div>
                <div className="grid grid-cols-5 gap-3">
                  {PRICE_FIELDS.map(({ key, label }) => (
                    <div key={key}>
                      <label className="block text-xs text-gray-500 dark:text-gray-400 mb-1">{label}</label>
                      <input
                        type="number"
                        step="0.001"
                        value={prices[key]}
                        onChange={(e) => handlePriceChange(modelName, key, e.target.value)}
                        className="w-full px-2.5 py-1.5 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 text-right font-mono text-sm"
                      />
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* 添加新模型 */}
          <div className="mt-4 flex items-center gap-2">
            <input
              type="text"
              value={newModelName}
              onChange={(e) => setNewModelName(e.target.value)}
              placeholder="模型名称（如 gpt-4o）"
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 text-sm"
              onKeyDown={(e) => e.key === 'Enter' && handleAddModel()}
            />
            <Button variant="outline" size="sm" onClick={handleAddModel} disabled={!newModelName.trim()}>
              <Plus className="w-4 h-4 mr-1" />
              添加模型
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default AdminPricingView;
