# 活动类型使用文档

## 概述

活动系统支持多种活动类型，每种类型都有特定的奖励规则和数据结构。本文档详细说明各类活动的数据配置方式。

## 活动类型一览

1. **邀请活动** (`invitation`) - 邀请好友获得奖励
2. **比赛活动** (`competition`) - 排名竞赛活动
3. **积分活动** (`points`) - 积分倍数或任务积分
4. **任务活动** (`mission`) - 完成任务获得奖励
5. **抽奖活动** (`lottery`) - 抽奖赢取奖品
6. **签到活动** (`checkin`) - 每日签到获得奖励

## 奖励类型

所有活动都可以使用以下奖励类型：

```typescript
enum RewardType {
  POINTS = 'points',        // 积分
  BADGE = 'badge',          // 徽章
  VIP = 'vip',              // 会员
  GIFT = 'gift',            // 实物奖品
  COUPON = 'coupon',        // 优惠券
  FEATURE = 'feature'       // 功能权益
}
```

## 1. 邀请活动 (Invitation Activity)

### 适用场景
- 用户增长活动
- 推荐奖励计划
- 老带新活动

### 数据结构示例

```typescript
const invitationActivity: Activity = {
  id: "inv-001",
  title: "邀请好友赢积分",
  subtitle: "邀请1人即可获得500积分",
  description: "邀请好友注册，双方都能获得积分奖励",
  bannerUrl: "https://example.com/banner.jpg",
  category: "邀请活动",
  type: ActivityType.INVITATION,
  status: ActivityStatus.ONGOING,
  format: ActivityFormat.ONLINE,
  startTime: "2025-12-01T00:00:00Z",
  endTime: "2025-12-31T23:59:59Z",
  participantCount: 1234,

  // 邀请活动特有规则
  rules: {
    type: ActivityType.INVITATION,
    inviterRewards: [
      {
        type: RewardType.POINTS,
        name: "邀请者奖励",
        amount: 500
      }
    ],
    inviteeRewards: [
      {
        type: RewardType.POINTS,
        name: "被邀请者奖励",
        amount: 300
      }
    ],
    invitationLimit: 10,  // 单个用户最多邀请10人
    requirementForInvitee: "完成首次创作任务"
  },

  participationSteps: [
    {
      step: 1,
      title: "获取邀请链接",
      description: "在个人中心生成专属邀请链接"
    },
    {
      step: 2,
      title: "分享给好友",
      description: "通过社交媒体分享邀请链接"
    },
    {
      step: 3,
      title: "好友完成任务",
      description: "好友注册并完成首次创作"
    },
    {
      step: 4,
      title: "获得奖励",
      description: "双方自动获得积分奖励"
    }
  ],

  notice: [
    "每个账号仅可参与一次",
    "被邀请用户需完成实名认证",
    "积分将在好友完成任务后3个工作日内发放"
  ],

  fullDescription: "通过邀请好友注册并完成任务，您和好友都能获得丰厚的积分奖励...",
  createdAt: "2025-12-01T00:00:00Z",
  updatedAt: "2025-12-01T00:00:00Z"
};
```

## 2. 比赛活动 (Competition Activity)

### 适用场景
- 创作大赛
- 排行榜竞赛
- 技能挑战赛

### 数据结构示例

