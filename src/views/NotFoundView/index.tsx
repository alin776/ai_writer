import React from 'react';
import { Link } from 'react-router-dom';
import { Home } from 'lucide-react';
import styles from './NotFoundView.module.css';

/**
 * NotFoundView 组件 - 404 页面
 * 极简设计，灰度色系
 */
const NotFoundView: React.FC = () => {
  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <h1 className={styles.title}>404</h1>
        <p className={styles.subtitle}>页面未找到</p>
        <Link to="/" className={styles.button}>
          <Home size={18} strokeWidth={2} />
          返回首页
        </Link>
      </div>
    </div>
  );
};

export default NotFoundView;
