/**
 * 活动系统 - TypeScript 类型定义
 */

// ==================== 枚举类型 ====================

/**
 * 活动类型
 */
export enum ActivityType {
  INVITATION = 'invitation',      // 邀请活动
  COMPETITION = 'competition',    // 比赛活动
  POINTS = 'points',              // 积分活动
  MISSION = 'mission',            // 任务活动
  LOTTERY = 'lottery',            // 抽奖活动
  CHECKIN = 'checkin'             // 签到活动
}

/**
 * 活动状态
 */
export enum ActivityStatus {
  UPCOMING = 'upcoming',    // 即将开始
  ONGOING = 'ongoing',      // 进行中
  ENDED = 'ended'           // 已结束
}

/**
 * 活动形式
 */
export enum ActivityFormat {
  ONLINE = 'online',        // 线上活动
  OFFLINE = 'offline',      // 线下活动
  HYBRID = 'hybrid'         // 线上线下结合
}

/**
 * 奖励类型
 */
export enum RewardType {
  POINTS = 'points',        // 积分
  BADGE = 'badge',          // 徽章
  VIP = 'vip',              // 会员
  GIFT = 'gift',            // 实物奖品
  COUPON = 'coupon',        // 优惠券
  FEATURE = 'feature'       // 功能权益
}

// ==================== 奖励接口 ====================

/**
 * 奖励基础接口
 */
export interface BaseReward {
  type: RewardType;
  name: string;
  description?: string;
  imageUrl?: string;
}

/**
 * 积分奖励
 */
export interface PointsReward extends BaseReward {
  type: RewardType.POINTS;
  amount: number;
}

/**
 * 徽章奖励
 */
export interface BadgeReward extends BaseReward {
  type: RewardType.BADGE;
  badgeId: string;
}

/**
 * 会员奖励
 */
export interface VipReward extends BaseReward {
  type: RewardType.VIP;
  duration: number;  // 天数
  level: string;     // 会员等级
}

/**
 * 实物奖励
 */
export interface GiftReward extends BaseReward {
  type: RewardType.GIFT;
  quantity: number;
}

/**
 * 优惠券奖励
 */
export interface CouponReward extends BaseReward {
  type: RewardType.COUPON;
  couponCode: string;
  discount: number;  // 折扣或金额
}

/**
 * 功能权益奖励
 */
export interface FeatureReward extends BaseReward {
  type: RewardType.FEATURE;
  featureId: string;
  duration?: number;  // 天数，null 表示永久
}

/**
 * 联合奖励类型
 */
export type Reward = PointsReward | BadgeReward | VipReward | GiftReward | CouponReward | FeatureReward;

// ==================== 特定活动规则 ====================

/**
 * 邀请活动规则
 */
export interface InvitationRules {
  type: ActivityType.INVITATION;
  inviterRewards: Reward[];      // 邀请者奖励
  inviteeRewards: Reward[];      // 被邀请者奖励
  invitationLimit?: number;       // 单个用户邀请上限
  requirementForInvitee?: string; // 被邀请者完成条件（如"完成首次任务"）
}

/**
 * 比赛活动规则
 */
export interface CompetitionRules {
  type: ActivityType.COMPETITION;
  rankRewards: {
    rankRange: [number, number];  // 排名范围，如 [1, 1] 表示第1名，[2, 10] 表示第2-10名
    rewards: Reward[];
    description: string;           // 如"一等奖"、"优胜奖"
  }[];
  scoringCriteria: string;        // 评分标准
  participationReward?: Reward[]; // 参与奖
}

/**
 * 积分活动规则
 */
export interface PointsRules {
  type: ActivityType.POINTS;
  pointsMultiplier?: number;      // 积分倍数（如双倍积分活动）
  bonusPoints?: number;           // 额外赠送积分
  tasks?: {
    taskName: string;
    pointsReward: number;
    description: string;
  }[];
}

/**
 * 任务活动规则
 */
export interface MissionRules {
  type: ActivityType.MISSION;
  missions: {
    missionId: string;
    title: string;
    description: string;
    requirement: string;           // 完成条件
    rewards: Reward[];
    sequence?: number;             // 任务顺序（用于连续任务）
  }[];
  completionReward?: Reward[];     // 全部完成奖励
}

/**
 * 抽奖活动规则
 */
export interface LotteryRules {
  type: ActivityType.LOTTERY;
  prizes: {
    prizeId: string;
    name: string;
    rewards: Reward[];
    probability: number;           // 中奖概率（0-1）
    totalQuantity?: number;        // 总数量
    remainingQuantity?: number;    // 剩余数量
  }[];
  drawCost?: {
    type: 'points' | 'free';
    amount?: number;               // 如果是积分抽奖，消耗的积分数
  };
  maxDrawsPerUser?: number;        // 每人最多抽奖次数
}

/**
 * 签到活动规则
 */
export interface CheckinRules {
  type: ActivityType.CHECKIN;
  dailyRewards: Reward[];          // 每日签到奖励
  consecutiveBonuses?: {
    days: number;                  // 连续签到天数
    rewards: Reward[];
  }[];
  totalCheckinsReward?: {          // 累计签到奖励
    days: number;
    rewards: Reward[];
  }[];
}

/**
 * 联合活动规则类型
 */
export type ActivityRules =
  | InvitationRules
  | CompetitionRules
  | PointsRules
  | MissionRules
  | LotteryRules
  | CheckinRules;

// ==================== 活动接口 ====================

/**
 * 活动基础信息
 */
export interface Activity {
  id: string;
  title: string;
  subtitle?: string;
  description: string;
  bannerUrl: string;
  category: string;                // 活动标签，如"积分活动"、"创作大赛"

  type: ActivityType;
  status: ActivityStatus;
  format: ActivityFormat;

  startTime: string;
  endTime: string;
  registrationDeadline?: string;   // 报名截止时间

  participantCount: number;        // 参与人数
  maxParticipants?: number;        // 最大参与人数

  rules: ActivityRules;            // 活动规则（根据 type 不同而不同）

  participationSteps: {            // 参与方式
    step: number;
    title: string;
    description: string;
  }[];

  notice: string[];                // 活动须知

  organizerName?: string;          // 主办方
  contactInfo?: string;            // 联系方式

  featured?: boolean;              // 是否为精选活动
  notificationId?: string;         // 关联的通知ID

  createdAt: string;
  updatedAt: string;
}

/**
 * 活动详情（包含更多信息）
 */
export interface ActivityDetail extends Activity {
  fullDescription: string;         // 完整的活动详情描述
  faq?: {
    question: string;
    answer: string;
  }[];
  relatedActivities?: string[];    // 相关活动ID列表
  userParticipationStatus?: {      // 当前用户参与状态
    isParticipating: boolean;
    participatedAt?: string;
    progress?: any;                // 根据活动类型不同，进度数据结构不同
  };
}

/**
 * 用户活动参与记录
 */
export interface UserActivityParticipation {
  id: string;
  userId: string;
  activityId: string;
  participatedAt: string;
  progress: any;                   // 活动进度（根据活动类型不同）
  earnedRewards: Reward[];         // 已获得的奖励
  status: 'active' | 'completed' | 'expired';
}