```typescript
const competitionActivity: Activity = {
  id: "comp-001",
  title: "2025年度创作大赛",
  subtitle: "展现你的创作才华，赢取丰厚奖品",
  description: "参与创作竞赛，优秀作品将获得奖励",
  bannerUrl: "https://example.com/competition-banner.jpg",
  category: "比赛活动",
  type: ActivityType.COMPETITION,
  status: ActivityStatus.ONGOING,
  format: ActivityFormat.ONLINE,
  startTime: "2025-12-01T00:00:00Z",
  endTime: "2025-12-31T23:59:59Z",
  registrationDeadline: "2025-12-20T23:59:59Z",
  participantCount: 5678,
  maxParticipants: 10000,

  // 比赛活动特有规则
  rules: {
    type: ActivityType.COMPETITION,
    rankRewards: [
      {
        rankRange: [1, 1],  // 第1名
        description: "一等奖",
        rewards: [
          {
            type: RewardType.POINTS,
            name: "积分奖励",
            amount: 10000
          },
          {
            type: RewardType.VIP,
            name: "年度VIP会员",
            duration: 365,
            level: "premium"
          },
          {
            type: RewardType.BADGE,
            name: "冠军徽章",
            badgeId: "champion-2025"
          }
        ]
      },
      {
        rankRange: [2, 3],  // 第2-3名
        description: "二等奖",
        rewards: [
          {
            type: RewardType.POINTS,
            name: "积分奖励",
            amount: 5000
          },
          {
            type: RewardType.VIP,
            name: "半年VIP会员",
            duration: 180,
            level: "premium"
          }
        ]
      },
      {
        rankRange: [4, 10],  // 第4-10名
        description: "三等奖",
        rewards: [
          {
            type: RewardType.POINTS,
            name: "积分奖励",
            amount: 2000
          }
        ]
      }
    ],
    scoringCriteria: "作品质量（40%）+ 创新性（30%）+ 完成度（30%）",
    participationReward: [
      {
        type: RewardType.POINTS,
        name: "参与奖",
        amount: 100
      }
    ]
  },

  participationSteps: [
    {
      step: 1,
      title: "报名参赛",
      description: "点击报名按钮完成报名"
    },
    {
      step: 2,
      title: "创作作品",
      description: "在规定时间内完成创作"
    },
    {
      step: 3,
      title: "提交作品",
      description: "在截止日期前提交作品"
    },
    {
      step: 4,
      title: "等待评选",
      description: "专业评委团队进行评选"
    }
  ],

  notice: [
    "作品必须为原创",
    "不得抄袭或侵权",
    "提交后不可修改",
    "评选结果将在活动结束后7个工作日内公布"
  ],

  fullDescription: "本次大赛旨在发掘优秀创作者...",
  createdAt: "2025-11-01T00:00:00Z",
  updatedAt: "2025-11-01T00:00:00Z"
};
```

## 3. 积分活动 (Points Activity)

### 适用场景
- 双倍积分活动
- 完成任务获积分
- 节日积分加成

### 数据结构示例

```typescript
const pointsActivity: Activity = {
  id: "pts-001",
  title: "双十二积分狂欢",
  subtitle: "全站双倍积分，完成任务额外送",
  description: "在活动期间，所有积分获取都将翻倍",
  bannerUrl: "https://example.com/points-banner.jpg",
  category: "积分活动",
  type: ActivityType.POINTS,
  status: ActivityStatus.ONGOING,
  format: ActivityFormat.ONLINE,
  startTime: "2025-12-12T00:00:00Z",
  endTime: "2025-12-12T23:59:59Z",
  participantCount: 8900,

  // 积分活动特有规则
  rules: {
    type: ActivityType.POINTS,
    pointsMultiplier: 2,  // 积分翻倍
    bonusPoints: 500,     // 额外赠送500积分
    tasks: [
      {
        taskName: "完成一篇创作",
        pointsReward: 200,
        description: "发布一篇原创作品"
      },
      {
        taskName: "邀请好友",
        pointsReward: 300,
        description: "成功邀请1位好友注册"
      },
      {
        taskName: "分享作品",
        pointsReward: 100,
        description: "分享作品到社交媒体"
      }
    ]
  },

  participationSteps: [
    {
      step: 1,
      title: "查看任务列表",
      description: "了解可获得积分的任务"
    },
    {
      step: 2,
      title: "完成任务",
      description: "按要求完成各项任务"
    },
    {
      step: 3,
      title: "自动获得积分",
      description: "任务完成后积分自动到账"
    }
  ],

  notice: [
    "积分翻倍仅限活动期间",
    "任务积分不受翻倍影响",
    "积分有效期为永久"
  ],

  fullDescription: "双十二特别活动，全站积分翻倍...",
  createdAt: "2025-12-01T00:00:00Z",
  updatedAt: "2025-12-01T00:00:00Z"
};
```

## 4. 任务活动 (Mission Activity)

### 适用场景
- 新手引导任务
- 连续任务挑战
- 成就解锁活动

### 数据结构示例

