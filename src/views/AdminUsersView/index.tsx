import React, { useState, useEffect } from 'react';
import { Search, Shield, ShieldOff, Ban, CheckCircle } from 'lucide-react';
import { Button, Card, Input, Loading } from '../../components/common';
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
  const { showToast } = useGlobalStore();
  const { user: currentUser } = useAuthStore();

  /**
   * 加载用户列表
   */
  useEffect(() => {
    const loadUsers = async () => {
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
    };

    loadUsers();
  }, [showToast]);

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
   * 加载用户列表
   */
  const loadUsers = async () => {
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
  };



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

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">用户管理</h1>
          <p className="mt-2 text-gray-600">管理系统用户 - 用户可通过注册页面自行注册</p>
        </div>
        {/* 添加用户按钮已隐藏 - 用户可以自己注册 */}
      </div>

      <Card background="blue">
        <div className="p-6 space-y-4">
          <Input
            placeholder="搜索用户..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            icon={<Search className="w-5 h-5 text-gray-400" />}
          />

          {/* 用户表格 */}
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">用户名</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">邮箱</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">角色</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">状态</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">创建时间</th>
                  <th className="px-4 py-3 text-right text-sm font-semibold text-gray-900">操作</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {filteredUsers.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="px-4 py-8 text-center text-gray-500">
                      {searchQuery ? '没有找到匹配的用户' : '暂无用户'}
                    </td>
                  </tr>
                ) : (
                  filteredUsers.map((user) => {
                    const isCurrentUser = user.id === currentUser?.id;
                    const isLoading = actionLoading === user.id;

                    return (
                      <tr key={user.id} className="hover:bg-gray-50">
                        <td className="px-4 py-3 text-sm font-medium text-gray-900">
                          {user.username}
                          {isCurrentUser && (
                            <span className="ml-2 text-xs text-blue-600">(当前用户)</span>
                          )}
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-600">{user.email}</td>
                        <td className="px-4 py-3 text-sm">
                          <span
                            className={`px-2 py-1 rounded-full text-xs font-medium ${
                              user.isAdmin
                                ? 'bg-purple-100 text-purple-700'
                                : 'bg-blue-100 text-blue-700'
                            }`}
                          >
                            {user.isAdmin ? '管理员' : '普通用户'}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-sm">
                          <span
                            className={`px-2 py-1 rounded-full text-xs font-medium ${
                              user.isActive
                                ? 'bg-green-100 text-green-700'
                                : 'bg-red-100 text-red-700'
                            }`}
                          >
                            {user.isActive ? '正常' : '已封禁'}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-600">
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
                                  className="p-1.5 text-red-600 hover:bg-red-50 rounded transition-colors disabled:opacity-50"
                                  title="封禁用户"
                                >
                                  <Ban className="w-4 h-4" />
                                </button>
                              ) : (
                                <button
                                  onClick={() => handleUnbanUser(user.id, user.username)}
                                  disabled={isLoading}
                                  className="p-1.5 text-green-600 hover:bg-green-50 rounded transition-colors disabled:opacity-50"
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
                                    ? 'text-orange-600 hover:bg-orange-50'
                                    : 'text-purple-600 hover:bg-purple-50'
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
      </Card>
    </div>
  );
};

export default AdminUsersView;
