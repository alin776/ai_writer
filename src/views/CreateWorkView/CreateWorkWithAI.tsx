import React, { useState, useRef, useEffect } from 'react';
import { ArrowLeft, Send, Sparkles, Edit2, Check, X } from 'lucide-react';
import WorldCompletionSidebar from './WorldCompletionSidebar';
import type { CreateWorkData } from '../../types';
import type { WorldViewData } from './index';
import styles from './CreateWorkView.module.css';

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
 * AI 引导问题列表
 * 按照顺序逐个询问，收集世界观信息
 */
const AI_QUESTIONS = [
  {
    key: 'genre',
    question: '你好！让我帮你构建一个完整的小说世界观。首先，你想创作什么类型的小说呢？（如：玄幻、都市、科幻、武侠等）',
    field: 'genre'
  },
  {
    key: 'setting',
    question: '很好！接下来，请描述一下故事发生的背景设定。比如时代、地点、社会环境等。',
    field: 'setting'
  },
  {
    key: 'powerSystem',
    question: '了解了。那么这个世界有什么特殊的力量体系或规则吗？（如修仙等级、魔法体系、科技水平等，如果没有可以跳过）',
    field: 'powerSystem'
  },
  {
    key: 'mainCharacter',
    question: '来说说主角吧！主角是什么样的人？有什么特殊的背景或能力吗？',
    field: 'mainCharacter'
  },
  {
    key: 'plotIdea',
    question: '太棒了！那么你对剧情有什么想法吗？主线故事会如何展开？',
    field: 'plotIdea'
  },
  {
    key: 'worldRules',
    question: '最后，这个世界有什么特殊的规则或法则吗？（可选）',
    field: 'worldRules'
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
    const newMessage: Message = {
      id: Date.now().toString(),
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
    const newMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, newMessage]);
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
    
    // 更新世界观数据
    setWorldViewData(prev => ({
      ...prev,
      [currentQuestion.field]: userInput
    }));

    // 模拟AI回复并进入下一个问题
    setTimeout(() => {
      const nextIndex = currentQuestionIndex + 1;
      
      if (nextIndex < AI_QUESTIONS.length) {
        // 还有问题，继续提问
        addAssistantMessage('非常好！' + AI_QUESTIONS[nextIndex].question);
        setCurrentQuestionIndex(nextIndex);
      } else {
        // 所有问题回答完毕
        addAssistantMessage('太棒了！世界观设定已经基本完成。你可以在右侧查看和编辑这些信息，完成后填写作品标题和简介即可开始创作！');
        setShowFinalForm(true);
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
   * 验证并提交
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
