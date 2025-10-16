import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { DataService } from '../../services/DataService';
import { Sparkles, ArrowLeft } from 'lucide-react';
import styles from './RegisterView.module.css';

/**
 * RegisterView 组件 - 注册页面
 * 极简美学设计
 */
const RegisterView: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuthStore();

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);

  /**
   * 处理输入变化
   */
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // 清除该字段的错误
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  /**
   * 表单验证
   */
  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.name) {
      newErrors.name = '请输入用户名';
    } else if (formData.name.length < 3) {
      newErrors.name = '用户名至少需要 3 个字符';
    }

    if (!formData.email) {
      newErrors.email = '请输入邮箱地址';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = '请输入有效的邮箱地址';
    }

    if (!formData.password) {
      newErrors.password = '请输入密码';
    } else if (formData.password.length < 6) {
      newErrors.password = '密码至少需要 6 个字符';
    }

    if (!formData.confirmPassword) {
      newErrors.confirmPassword = '请确认密码';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = '两次输入的密码不一致';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  /**
   * 处理表单提交
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) return;

    setIsLoading(true);

    try {
      // 调用 DataService 注册
      const response = await DataService.register({
        name: formData.name,
        email: formData.email,
        password: formData.password,
      });

      // 注册成功并自动登录
      login(response.user, response.token);
      navigate('/works');
    } catch (error) {
      setErrors({ submit: '注册失败，请稍后重试' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        {/* 返回首页 */}
        <Link to="/" className={styles.backLink}>
          <ArrowLeft size={16} />
          <span>返回首页</span>
        </Link>

        {/* Logo 和标题 */}
        <div className={styles.logo}>
          <div className={styles.logoIcon}>
            <Sparkles size={24} color="#ffffff" />
          </div>
          <h1 className={styles.logoText}>创建账户</h1>
          <p className={styles.logoSubtext}>开始您的 AI 写作之旅</p>
        </div>

        {/* 注册表单 */}
        <form onSubmit={handleSubmit} className={styles.form}>
          {/* 用户名输入 */}
          <div className={styles.formGroup}>
            <label htmlFor="name" className={styles.label}>
              用户名
            </label>
            <input
              id="name"
              name="name"
              type="text"
              value={formData.name}
              onChange={handleChange}
              placeholder="您的用户名"
              className={`${styles.input} ${errors.name ? styles.error : ''}`}
            />
            {errors.name && <span className={styles.errorMessage}>{errors.name}</span>}
          </div>

          {/* 邮箱输入 */}
          <div className={styles.formGroup}>
            <label htmlFor="email" className={styles.label}>
              邮箱地址
            </label>
            <input
              id="email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="your@email.com"
              className={`${styles.input} ${errors.email ? styles.error : ''}`}
            />
            {errors.email && <span className={styles.errorMessage}>{errors.email}</span>}
          </div>

          {/* 密码输入 */}
          <div className={styles.formGroup}>
            <label htmlFor="password" className={styles.label}>
              密码
            </label>
            <input
              id="password"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="至少 6 个字符"
              className={`${styles.input} ${errors.password ? styles.error : ''}`}
            />
            {errors.password && <span className={styles.errorMessage}>{errors.password}</span>}
          </div>

          {/* 确认密码输入 */}
          <div className={styles.formGroup}>
            <label htmlFor="confirmPassword" className={styles.label}>
              确认密码
            </label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="再次输入密码"
              className={`${styles.input} ${errors.confirmPassword ? styles.error : ''}`}
            />
            {errors.confirmPassword && <span className={styles.errorMessage}>{errors.confirmPassword}</span>}
          </div>

          {/* 提交错误提示 */}
          {errors.submit && (
            <div className={styles.errorMessage} style={{ textAlign: 'center' }}>
              {errors.submit}
            </div>
          )}

          {/* 注册按钮 */}
          <button type="submit" disabled={isLoading} className={styles.submitButton}>
            {isLoading ? '注册中...' : '注册'}
          </button>
        </form>

        {/* 登录链接 */}
        <div className={styles.footer}>
          <p className={styles.footerText}>
            已有账号？
            <Link to="/login" className={styles.footerLink}>
              立即登录
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default RegisterView;