```typescript
const missionActivity: Activity = {
  id: "miss-001",
  title: "新手成长计划",
  subtitle: "完成7天任务，解锁全部奖励",
  description: "按顺序完成任务，获得丰厚奖励",
  bannerUrl: "https://example.com/mission-banner.jpg",
  category: "任务活动",
  type: ActivityType.MISSION,
  status: ActivityStatus.ONGOING,
  format: ActivityFormat.ONLINE,
  startTime: "2025-12-01T00:00:00Z",
  endTime: "2025-12-31T23:59:59Z",
  participantCount: 3456,

  // 任务活动特有规则
  rules: {
    type: ActivityType.MISSION,
    missions: [
      {
        missionId: "m1",
        title: "完善个人资料",
        description: "填写昵称、头像、简介",
        requirement: "完善度达到100%",
        sequence: 1,
        rewards: [
          {
            type: RewardType.POINTS,
            name: "新手奖励",
            amount: 100
          }
        ]
      },
      {
        missionId: "m2",
        title: "发布第一篇作品",
        description: "创作并发布第一篇作品",
        requirement: "作品字数不少于500字",
        sequence: 2,
        rewards: [
          {
            type: RewardType.POINTS,
            name: "创作奖励",
            amount: 200
          },
          {
            type: RewardType.BADGE,
            name: "创作新星",
            badgeId: "newbie-writer"
          }
        ]
      },
      {
        missionId: "m3",
        title: "连续创作7天",
        description: "连续7天每天至少创作一篇",
        requirement: "连续7天发布作品",
        sequence: 3,
        rewards: [
          {
            type: RewardType.POINTS,
            name: "坚持奖励",
            amount: 500
          },
          {
            type: RewardType.VIP,
            name: "7天VIP体验",
            duration: 7,
            level: "basic"
          }
        ]
      }
    ],
    completionReward: [
      {
        type: RewardType.POINTS,
        name: "全部完成奖励",
        amount: 1000
      },
      {
        type: RewardType.BADGE,
        name: "成长达人",
        badgeId: "growth-master"
      }
    ]
  },

  participationSteps: [
    {
      step: 1,
      title: "查看任务列表",
      description: "了解需要完成的任务"
    },
    {
      step: 2,
      title: "按顺序完成任务",
      description: "从第一个任务开始逐个完成"
    },
    {
      step: 3,
      title: "领取奖励",
      description: "每完成一个任务即可领取奖励"
    }
  ],

  notice: [
    "任务需按顺序完成",
    "完成全部任务可获得额外奖励",
    "任务进度保存，可随时继续"
  ],

  fullDescription: "新手成长计划帮助您快速熟悉平台功能...",
  createdAt: "2025-12-01T00:00:00Z",
  updatedAt: "2025-12-01T00:00:00Z"
};
```

## 5. 抽奖活动 (Lottery Activity)

### 适用场景
- 幸运抽奖
- 节日抽奖
- 消耗积分抽奖

### 数据结构示例

```typescript
const lotteryActivity: Activity = {
  id: "lot-001",
  title: "新年幸运大抽奖",
  subtitle: "每天免费抽1次，VIP会员抽3次",
  description: "参与抽奖，赢取丰厚奖品",
  bannerUrl: "https://example.com/lottery-banner.jpg",
  category: "抽奖活动",
  type: ActivityType.LOTTERY,
  status: ActivityStatus.ONGOING,
  format: ActivityFormat.ONLINE,
  startTime: "2025-12-25T00:00:00Z",
  endTime: "2025-12-31T23:59:59Z",
  participantCount: 12345,

  // 抽奖活动特有规则
  rules: {
    type: ActivityType.LOTTERY,
    prizes: [
      {
        prizeId: "p1",
        name: "一等奖 - 年度VIP",
        probability: 0.01,  // 1%中奖率
        totalQuantity: 10,
        remainingQuantity: 7,
        rewards: [
          {
            type: RewardType.VIP,
            name: "年度VIP会员",
            duration: 365,
            level: "premium"
          }
        ]
      },
      {
        prizeId: "p2",
        name: "二等奖 - 5000积分",
        probability: 0.05,  // 5%中奖率
        totalQuantity: 100,
        remainingQuantity: 78,
        rewards: [
          {
            type: RewardType.POINTS,
            name: "积分奖励",
            amount: 5000
          }
        ]
      },
      {
        prizeId: "p3",
        name: "三等奖 - 1000积分",
        probability: 0.15,  // 15%中奖率
        rewards: [
          {
            type: RewardType.POINTS,
            name: "积分奖励",
            amount: 1000
          }
        ]
      },
      {
        prizeId: "p4",
        name: "参与奖 - 100积分",
        probability: 0.79,  // 79%中奖率
        rewards: [
          {
            type: RewardType.POINTS,
            name: "参与奖",
            amount: 100
          }
        ]
      }
    ],
    drawCost: {
      type: "free"  // 也可以是 { type: "points", amount: 100 }
    },
    maxDrawsPerUser: 3  // 每人最多抽3次
  },

  participationSteps: [
    {
      step: 1,
      title: "点击抽奖按钮",
      description: "每天有免费抽奖机会"
    },
    {
      step: 2,
      title: "查看中奖结果",
      description: "系统随机抽取奖品"
    },
    {
      step: 3,
      title: "领取奖励",
      description: "奖励自动发放到账户"
    }
  ],

  notice: [
    "每人每天最多抽3次",
    "VIP会员有额外抽奖机会",
    "奖品数量有限，先到先得",
    "中奖记录可在个人中心查看"
  ],

  fullDescription: "新年特别抽奖活动，多重大奖等你来拿...",
  createdAt: "2025-12-20T00:00:00Z",
  updatedAt: "2025-12-20T00:00:00Z"
};
```

