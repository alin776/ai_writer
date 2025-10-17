import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CreateWorkChoice from './CreateWorkChoice';
import CreateWorkManual from './CreateWorkManual';
import CreateWorkWithAI from './CreateWorkWithAI';
import { DataService } from '../../services/DataService';
import { useGlobalStore } from '../../store/globalStore';
import type { CreateWorkData } from '../../types';
import styles from './CreateWorkView.module.css';

/**
 * 创建模式
 */
type CreateMode = 'choice' | 'manual' | 'ai';

/**
 * 世界观数据结构
 */
export interface WorldViewData {
  genre?: string; // 小说类型（玄幻、都市、科幻等）
  setting?: string; // 背景设定
  powerSystem?: string; // 力量体系
  mainCharacter?: string; // 主角设定
  plotIdea?: string; // 剧情构思
  worldRules?: string; // 世界规则
  [key: string]: string | undefined;
}

/**
 * CreateWorkView 组件 - 创建小说流程页面
 * 
 * 流程：
 * 1. 选择模式（已有思路 or AI辅助）
 * 2. 填写信息（手动填写 or AI对话）
 * 3. 完成创建，跳转到编辑界面
 */
const CreateWorkView: React.FC = () => {
  const navigate = useNavigate();
  const { showToast } = useGlobalStore();
  
  // 当前模式
  const [mode, setMode] = useState<CreateMode>('choice');
  
  // 小说基本信息
  const [workData, setWorkData] = useState<CreateWorkData>({
    title: '',
    description: '',
  });
  
  // 世界观数据
  const [worldViewData, setWorldViewData] = useState<WorldViewData>({});

  /**
   * 处理模式选择
   */
  const handleModeSelect = (selectedMode: 'manual' | 'ai') => {
    setMode(selectedMode);
  };

  /**
   * 处理手动创建提交
   */
  const handleManualSubmit = async (data: CreateWorkData, worldView: WorldViewData) => {
    try {
      // 保存数据
      setWorkData(data);
      setWorldViewData(worldView);
      
      // 创建作品
      const newWork = await DataService.createWork({
        title: data.title,
        description: data.description,
      });
      
      showToast('success', '作品创建成功！');
      
      // 跳转到作品详情页
      navigate(`/works/${newWork.id}`);
    } catch (error) {
      showToast('error', '创建失败，请重试');
      console.error('Failed to create work:', error);
    }
  };

  /**
   * 处理AI辅助完成
   */
  const handleAIComplete = async (data: CreateWorkData, worldView: WorldViewData) => {
    try {
      // 保存数据
      setWorkData(data);
      setWorldViewData(worldView);
      
      // 创建作品
      const newWork = await DataService.createWork({
        title: data.title,
        description: data.description,
      });
      
      showToast('success', '作品创建成功！');
      
      // 跳转到作品详情页
      navigate(`/works/${newWork.id}`);
    } catch (error) {
      showToast('error', '创建失败，请重试');
      console.error('Failed to create work:', error);
    }
  };

  /**
   * 返回上一步
   */
  const handleBack = () => {
    if (mode === 'manual' || mode === 'ai') {
      setMode('choice');
    } else {
      navigate('/works');
    }
  };

  return (
    <div className={styles.container}>
      {mode === 'choice' && (
        <CreateWorkChoice
          onSelect={handleModeSelect}
          onBack={handleBack}
        />
      )}
      
      {mode === 'manual' && (
        <CreateWorkManual
          onSubmit={handleManualSubmit}
          onBack={handleBack}
        />
      )}
      
      {mode === 'ai' && (
        <CreateWorkWithAI
          onComplete={handleAIComplete}
          onBack={handleBack}
        />
      )}
    </div>
  );
};

export default CreateWorkView;
