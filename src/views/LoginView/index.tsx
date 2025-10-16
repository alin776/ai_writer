import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { AuthService } from '../../services/AuthService';
import { Sparkles, ArrowLeft } from 'lucide-react';
import styles from './LoginView.module.css';

/**
 * LoginView 组件 - 登录页面
 * 极简美学设计
 */
const LoginView: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuthStore();

  const [formData, setFormData] = useState({
    username: '',  // 后端使用 username（可以是邮箱或用户名）
    password: '',
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

    if (!formData.username) {
      newErrors.username = '请输入用户名或邮箱';
    }

    if (!formData.password) {
      newErrors.password = '请输入密码';
    } else if (formData.password.length < 6) {
      newErrors.password = '密码至少需要 6 个字符';
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
      // 调用 AuthService 登录
      const response = await AuthService.login({
        username: formData.username,
        password: formData.password,
      });

      // 登录成功
      login(response.user, response.token);
      navigate('/works');
    } catch (error: any) {
      const errorMessage = error.message || '登录失败，请检查用户名和密码';
      setErrors({ submit: errorMessage });
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
          <h1 className={styles.logoText}>登录账户</h1>
          <p className={styles.logoSubtext}>欢迎回到 AI Writer</p>
        </div>

        {/* 登录表单 */}
        <form onSubmit={handleSubmit} className={styles.form}>
          {/* 用户名/邮箱输入 */}
          <div className={styles.formGroup}>
            <label htmlFor="username" className={styles.label}>
              用户名或邮箱
            </label>
            <input
              id="username"
              name="username"
              type="text"
              value={formData.username}
              onChange={handleChange}
              placeholder="用户名或邮箱地址"
              className={`${styles.input} ${errors.username ? styles.error : ''}`}
            />
            {errors.username && <span className={styles.errorMessage}>{errors.username}</span>}
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

          {/* 提交错误提示 */}
          {errors.submit && (
            <div className={styles.errorMessage} style={{ textAlign: 'center' }}>
              {errors.submit}
            </div>
          )}

          {/* 登录按钮 */}
          <button type="submit" disabled={isLoading} className={styles.submitButton}>
            {isLoading ? '登录中...' : '登录'}
          </button>
        </form>

        {/* 注册链接 */}
        <div className={styles.footer}>
          <p className={styles.footerText}>
            还没有账号？
            <Link to="/register" className={styles.footerLink}>
              立即注册
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginView;
