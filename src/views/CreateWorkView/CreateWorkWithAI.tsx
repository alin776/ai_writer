import React, { useState, useRef, useEffect } from 'react';
import { ArrowLeft, Send, Sparkles, Pencil, Check, X, Circle, CheckCircle2 } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import type { CreateWorkData } from '../../types';
import type { WorldViewData } from './index';
import AIService from '../../services/AIService';

interface CreateWorkWithAIProps {
  onComplete: (data: CreateWorkData, worldView: WorldViewData) => void;
  onBack: () => void;
}

/**
 * 消息类型
 */
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

/**
 * 世界观字段定义
 */
interface WorldviewField {
  id: string;
  label: string;
  value: string;
  required: boolean;
  completed: boolean;
}

interface WorldviewModule {
  id: string;
  name: string;
  color: string;
  fields: WorldviewField[];
}

/**
 * AI 引导问题列表 - 阶段一：创作规范问诊（15个问题）
 */
const AI_QUESTIONS = [
  // === 模块一：战略定位 ===
  '你好！我是你的商业IP总策划师。让我帮助你系统化地构建一部具备商业潜力的小说！\n\n我们将分5个模块，共14个问题来完成创作规范的制定。准备好了吗？让我们从第一个模块开始！\n\n【模块一：战略定位】\n首先，这部小说的核心商业目标是什么？（例如：快速盈利、打造IP、建立作者品牌）',
  '很好！那么我们明确瞄准的读者画像是怎样的？请描述年龄、性别、阅读偏好、消费能力等。',
  '了解。请提供1-2个商业对标作品，并说明我们希望借鉴其哪些优点，以及在哪些方面实现差异化？',
  '请用一句话，提炼出我们小说的高概念卖点。格式：当[经典类型]遇上[新奇元素]。',

  // === 模块二：IP架构 ===
  '【模块二：IP架构】\n这个故事最核心的、能引发讨论的核心悖论或世界观亮点是什么？（例如：不能说话的播音员、害怕水的航海家）',
  '我们希望读者在读完小说后，带走哪一种最主要的情感体验？（例如：逆袭的爽感、被理解的慰藉、探索的惊奇）',
  '请构思2-3个具有高辨识度和衍生潜力的核心IP符号。（如：一个标志性道具、一个独特地点、一种视觉特征）',

  // === 模块三：叙事引擎 ===
  '【模块三：叙事引擎】\n主角最大的内在缺陷和最强的核心能力分别是什么？他/她必须完成的核心转变是什么？',
  '主角与主要对手/伙伴之间，最根本的价值观冲突是什么？',
  '我们计划采用什么样的叙事节奏？（例如：快节奏强冲突、慢热型注重铺垫，或3章一小爽、10章一大爽）',

  // === 模块四：文字质感 ===
  '【模块四：文字质感】\n我们希望这部小说的文字风格偏向哪种？（例如：冷峻简洁、华丽诗性、幽默诙谐、平实感人）',
  '是否有必须避免的文风或写作习惯？（例如：避免冗长对话、多用动作描写）',

  // === 模块五：技术规范 ===
  '【模块五：技术规范】\n计划的平均章节字数是多少？（例如：2000-3000字）',
  '最后一个问题！需要严格遵守的内容禁忌有哪些？（例如：政治红线、特定类型的描写限制）',
];

// 问题对应的字段key
const QUESTION_FIELD_KEYS = [
  'businessGoal', 'targetAudience', 'commercialBenchmark', 'highConcept',
  'coreParadox', 'dominantEmotion', 'coreIpSymbols',
  'protagonistArc', 'coreConflict', 'narrativeRhythm',
  'writingStyle', 'styleNotes',
  'chapterLength', 'contentTaboos'
];

/**
 * CreateWorkWithAI 组件 - AI辅助创建作品
 *
 * 功能：
 * - AI对话界面（左侧50%）
 * - 世界观完成度展示（右侧50%，时间轴样式）
 * - 用户可以随时编辑AI填写的世界观信息
 */
