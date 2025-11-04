import React, { useState, useRef, useEffect } from 'react';
import { ArrowLeft, Send, Sparkles } from 'lucide-react';
import WorldCompletionSidebar from './WorldCompletionSidebar';
import type { CreateWorkData } from '../../types';
import type { WorldViewData } from './index';
import styles from './CreateWorkView.module.css';
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
 * AI 引导问题列表 - 阶段一：创作规范问诊
 * 按照商业IP总策划师的方式，系统化收集创作规范信息
 */
const AI_QUESTIONS = [
  // === 模块一：战略定位 ===
  {
    key: 'intro',
    module: '战略定位',
    question: '你好！我是你的商业IP总策划师。让我帮助你系统化地构建一部具备商业潜力的小说！\n\n我们将分5个模块，共15个问题来完成创作规范的制定。准备好了吗？让我们从第一个模块开始！\n\n【模块一：战略定位】\n首先，这部小说的核心商业目标是什么？（例如：快速盈利、打造IP、建立作者品牌）',
    field: 'businessGoal'
  },
  {
    key: 'targetAudience',
    module: '战略定位',
    question: '很好！那么我们明确瞄准的读者画像是怎样的？请描述年龄、性别、阅读偏好、消费能力等。',
    field: 'targetAudience'
  },
  {
    key: 'commercialBenchmark',
    module: '战略定位',
    question: '了解。请提供1-2个商业对标作品，并说明我们希望借鉴其哪些优点，以及在哪些方面实现差异化？',
    field: 'commercialBenchmark'
  },
  {
    key: 'highConcept',
    module: '战略定位',
    question: '请用一句话，提炼出我们小说的高概念卖点。格式：当[经典类型]遇上[新奇元素]。',
    field: 'highConcept'
  },
  
  // === 模块二：IP架构 ===
  {
    key: 'coreParadox',
    module: 'IP架构',
    question: '【模块二：IP架构】\n这个故事最核心的、能引发讨论的核心悖论或世界观亮点是什么？（例如：不能说话的播音员、害怕水的航海家）',
    field: 'coreParadox'
  },
  {
    key: 'dominantEmotion',
    module: 'IP架构',
    question: '我们希望读者在读完小说后，带走哪一种最主要的情感体验？（例如：逆袭的爽感、被理解的慰藉、探索的惊奇）',
    field: 'dominantEmotion'
  },
  {
    key: 'coreIpSymbols',
    module: 'IP架构',
    question: '请构思2-3个具有高辨识度和衍生潜力的核心IP符号。（如：一个标志性道具、一个独特地点、一种视觉特征）',
    field: 'coreIpSymbols'
  },
  
  // === 模块三：叙事引擎 ===
  {
    key: 'protagonistArc',
    module: '叙事引擎',
    question: '【模块三：叙事引擎】\n主角最大的内在缺陷和最强的核心能力分别是什么？他/她必须完成的核心转变是什么？',
    field: 'protagonistArc'
  },
  {
    key: 'coreConflict',
    module: '叙事引擎',
    question: '主角与主要对手/伙伴之间，最根本的价值观冲突是什么？',
    field: 'coreConflict'
  },
  {
    key: 'narrativeRhythm',
    module: '叙事引擎',
    question: '我们计划采用什么样的叙事节奏？（例如：快节奏强冲突、慢热型注重铺垫，或3章一小爽、10章一大爽）',
    field: 'narrativeRhythm'
  },
  
  // === 模块四：文字质感 ===
  {
    key: 'writingStyle',
    module: '文字质感',
    question: '【模块四：文字质感】\n我们希望这部小说的文字风格偏向哪种？（例如：冷峻简洁、华丽诗性、幽默诙谐、平实感人）',
    field: 'writingStyle'
  },
  {
    key: 'styleNotes',
    module: '文字质感',
    question: '是否有必须避免的文风或写作习惯？（例如：避免冗长对话、多用动作描写）',
    field: 'styleNotes'
  },
  
  // === 模块五：技术规范 ===
  {
    key: 'chapterLength',
    module: '技术规范',
    question: '【模块五：技术规范】\n计划的平均章节字数是多少？（例如：2000-3000字）',
    field: 'chapterLength'
  },
  {
    key: 'contentTaboos',
    module: '技术规范',
    question: '最后一个问题！需要严格遵守的内容禁忌有哪些？（例如：政治红线、特定类型的描写限制）',
    field: 'contentTaboos'
  }
];

/**
 * CreateWorkWithAI 组件 - AI辅助创建作品
 * 
 * 功能：
 * - AI对话界面（左侧）
 * - 世界观完成度展示（右侧侧边栏）
 * - 用户可以随时编辑AI填写的世界观信息
 */
