import React, { useState } from 'react';
import { ArrowLeft, Sparkles, ChevronDown, ChevronUp, Check, X } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import type { CreateWorkData } from '../../types';
import type { WorldViewData } from './index';
import { DataService } from '../../services/DataService';

interface CreateWorkWithAIProps {
  onComplete: (data: CreateWorkData, worldView: WorldViewData) => void;
  onBack: () => void;
}

/**
 * 世界观模块定义（5个折叠模块，共22个字段）
 */
interface WorldViewField {
  id: keyof WorldViewData;
  label: string;
  placeholder: string;
}

interface WorldViewModule {
  id: string;
  title: string;
  description: string;
  fields: WorldViewField[];
}

const WORLDVIEW_MODULES: WorldViewModule[] = [
  {
    id: 'core-specs',
    title: '核心创作规范',
    description: '5个核心字段定义创作方向',
    fields: [
      { id: 'targetAudience', label: '目标读者', placeholder: '例如：18-25岁男性，喜欢玄幻、热血' },
      { id: 'highConcept', label: '高概念卖点', placeholder: '一句话总结核心吸引力' },
      { id: 'dominantEmotion', label: '主导情感', placeholder: '例如：逆袭的爽感、探索的惊奇' },
      { id: 'writingStyle', label: '文笔风格', placeholder: '例如：冷峻简洁、华丽诗性' },
      { id: 'chapterLength', label: '章节长度', placeholder: '例如：2000-3000字' },
    ],
  },
  {
    id: 'genre',
    title: '小说类型',
    description: '类型、标签、基调',
    fields: [
      { id: 'primaryGenre', label: '一级类型', placeholder: '例如：玄幻、都市、科幻' },
      { id: 'secondaryTags', label: '二级标签', placeholder: '例如：修真、冒险、热血' },
      { id: 'creativeTone', label: '创作基调', placeholder: '例如：激昂向上、黑暗压抑' },
    ],
  },
  {
    id: 'world',
    title: '世界背景',
    description: '世界观、场景、规则',
    fields: [
      { id: 'worldIntro', label: '核心世界观简介', placeholder: '200字内描述世界设定' },
      { id: 'mainLocations', label: '主要场景/地点', placeholder: '列出3-5个核心场景' },
      { id: 'worldRules', label: '世界规则', placeholder: '这个世界的独特规则和限制' },
    ],
  },
  {
    id: 'power',
    title: '力量体系',
    description: '体系名称、等级、代价',
    fields: [
      { id: 'powerSystemName', label: '体系名称', placeholder: '例如：境界修炼体系、异能等级' },
      { id: 'powerLevels', label: '等级划分', placeholder: '列出主要等级' },
      { id: 'powerCost', label: '代价与限制', placeholder: '获得力量的代价和限制' },
    ],
  },
  {
    id: 'protagonist-plot',
    title: '主角与剧情',
    description: '主角设定和剧情三幕',
    fields: [
      { id: 'protagonistName', label: '主角名字', placeholder: '主角的名字' },
      { id: 'protagonistIdentity', label: '身份与背景', placeholder: '主角的身份和背景故事' },
      { id: 'protagonistTraits', label: '性格特点', placeholder: '3-5个关键性格特征' },
      { id: 'protagonistGoal', label: '终极目标', placeholder: '主角的最终目标' },
      { id: 'conflictDesign', label: '冲突设计', placeholder: '核心冲突是什么' },
      { id: 'actOne', label: '第一幕', placeholder: '故事开端（0-30%）' },
      { id: 'actTwo', label: '第二幕', placeholder: '故事发展（30-80%）' },
      { id: 'actThree', label: '第三幕', placeholder: '故事高潮与结局（80-100%）' },
    ],
  },
];

/**
 * 步骤类型
 */
type Step = 'input' | 'generating' | 'review';

/**
 * CreateWorkWithAI 组件 - 方案C：表单化 + 智能预填
 *
 * 流程：
 * 1. 用户输入故事梗概（一段话）
 * 2. 点击"AI智能生成" -> 生成22个字段
 * 3. 显示5个折叠模块，用户可编辑任意字段
 * 4. 确认后填写标题和简介，完成创建
 */
