import React, { useState, useEffect } from 'react';
import { Plus, Cpu } from 'lucide-react';
import { Button, Card, Loading } from '../../components/common';
import { DataService } from '../../services/DataService';
import { useGlobalStore } from '../../store/globalStore';
import type { AIModel } from '../../types';
import { getTypicalCostRange } from '../../utils/costCalculator';

/**
 * AdminAIModelsView 组件 - AI 模型管理页面
 *
 * 功能：
 * - 显示 AI 模型列表
 * - 表格形式展示
 * - 使用 DataService.getAIModels
 */
const AdminAIModelsView: React.FC = () => {
  const [models, setModels] = useState<AIModel[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const { showToast } = useGlobalStore();

  /**
   * 加载 AI 模型列表
   */
  useEffect(() => {
    const loadModels = async () => {
      try {
        setIsLoading(true);
        const data = await DataService.getAIModels();
        setModels(data);
      } catch (err) {
        const message = err instanceof Error ? err.message : '加载 AI 模型失败';
        showToast('error', message);
      } finally {
        setIsLoading(false);
      }
    };

    loadModels();
  }, [showToast]);

  /**
   * 处理添加模型
   */
  const handleAddModel = () => {
    showToast('info', '添加模型功能待实现');
  };

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">AI 模型管理</h1>
          <p className="mt-2 text-gray-600">配置和管理 AI 模型</p>
        </div>
        <Button variant="primary" icon={<Plus className="w-5 h-5" />} onClick={handleAddModel}>
          添加模型
        </Button>
      </div>

      <Card>
        {/* 功能开发中占位符 */}
        <div className="p-12 text-center">
          <Cpu className="w-16 h-16 mx-auto mb-4 text-gray-300" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">功能开发中</h3>
          <p className="text-gray-500 mb-4">AI模型管理功能将在未来版本中开放</p>
          <div className="max-w-md mx-auto text-left bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600 mb-2">
              <strong>当前配置方式：</strong>
            </p>
            <p className="text-xs text-gray-500">
              请通过后端 <code className="bg-white px-1 py-0.5 rounded">.env</code> 文件配置AI模型：
            </p>
            <pre className="text-xs text-gray-600 mt-2 bg-white p-2 rounded">
OPENAI_API_KEY=your_key{'\n'}
OPENAI_MODEL=gemini-2.5-pro
            </pre>
          </div>
        </div>
        
        {/* 原来的代码 - 暂时隐藏 */}
        {false && models.length === 0 ? (
          <div className="p-6 text-center text-gray-500">
            <Cpu className="w-12 h-12 mx-auto mb-4 text-gray-400" />
            <p>暂无 AI 模型配置</p>
          </div>
        ) : false && (
          <div className="p-6">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">模型名称</th>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">提供商</th>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">类型</th>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">成本</th>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">状态</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {models.map((model) => (
                    <tr key={model.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 text-sm font-medium text-gray-900">{model.name}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">{model.provider}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">
                        {model.type}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600">
                        {getTypicalCostRange(model)}
                      </td>
                      <td className="px-4 py-3 text-sm">
                        <span
                          className={`px-2 py-1 rounded-full text-xs font-medium ${
                            model.status === 'active'
                              ? 'bg-green-100 text-green-700'
                              : model.status === 'maintenance'
                              ? 'bg-yellow-100 text-yellow-700'
                              : 'bg-gray-100 text-gray-700'
                          }`}
                        >
                          {model.status === 'active' ? '启用中' : model.status === 'maintenance' ? '维护中' : '已禁用'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
};

export default AdminAIModelsView;