const CreateWorkWithAI: React.FC<CreateWorkWithAIProps> = ({ onComplete, onBack }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [isGenerating, setIsGenerating] = useState(false);
  const [showFinalForm, setShowFinalForm] = useState(false);
  const [finalData, setFinalData] = useState({ title: '', description: '' });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [editingModuleId, setEditingModuleId] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const messageIdCounter = useRef(0);
  const isInitialized = useRef(false);

  // 世界观数据结构（10个模块，31个字段）
  const [worldviewData, setWorldviewData] = useState<WorldviewModule[]>([
    {
      id: 'strategy',
      name: '战略定位',
      color: 'blue',
      fields: [
        { id: 'businessGoal', label: '商业目标', value: '', required: true, completed: false },
        { id: 'targetAudience', label: '目标读者', value: '', required: true, completed: false },
        { id: 'commercialBenchmark', label: '商业对标', value: '', required: true, completed: false },
        { id: 'highConcept', label: '高概念卖点', value: '', required: true, completed: false },
      ]
    },
    {
      id: 'ip',
      name: 'IP架构',
      color: 'purple',
      fields: [
        { id: 'coreParadox', label: '核心悖论/设定', value: '', required: true, completed: false },
        { id: 'dominantEmotion', label: '主导情感', value: '', required: true, completed: false },
        { id: 'coreIpSymbols', label: '核心IP符号', value: '', required: true, completed: false },
      ]
    },
    {
      id: 'narrative',
      name: '叙事引擎',
      color: 'green',
      fields: [
        { id: 'protagonistArc', label: '主角弧光', value: '', required: true, completed: false },
        { id: 'coreConflict', label: '核心关系冲突', value: '', required: true, completed: false },
        { id: 'narrativeRhythm', label: '叙事节奏', value: '', required: true, completed: false },
      ]
    },
    {
      id: 'style',
      name: '文字质感',
      color: 'amber',
      fields: [
        { id: 'writingStyle', label: '文笔风格', value: '', required: true, completed: false },
        { id: 'styleNotes', label: '文风注意事项', value: '', required: false, completed: false },
      ]
    },
    {
      id: 'technical',
      name: '技术规范',
      color: 'red',
      fields: [
        { id: 'chapterLength', label: '章节长度', value: '', required: true, completed: false },
        { id: 'contentTaboos', label: '内容禁忌', value: '', required: false, completed: false },
      ]
    },
    {
      id: 'genre',
      name: '小说类型',
      color: 'indigo',
      fields: [
        { id: 'primaryGenre', label: '一级类型', value: '', required: false, completed: false },
        { id: 'secondaryTags', label: '二级标签', value: '', required: false, completed: false },
        { id: 'creativeTone', label: '创作基调', value: '', required: false, completed: false },
      ]
    },
    {
      id: 'world',
      name: '世界背景',
      color: 'cyan',
      fields: [
        { id: 'worldIntro', label: '核心世界观简介', value: '', required: false, completed: false },
        { id: 'mainLocations', label: '主要场景/地点', value: '', required: false, completed: false },
        { id: 'worldRules', label: '世界规则', value: '', required: false, completed: false },
      ]
    },
    {
      id: 'power',
      name: '力量体系',
      color: 'pink',
      fields: [
        { id: 'powerSystemName', label: '体系名称', value: '', required: false, completed: false },
        { id: 'powerLevels', label: '等级划分', value: '', required: false, completed: false },
        { id: 'powerCost', label: '代价与限制', value: '', required: false, completed: false },
      ]
    },
    {
      id: 'protagonist',
      name: '主角设定',
      color: 'teal',
      fields: [
        { id: 'protagonistName', label: '主角名字', value: '', required: false, completed: false },
        { id: 'protagonistIdentity', label: '身份与背景', value: '', required: false, completed: false },
        { id: 'protagonistTraits', label: '性格特点', value: '', required: false, completed: false },
        { id: 'protagonistGoal', label: '终极目标', value: '', required: false, completed: false },
      ]
    },
    {
      id: 'plot',
      name: '剧情构思',
      color: 'orange',
      fields: [
        { id: 'conflictDesign', label: '冲突设计', value: '', required: false, completed: false },
        { id: 'actOne', label: '第一幕', value: '', required: false, completed: false },
        { id: 'actTwo', label: '第二幕', value: '', required: false, completed: false },
        { id: 'actThree', label: '第三幕', value: '', required: false, completed: false },
      ]
    },
  ]);

  /**
   * 初始化 - 发送第一个问题
   */
  useEffect(() => {
    if (!isInitialized.current && messages.length === 0) {
      isInitialized.current = true;
      addAssistantMessage(AI_QUESTIONS[0]);
    }
    setTimeout(() => {
      window.scrollTo({ top: 0, behavior: 'auto' });
    }, 0);
  }, []);

  /**
   * 滚动到底部（仅在聊天容器内滚动）
   */
  useEffect(() => {
    if (messages.length > 0 && chatContainerRef.current) {
      const container = chatContainerRef.current;
      requestAnimationFrame(() => {
        container.scrollTop = container.scrollHeight;
      });
    }
  }, [messages]);

  /**
   * 监听世界观完成度 - 当达到100%时自动显示最终表单
   * 修复：用户通过右侧编辑功能绕过对话流程时，也能显示完成按钮
   */
  useEffect(() => {
    const allFields = worldviewData.flatMap(module => module.fields);
    const completedFields = allFields.filter(field => field.completed);
    const completion = Math.round((completedFields.length / allFields.length) * 100);

    if (completion === 100 && !showFinalForm && !isGenerating) {
      setShowFinalForm(true);
    }
  }, [worldviewData, showFinalForm, isGenerating]);

  /**
   * 添加助手消息
   */
  const addAssistantMessage = (content: string) => {
    messageIdCounter.current += 1;
    const newMessage: Message = {
      id: `assistant-${messageIdCounter.current}`,
      role: 'assistant',
      content,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, newMessage]);
  };

  /**
   * 添加用户消息
   */
  const addUserMessage = (content: string) => {
    messageIdCounter.current += 1;
    const newMessage: Message = {
      id: `user-${messageIdCounter.current}`,
      role: 'user',
      content,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, newMessage]);
  };

  /**
   * 阶段二：AI自动生成核心设定
   */
  const generatePhase2Content = async (phase1Fields: Record<string, string>): Promise<Record<string, string>> => {
    try {
      const phase2Data = await AIService.generatePhase2Content(phase1Fields);
      return phase2Data as Record<string, string>;
    } catch (error) {
      console.error('生成阶段二内容失败:', error);
      // 返回默认值
      return {
        primaryGenre: '玄幻',
        secondaryTags: '修真、冒险、热血',
        creativeTone: '激昂向上、充满希望',
        worldIntro: '修仙世界，分为凡界、灵界、仙界三个层次',
        mainLocations: '青云宗、万妖森林、天机阁',
        worldRules: '灵气越高的地方，修炼速度越快',
        powerSystemName: '境界修炼体系',
        powerLevels: '练气、筑基、金丹、元婴、化神',
        powerCost: '突破需要渡劫，失败会受重伤',
        protagonistName: '陈羽',
        protagonistIdentity: '平凡少年，意外获得古老传承',
        protagonistTraits: '坚韧不拔、重情重义',
        protagonistGoal: '登临仙界巅峰，守护家人',
        conflictDesign: '主角与宗门、魔道、天劫的多重冲突',
        actOne: '主角获得传承，进入青云宗修炼',
        actTwo: '宗门大比、魔道入侵、寻找突破契机',
        actThree: '渡劫飞升，成就仙道',
      };
    }
  };

  /**
   * 处理发送消息
   */
  const handleSend = () => {
    if (!inputValue.trim() || isGenerating) return;

    const userInput = inputValue.trim();
    addUserMessage(userInput);
    setInputValue('');

    // 获取当前问题对应的字段
    const fieldKey = QUESTION_FIELD_KEYS[currentQuestionIndex];

    // 更新世界观数据（前5个模块，共14个字段）
    const newWorldviewData = [...worldviewData];
    for (let i = 0; i < 5; i++) {
      const module = newWorldviewData[i];
      const field = module.fields.find(f => f.id === fieldKey);
      if (field) {
        field.value = userInput;
        field.completed = true;
        break;
      }
    }
    setWorldviewData(newWorldviewData);

    // 模拟AI回复并进入下一个问题
    setTimeout(() => {
      const nextIndex = currentQuestionIndex + 1;

      if (nextIndex < AI_QUESTIONS.length) {
        // 还有问题，继续提问
        addAssistantMessage('非常好！' + AI_QUESTIONS[nextIndex]);
        setCurrentQuestionIndex(nextIndex);
      } else {
        // 阶段一完成，开始阶段二
        addAssistantMessage('✨ 太棒了！【阶段一：创作规范】已经完成！\n\n现在让我基于您提供的信息，为您自动生成【阶段二：核心设定】...');
        setIsGenerating(true);

        // 收集阶段一的数据
        const phase1Fields: Record<string, string> = {};
        newWorldviewData.slice(0, 5).forEach(module => {
          module.fields.forEach(field => {
            if (field.completed) {
              phase1Fields[field.id] = field.value;
            }
          });
        });

        // 调用API生成阶段二内容
        (async () => {
          try {
            const phase2Data = await generatePhase2Content(phase1Fields);

            // 更新后5个模块的数据
            const updatedData = [...newWorldviewData];
            updatedData.slice(5).forEach(module => {
              module.fields.forEach(field => {
                if (phase2Data[field.id]) {
                  field.value = phase2Data[field.id];
                  field.completed = true;
                }
              });
            });
            setWorldviewData(updatedData);
            setIsGenerating(false);

            addAssistantMessage(
              '🎉 【阶段二：核心设定】已自动生成完成！\n\n' +
              '我已经为您生成了：\n' +
              '✓ 小说类型与体裁\n' +
              '✓ 世界背景设定\n' +
              '✓ 力量体系\n' +
              '✓ 主角核心设定\n' +
              '✓ 剧情三幕式大纲\n\n' +
              '你可以在右侧查看和编辑所有31个字段的完整内容。如果满意，请填写作品标题和简介，即可开始创作！'
            );
            setShowFinalForm(true);
          } catch (error) {
            console.error('生成阶段二内容失败:', error);
            setIsGenerating(false);
            addAssistantMessage('⚠️ 生成内容时出现问题，但您仍然可以手动填写和编辑世界观内容。请填写作品标题和简介继续。');
            setShowFinalForm(true);
          }
        })();
      }
    }, 800);
  };

  /**
   * 处理回车发送
   */
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  /**
   * 计算完成度
   */
  const calculateCompletion = () => {
    const allFields = worldviewData.flatMap(module => module.fields);
    const completedFields = allFields.filter(field => field.completed);
    return Math.round((completedFields.length / allFields.length) * 100);
  };

  /**
   * 检查模块是否已完成
   */
  const isModuleCompleted = (module: WorldviewModule) => {
    return module.fields.every(field => field.completed);
  };

  /**
   * 检查模块是否有部分完成
   */
  const isModulePartial = (module: WorldviewModule) => {
    return module.fields.some(field => field.completed) && !isModuleCompleted(module);
  };

  /**
   * 处理最终表单变化
   */
  const handleFinalChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFinalData(prev => ({ ...prev, [name]: value }));

    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  /**
   * 验证并提交
   */
  const handleFinish = () => {
    const newErrors: Record<string, string> = {};

    // 验证基本信息
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

    // 转换世界观数据为WorldViewData格式
    const worldView: WorldViewData = {};
    worldviewData.forEach(module => {
      module.fields.forEach(field => {
        if (field.completed) {
          worldView[field.id] = field.value;
        }
      });
    });

    onComplete(
      {
        title: finalData.title,
        description: finalData.description,
      },
      worldView
    );
  };

  return (
    <div className="h-screen bg-[#faf9f6] dark:bg-slate-900 flex flex-col">
      {/* 顶部标题栏 */}
      <div className="border-b border-gray-200/50 dark:border-gray-700/50 bg-white/30 dark:bg-slate-800/30 backdrop-blur-sm">
        <div className="max-w-[1600px] mx-auto px-12 py-6 flex items-center justify-between">
          <button
            onClick={onBack}
            className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>返回</span>
          </button>

          <div className="flex items-center gap-4">
            <Sparkles className="w-5 h-5 text-gray-700 dark:text-gray-300" />
            <h1 className="text-gray-800 dark:text-gray-100 tracking-wider">AI 创作助手</h1>
          </div>

          <div className="flex items-center gap-3">
            <span className="text-sm text-gray-500 dark:text-gray-400">世界观完成度</span>
            <div className="bg-gray-800 dark:bg-gray-200 text-white dark:text-slate-900 border-0 px-3 py-1 rounded text-sm">
              {calculateCompletion()}%
            </div>
          </div>
        </div>
      </div>

      {/* 主体区域 */}
      <div className="flex-1 flex max-w-[1600px] mx-auto w-full overflow-hidden">
        {/* 左侧对话区 - 50% 宽度 */}
        <div className="w-1/2 flex flex-col overflow-hidden">
          {/* 对话内容区 - 居中，左右各留10%空白 */}
          <div className="flex-1 flex flex-col px-[10%] py-8 overflow-hidden">
            {/* 消息区域 */}
            <div className="flex-1 overflow-y-auto pr-4" ref={chatContainerRef}>
              <div className="space-y-6 pb-4">
                {messages.map((message) => (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[75%] px-4 py-3 rounded-lg whitespace-pre-wrap ${
                        message.role === 'user'
                          ? 'bg-gray-800 dark:bg-gray-200 text-white dark:text-slate-900 shadow-sm'
                          : 'bg-white dark:bg-slate-800 text-gray-700 dark:text-gray-200 border border-gray-200 dark:border-gray-700 shadow-sm'
                      }`}
                      style={{ fontSize: '0.75rem', lineHeight: '1.5' }}
                    >
                      {message.content}
                    </div>
                  </motion.div>
                ))}
                {isGenerating && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="flex justify-start"
                  >
                    <div className="bg-white dark:bg-slate-800 text-gray-700 dark:text-gray-200 border border-gray-200 dark:border-gray-700 px-5 py-4 rounded-lg shadow-sm">
                      <div className="flex items-center gap-2">
                        <div className="flex gap-1">
                          <motion.div
                            className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full"
                            animate={{ opacity: [0.3, 1, 0.3] }}
                            transition={{ duration: 1.5, repeat: Infinity, delay: 0 }}
                          />
                          <motion.div
                            className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full"
                            animate={{ opacity: [0.3, 1, 0.3] }}
                            transition={{ duration: 1.5, repeat: Infinity, delay: 0.2 }}
                          />
                          <motion.div
                            className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full"
                            animate={{ opacity: [0.3, 1, 0.3] }}
                            transition={{ duration: 1.5, repeat: Infinity, delay: 0.4 }}
                          />
                        </div>
                        <span className="text-sm">正在生成...</span>
                      </div>
                    </div>
                  </motion.div>
                )}
                <div ref={messagesEndRef} />
              </div>
            </div>

            {/* 输入区或最终表单 */}
            <div className="mt-6 pt-6 border-t border-gray-200/50 dark:border-gray-700/50">
              {!showFinalForm ? (
                <div className="flex gap-3">
                  <textarea
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="输入您的回答..."
                    className="flex-1 resize-none bg-white dark:bg-slate-800 border border-gray-300 dark:border-gray-600 rounded px-3 py-2 outline-none focus:border-gray-600 dark:focus:border-gray-400 focus:ring-1 focus:ring-gray-600/20 dark:focus:ring-gray-400/20 shadow-sm text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500"
                    rows={3}
                    disabled={isGenerating}
                  />
                  <button
                    onClick={handleSend}
                    disabled={!inputValue.trim() || isGenerating}
                    className="bg-gray-800 dark:bg-gray-200 hover:bg-gray-900 dark:hover:bg-gray-100 text-white dark:text-slate-900 px-6 rounded shadow-sm disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    <Send className="w-4 h-4" />
                  </button>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="text-center mb-6">
                    <h3 className="text-gray-800 dark:text-gray-100 tracking-wide">完善作品信息</h3>
                    <div className="w-12 h-px bg-gray-300 dark:bg-gray-600 mx-auto mt-3"></div>
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
                      className={`w-full bg-white dark:bg-slate-800 border ${errors.title ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'} rounded px-3 py-2 outline-none focus:border-gray-600 dark:focus:border-gray-400 focus:ring-1 focus:ring-gray-600/20 dark:focus:ring-gray-400/20 shadow-sm text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500`}
                    />
                    {errors.title && <span className="text-sm text-red-500">{errors.title}</span>}
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
                      className={`w-full bg-white dark:bg-slate-800 border ${errors.description ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'} rounded px-3 py-2 outline-none focus:border-gray-600 dark:focus:border-gray-400 focus:ring-1 focus:ring-gray-600/20 dark:focus:ring-gray-400/20 shadow-sm resize-none text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500`}
                      rows={4}
                    />
                    {errors.description && <span className="text-sm text-red-500">{errors.description}</span>}
                  </div>
                  <button
                    onClick={handleFinish}
                    className="w-full bg-gray-800 dark:bg-gray-200 hover:bg-gray-900 dark:hover:bg-gray-100 text-white dark:text-slate-900 py-2 rounded shadow-sm transition-colors"
                  >
                    完成创建
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* 中间分隔线 - 水墨竹影装饰 */}
        <div className="relative w-px">
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-gray-300 dark:via-gray-600 to-transparent"></div>
          {/* 竹节装饰点 */}
          <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full"></div>
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full"></div>
          <div className="absolute top-3/4 left-1/2 -translate-x-1/2 w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full"></div>
        </div>

        {/* 右侧世界观区 - 50% 宽度，时间轴式 */}
        <div className="w-1/2 flex flex-col overflow-hidden">
          <div className="flex-1 px-12 py-8 overflow-y-auto">
            {/* 时间轴容器 */}
            <div className="relative pl-8">
              {/* 时间轴竖线 */}
              <div className="absolute left-4 top-0 bottom-0 w-px bg-gradient-to-b from-gray-300 dark:from-gray-600 via-gray-400 dark:via-gray-500 to-gray-300 dark:to-gray-600"></div>

              {/* 第一部分：创作规范 */}
              <div className="mb-12">
                <div className="flex items-center gap-3 mb-8 -ml-8">
                  <div className="w-8 h-px bg-gray-300 dark:bg-gray-600"></div>
                  <h3 className="text-sm text-gray-500 dark:text-gray-400 tracking-wider">创作规范</h3>
                  <div className="flex-1 h-px bg-gray-300 dark:bg-gray-600"></div>
                </div>

                <div className="space-y-5">
                  {worldviewData.slice(0, 5).map((module, index) => (
                    <motion.div
                      key={module.id}
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="relative"
                    >
                      {/* 时间轴节点 */}
                      <div className="absolute -left-8 top-2">
                        {isModuleCompleted(module) ? (
                          <>
                            <motion.div
                              initial={{ scale: 0 }}
                              animate={{ scale: 1 }}
                              className="absolute inset-0 -m-1.5"
                            >
                              <div className="w-full h-full bg-gray-900/5 dark:bg-gray-100/10 rounded-full blur-sm"></div>
                            </motion.div>
                            <div className="relative w-2.5 h-2.5 bg-gray-800 dark:bg-gray-200 rounded-full border-2 border-[#faf9f6] dark:border-slate-900"></div>
                          </>
                        ) : isModulePartial(module) ? (
                          <div className="w-2.5 h-2.5 bg-gray-400 dark:bg-gray-500 rounded-full border-2 border-[#faf9f6] dark:border-slate-900"></div>
                        ) : (
                          <div className="w-2.5 h-2.5 bg-white dark:bg-slate-800 rounded-full border-2 border-gray-300 dark:border-gray-600"></div>
                        )}
                      </div>

                      {/* 模块卡片 */}
                      <div className="bg-white dark:bg-slate-800 border border-gray-200 dark:border-gray-700 rounded-lg p-3.5 shadow-sm hover:shadow-md transition-shadow">
                        <div className="flex items-center justify-between mb-2.5">
                          <h4 className="text-sm text-gray-800 dark:text-gray-100 tracking-wide">{module.name}</h4>
                          <button
                            onClick={() => setEditingModuleId(editingModuleId === module.id ? null : module.id)}
                            className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
                          >
                            {editingModuleId === module.id ? (
                              <X className="w-2.5 h-2.5 text-gray-600 dark:text-gray-400" />
                            ) : (
                              <Pencil className="w-2.5 h-2.5 text-gray-600 dark:text-gray-400" />
                            )}
                          </button>
                        </div>

                        <div className="space-y-2">
                          {module.fields.map((field) => {
                            if (!editingModuleId && editingModuleId !== module.id && !field.completed) return null;

                            return (
                              <div key={field.id} className="space-y-1">
                                <div className="flex items-center gap-1.5 text-xs">
                                  {field.completed ? (
                                    <CheckCircle2 className="w-3 h-3 text-green-600 dark:text-green-400 flex-shrink-0" />
                                  ) : (
                                    <Circle className="w-3 h-3 text-gray-300 dark:text-gray-600 flex-shrink-0" />
                                  )}
                                  <span className="text-gray-600 dark:text-gray-400">
                                    {field.label}
                                    {field.required && <span className="text-red-500 ml-1">*</span>}
                                  </span>
                                </div>
                                {editingModuleId === module.id ? (
                                  <textarea
                                    value={field.value}
                                    onChange={(e) => {
                                      const newData = [...worldviewData];
                                      const moduleIndex = worldviewData.findIndex(m => m.id === module.id);
                                      const fieldIndex = module.fields.findIndex(f => f.id === field.id);
                                      newData[moduleIndex].fields[fieldIndex].value = e.target.value;
                                      newData[moduleIndex].fields[fieldIndex].completed = e.target.value.trim() !== '';
                                      setWorldviewData(newData);
                                    }}
                                    placeholder={`请输入${field.label}`}
                                    className="w-full text-xs bg-[#faf9f6] dark:bg-slate-900 border border-gray-300 dark:border-gray-600 rounded px-2 py-1 outline-none focus:border-gray-600 dark:focus:border-gray-400 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500"
                                    rows={1}
                                  />
                                ) : (
                                  <p className="text-xs text-gray-500 dark:text-gray-400 pl-4 leading-relaxed">{field.value}</p>
                                )}
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* 第二部分：核心设定 */}
              <div>
                <div className="flex items-center gap-3 mb-8 -ml-8">
                  <div className="w-8 h-px bg-gray-300 dark:bg-gray-600"></div>
                  <h3 className="text-sm text-gray-500 dark:text-gray-400 tracking-wider">核心设定（AI生成）</h3>
                  <div className="flex-1 h-px bg-gray-300 dark:bg-gray-600"></div>
                </div>

                <div className="space-y-8">
                  {worldviewData.slice(5).map((module, index) => {
                    const hasCompletedFields = module.fields.some(f => f.completed);
                    if (!editingModuleId && editingModuleId !== module.id && !hasCompletedFields) return null;

                    return (
                      <motion.div
                        key={module.id}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="relative"
                      >
                        {/* 时间轴节点 */}
                        <div className="absolute -left-8 top-3">
                          {isModuleCompleted(module) ? (
                            <>
                              <motion.div
                                initial={{ scale: 0 }}
                                animate={{ scale: 1 }}
                                className="absolute inset-0 -m-2"
                              >
                                <div className="w-full h-full bg-gray-900/5 dark:bg-gray-100/10 rounded-full blur-sm"></div>
                              </motion.div>
                              <div className="relative w-3 h-3 bg-gray-800 dark:bg-gray-200 rounded-full border-2 border-[#faf9f6] dark:border-slate-900"></div>
                            </>
                          ) : isModulePartial(module) ? (
                            <div className="w-3 h-3 bg-gray-400 dark:bg-gray-500 rounded-full border-2 border-[#faf9f6] dark:border-slate-900"></div>
                          ) : (
                            <div className="w-3 h-3 bg-white dark:bg-slate-800 rounded-full border-2 border-gray-300 dark:border-gray-600"></div>
                          )}
                        </div>

                        {/* 模块卡片 */}
                        <div className="bg-white dark:bg-slate-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5 shadow-sm hover:shadow-md transition-shadow">
                          <div className="flex items-center justify-between mb-4">
                            <h4 className="text-gray-800 dark:text-gray-100 tracking-wide">{module.name}</h4>
                            <button
                              onClick={() => setEditingModuleId(editingModuleId === module.id ? null : module.id)}
                              className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
                            >
                              {editingModuleId === module.id ? (
                                <X className="w-3 h-3 text-gray-600 dark:text-gray-400" />
                              ) : (
                                <Pencil className="w-3 h-3 text-gray-600 dark:text-gray-400" />
                              )}
                            </button>
                          </div>

                          <div className="space-y-3">
                            {module.fields.map((field) => {
                              if (!editingModuleId && editingModuleId !== module.id && !field.completed) return null;

                              return (
                                <div key={field.id} className="space-y-1.5">
                                  <div className="flex items-center gap-2 text-sm">
                                    {field.completed ? (
                                      <CheckCircle2 className="w-3.5 h-3.5 text-green-600 dark:text-green-400 flex-shrink-0" />
                                    ) : (
                                      <Circle className="w-3.5 h-3.5 text-gray-300 dark:text-gray-600 flex-shrink-0" />
                                    )}
                                    <span className="text-gray-600 dark:text-gray-400">{field.label}</span>
                                  </div>
                                  {editingModuleId === module.id ? (
                                    <textarea
                                      value={field.value}
                                      onChange={(e) => {
                                        const newData = [...worldviewData];
                                        const moduleIndex = worldviewData.findIndex(m => m.id === module.id);
                                        const fieldIndex = module.fields.findIndex(f => f.id === field.id);
                                        newData[moduleIndex].fields[fieldIndex].value = e.target.value;
                                        newData[moduleIndex].fields[fieldIndex].completed = e.target.value.trim() !== '';
                                        setWorldviewData(newData);
                                      }}
                                      placeholder={`请输入${field.label}`}
                                      className="w-full text-sm bg-[#faf9f6] dark:bg-slate-900 border border-gray-300 dark:border-gray-600 rounded px-2 py-1 outline-none focus:border-gray-600 dark:focus:border-gray-400 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500"
                                      rows={1}
                                    />
                                  ) : (
                                    <p className="text-sm text-gray-500 dark:text-gray-400 pl-5 leading-relaxed">{field.value}</p>
                                  )}
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      </motion.div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateWorkWithAI;
