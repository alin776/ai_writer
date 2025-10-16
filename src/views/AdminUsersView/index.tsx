import React, { useState, useEffect } from 'react';
import { Search, UserPlus } from 'lucide-react';
import { Button, Card, Input, Loading } from '../../components/common';
import { DataService } from '../../services/DataService';
import { useGlobalStore } from '../../store/globalStore';
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
  const { showToast } = useGlobalStore();

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
        user.name.toLowerCase().includes(query) ||
        user.email.toLowerCase().includes(query)
    );
    setFilteredUsers(filtered);
  }, [searchQuery, users]);

  /**
   * 处理添加用户
   */
  const handleAddUser = () => {
    showToast('info', '添加用户功能待实现');
  };

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">用户管理</h1>
          <p className="mt-2 text-gray-600">管理系统用户</p>
        </div>
        <Button variant="primary" icon={<UserPlus className="w-5 h-5" />} onClick={handleAddUser}>
          添加用户
        </Button>
      </div>

      <Card>
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
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">创建时间</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {filteredUsers.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="px-4 py-8 text-center text-gray-500">
                      {searchQuery ? '没有找到匹配的用户' : '暂无用户'}
                    </td>
                  </tr>
                ) : (
                  filteredUsers.map((user) => (
                    <tr key={user.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 text-sm text-gray-900">{user.name}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">{user.email}</td>
                      <td className="px-4 py-3 text-sm">
                        <span
                          className={`px-2 py-1 rounded-full text-xs font-medium ${
                            user.role === 'admin'
                              ? 'bg-purple-100 text-purple-700'
                              : 'bg-blue-100 text-blue-700'
                          }`}
                        >
                          {user.role === 'admin' ? '管理员' : '普通用户'}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600">{formatDate(user.registrationDate)}</td>
                    </tr>
                  ))
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
