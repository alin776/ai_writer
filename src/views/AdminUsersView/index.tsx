import React, { useState, useEffect, useCallback } from 'react';
import { Search, Shield, ShieldOff, Ban, CheckCircle, Award, X, Check, Users } from 'lucide-react';
import { ADMIN_STYLES } from '../../styles/adminStyles';
import { DataService } from '../../services/DataService';
import { useGlobalStore } from '../../store/globalStore';
import { useAuthStore } from '../../store/authStore';
import type { User } from '../../types';
import { formatDate } from '../../utils/formatDate';

/**
 * AdminUsersView 组件 - 用户管理页面
 *
 * 功能：
 * - 显示用户列表
 * - 表格形式展示
 * - 使用 DataService.getUsers
 */
const AdminUsersView: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [filteredUsers, setFilteredUsers] = useState<User[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  const [editingHonor, setEditingHonor] = useState<string | null>(null);
  const [honorValue, setHonorValue] = useState('');
  const { showToast } = useGlobalStore();
  const { user: currentUser } = useAuthStore();

  /**
   * 加载用户列表
   */
  const loadUsers = useCallback(async () => {
    try {
      setIsLoading(true);
      const data = await DataService.getUsers();
      setUsers(data);
      setFilteredUsers(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : '加载用户失败';
      showToast('error', message);
    } finally {
      setIsLoading(false);
    }
  }, [showToast]);

  useEffect(() => {
    loadUsers();
  }, [loadUsers]);

  /**
   * 处理搜索
   */
  useEffect(() => {
    if (!searchQuery.trim()) {
      setFilteredUsers(users);
      return;
    }

    const query = searchQuery.toLowerCase();
    const filtered = users.filter(
      (user) =>
        user.username?.toLowerCase().includes(query) ||
        user.email?.toLowerCase().includes(query)
    );
    setFilteredUsers(filtered);
  }, [searchQuery, users]);

  /**
   * 处理封禁用户
   */
  const handleBanUser = async (userId: string, username: string) => {
    if (!confirm(`确定要封禁用户 ${username} 吗？`)) {
      return;
    }

    try {
      setActionLoading(userId);
      await DataService.banUser(userId);
      showToast('success', '用户已封禁');
      await loadUsers();
    } catch (err) {
      const message = err instanceof Error ? err.message : '封禁失败';
      showToast('error', message);
    } finally {
      setActionLoading(null);
    }
  };

  /**
   * 处理解封用户
   */
  const handleUnbanUser = async (userId: string, username: string) => {
    if (!confirm(`确定要解封用户 ${username} 吗？`)) {
      return;
    }

    try {
      setActionLoading(userId);
      await DataService.unbanUser(userId);
      showToast('success', '用户已解封');
      await loadUsers();
    } catch (err) {
      const message = err instanceof Error ? err.message : '解封失败';
      showToast('error', message);
    } finally {
      setActionLoading(null);
    }
  };

  /**
   * 处理切换管理员角色
   */
  const handleToggleAdmin = async (userId: string, username: string, isAdmin: boolean) => {
    const action = isAdmin ? '移除管理员权限' : '授予管理员权限';
    if (!confirm(`确定要${action}给用户 ${username} 吗？`)) {
      return;
    }

    try {
      setActionLoading(userId);
      await DataService.toggleAdminRole(userId);
      showToast('success', `已${action}`);
      await loadUsers();
    } catch (err) {
      const message = err instanceof Error ? err.message : '操作失败';
      showToast('error', message);
    } finally {
      setActionLoading(null);
    }
  };

  /**
   * 开始编辑称号
   */
  const handleStartEditHonor = (userId: string, currentHonor: string | undefined) => {
    setEditingHonor(userId);
    setHonorValue(currentHonor || '');
  };

  /**
   * 取消编辑称号
   */
  const handleCancelEditHonor = () => {
    setEditingHonor(null);
    setHonorValue('');
  };

  /**
   * 保存称号
   */
  const handleSaveHonor = async (userId: string) => {
    try {
      setActionLoading(userId);
      await DataService.updateUserHonor(userId, honorValue || null);
      showToast('success', honorValue ? '称号已更新' : '称号已清除');
      setEditingHonor(null);
      setHonorValue('');
      await loadUsers();
    } catch (err) {
      const message = err instanceof Error ? err.message : '更新称号失败';
      showToast('error', message);
    } finally {
      setActionLoading(null);
    }
  };

  if (isLoading) {
    return (
      <div className={ADMIN_STYLES.page}>
        <div className={ADMIN_STYLES.loadingContainer}>
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
        </div>
      </div>
    );
  }

  return (
    <div className={ADMIN_STYLES.page}>
      <div className={ADMIN_STYLES.stickyHeader}>
        <div className={ADMIN_STYLES.titleSection}>
          <h1 className={ADMIN_STYLES.title}><Users className={ADMIN_STYLES.titleIcon} />用户管理</h1>
          <p className={ADMIN_STYLES.subtitle}>管理系统用户 - 用户可通过注册页面自行注册</p>
        </div>

        <div className={ADMIN_STYLES.filterCard}>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="搜索用户..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className={ADMIN_STYLES.searchInput}
            />
          </div>
        </div>
      </div>

      <div className={ADMIN_STYLES.tableContainer}>
        {/* 用户表格 */}
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className={ADMIN_STYLES.tableHead}>
              <tr>
                <th className={ADMIN_STYLES.th}>用户名</th>
                <th className={ADMIN_STYLES.th}>邮箱</th>
                <th className={ADMIN_STYLES.th}>称号</th>
                <th className={ADMIN_STYLES.th}>角色</th>
                <th className={ADMIN_STYLES.th}>状态</th>
                <th className={ADMIN_STYLES.th}>创建时间</th>
                <th className={ADMIN_STYLES.thRight}>操作</th>
              </tr>
            </thead>
            <tbody className={ADMIN_STYLES.tbody}>
              {filteredUsers.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-4 py-8 text-center text-gray-500 dark:text-gray-400">
                    {searchQuery ? '没有找到匹配的用户' : '暂无用户'}
                  </td>
                </tr>
              ) : (
                filteredUsers.map((user) => {
                  const isCurrentUser = user.id === currentUser?.id;
                  const isLoading = actionLoading === user.id;

                  return (
                    <tr key={user.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                      <td className="px-4 py-3 text-sm font-medium text-gray-900 dark:text-gray-100">
                        {user.username}
                        {isCurrentUser && (
                          <span className="ml-2 text-xs text-blue-600 dark:text-blue-400">(当前用户)</span>
                        )}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">{user.email}</td>
                      <td className="px-4 py-3 text-sm">
                        {editingHonor === user.id ? (
                          <div className="flex items-center gap-1">
                            <input
                              type="text"
                              value={honorValue}
                              onChange={(e) => setHonorValue(e.target.value)}
                              placeholder="输入称号"
                              className="w-24 px-2 py-1 text-xs border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                              maxLength={50}
                              autoFocus
                              onKeyDown={(e) => {
                                if (e.key === 'Enter') handleSaveHonor(user.id);
                                if (e.key === 'Escape') handleCancelEditHonor();
                              }}
                            />
                            <button
                              onClick={() => handleSaveHonor(user.id)}
                              disabled={isLoading}
                              className="p-1 text-green-600 dark:text-green-400 hover:bg-green-50 dark:hover:bg-green-900/30 rounded disabled:opacity-50"
                              title="保存"
                            >
                              <Check className="w-3.5 h-3.5" />
                            </button>
                            <button
                              onClick={handleCancelEditHonor}
                              disabled={isLoading}
                              className="p-1 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded disabled:opacity-50"
                              title="取消"
                            >
                              <X className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        ) : (
                          <div className="flex items-center gap-1">
                            {user.honor ? (
                              <span className="px-2 py-0.5 rounded bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300 text-xs font-medium">
                                {user.honor}
                              </span>
                            ) : (
                              <span className="text-gray-400 dark:text-gray-500 text-xs">-</span>
                            )}
                            <button
                              onClick={() => handleStartEditHonor(user.id, user.honor)}
                              className="p-1 text-gray-400 hover:text-amber-600 dark:hover:text-amber-400 hover:bg-amber-50 dark:hover:bg-amber-900/30 rounded transition-colors"
                              title="编辑称号"
                            >
                              <Award className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        )}
                      </td>
                      <td className="px-4 py-3 text-sm">
                        <span
                          className={`px-2 py-1 rounded text-xs font-medium ${
                            user.isAdmin
                              ? 'bg-purple-100 dark:bg-purple-900/50 text-purple-700 dark:text-purple-300'
                              : 'bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300'
                          }`}
                        >
                          {user.isAdmin ? '管理员' : '普通用户'}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm">
                        <span
                          className={`px-2 py-1 rounded text-xs font-medium ${
                            user.isActive
                              ? 'bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-300'
                              : 'bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-300'
                          }`}
                        >
                          {user.isActive ? '正常' : '已封禁'}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                        {formatDate(user.createdAt)}
                      </td>
                      <td className="px-4 py-3 text-sm text-right">
                        <div className="flex items-center justify-end space-x-2">
                          {/* 封禁/解封按钮 */}
                          {!isCurrentUser && (
                            user.isActive ? (
                              <button
                                onClick={() => handleBanUser(user.id, user.username)}
                                disabled={isLoading}
                                className="p-1.5 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/30 rounded transition-colors disabled:opacity-50"
                                title="封禁用户"
                              >
                                <Ban className="w-4 h-4" />
                              </button>
                            ) : (
                              <button
                                onClick={() => handleUnbanUser(user.id, user.username)}
                                disabled={isLoading}
                                className="p-1.5 text-green-600 dark:text-green-400 hover:bg-green-50 dark:hover:bg-green-900/30 rounded transition-colors disabled:opacity-50"
                                title="解封用户"
                              >
                                <CheckCircle className="w-4 h-4" />
                              </button>
                            )
                          )}

                          {/* 管理员角色切换按钮 */}
                          {!isCurrentUser && (
                            <button
                              onClick={() => handleToggleAdmin(user.id, user.username, user.isAdmin)}
                              disabled={isLoading}
                              className={`p-1.5 rounded transition-colors disabled:opacity-50 ${
                                user.isAdmin
                                  ? 'text-orange-600 dark:text-orange-400 hover:bg-orange-50 dark:hover:bg-orange-900/30'
                                  : 'text-purple-600 dark:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-900/30'
                              }`}
                              title={user.isAdmin ? '移除管理员' : '设为管理员'}
                            >
                              {user.isAdmin ? <ShieldOff className="w-4 h-4" /> : <Shield className="w-4 h-4" />}
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AdminUsersView;