const CreateWorkWithAI: React.FC<CreateWorkWithAIProps> = ({ onComplete, onBack }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [worldViewData, setWorldViewData] = useState<WorldViewData>({});
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState<WorldViewData>({});
  const [showFinalForm, setShowFinalForm] = useState(false);
  const [finalData, setFinalData] = useState({ title: '', description: '' });
  const [errors, setErrors] = useState<Record<string, string>>({});
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const messageIdCounter = useRef(0);

  /**
   * 初始化 - 发送第一个问题，并滚动到顶部
   */
  useEffect(() => {
    if (messages.length === 0) {
      addAssistantMessage(AI_QUESTIONS[0].question);
    }
    
    // 延迟滚动到页面顶部，确保在消息添加后执行
    setTimeout(() => {
      window.scrollTo({ top: 0, behavior: 'auto' });
    }, 0);
  }, []);

  /**
   * 滚动到底部（仅在聊天容器内滚动）
   */
  useEffect(() => {
    // 只有在有消息时才滚动聊天容器
    if (messages.length > 0 && chatContainerRef.current) {
      const container = chatContainerRef.current;
      // 使用 requestAnimationFrame 确保DOM更新完成后再滚动
      requestAnimationFrame(() => {
        container.scrollTop = container.scrollHeight;
      });
    }
  }, [messages]);

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
   * 基于阶段一的15个回答，调用后端API自动生成17个核心设定字段
   */
  const generatePhase2Content = async (phase1Data: WorldViewData): Promise<WorldViewData> => {
    try {
      // AIService 是单例实例，直接使用
      // 调用后端API生成阶段二内容
      const phase2Data = await AIService.generatePhase2Content({
        businessGoal: phase1Data.businessGoal,
        targetAudience: phase1Data.targetAudience,
        commercialBenchmark: phase1Data.commercialBenchmark,
        highConcept: phase1Data.highConcept,
        coreParadox: phase1Data.coreParadox,
        dominantEmotion: phase1Data.dominantEmotion,
        coreIpSymbols: phase1Data.coreIpSymbols,
        protagonistArc: phase1Data.protagonistArc,
        coreConflict: phase1Data.coreConflict,
        narrativeRhythm: phase1Data.narrativeRhythm,
        writingStyle: phase1Data.writingStyle,
        styleNotes: phase1Data.styleNotes,
        chapterLength: phase1Data.chapterLength,
        contentTaboos: phase1Data.contentTaboos,
      });
      
      return phase2Data as WorldViewData;
    } catch (error) {
      console.error('生成阶段二内容失败:', error);
      // 如果API失败，使用备用方案
      return {
        primaryGenre: '都市异能',
        secondaryTags: '职场、悬疑、升级流',
        creativeTone: '明快积极，主打逆袭爽感',
        worldIntro: '现代都市与超能力交织的世界',
        mainLocations: '写字楼、秘密研究所、关键地点',
        worldRules: '人类的情绪波动会产生能量',
        powerSystemName: '特殊能力体系',
        powerLevels: '初级 → 中级 → 高级 → 顶级',
        powerCost: '需要付出代价才能获得或提升力量',
        protagonistName: '林默',
        protagonistIdentity: '普通人出身，拥有特殊潜质',
        protagonistTraits: '隐忍、果敢、内心细腻',
        protagonistGoal: '实现自我价值，保护重要的人',
        conflictDesign: '主角理想与现实的冲突',
        actOne: '建立世界观，主角遭遇变故，踏上旅程',
        actTwo: '主角成长，遭遇挫折，逐渐变强',
        actThree: '最终对决，解决核心冲突，完成成长蜕变'
      };
    }
  };

  /**
   * 处理发送消息
   */
  const handleSend = () => {
    if (!inputValue.trim()) return;

    const userInput = inputValue.trim();
    addUserMessage(userInput);
    setInputValue('');

    // 获取当前问题对应的字段
    const currentQuestion = AI_QUESTIONS[currentQuestionIndex];
    
    // 更新世界观数据（阶段一数据）
    const updatedData = {
      ...worldViewData,
      [currentQuestion.field]: userInput
    };
    setWorldViewData(updatedData);

    // 模拟AI回复并进入下一个问题
    setTimeout(() => {
      const nextIndex = currentQuestionIndex + 1;
      
      if (nextIndex < AI_QUESTIONS.length) {
        // 还有问题，继续提问
        const nextQuestion = AI_QUESTIONS[nextIndex];
        const prefix = nextQuestion.module !== currentQuestion.module ? '' : '非常好！';
        addAssistantMessage(prefix + nextQuestion.question);
        setCurrentQuestionIndex(nextIndex);
      } else {
        // 阶段一完成，开始阶段二
        addAssistantMessage('✨ 太棒了！【阶段一：创作规范】已经完成！\n\n现在让我基于您提供的信息，为您自动生成【阶段二：核心设定】...');
        
        // 调用真实的API生成阶段二内容
        (async () => {
          try {
            const phase2Data = await generatePhase2Content(updatedData);
            const fullData = { ...updatedData, ...phase2Data };
            setWorldViewData(fullData);
            
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
   * 开始编辑世界观
   */
  const handleStartEdit = () => {
    setEditData({ ...worldViewData });
    setIsEditing(true);
  };

  /**
   * 保存编辑
   */
  const handleSaveEdit = () => {
    setWorldViewData(editData);
    setIsEditing(false);
  };

  /**
   * 取消编辑
   */
  const handleCancelEdit = () => {
    setEditData({});
    setIsEditing(false);
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
   * 验证必填字段
   */
  const validateRequiredFields = (): Record<string, string> => {
    const errors: Record<string, string> = {};
    
    // 验证阶段一的必填字段（14个必填）
    const requiredPhase1Fields = [
      { key: 'businessGoal', label: '商业目标' },
      { key: 'targetAudience', label: '目标读者' },
      { key: 'commercialBenchmark', label: '商业对标' },
      { key: 'highConcept', label: '高概念卖点' },
      { key: 'coreParadox', label: '核心悖论/设定' },
      { key: 'dominantEmotion', label: '主导情感' },
      { key: 'coreIpSymbols', label: '核心IP符号' },
      { key: 'protagonistArc', label: '主角弧光' },
      { key: 'coreConflict', label: '核心关系冲突' },
      { key: 'narrativeRhythm', label: '叙事节奏' },
      { key: 'writingStyle', label: '文笔风格' },
      { key: 'chapterLength', label: '章节长度' },
    ];
    
    let missingFields: string[] = [];
    requiredPhase1Fields.forEach(field => {
      const value = worldViewData[field.key];
      if (!value || !value.trim()) {
        missingFields.push(field.label);
      }
    });
    
    if (missingFields.length > 0) {
      errors.worldview = `请完成所有必填项：${missingFields.join('、')}`;
    }
    
    return errors;
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

    // 验证世界观必填字段
    const worldviewErrors = validateRequiredFields();
    Object.assign(newErrors, worldviewErrors);

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      // 如果有世界观错误，显示提示
      if (worldviewErrors.worldview) {
        addAssistantMessage(`⚠️ ${worldviewErrors.worldview}`);
      }
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
    <div className={styles.aiContainer}>
      {/* 返回按钮 */}
      <button className={styles.backButton} onClick={onBack}>
        <ArrowLeft size={20} />
        <span>返回</span>
      </button>

      {/* 主内容区 */}
      <div className={styles.aiContent}>
        {/* 左侧：对话区 */}
        <div className={styles.chatSection}>
          <div className={styles.chatHeader}>
            <Sparkles size={24} />
            <div>
              <h2 className={styles.chatTitle}>AI 创作助手</h2>
              <p className={styles.chatSubtitle}>让我帮你构建完整的世界观</p>
            </div>
          </div>

          {/* 消息列表 */}
          <div className={styles.chatMessages} ref={chatContainerRef}>
            {messages.map((message) => (
              <div
                key={message.id}
                className={`${styles.message} ${
                  message.role === 'assistant' ? styles.messageAssistant : styles.messageUser
                }`}
              >
                <div className={styles.messageContent}>{message.content}</div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* 输入区 */}
          {!showFinalForm && (
            <div className={styles.chatInput}>
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="输入您的回答..."
                className={styles.chatTextarea}
                rows={3}
              />
              <button
                onClick={handleSend}
                disabled={!inputValue.trim()}
                className={styles.sendButton}
              >
                <Send size={20} />
              </button>
            </div>
          )}

          {/* 最终表单 */}
          {showFinalForm && (
            <div className={styles.finalForm}>
              <h3 className={styles.finalFormTitle}>完善作品信息</h3>
              
              <div className={styles.formGroup}>
                <label className={styles.label}>
                  作品标题 <span className={styles.required}>*</span>
                </label>
                <input
                  type="text"
                  name="title"
                  value={finalData.title}
                  onChange={handleFinalChange}
                  placeholder="请输入作品标题"
                  className={`${styles.input} ${errors.title ? styles.inputError : ''}`}
                />
                {errors.title && <span className={styles.errorMessage}>{errors.title}</span>}
              </div>

              <div className={styles.formGroup}>
                <label className={styles.label}>
                  作品简介 <span className={styles.required}>*</span>
                </label>
                <textarea
                  name="description"
                  value={finalData.description}
                  onChange={handleFinalChange}
                  placeholder="简要描述您的作品"
                  className={`${styles.textarea} ${errors.description ? styles.inputError : ''}`}
                  rows={4}
                />
                {errors.description && <span className={styles.errorMessage}>{errors.description}</span>}
              </div>

              <button onClick={handleFinish} className={styles.finishButton}>
                完成创建
              </button>
            </div>
          )}
        </div>

        {/* 右侧：世界观完成度侧边栏 */}
        <WorldCompletionSidebar
          worldViewData={isEditing ? editData : worldViewData}
          isEditing={isEditing}
          onEdit={handleStartEdit}
          onSave={handleSaveEdit}
          onCancel={handleCancelEdit}
          onChange={(field, value) => setEditData(prev => ({ ...prev, [field]: value }))}
        />
      </div>
    </div>
  );
};

export default CreateWorkWithAI;