## 6. 签到活动 (Check-in Activity)

### 适用场景
- 每日签到
- 连续签到奖励
- 累计签到里程碑

### 数据结构示例

```typescript
const checkinActivity: Activity = {
  id: "chk-001",
  title: "每日签到领积分",
  subtitle: "连续签到奖励更丰厚",
  description: "每天签到获得积分，连续签到有额外奖励",
  bannerUrl: "https://example.com/checkin-banner.jpg",
  category: "签到活动",
  type: ActivityType.CHECKIN,
  status: ActivityStatus.ONGOING,
  format: ActivityFormat.ONLINE,
  startTime: "2025-12-01T00:00:00Z",
  endTime: "2025-12-31T23:59:59Z",
  participantCount: 23456,

  // 签到活动特有规则
  rules: {
    type: ActivityType.CHECKIN,
    dailyRewards: [
      {
        type: RewardType.POINTS,
        name: "每日签到",
        amount: 50
      }
    ],
    consecutiveBonuses: [
      {
        days: 7,
        rewards: [
          {
            type: RewardType.POINTS,
            name: "连续7天奖励",
            amount: 200
          }
        ]
      },
      {
        days: 14,
        rewards: [
          {
            type: RewardType.POINTS,
            name: "连续14天奖励",
            amount: 500
          }
        ]
      },
      {
        days: 30,
        rewards: [
          {
            type: RewardType.POINTS,
            name: "连续30天奖励",
            amount: 1500
          },
          {
            type: RewardType.BADGE,
            name: "签到达人",
            badgeId: "checkin-master"
          }
        ]
      }
    ],
    totalCheckinsReward: [
      {
        days: 50,
        rewards: [
          {
            type: RewardType.VIP,
            name: "30天VIP体验",
            duration: 30,
            level: "basic"
          }
        ]
      },
      {
        days: 100,
        rewards: [
          {
            type: RewardType.VIP,
            name: "90天VIP会员",
            duration: 90,
            level: "premium"
          }
        ]
      }
    ]
  },

  participationSteps: [
    {
      step: 1,
      title: "每日登录",
      description: "在活动期间每天登录平台"
    },
    {
      step: 2,
      title: "点击签到",
      description: "点击签到按钮完成签到"
    },
    {
      step: 3,
      title: "获得奖励",
      description: "签到成功后立即获得积分"
    }
  ],

  notice: [
    "每天只能签到一次",
    "中断后连续签到天数重置",
    "累计签到天数永久保留",
    "奖励自动发放，无需手动领取"
  ],

  fullDescription: "坚持每日签到，不仅能获得每日积分，还有连续签到奖励...",
  createdAt: "2025-12-01T00:00:00Z",
  updatedAt: "2025-12-01T00:00:00Z"
};
```

## 使用建议

### 1. 选择合适的活动类型
- **用户增长** → 邀请活动
- **用户留存** → 签到活动、任务活动
- **用户活跃** → 积分活动、抽奖活动
- **用户质量** → 比赛活动

### 2. 奖励设计原则
- 奖励要有吸引力但不能过度
- 设置阶梯式奖励增加参与感
- 平衡短期奖励和长期奖励
- 考虑成本和用户价值

### 3. 活动时间规划
- 短期活动（1-7天）：抽奖、积分倍数
- 中期活动（1-4周）：比赛、任务挑战
- 长期活动（1-3个月）：签到、邀请

### 4. 数据监控指标
- 参与人数
- 完成率
- 转化率
- ROI（投入产出比）
- 用户反馈

## API 接口示例

```typescript
// 获取活动列表
GET /api/activities?type=invitation&status=ongoing

// 获取活动详情
GET /api/activities/:activityId

// 参与活动
POST /api/activities/:activityId/participate

// 获取用户参与记录
GET /api/activities/:activityId/participation

// 领取奖励
POST /api/activities/:activityId/claim-reward
```
