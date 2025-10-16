/**
 * AI 续写配置弹窗
 * 让用户配置详细的续写参数
 * 设计规范：极简主义，清晰层级，遵循 design_system.md
 */
import React, { useState, useEffect } from 'react';
import { X, Sparkles, Info, Plus, Trash2 } from 'lucide-react';

export interface AIContinueConfig {
  // 模块二：背景与上下文（自动提取，不在UI显示）
  lastChapterContext: string; // 最新章节结尾（自动提取最后1000字）
  focusCharacter: string; // 焦点人物
  characterStatus: string; // 角色状态
  coreLocation: string; // 核心地点
  environmentStatus: string; // 环境状态
  settingConstraints: string; // 关键设定限制
  styleAdjectives: string; // 文风形容词（3个）
  emotionalTone: string; // 情绪基调
  narrativePerspective: '第一人称' | '第三人称受限视角' | '全知视角'; // 叙事视角
  perspectiveFocusCharacter: string; // 受限视角的焦点角色

  // 模块三：精确续写要求
  targetLength: number; // 目标长度（字数）
  endingStyle: string; // 结尾形式
  plotPoints: string[]; // 关键情节目标（2-5个）
  prohibitedContent: string[]; // 限制与禁止内容
}

interface AIContinueDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (config: AIContinueConfig) => void;
  editorContent: string; // 编辑器完整内容，用于自动提取上下文
}