const CreateWorkWithAI: React.FC<CreateWorkWithAIProps> = ({ onComplete, onBack }) => {
  const [step, setStep] = useState<Step>('input');
  const [storyConcept, setStoryConcept] = useState('');
  const [worldViewData, setWorldViewData] = useState<WorldViewData>({});
  const [expandedModules, setExpandedModules] = useState<Set<string>>(new Set());
  const [editingFields, setEditingFields] = useState<Set<string>>(new Set());
  const [finalData, setFinalData] = useState({ title: '', description: '' });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [showFinalForm, setShowFinalForm] = useState(false);

  /**
   * 处理AI生成
   */
  const handleGenerate = async () => {
    if (!storyConcept.trim()) {
      alert('请输入故事梗概');
      return;
    }

    setStep('generating');

    try {
      const response = await DataService.generateAIGuidelines({
        storyConcept: storyConcept.trim(),
      });

      console.log('AI生成的原始响应:', response);

      // axios自动解包，数据直接在response中，已经是camelCase格式
      const generatedData: WorldViewData = {
        targetAudience: response.targetAudience,
        highConcept: response.highConcept,
        dominantEmotion: response.dominantEmotion,
        writingStyle: response.writingStyle,
        chapterLength: response.chapterLength,
        primaryGenre: response.primaryGenre,
        secondaryTags: response.secondaryTags,
        creativeTone: response.creativeTone,
        worldIntro: response.worldIntro,
        mainLocations: response.mainLocations,
        worldRules: response.worldRules,
        powerSystemName: response.powerSystemName,
        powerLevels: response.powerLevels,
        powerCost: response.powerCost,
        protagonistName: response.protagonistName,
        protagonistIdentity: response.protagonistIdentity,
        protagonistTraits: response.protagonistTraits,
        protagonistGoal: response.protagonistGoal,
        conflictDesign: response.conflictDesign,
        actOne: response.actOne,
        actTwo: response.actTwo,
        actThree: response.actThree,
      };

      setWorldViewData(generatedData);
      setStep('review');
      // 默认展开第一个模块
      setExpandedModules(new Set([WORLDVIEW_MODULES[0].id]));
    } catch (error) {
      console.error('AI生成失败:', error);
      alert('生成失败，请重试');
      setStep('input');
    }
  };

  /**
   * 切换模块展开/折叠
   */
  const toggleModule = (moduleId: string) => {
    const newExpanded = new Set(expandedModules);
    if (newExpanded.has(moduleId)) {
      newExpanded.delete(moduleId);
    } else {
      newExpanded.add(moduleId);
    }
    setExpandedModules(newExpanded);
  };

  /**
   * 开始编辑字段
   */
  const startEditing = (fieldId: string) => {
    setEditingFields(new Set([...editingFields, fieldId]));
  };

  /**
   * 保存字段编辑
   */
  const saveField = (fieldId: string) => {
    const newEditing = new Set(editingFields);
    newEditing.delete(fieldId);
    setEditingFields(newEditing);
  };

  /**
   * 取消字段编辑
   */
  const cancelField = (fieldId: string) => {
    const newEditing = new Set(editingFields);
    newEditing.delete(fieldId);
    setEditingFields(newEditing);
  };

  /**
   * 更新字段值
   */
  const updateField = (fieldId: keyof WorldViewData, value: string) => {
    setWorldViewData({ ...worldViewData, [fieldId]: value });
  };

  /**
   * 处理最终表单变化
   */
  const handleFinalChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFinalData((prev) => ({ ...prev, [name]: value }));

    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  /**
   * 完成创建
   */
  const handleFinish = () => {
    const newErrors: Record<string, string> = {};

    if (!finalData.title.trim()) {
      newErrors.title = '请输入作品标题';
    }
    if (!finalData.description.trim()) {
      newErrors.description = '请输入作品简介';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    onComplete(
      {
        title: finalData.title,
        description: finalData.description,
      },
      worldViewData
    );
  };

  return (
    <div className="min-h-screen bg-[#faf9f6] dark:bg-slate-900 flex flex-col">
      {/* 顶部标题栏 */}
      <div className="border-b border-gray-200/50 dark:border-gray-700/50 bg-white/30 dark:bg-slate-800/30 backdrop-blur-sm">
        <div className="max-w-4xl mx-auto px-8 py-6 flex items-center justify-between">
          <button
            onClick={onBack}
            className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>返回</span>
          </button>

          <div className="flex items-center gap-3">
            <Sparkles className="w-5 h-5 text-gray-700 dark:text-gray-300" />
            <h1 className="text-gray-800 dark:text-gray-100 tracking-wider">AI 智能创建</h1>
          </div>

          <div className="w-20"></div>
        </div>
      </div>

      {/* 主体区域 */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-8 py-12">
          <AnimatePresence mode="wait">
            {/* 步骤1：输入故事梗概 */}
            {step === 'input' && (
              <motion.div
                key="input"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-6"
              >
                <div className="text-center mb-8">
                  <h2 className="text-2xl text-gray-800 dark:text-gray-100 mb-3">描述你的故事</h2>
                  <p className="text-gray-500 dark:text-gray-400">
                    用一段话描述你想创作的故事，AI 将自动生成完整的世界观设定
                  </p>
                </div>

                <div className="bg-white dark:bg-slate-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 shadow-sm">
                  <label className="block text-sm text-gray-600 dark:text-gray-400 mb-3">
                    故事梗概 <span className="text-red-500">*</span>
                  </label>
                  <textarea
                    value={storyConcept}
                    onChange={(e) => setStoryConcept(e.target.value)}
                    placeholder="例如：一个普通高中生意外穿越到修仙世界，凭借现代知识和独特的金手指，在这个充满危险的世界中逐步崛起，最终成为一代仙尊的故事..."
                    className="w-full bg-[#faf9f6] dark:bg-slate-900 border border-gray-300 dark:border-gray-600 rounded px-4 py-3 outline-none focus:border-gray-600 dark:focus:border-gray-400 focus:ring-2 focus:ring-gray-600/20 dark:focus:ring-gray-400/20 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 resize-none"
                    rows={8}
                  />
                </div>

                <button
                  onClick={handleGenerate}
                  disabled={!storyConcept.trim()}
                  className="w-full bg-gray-800 dark:bg-gray-200 hover:bg-gray-900 dark:hover:bg-gray-100 text-white dark:text-slate-900 py-3 rounded-lg shadow-sm disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
                >
                  <Sparkles className="w-4 h-4" />
                  <span>AI 智能生成</span>
                </button>
              </motion.div>
            )}

            {/* 步骤2：生成中 */}
            {step === 'generating' && (
              <motion.div
                key="generating"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex flex-col items-center justify-center py-20"
              >
                <div className="flex gap-2 mb-6">
                  <motion.div
                    className="w-3 h-3 bg-gray-800 dark:bg-gray-200 rounded-full"
                    animate={{ opacity: [0.3, 1, 0.3] }}
                    transition={{ duration: 1.5, repeat: Infinity, delay: 0 }}
                  />
                  <motion.div
                    className="w-3 h-3 bg-gray-800 dark:bg-gray-200 rounded-full"
                    animate={{ opacity: [0.3, 1, 0.3] }}
                    transition={{ duration: 1.5, repeat: Infinity, delay: 0.2 }}
                  />
                  <motion.div
                    className="w-3 h-3 bg-gray-800 dark:bg-gray-200 rounded-full"
                    animate={{ opacity: [0.3, 1, 0.3] }}
                    transition={{ duration: 1.5, repeat: Infinity, delay: 0.4 }}
                  />
                </div>
                <p className="text-gray-600 dark:text-gray-400">AI 正在生成世界观设定...</p>
                <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">预计需要 10-20 秒</p>
              </motion.div>
            )}

            {/* 步骤3：审阅和编辑 */}
            {step === 'review' && (
              <motion.div
                key="review"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-6"
              >
                <div className="text-center mb-8">
                  <h2 className="text-2xl text-gray-800 dark:text-gray-100 mb-3">
                    审阅世界观设定
                  </h2>
                  <p className="text-gray-500 dark:text-gray-400">
                    AI 已生成完整设定，您可以展开查看和编辑任意字段
                  </p>
                </div>

                {/* 5个折叠模块 */}
                <div className="space-y-4">
                  {WORLDVIEW_MODULES.map((module) => {
                    const isExpanded = expandedModules.has(module.id);

                    return (
                      <div
                        key={module.id}
                        className="bg-white dark:bg-slate-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm overflow-hidden"
                      >
                        {/* 模块标题栏 */}
                        <button
                          onClick={() => toggleModule(module.id)}
                          className="w-full flex items-center justify-between px-5 py-4 hover:bg-gray-50 dark:hover:bg-slate-700/50 transition-colors"
                        >
                          <div className="flex items-center gap-3">
                            {isExpanded ? (
                              <ChevronUp className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                            ) : (
                              <ChevronDown className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                            )}
                            <div className="text-left">
                              <h3 className="text-gray-800 dark:text-gray-100 font-medium">
                                {module.title}
                              </h3>
                              <p className="text-sm text-gray-500 dark:text-gray-400">
                                {module.description}
                              </p>
                            </div>
                          </div>
                        </button>

                        {/* 模块内容 */}
                        <AnimatePresence>
                          {isExpanded && (
                            <motion.div
                              initial={{ height: 0, opacity: 0 }}
                              animate={{ height: 'auto', opacity: 1 }}
                              exit={{ height: 0, opacity: 0 }}
                              transition={{ duration: 0.2 }}
                              className="border-t border-gray-200 dark:border-gray-700"
                            >
                              <div className="px-5 py-4 space-y-4">
                                {module.fields.map((field) => {
                                  const isEditing = editingFields.has(field.id);
                                  const value = worldViewData[field.id] || '';

                                  return (
                                    <div key={field.id} className="space-y-2">
                                      <div className="flex items-center justify-between">
                                        <label className="text-sm text-gray-600 dark:text-gray-400">
                                          {field.label}
                                        </label>
                                        {!isEditing && (
                                          <button
                                            onClick={() => startEditing(field.id)}
                                            className="text-xs text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 transition-colors"
                                          >
                                            编辑
                                          </button>
                                        )}
                                      </div>

                                      {isEditing ? (
                                        <div className="space-y-2">
                                          <textarea
                                            value={value}
                                            onChange={(e) => updateField(field.id, e.target.value)}
                                            placeholder={field.placeholder}
                                            className="w-full bg-[#faf9f6] dark:bg-slate-900 border border-gray-300 dark:border-gray-600 rounded px-3 py-2 outline-none focus:border-gray-600 dark:focus:border-gray-400 focus:ring-1 focus:ring-gray-600/20 dark:focus:ring-gray-400/20 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 resize-none text-sm"
                                            rows={3}
                                          />
                                          <div className="flex gap-2">
                                            <button
                                              onClick={() => saveField(field.id)}
                                              className="flex items-center gap-1 px-3 py-1 bg-gray-800 dark:bg-gray-200 text-white dark:text-slate-900 rounded text-xs hover:bg-gray-900 dark:hover:bg-gray-100 transition-colors"
                                            >
                                              <Check className="w-3 h-3" />
                                              保存
                                            </button>
                                            <button
                                              onClick={() => cancelField(field.id)}
                                              className="flex items-center gap-1 px-3 py-1 bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-gray-300 rounded text-xs hover:bg-gray-300 dark:hover:bg-slate-600 transition-colors"
                                            >
                                              <X className="w-3 h-3" />
                                              取消
                                            </button>
                                          </div>
                                        </div>
                                      ) : (
                                        <p className="text-sm text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-slate-900/50 px-3 py-2 rounded">
                                          {value || <span className="text-gray-400">未填写</span>}
                                        </p>
                                      )}
                                    </div>
                                  );
                                })}
                              </div>
                            </motion.div>
                          )}
                        </AnimatePresence>
                      </div>
                    );
                  })}
                </div>

                {/* 确认按钮 */}
                {!showFinalForm && (
                  <button
                    onClick={() => setShowFinalForm(true)}
                    className="w-full bg-gray-800 dark:bg-gray-200 hover:bg-gray-900 dark:hover:bg-gray-100 text-white dark:text-slate-900 py-3 rounded-lg shadow-sm transition-colors"
                  >
                    确认设定，填写作品信息
                  </button>
                )}

                {/* 最终表单 */}
                {showFinalForm && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-white dark:bg-slate-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 shadow-sm space-y-4"
                  >
                    <div className="text-center mb-4">
                      <h3 className="text-lg text-gray-800 dark:text-gray-100">完善作品信息</h3>
                      <div className="w-12 h-px bg-gray-300 dark:bg-gray-600 mx-auto mt-2"></div>
                    </div>

                    <div>
                      <label className="block text-sm text-gray-600 dark:text-gray-400 mb-2">
                        作品标题 <span className="text-red-500">*</span>
                      </label>
                      <input
                        name="title"
                        value={finalData.title}
                        onChange={handleFinalChange}
                        placeholder="请输入作品标题"
                        className={`w-full bg-[#faf9f6] dark:bg-slate-900 border ${
                          errors.title ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
                        } rounded px-4 py-2 outline-none focus:border-gray-600 dark:focus:border-gray-400 focus:ring-2 focus:ring-gray-600/20 dark:focus:ring-gray-400/20 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500`}
                      />
                      {errors.title && (
                        <span className="text-sm text-red-500 mt-1">{errors.title}</span>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm text-gray-600 dark:text-gray-400 mb-2">
                        作品简介 <span className="text-red-500">*</span>
                      </label>
                      <textarea
                        name="description"
                        value={finalData.description}
                        onChange={handleFinalChange}
                        placeholder="请输入作品简介"
                        className={`w-full bg-[#faf9f6] dark:bg-slate-900 border ${
                          errors.description
                            ? 'border-red-500'
                            : 'border-gray-300 dark:border-gray-600'
                        } rounded px-4 py-2 outline-none focus:border-gray-600 dark:focus:border-gray-400 focus:ring-2 focus:ring-gray-600/20 dark:focus:ring-gray-400/20 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 resize-none`}
                        rows={4}
                      />
                      {errors.description && (
                        <span className="text-sm text-red-500 mt-1">{errors.description}</span>
                      )}
                    </div>

                    <button
                      onClick={handleFinish}
                      className="w-full bg-gray-800 dark:bg-gray-200 hover:bg-gray-900 dark:hover:bg-gray-100 text-white dark:text-slate-900 py-3 rounded-lg shadow-sm transition-colors"
                    >
                      完成创建
                    </button>
                  </motion.div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};

export default CreateWorkWithAI;
