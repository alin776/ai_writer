/**
 * 首页视图
 *
 * 极简美学设计 - 专注、简约、呼吸感
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, BookOpen, Edit3, Lightbulb, Zap, Users, ArrowRight } from 'lucide-react';
import styles from './HomeView.module.css';

const HomeView: React.FC = () => {
  const navigate = useNavigate();

  // 功能特性 - 精简描述
  const features = [
    {
      icon: <Edit3 />,
      title: 'AI 智能续写',
      description: '基于上下文，生成连贯内容',
    },
    {
      icon: <Lightbulb />,
      title: '情节生成',
      description: '快速构建故事框架与转折',
    },
    {
      icon: <Users />,
      title: '角色设定',
      description: '自动生成完整人物背景',
    },
    {
      icon: <Zap />,
      title: '实时润色',
      description: '优化表达，提升文字质量',
    },
    {
      icon: <BookOpen />,
      title: '章节管理',
      description: '结构化组织作品内容',
    },
    {
      icon: <Sparkles />,
      title: '世界观构建',
      description: '系统化管理创作元素',
    },
  ];

  return (
    <div className={styles.page}>
      {/* Header - 极简设计 */}
      <header className={styles.header}>
        <div className={styles.headerContainer}>
          {/* Logo - 简约 */}
          <div className={styles.logo} onClick={() => navigate('/')}>
            <div className={styles.logoIcon}>
              <Sparkles size={14} color="#ffffff" />
            </div>
            <span className={styles.logoText}>AI Writer</span>
          </div>

          {/* Navigation - 去除装饰 */}
          <nav className={styles.nav}>
            <a href="#features" className={styles.navLink}>
              功能
            </a>
            <a href="#examples" className={styles.navLink}>
              示例
            </a>
          </nav>

          {/* CTA - 极简按钮 */}
          <div className={styles.cta}>
            <button onClick={() => navigate('/login')} className={styles.loginButton}>
              登录
            </button>
            <button onClick={() => navigate('/register')} className={styles.registerButton}>
              开始使用
            </button>
          </div>
        </div>
      </header>

      {/* Hero Section - 极简主义 */}
      <section className={styles.hero}>
        <div className={styles.heroContainer}>
          {/* Badge - 微妙标识 */}
          <div className={styles.badge}>
            <Sparkles size={12} />
            <span>AI-POWERED WRITING</span>
          </div>

          {/* Main Heading - 大标题，充足留白 */}
          <h1 className={styles.title}>
            专注创作
            <br />
            <span className={styles.titleEmphasis}>让 AI 处理其余</span>
          </h1>

          {/* Subtitle - 精简描述 */}
          <p className={styles.subtitle}>
            智能续写、情节生成、角色设定
            <br />
            专业的 AI 写作工具，让创作更高效
          </p>

          {/* CTA - 极简按钮组 */}
          <div className={styles.heroButtons}>
            <button onClick={() => navigate('/register')} className={styles.primaryButton}>
              开始创作
              <ArrowRight size={16} className={styles.arrowIcon} />
            </button>
            <button onClick={() => navigate('/login')} className={styles.secondaryButton}>
              查看示例
            </button>
          </div>
        </div>
      </section>

      {/* Features Section - 卡片式布局，大量留白 */}
      <section id="features" className={styles.features}>
        <div className={styles.featuresContainer}>
          {/* Section Header - 极简标题 */}
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>核心功能</h2>
            <p className={styles.sectionSubtitle}>专业工具集，简化创作流程</p>
          </div>

          {/* Feature Grid - 3列网格，充分留白 */}
          <div className={styles.featureGrid}>
            {features.map((feature, index) => (
              <div key={index} className={styles.featureCard}>
                {/* Icon - 极简图标 */}
                <div className={styles.featureIcon}>{feature.icon}</div>

                {/* Title - 清晰层级 */}
                <h3 className={styles.featureTitle}>{feature.title}</h3>

                {/* Description - 辅助文字 */}
                <p className={styles.featureDescription}>{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section - 极简黑白 */}
      <section className={styles.ctaSection}>
        <div className={styles.ctaSectionContainer}>
          <h2 className={styles.ctaSectionTitle}>开始你的创作</h2>
          <p className={styles.ctaSectionSubtitle}>免费注册，立即体验 AI 辅助写作</p>
          <div className={styles.ctaSectionButtons}>
            <button onClick={() => navigate('/register')} className={styles.ctaPrimaryButton}>
              免费注册
            </button>
            <button onClick={() => navigate('/login')} className={styles.ctaSecondaryButton}>
              登录账户
            </button>
          </div>
        </div>
      </section>

      {/* Footer - 极简页脚 */}
      <footer className={styles.footer}>
        <div className={styles.footerContainer}>
          <div className={styles.footerBrand}>
            <Sparkles size={12} />
            <span>AI Writer</span>
          </div>
          <div className={styles.footerCopyright}>© 2025</div>
        </div>
      </footer>
    </div>
  );
};

export default HomeView;
