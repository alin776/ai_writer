import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Calendar, MapPin, Users, Clock, Trophy, Gift, Award } from 'lucide-react';
import { ImageWithFallback } from '../components/notifications/ImageWithFallback';
import type { ActivityDetail as ActivityDetailType, Reward } from '../types/activity';
import { RewardType, ActivityStatus, ActivityFormat, ActivityType } from '../types/activity';

export default function ActivityDetail() {
  const { activityId } = useParams<{ activityId: string }>();
  const navigate = useNavigate();
  const [activity, setActivity] = useState<ActivityDetailType | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadActivityDetail();
  }, [activityId]);

  const loadActivityDetail = async () => {
    try {
      setLoading(true);

      if (!activityId) {
        console.error('活动ID不存在');
        setLoading(false);
        return;
      }

      // 通过通知ID获取通知数据
      const { getUserNotifications } = await import('../services/notificationApi');
      const response = await getUserNotifications({ page: 1, pageSize: 100 });

      // 根据activityId查找对应的通知
      const notification = response.items.find(n => n.id === activityId);

      if (!notification) {
        console.error('未找到对应的活动通知:', activityId);
        // 如果找不到，使用模拟数据
        setActivity(getMockActivityDetail(activityId));
        setLoading(false);
        return;
      }

      console.log('📖 加载活动详情 - 原始通知数据:', {
        notificationId: notification.id,
        title: notification.title,
        type: notification.type,
        activity_type: (notification as any).activity_type,
        activity_rules: (notification as any).activity_rules,
        fullNotification: notification  // 打印完整通知对象
      });

      // 将通知数据转换为活动详情格式
      const activityDetail = convertNotificationToActivity(notification);

      console.log('📖 转换后的活动详情:', {
        id: activityDetail.id,
        title: activityDetail.title,
        type: activityDetail.type,
        category: activityDetail.category,
        rulesType: activityDetail.rules.type
      });

      setActivity(activityDetail);
    } catch (error) {
      console.error('加载活动详情失败:', error);
      // 发生错误时使用模拟数据
      setActivity(getMockActivityDetail(activityId));
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return `${date.getMonth() + 1}.${date.getDate()}`;
  };

  const formatDateTime = (dateStr: string) => {
    const date = new Date(dateStr);
    return `${date.getMonth() + 1}.${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`;
  };

  const getRewardIcon = (type: RewardType) => {
    switch (type) {
      case RewardType.POINTS: return <Gift className="w-4 h-4" />;
      case RewardType.BADGE: return <Award className="w-4 h-4" />;
      case RewardType.VIP: return <Trophy className="w-4 h-4" />;
      default: return <Gift className="w-4 h-4" />;
    }
  };

  const renderReward = (reward: Reward) => {
    switch (reward.type) {
      case RewardType.POINTS:
        return (
          <div className="border border-gray-100 px-6 py-5">
            <div className="flex items-center gap-2 text-gray-500 mb-2">
              {getRewardIcon(reward.type)}
              <div className="text-xs">{reward.name}</div>
            </div>
            <div className="text-3xl mb-1">{reward.amount}</div>
            <div className="text-xs text-gray-400">积分</div>
          </div>
        );
      case RewardType.BADGE:
      case RewardType.VIP:
      case RewardType.GIFT:
      case RewardType.COUPON:
      case RewardType.FEATURE:
        return (
          <div className="border border-gray-100 px-6 py-5">
            <div className="flex items-center gap-2 text-gray-500 mb-2">
              {getRewardIcon(reward.type)}
              <div className="text-xs">{reward.name}</div>
            </div>
            {reward.description && (
              <div className="text-xs text-gray-600">{reward.description}</div>
            )}
          </div>
        );
      default:
        return null;
    }
  };

  const renderRewardsByType = () => {
    if (!activity) return null;

    switch (activity.type) {
      case 'invitation':
        if (activity.rules.type === 'invitation') {
          return (
            <div className="bg-white px-8 py-6 mb-6">
              <h2 className="text-sm mb-4">活动奖励</h2>
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <div className="text-xs text-gray-400 mb-3">邀请者奖励</div>
                  <div className="space-y-3">
                    {activity.rules.inviterRewards.map((reward, index) => (
                      <div key={index}>{renderReward(reward)}</div>
                    ))}
                  </div>
                </div>
                <div>
                  <div className="text-xs text-gray-400 mb-3">被邀请者奖励</div>
                  <div className="space-y-3">
                    {activity.rules.inviteeRewards.map((reward, index) => (
                      <div key={index}>{renderReward(reward)}</div>
                    ))}
                  </div>
                </div>
              </div>
              {activity.rules.requirementForInvitee && (
                <div className="mt-4 text-xs text-gray-500">
                  ⚠️ 被邀请者需满足条件：{activity.rules.requirementForInvitee}
                </div>
              )}
            </div>
          );
        }
        break;

      case 'competition':
        if (activity.rules.type === 'competition') {
          return (
            <div className="bg-white px-8 py-6 mb-6">
              <h2 className="text-sm mb-4">奖励设置</h2>
              <div className="space-y-4">
                {activity.rules.rankRewards.map((rank, index) => (
                  <div key={index} className="border border-gray-100 px-6 py-4">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <Trophy className="w-5 h-5 text-gray-400" />
                        <div>
                          <div className="text-sm font-medium">{rank.description}</div>
                          <div className="text-xs text-gray-500">
                            {rank.rankRange[0] === rank.rankRange[1]
                              ? `第 ${rank.rankRange[0]} 名`
                              : `第 ${rank.rankRange[0]}-${rank.rankRange[1]} 名`}
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="grid grid-cols-3 gap-3">
                      {rank.rewards.map((reward, rIndex) => (
                        <div key={rIndex} className="text-xs">
                          {reward.type === RewardType.POINTS && (
                            <div className="text-center">
                              <div className="text-lg font-medium">{reward.amount}</div>
                              <div className="text-gray-500">{reward.name}</div>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
              {activity.rules.participationReward && (
                <div className="mt-4 border border-gray-100 px-6 py-4">
                  <div className="text-xs text-gray-500 mb-2">参与奖</div>
                  <div className="grid grid-cols-3 gap-3">
                    {activity.rules.participationReward.map((reward, index) => (
                      <div key={index}>{renderReward(reward)}</div>
                    ))}
                  </div>
                </div>
              )}
              <div className="mt-4 text-xs text-gray-500">
                📊 评分标准：{activity.rules.scoringCriteria}
              </div>
            </div>
          );
        }
        break;

      default:
        return null;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-500">加载中...</div>
      </div>
    );
  }

  if (!activity) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-500">活动不存在</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-6 py-8">
        {/* Back Button */}
        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 text-gray-400 hover:text-gray-900 transition-colors text-xs mb-6"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>返回</span>
        </button>

        {/* Hero Banner */}
        <div className="mb-8 aspect-[21/9] overflow-hidden rounded-2xl">
          <ImageWithFallback
            src={activity.bannerUrl}
            alt={activity.title}
            className="w-full h-full object-cover"
          />
        </div>

        {/* Title Section */}
        <div className="bg-white px-8 py-8 mb-6 rounded-2xl">
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <div className="inline-block px-2.5 py-1 bg-gray-100 text-xs text-gray-600 mb-3 rounded-full">
                {activity.category}
              </div>
              <h1 className="text-3xl mb-2">{activity.title}</h1>
              {activity.subtitle && (
                <p className="text-sm text-gray-500">{activity.subtitle}</p>
              )}
            </div>
          </div>
        </div>

        {/* Info Cards */}
        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="bg-white px-4 py-4 rounded-xl">
            <div className="flex items-center gap-2 mb-2">
              <Calendar className="w-4 h-4 text-gray-400" />
              <div className="text-xs text-gray-400">活动时间</div>
            </div>
            <div className="text-xs text-gray-900">
              {formatDate(activity.startTime)} - {formatDate(activity.endTime)}
            </div>
          </div>
          <div className="bg-white px-4 py-4 rounded-xl">
            <div className="flex items-center gap-2 mb-2">
              <MapPin className="w-4 h-4 text-gray-400" />
              <div className="text-xs text-gray-400">活动形式</div>
            </div>
            <div className="text-xs text-gray-900">
              {activity.format === 'online' ? '线上活动' : activity.format === 'offline' ? '线下活动' : '线上线下'}
            </div>
          </div>
          <div className="bg-white px-4 py-4 rounded-xl">
            <div className="flex items-center gap-2 mb-2">
              <Users className="w-4 h-4 text-gray-400" />
              <div className="text-xs text-gray-400">参与人数</div>
            </div>
            <div className="text-xs text-gray-900">
              {activity.participantCount.toLocaleString()} 人
            </div>
          </div>
          <div className="bg-white px-4 py-4 rounded-xl">
            <div className="flex items-center gap-2 mb-2">
              <Clock className="w-4 h-4 text-gray-400" />
              <div className="text-xs text-gray-400">报名截止</div>
            </div>
            <div className="text-xs text-gray-900">
              {activity.registrationDeadline ? formatDateTime(activity.registrationDeadline) : '无截止时间'}
            </div>
          </div>
        </div>

        {/* Rewards */}
        {renderRewardsByType()}

        {/* Activity Details */}
        <div className="bg-white px-8 py-6 mb-6 rounded-2xl">
          <h2 className="text-sm mb-4">活动详情</h2>
          <div className="text-xs text-gray-600 leading-relaxed space-y-3">
            {activity.fullDescription.split('\n\n').map((paragraph, index) => (
              <p key={index}>{paragraph}</p>
            ))}
          </div>
        </div>

        {/* Participation Steps */}
        <div className="bg-white px-8 py-6 mb-6 rounded-2xl">
          <h2 className="text-sm mb-4">参与方式</h2>
          <div className="space-y-4">
            {activity.participationSteps.map((step) => (
              <div key={step.step} className="flex gap-4">
                <div className="flex-shrink-0 w-6 h-6 bg-black text-white flex items-center justify-center text-xs rounded-full">
                  {step.step}
                </div>
                <div className="flex-1">
                  <div className="text-xs text-gray-900 mb-1">{step.title}</div>
                  <div className="text-xs text-gray-500">{step.description}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Notice */}
        <div className="bg-white px-8 py-6 mb-6 rounded-2xl">
          <h2 className="text-sm mb-4">活动须知</h2>
          <ul className="space-y-2 text-xs text-gray-600">
            {activity.notice.map((item, index) => (
              <li key={index}>· {item}</li>
            ))}
          </ul>
        </div>

        {/* Bottom CTA */}
        <div className="bg-white px-8 py-6 rounded-2xl">
          <button className="w-full bg-black text-white py-3 text-sm hover:bg-gray-800 transition-colors rounded-xl">
            {activity.userParticipationStatus?.isParticipating ? '查看我的参与记录' : '立即参与活动'}
          </button>
        </div>
      </div>
    </div>
  );
}

// 将通知数据转换为活动详情格式
function convertNotificationToActivity(notification: any): ActivityDetailType {
  // 优先使用 notification.activity_type，如果不存在则使用默认值
  const activity_type = notification.activity_type || 'invitation';
  const activity_rules = notification.activity_rules;

  console.log('🔄 转换通知数据:', {
    hasActivityType: !!notification.activity_type,
    activity_type,
    hasActivityRules: !!notification.activity_rules,
    rulesType: activity_rules?.type
  });

  // 如果没有活动规则，根据活动类型创建默认规则
  const defaultRules = activity_rules || {
    type: activity_type,
    // 根据不同类型设置默认值
    ...(activity_type === 'invitation' && {
      inviterRewards: [],
      inviteeRewards: [],
      requirementForInvitee: ''
    })
  };

  return {
    id: notification.id,
    title: notification.title,
    subtitle: notification.content ? notification.content.split('\n\n')[0] : '',
    description: notification.content || '',
    bannerUrl: notification.coverImageUrl || 'https://images.unsplash.com/photo-1611376299769-0abfd5941d40?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBtaW5pbWFsJTIwYmFubmVyfGVufDF8fHx8MTc2NTUyNzMyMHww&ixlib=rb-4.1.0&q=80&w=1080',
    category: getActivityCategoryFromType(activity_type),
    type: activity_type as ActivityType,
    status: ActivityStatus.ONGOING,
    format: ActivityFormat.ONLINE,
    startTime: notification.validFrom || notification.createdAt,
    endTime: notification.validUntil || notification.createdAt,
    registrationDeadline: notification.validUntil,
    participantCount: 0,
    rules: defaultRules as any,
    participationSteps: getDefaultParticipationSteps(activity_type),
    notice: [
      '每个账号仅可参与一次，请勿重复注册',
      '请确保遵守活动规则，如发现作弊行为，平台有权取消参与资格',
      '奖励将在活动结束后统一发放',
      '本次活动最终解释权归平台所有'
    ],
    fullDescription: notification.content || '活动详情',
    createdAt: notification.createdAt,
    updatedAt: notification.updatedAt || notification.createdAt
  };
}

// 根据活动类型获取分类名称
function getActivityCategoryFromType(activity_type: string): string {
  switch (activity_type) {
    case 'invitation': return '邀请活动';
    case 'competition': return '比赛活动';
    case 'points': return '积分活动';
    case 'mission': return '任务活动';
    case 'lottery': return '抽奖活动';
    case 'checkin': return '签到活动';
    default: return '活动';
  }
}

// 获取默认的参与步骤
function getDefaultParticipationSteps(activity_type: string) {
  switch (activity_type) {
    case 'invitation':
      return [
        { step: 1, title: '注册并登录账号', description: '使用手机号或邮箱完成账号注册' },
        { step: 2, title: '获取专属邀请链接', description: '在个人中心生成您的专属邀请码' },
        { step: 3, title: '分享给朋友', description: '通过社交媒体、即时通讯等方式分享链接' },
        { step: 4, title: '获得奖励', description: '好友完成注册后自动发放奖励' }
      ];
    case 'competition':
      return [
        { step: 1, title: '报名参赛', description: '点击下方按钮报名参加比赛' },
        { step: 2, title: '提交作品', description: '在规定时间内提交您的参赛作品' },
        { step: 3, title: '等待评审', description: '评委将根据评分标准进行评审' },
        { step: 4, title: '查看结果', description: '活动结束后公布获奖名单' }
      ];
    default:
      return [
        { step: 1, title: '了解活动规则', description: '仔细阅读活动详情和参与要求' },
        { step: 2, title: '立即参与', description: '点击下方按钮参与活动' },
        { step: 3, title: '完成任务', description: '按照要求完成活动任务' },
        { step: 4, title: '领取奖励', description: '任务完成后领取相应奖励' }
      ];
  }
}

// 模拟数据（当找不到通知时使用）
function getMockActivityDetail(activityId?: string): ActivityDetailType {
  return {
    id: activityId || '1',
    title: '积分赠送活动',
    subtitle: '邀请1人即可获得丰厚奖励',
    description: '邀请好友注册，双方都能获得积分奖励',
    bannerUrl: 'https://images.unsplash.com/photo-1611376299769-0abfd5941d40?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBtaW5pbWFsJTIwYmFubmVyfGVufDF8fHx8MTc2NTUyNzMyMHww&ixlib=rb-4.1.0&q=80&w=1080',
    category: '积分活动',
    type: ActivityType.INVITATION,
    status: ActivityStatus.ONGOING,
    format: ActivityFormat.ONLINE,
    startTime: '2025-12-12T00:00:00Z',
    endTime: '2025-12-20T23:59:59Z',
    registrationDeadline: '2025-12-19T23:59:59Z',
    participantCount: 1234,
    rules: {
      type: ActivityType.INVITATION,
      inviterRewards: [
        {
          type: RewardType.POINTS,
          name: '邀请者奖励',
          amount: 500
        }
      ],
      inviteeRewards: [
        {
          type: RewardType.POINTS,
          name: '被邀请者奖励',
          amount: 300
        }
      ],
      requirementForInvitee: '完成首次任务'
    },
    participationSteps: [
      {
        step: 1,
        title: '注册并登录账号',
        description: '使用手机号或邮箱完成账号注册'
      },
      {
        step: 2,
        title: '获取专属邀请链接',
        description: '在个人中心生成您的专属邀请码'
      },
      {
        step: 3,
        title: '分享给朋友',
        description: '通过社交媒体、即时通讯等方式分享链接'
      },
      {
        step: 4,
        title: '获得积分奖励',
        description: '好友完成注册和首次任务后自动发放积分'
      }
    ],
    notice: [
      '每个账号仅可参与一次，请勿重复注册',
      '邀请的用户需完成实名认证方可计入有效邀请',
      '积分将在好友完成任务后3个工作日内发放',
      '如发现作弊行为，平台有权取消参与资格',
      '本次活动最终解释权归平台所有'
    ],
    fullDescription: `这是一次回馈用户的特别活动，我们诚邀每一位用户参与其中。通过简单的邀请机制，您不仅可以获得丰厚的积分奖励，还能与朋友一起体验我们的优质服务。

活动期间，每成功邀请1位新用户注册并完成首次任务，您即可获得500积分奖励。被邀请的用户同样可以获得300积分的新人礼包。

积分可用于兑换平台内的各种权益，包括但不限于高级功能使用权、专属作品展示位、优先客服支持等。`,
    createdAt: '2025-12-10T00:00:00Z',
    updatedAt: '2025-12-10T00:00:00Z'
  };
}