const AIContinueDialog: React.FC<AIContinueDialogProps> = ({
  isOpen,
  onClose,
  onConfirm,
  editorContent,
}) => {
  const [config, setConfig] = useState<AIContinueConfig>({
    lastChapterContext: '',
    focusCharacter: '',
    characterStatus: '',
    coreLocation: '',
    environmentStatus: '',
    settingConstraints: '',
    styleAdjectives: '',
    emotionalTone: '',
    narrativePerspective: '第三人称受限视角',
    perspectiveFocusCharacter: '',
    targetLength: 400,
    endingStyle: '',
    plotPoints: [''],
    prohibitedContent: [''],
  });

  // 自动提取最后1000字作为上下文
  useEffect(() => {
    if (isOpen && editorContent) {
      // 提取最后1000个字符
      const context = editorContent.slice(-1000);
      setConfig((prev) => ({ ...prev, lastChapterContext: context }));
    }
  }, [isOpen, editorContent]);

  const handleInputChange = (field: keyof AIContinueConfig, value: any) => {
    setConfig((prev) => ({ ...prev, [field]: value }));
  };

  const handleArrayChange = (field: 'plotPoints' | 'prohibitedContent', index: number, value: string) => {
    setConfig((prev) => ({
      ...prev,
      [field]: prev[field].map((item, i) => (i === index ? value : item)),
    }));
  };

  const addArrayItem = (field: 'plotPoints' | 'prohibitedContent') => {
    setConfig((prev) => ({
      ...prev,
      [field]: [...prev[field], ''],
    }));
  };

  const removeArrayItem = (field: 'plotPoints' | 'prohibitedContent', index: number) => {
    setConfig((prev) => ({
      ...prev,
      [field]: prev[field].filter((_, i) => i !== index),
    }));
  };

  const handleSubmit = () => {
    onConfirm(config);
  };

  if (!isOpen) return null;

  return (
    <>
      {/* 遮罩层 */}
      <div
        className="fixed inset-0 bg-black/30 z-50 flex items-center justify-center"
        onClick={onClose}
      >
        {/* 弹窗容器 - 点击内部不关闭 */}
        <div
          className="bg-white rounded-xl shadow-md w-full max-w-2xl max-h-[85vh] overflow-hidden flex flex-col mx-6"
          onClick={(e) => e.stopPropagation()}
        >
          {/* 标题栏 */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-gray-900" />
              <h2 className="text-sm font-medium text-gray-900">AI 续写配置</h2>
            </div>
            <button
              onClick={onClose}
              className="p-1.5 rounded hover:bg-gray-50 transition-colors duration-200"
            >
              <X className="w-4 h-4 text-gray-600" />
            </button>
          </div>

          {/* 内容区 - 可滚动 */}
          <div className="flex-1 overflow-y-auto px-6 py-6">
            {/* 提示信息 */}
            <div className="mb-6 p-4 bg-gray-50 rounded-lg flex gap-3">
              <Info className="w-4 h-4 text-gray-600 flex-shrink-0 mt-0.5" />
              <p className="text-xs text-gray-600 leading-relaxed">
                所有字段均为可选。已自动提取最后 1000 字作为上下文，您只需填写必要的配置即可。
              </p>
            </div>

            {/* 背景与上下文 */}
            <section className="mb-8">
              <h3 className="text-sm font-medium text-gray-900 mb-4">背景与上下文</h3>

              <div className="space-y-4">
                {/* 焦点人物与状态 */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-gray-700 mb-1.5">
                      焦点人物
                    </label>
                    <input
                      type="text"
                      value={config.focusCharacter}
                      onChange={(e) => handleInputChange('focusCharacter', e.target.value)}
                      className="w-full px-4 py-2.5 text-sm border border-gray-200 rounded focus:border-gray-400 focus:outline-none transition-colors duration-200"
                      placeholder="例如：张三"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-700 mb-1.5">
                      角色状态
                    </label>
                    <input
                      type="text"
                      value={config.characterStatus}
                      onChange={(e) => handleInputChange('characterStatus', e.target.value)}
                      className="w-full px-4 py-2.5 text-sm border border-gray-200 rounded focus:border-gray-400 focus:outline-none transition-colors duration-200"
                      placeholder="例如：极度疲惫、愤怒"
                    />
                  </div>
                </div>

                {/* 核心地点与环境 */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-gray-700 mb-1.5">
                      核心地点
                    </label>
                    <input
                      type="text"
                      value={config.coreLocation}
                      onChange={(e) => handleInputChange('coreLocation', e.target.value)}
                      className="w-full px-4 py-2.5 text-sm border border-gray-200 rounded focus:border-gray-400 focus:outline-none transition-colors duration-200"
                      placeholder="例如：废弃工厂"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-700 mb-1.5">
                      环境状态
                    </label>
                    <input
                      type="text"
                      value={config.environmentStatus}
                      onChange={(e) => handleInputChange('environmentStatus', e.target.value)}
                      className="w-full px-4 py-2.5 text-sm border border-gray-200 rounded focus:border-gray-400 focus:outline-none transition-colors duration-200"
                      placeholder="例如：暴风雨中"
                    />
                  </div>
                </div>

                {/* 关键设定限制 */}
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1.5">
                    关键设定限制
                  </label>
                  <textarea
                    value={config.settingConstraints}
                    onChange={(e) => handleInputChange('settingConstraints', e.target.value)}
                    className="w-full px-4 py-2.5 text-sm border border-gray-200 rounded focus:border-gray-400 focus:outline-none transition-colors duration-200 resize-none"
                    rows={2}
                    placeholder="例如：禁止使用第五级魔法；角色 B 的武器已损坏"
                  />
                </div>

                {/* 文风与语气 */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-gray-700 mb-1.5">
                      文风形容词 <span className="text-gray-400 font-normal">(3个)</span>
                    </label>
                    <input
                      type="text"
                      value={config.styleAdjectives}
                      onChange={(e) => handleInputChange('styleAdjectives', e.target.value)}
                      className="w-full px-4 py-2.5 text-sm border border-gray-200 rounded focus:border-gray-400 focus:outline-none transition-colors duration-200"
                      placeholder="例如：沉稳、冷静、富有画面感"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-700 mb-1.5">
                      情绪基调
                    </label>
                    <input
                      type="text"
                      value={config.emotionalTone}
                      onChange={(e) => handleInputChange('emotionalTone', e.target.value)}
                      className="w-full px-4 py-2.5 text-sm border border-gray-200 rounded focus:border-gray-400 focus:outline-none transition-colors duration-200"
                      placeholder="例如：紧张、绝望、悬疑"
                    />
                  </div>
                </div>

                {/* 叙事视角 */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-gray-700 mb-1.5">
                      叙事视角
                    </label>
                    <select
                      value={config.narrativePerspective}
                      onChange={(e) => handleInputChange('narrativePerspective', e.target.value)}
                      className="w-full px-4 py-2.5 text-sm border border-gray-200 rounded focus:border-gray-400 focus:outline-none transition-colors duration-200"
                    >
                      <option value="第一人称">第一人称</option>
                      <option value="第三人称受限视角">第三人称受限视角</option>
                      <option value="全知视角">全知视角</option>
                    </select>
                  </div>
                  {config.narrativePerspective === '第三人称受限视角' && (
                    <div>
                      <label className="block text-xs font-medium text-gray-700 mb-1.5">
                        焦点角色
                      </label>
                      <input
                        type="text"
                        value={config.perspectiveFocusCharacter}
                        onChange={(e) => handleInputChange('perspectiveFocusCharacter', e.target.value)}
                        className="w-full px-4 py-2.5 text-sm border border-gray-200 rounded focus:border-gray-400 focus:outline-none transition-colors duration-200"
                        placeholder="受限视角的焦点角色"
                      />
                    </div>
                  )}
                </div>
              </div>
            </section>

            {/* 精确续写要求 */}
            <section className="mb-6">
              <h3 className="text-sm font-medium text-gray-900 mb-4">精确续写要求</h3>

              <div className="space-y-4">
                {/* 目标长度与结束方式 */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-gray-700 mb-1.5">
                      目标长度（字数）
                    </label>
                    <input
                      type="number"
                      value={config.targetLength}
                      onChange={(e) => handleInputChange('targetLength', parseInt(e.target.value) || 400)}
                      className="w-full px-4 py-2.5 text-sm border border-gray-200 rounded focus:border-gray-400 focus:outline-none transition-colors duration-200"
                      min="100"
                      max="2000"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-700 mb-1.5">
                      结尾形式
                    </label>
                    <input
                      type="text"
                      value={config.endingStyle}
                      onChange={(e) => handleInputChange('endingStyle', e.target.value)}
                      className="w-full px-4 py-2.5 text-sm border border-gray-200 rounded focus:border-gray-400 focus:outline-none transition-colors duration-200"
                      placeholder="例如：一个未解决的疑问"
                    />
                  </div>
                </div>

                {/* 关键情节目标 */}
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className="text-xs font-medium text-gray-700">
                      关键情节目标 <span className="text-gray-400 font-normal">(可选)</span>
                    </label>
                    {config.plotPoints.length < 5 && (
                      <button
                        onClick={() => addArrayItem('plotPoints')}
                        className="text-xs text-gray-700 hover:text-gray-900 transition-colors duration-200 flex items-center gap-1"
                      >
                        <Plus className="w-3 h-3" />
                        添加
                      </button>
                    )}
                  </div>
                  <div className="space-y-2">
                    {config.plotPoints.map((point, index) => (
                      <div key={index} className="flex gap-2">
                        <input
                          type="text"
                          value={point}
                          onChange={(e) => handleArrayChange('plotPoints', index, e.target.value)}
                          className="flex-1 px-4 py-2.5 text-sm border border-gray-200 rounded focus:border-gray-400 focus:outline-none transition-colors duration-200"
                          placeholder={`任务 ${index + 1}：例如：主角必须通过隐蔽通道离开`}
                        />
                        {config.plotPoints.length > 1 && (
                          <button
                            onClick={() => removeArrayItem('plotPoints', index)}
                            className="px-2.5 py-2.5 text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded transition-all duration-200"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                {/* 限制与禁止内容 */}
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className="text-xs font-medium text-gray-700">
                      限制与禁止内容 <span className="text-gray-400 font-normal">(可选)</span>
                    </label>
                    <button
                      onClick={() => addArrayItem('prohibitedContent')}
                      className="text-xs text-gray-700 hover:text-gray-900 transition-colors duration-200 flex items-center gap-1"
                    >
                      <Plus className="w-3 h-3" />
                      添加
                    </button>
                  </div>
                  <div className="space-y-2">
                    {config.prohibitedContent.map((item, index) => (
                      <div key={index} className="flex gap-2">
                        <input
                          type="text"
                          value={item}
                          onChange={(e) => handleArrayChange('prohibitedContent', index, e.target.value)}
                          className="flex-1 px-4 py-2.5 text-sm border border-gray-200 rounded focus:border-gray-400 focus:outline-none transition-colors duration-200"
                          placeholder={`禁止 ${index + 1}：例如：禁止提及任何与"时间"相关的词汇`}
                        />
                        {config.prohibitedContent.length > 1 && (
                          <button
                            onClick={() => removeArrayItem('prohibitedContent', index)}
                            className="px-2.5 py-2.5 text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded transition-all duration-200"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </section>
          </div>

          {/* 底部按钮栏 */}
          <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-100">
            <button
              onClick={onClose}
              className="px-6 py-2.5 text-sm text-gray-700 border border-gray-200 rounded hover:border-gray-300 hover:bg-gray-50 transition-all duration-200"
            >
              取消
            </button>
            <button
              onClick={handleSubmit}
              className="px-6 py-2.5 bg-gray-900 text-white text-sm rounded hover:bg-gray-800 transition-colors duration-200 flex items-center gap-2"
            >
              <Sparkles className="w-4 h-4" />
              开始续写
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default AIContinueDialog;
