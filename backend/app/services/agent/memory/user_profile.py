"""
用户画像记忆系统 (User Profile Memory)

功能:
1. 自动构建用户画像
2. 追踪用户行为模式
3. 预测用户需求
4. 提供个性化推荐

用户画像维度:
- 创作习惯: 活跃时段、创作频率、常用功能
- 技能水平: 新手/进阶/专家
- 作品类型: 玄幻/都市/言情等
- 互动模式: 依赖Agent vs 自主创作
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import Counter
import json
import redis
from pydantic import BaseModel
from app.utils.datetime_utils import get_utc_now


class UserBehaviorPattern(BaseModel):
    """用户行为模式"""
    # 活跃度
    daily_active_hours: List[int] = []  # 常在哪些小时活跃
    avg_session_duration: float = 0.0  # 平均会话时长(分钟)
    sessions_per_week: float = 0.0  # 每周会话次数

    # 功能使用偏好
    most_used_features: List[str] = []  # 最常用功能
    feature_usage_count: Dict[str, int] = {}  # 功能使用计数

    # 创作模式
    avg_words_per_session: float = 0.0  # 每次会话平均创作字数
    primary_work_genres: List[str] = []  # 主要创作类型

    # 更新时间
    last_updated: str = ""


class UserSkillLevel(BaseModel):
    """用户技能等级"""
    overall_level: str = "novice"  # novice/intermediate/expert
    level_score: float = 0.0  # 0-100

    # 各维度得分
    creativity_score: float = 0.0  # 创意能力
    proficiency_score: float = 0.0  # 熟练程度
    independence_score: float = 0.0  # 独立性（是否依赖Agent）

    # 评估依据
    total_works: int = 0
    total_words: int = 0
    total_sessions: int = 0

    last_updated: str = ""


class InteractionMode(BaseModel):
    """互动模式"""
    agent_dependency: float = 0.5  # 0-1, Agent依赖度
    autonomy_level: float = 0.5  # 0-1, 自主创作程度

    # 提问习惯
    avg_questions_per_session: float = 0.0
    question_types: List[str] = []  # ["how_to", "suggestion", "debug"]

    # 反馈习惯
    feedback_frequency: float = 0.0  # 反馈频率
    avg_iterations: float = 1.0  # 平均修改迭代次数

    last_updated: str = ""


class UserProfileMemory:
    """用户画像记忆服务"""

    def __init__(self, redis_client: redis.Redis):
        """
        初始化用户画像服务

        Args:
            redis_client: Redis客户端
        """
        self.redis = redis_client
        self.profile_ttl = 60 * 60 * 24 * 180  # 180天过期

    # ==================== 行为模式追踪 ====================

    def track_session_start(self, user_id: str):
        """
        记录会话开始

        Args:
            user_id: 用户ID
        """
        key = f"user:{user_id}:current_session"
        data = {
            "start_time": get_utc_now().isoformat(),
            "actions": []
        }
        self.redis.setex(key, 3600 * 4, json.dumps(data))  # 4小时过期

    def track_action(
        self,
        user_id: str,
        action_type: str,
        details: Dict[str, Any] = None
    ):
        """
        记录用户操作

        Args:
            user_id: 用户ID
            action_type: 操作类型
            details: 操作详情
        """
        # 记录到当前会话
        session_key = f"user:{user_id}:current_session"
        session_data = self.redis.get(session_key)

        if session_data:
            session = json.loads(session_data)
            session["actions"].append({
                "type": action_type,
                "timestamp": get_utc_now().isoformat(),
                "details": details or {}
            })
            self.redis.setex(session_key, 3600 * 4, json.dumps(session))

        # 更新功能使用计数
        count_key = f"user:{user_id}:feature_usage"
        self.redis.hincrby(count_key, action_type, 1)
        self.redis.expire(count_key, self.profile_ttl)

    def track_session_end(self, user_id: str, words_created: int = 0):
        """
        记录会话结束

        Args:
            user_id: 用户ID
            words_created: 本次会话创作的字数
        """
        session_key = f"user:{user_id}:current_session"
        session_data = self.redis.get(session_key)

        if not session_data:
            return

        session = json.loads(session_data)
        start_time = datetime.fromisoformat(session["start_time"])
        duration = (get_utc_now() - start_time).total_seconds() / 60  # 分钟

        # 保存会话摘要
        summary = {
            "start_time": session["start_time"],
            "end_time": get_utc_now().isoformat(),
            "duration_minutes": duration,
            "actions_count": len(session["actions"]),
            "words_created": words_created,
            "hour_of_day": start_time.hour
        }

        # 添加到会话历史
        history_key = f"user:{user_id}:session_history"
        self.redis.lpush(history_key, json.dumps(summary))
        self.redis.ltrim(history_key, 0, 99)  # 保留最近100次会话
        self.redis.expire(history_key, self.profile_ttl)

        # 删除当前会话
        self.redis.delete(session_key)

        # 更新行为模式
        self._update_behavior_pattern(user_id)

    def _update_behavior_pattern(self, user_id: str):
        """
        更新用户行为模式

        Args:
            user_id: 用户ID
        """
        # 获取会话历史
        history_key = f"user:{user_id}:session_history"
        sessions = self.redis.lrange(history_key, 0, 49)  # 最近50次

        if not sessions:
            return

        # 解析会话数据
        session_data = [json.loads(s) for s in sessions]

        # 计算活跃时段
        hours = [s["hour_of_day"] for s in session_data]
        hour_counter = Counter(hours)
        top_hours = [h for h, _ in hour_counter.most_common(5)]

        # 计算平均会话时长
        avg_duration = sum(s["duration_minutes"] for s in session_data) / len(session_data)

        # 计算每周会话次数（基于最近30天的数据）
        recent_30d = [
            s for s in session_data
            if (get_utc_now() - datetime.fromisoformat(s["end_time"])).days <= 30
        ]
        sessions_per_week = len(recent_30d) / 4.3 if recent_30d else 0

        # 计算平均创作字数
        avg_words = sum(s.get("words_created", 0) for s in session_data) / len(session_data)

        # 获取最常用功能
        usage_key = f"user:{user_id}:feature_usage"
        feature_counts = self.redis.hgetall(usage_key)
        sorted_features = sorted(
            feature_counts.items(),
            key=lambda x: int(x[1]),
            reverse=True
        )
        most_used = [f[0].decode() for f in sorted_features[:10]]

        # 保存行为模式
        pattern = UserBehaviorPattern(
            daily_active_hours=top_hours,
            avg_session_duration=round(avg_duration, 2),
            sessions_per_week=round(sessions_per_week, 2),
            most_used_features=most_used,
            avg_words_per_session=round(avg_words, 2),
            last_updated=get_utc_now().isoformat()
        )

        pattern_key = f"user:{user_id}:behavior_pattern"
        self.redis.setex(
            pattern_key,
            self.profile_ttl,
            json.dumps(pattern.dict())
        )

    def get_behavior_pattern(self, user_id: str) -> UserBehaviorPattern:
        """
        获取用户行为模式

        Args:
            user_id: 用户ID

        Returns:
            UserBehaviorPattern: 行为模式
        """
        key = f"user:{user_id}:behavior_pattern"
        data = self.redis.get(key)

        if data:
            return UserBehaviorPattern(**json.loads(data))
        else:
            return UserBehaviorPattern(
                last_updated=get_utc_now().isoformat()
            )

    # ==================== 技能等级评估 ====================

    def update_skill_level(
        self,
        user_id: str,
        total_works: int,
        total_words: int,
        total_sessions: int
    ):
        """
        更新用户技能等级

        Args:
            user_id: 用户ID
            total_works: 总作品数
            total_words: 总创作字数
            total_sessions: 总会话数
        """
        # 计算各维度得分
        # 1. 熟练程度 (基于使用频率和时长)
        proficiency = min(100, total_sessions * 2)

        # 2. 创意能力 (基于作品数量和字数)
        creativity = min(100, (total_works * 10 + total_words / 1000))

        # 3. 独立性 (基于Agent依赖度)
        interaction = self.get_interaction_mode(user_id)
        independence = (1 - interaction.agent_dependency) * 100

        # 综合得分
        overall_score = (proficiency + creativity + independence) / 3

        # 判定等级
        if overall_score < 30:
            level = "novice"
        elif overall_score < 70:
            level = "intermediate"
        else:
            level = "expert"

        skill = UserSkillLevel(
            overall_level=level,
            level_score=round(overall_score, 2),
            creativity_score=round(creativity, 2),
            proficiency_score=round(proficiency, 2),
            independence_score=round(independence, 2),
            total_works=total_works,
            total_words=total_words,
            total_sessions=total_sessions,
            last_updated=get_utc_now().isoformat()
        )

        key = f"user:{user_id}:skill_level"
        self.redis.setex(
            key,
            self.profile_ttl,
            json.dumps(skill.dict())
        )

        return skill

    def get_skill_level(self, user_id: str) -> UserSkillLevel:
        """
        获取用户技能等级

        Args:
            user_id: 用户ID

        Returns:
            UserSkillLevel: 技能等级
        """
        key = f"user:{user_id}:skill_level"
        data = self.redis.get(key)

        if data:
            return UserSkillLevel(**json.loads(data))
        else:
            return UserSkillLevel(
                last_updated=get_utc_now().isoformat()
            )

    # ==================== 互动模式分析 ====================

    def update_interaction_mode(
        self,
        user_id: str,
        agent_actions: int,
        manual_actions: int,
        questions_asked: int = 0
    ):
        """
        更新互动模式

        Args:
            user_id: 用户ID
            agent_actions: Agent辅助的操作数
            manual_actions: 手动操作数
            questions_asked: 提问次数
        """
        total_actions = agent_actions + manual_actions

        if total_actions == 0:
            agent_dependency = 0.5
            autonomy = 0.5
        else:
            agent_dependency = agent_actions / total_actions
            autonomy = manual_actions / total_actions

        # 获取会话数
        behavior = self.get_behavior_pattern(user_id)
        sessions = behavior.sessions_per_week * 4 if behavior.sessions_per_week else 1

        mode = InteractionMode(
            agent_dependency=round(agent_dependency, 2),
            autonomy_level=round(autonomy, 2),
            avg_questions_per_session=round(questions_asked / sessions, 2),
            last_updated=get_utc_now().isoformat()
        )

        key = f"user:{user_id}:interaction_mode"
        self.redis.setex(
            key,
            self.profile_ttl,
            json.dumps(mode.dict())
        )

        return mode

    def get_interaction_mode(self, user_id: str) -> InteractionMode:
        """
        获取互动模式

        Args:
            user_id: 用户ID

        Returns:
            InteractionMode: 互动模式
        """
        key = f"user:{user_id}:interaction_mode"
        data = self.redis.get(key)

        if data:
            return InteractionMode(**json.loads(data))
        else:
            return InteractionMode(
                last_updated=get_utc_now().isoformat()
            )

    # ==================== 综合画像 ====================

    def get_full_profile(self, user_id: str) -> Dict[str, Any]:
        """
        获取完整用户画像

        Args:
            user_id: 用户ID

        Returns:
            Dict: 完整画像
        """
        behavior = self.get_behavior_pattern(user_id)
        skill = self.get_skill_level(user_id)
        interaction = self.get_interaction_mode(user_id)

        return {
            "behavior_pattern": behavior.dict(),
            "skill_level": skill.dict(),
            "interaction_mode": interaction.dict(),
            "recommendations": self._generate_recommendations(
                behavior,
                skill,
                interaction
            )
        }

    def _generate_recommendations(
        self,
        behavior: UserBehaviorPattern,
        skill: UserSkillLevel,
        interaction: InteractionMode
    ) -> List[str]:
        """
        生成个性化推荐

        Returns:
            List[str]: 推荐建议
        """
        recommendations = []

        # 基于技能等级的推荐
        if skill.overall_level == "novice":
            recommendations.append("建议使用Agent模式，让AI手把手引导创作")
            recommendations.append("可以多使用'我想写xxx'这样的自然语言指令")
        elif skill.overall_level == "expert":
            recommendations.append("建议使用传统模式，可以更精确控制每个细节")
            recommendations.append("可以使用快捷键提升创作效率")

        # 基于活跃度的推荐
        if behavior.sessions_per_week < 2:
            recommendations.append("建议设置创作提醒，保持创作习惯")

        # 基于Agent依赖度的推荐
        if interaction.agent_dependency > 0.8:
            recommendations.append("可以尝试手动调整一些细节，提升创作自主性")
        elif interaction.agent_dependency < 0.2:
            recommendations.append("Agent可以帮你节省很多时间，不妨多尝试")

        return recommendations

    def format_profile_for_agent(self, user_id: str) -> str:
        """
        为Agent格式化用户画像
        （供Agent了解用户特征）

        Args:
            user_id: 用户ID

        Returns:
            str: 格式化的画像文本
        """
        profile = self.get_full_profile(user_id)
        behavior = profile["behavior_pattern"]
        skill = profile["skill_level"]
        interaction = profile["interaction_mode"]

        prompt_parts = ["# 用户画像\n"]

        # 技能等级
        level_map = {
            "novice": "新手",
            "intermediate": "进阶",
            "expert": "专家"
        }
        prompt_parts.append(f"- 技能等级: {level_map[skill['overall_level']]} (得分: {skill['level_score']:.1f}/100)")

        # 使用习惯
        if behavior["most_used_features"]:
            top_features = ", ".join(behavior["most_used_features"][:3])
            prompt_parts.append(f"- 常用功能: {top_features}")

        prompt_parts.append(f"- 平均会话时长: {behavior['avg_session_duration']:.1f}分钟")
        prompt_parts.append(f"- 每周活跃: {behavior['sessions_per_week']:.1f}次")

        # Agent依赖度
        dependency = interaction["agent_dependency"]
        if dependency > 0.7:
            prompt_parts.append("- 用户偏好: 高度依赖Agent辅助，需要详细指导")
        elif dependency < 0.3:
            prompt_parts.append("- 用户偏好: 倾向自主创作，Agent提供建议即可")
        else:
            prompt_parts.append("- 用户偏好: Agent与手动操作并重")

        return "\n".join(prompt_parts)
