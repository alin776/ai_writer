import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CreateWorkChoice from './CreateWorkChoice';
import CreateWorkManual from './CreateWorkManual';
import CreateWorkWithAI from './CreateWorkWithAI';
import { DataService } from '../../services/DataService';
import { useGlobalStore } from '../../store/globalStore';
import type { CreateWorkData } from '../../types';

/**
 * 创建模式
 */
type CreateMode = 'choice' | 'manual' | 'ai';

/**
 * 世界观数据结构（对应后端AIGuidelines的31个字段）
 */
export interface WorldViewData {
  // 阶段一：创作规范（用户回答的15个字段）
  // 战略定位
  businessGoal?: string; // 商业目标
  targetAudience?: string; // 目标读者
  commercialBenchmark?: string; // 商业对标
  highConcept?: string; // 高概念卖点
  // IP架构
  coreParadox?: string; // 核心悖论/设定
  dominantEmotion?: string; // 主导情感
  coreIpSymbols?: string; // 核心IP符号
  // 叙事引擎
  protagonistArc?: string; // 主角弧光
  coreConflict?: string; // 核心关系冲突
  narrativeRhythm?: string; // 叙事节奏
  // 文字质感
  writingStyle?: string; // 文笔风格
  styleNotes?: string; // 文风注意事项
  // 技术规范
  chapterLength?: string; // 章节长度
  contentTaboos?: string; // 内容禁忌
  
  // 阶段二：核心设定（AI自动生成的17个字段）
  // 小说类型
  primaryGenre?: string; // 一级类型
  secondaryTags?: string; // 二级标签
  creativeTone?: string; // 创作基调
  // 世界背景
  worldIntro?: string; // 核心世界观简介
  mainLocations?: string; // 主要场景/地点
  worldRules?: string; // 世界规则
  // 力量体系
  powerSystemName?: string; // 体系名称
  powerLevels?: string; // 等级划分
  powerCost?: string; // 代价与限制
  // 主角设定
  protagonistName?: string; // 主角名字
  protagonistIdentity?: string; // 身份与背景
  protagonistTraits?: string; // 性格特点
  protagonistGoal?: string; // 终极目标
  // 剧情构思
  conflictDesign?: string; // 冲突设计
  actOne?: string; // 第一幕
  actTwo?: string; // 第二幕
  actThree?: string; // 第三幕
  
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
      
      // 如果有世界观数据，保存AI规范到数据库
      if (Object.keys(worldView).length > 0) {
        try {
          console.log('[CreateWorkView] 保存AI规范数据...');
          await DataService.createOrUpdateAIGuidelines(newWork.id, worldView);
          console.log('[CreateWorkView] AI规范保存成功');
        } catch (error) {
          console.error('[CreateWorkView] 保存AI规范失败:', error);
          // 不影响主流程，只记录错误
        }
      }
      
      showToast('success', '作品创建成功！');

      // 跳转到作品详情页，标记为新建作品
      navigate(`/works/${newWork.id}`, {
        state: { fromCreate: true }
      });
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
      
      // 如果有世界观数据，保存AI规范到数据库
      if (Object.keys(worldView).length > 0) {
        try {
          console.log('[CreateWorkView] 保存AI规范数据...');
          await DataService.createOrUpdateAIGuidelines(newWork.id, worldView);
          console.log('[CreateWorkView] AI规范保存成功');
        } catch (error) {
          console.error('[CreateWorkView] 保存AI规范失败:', error);
          // 不影响主流程，只记录错误
        }
      }
      
      showToast('success', '作品创建成功！');

      // 跳转到作品详情页，标记为新建作品
      navigate(`/works/${newWork.id}`, {
        state: { fromCreate: true }
      });
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
    <div className="w-screen min-h-screen">
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
