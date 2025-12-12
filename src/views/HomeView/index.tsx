/**
 * 首页视图 - 全屏滚动式设计
 *
 * 采用现代化的全屏滚动效果，5个章节展示产品特性
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import ChapterHomePage from './ChapterHomePage';

const HomeView: React.FC = () => {
  const navigate = useNavigate();

  return (
    <ChapterHomePage
      onNavigateToAuth={() => navigate('/login')}
      onNavigateToSubscription={() => navigate('/subscription')}
      onNavigateToContact={() => navigate('/contact')}
    />
  );
};

export default HomeView;
