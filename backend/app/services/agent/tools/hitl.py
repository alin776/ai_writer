"""
人机协同 (Human-in-the-Loop) 系统

功能:
1. Agent执行关键操作前暂停，等待人工批准
2. 用户可以批准/修改/拒绝Agent的计划
3. 支持暂停点(Checkpoint)机制
4. 保存Agent状态，可随时恢复

使用场景:
- 生成大纲前确认思路
- 批量操作前确认范围
- 重要修改前征求同意
- 创建角色/世界观前确认设定

工作流:
1. Agent生成计划 → 2. 暂停并请求批准 → 3. 用户操作 → 4. 恢复执行
"""

from typing import Dict, List, Optional, Any, Literal
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
import json
import redis
import uuid
from app.utils.datetime_utils import get_utc_now


class ApprovalStatus(str, Enum):
    """批准状态"""
    PENDING = "pending"  # 等待批准
    APPROVED = "approved"  # 已批准
    MODIFIED = "modified"  # 已修改后批准
    REJECTED = "rejected"  # 已拒绝
    TIMEOUT = "timeout"  # 超时


class ApprovalRequest(BaseModel):
    """批准请求"""
    request_id: str  # 请求ID
    agent_id: str  # Agent ID
    user_id: str  # 用户ID

    # 请求内容
    title: str  # 请求标题
    description: str  # 详细说明
    proposed_action: Dict[str, Any]  # 建议的操作
    alternatives: List[Dict[str, Any]] = []  # 备选方案

    # 上下文
    context: Dict[str, Any] = {}  # 当前上下文
    checkpoint_data: Dict[str, Any] = {}  # 检查点数据

    # 元数据
    created_at: str
    expires_at: Optional[str] = None  # 过期时间
    status: ApprovalStatus = ApprovalStatus.PENDING

    # 用户响应
    user_response: Optional[Dict[str, Any]] = None
    responded_at: Optional[str] = None


class ApprovalResponse(BaseModel):
    """批准响应"""
    request_id: str
    status: ApprovalStatus
    modifications: Optional[Dict[str, Any]] = None  # 用户修改
    feedback: Optional[str] = None  # 用户反馈
    timestamp: str


class HITLManager:
    """人机协同管理器"""

    def __init__(self, redis_client: redis.Redis):
        """
        初始化HITL管理器

        Args:
            redis_client: Redis客户端
        """
        self.redis = redis_client
        self.default_timeout = 3600 * 2  # 2小时超时

    # ==================== 批准请求管理 ====================

    def create_approval_request(
        self,
        agent_id: str,
        user_id: str,
        title: str,
        description: str,
        proposed_action: Dict[str, Any],
        context: Dict[str, Any] = None,
        alternatives: List[Dict[str, Any]] = None,
        checkpoint_data: Dict[str, Any] = None,
        timeout_seconds: int = None
    ) -> ApprovalRequest:
        """
        创建批准请求

        Args:
            agent_id: Agent ID
            user_id: 用户ID
            title: 请求标题
            description: 详细说明
            proposed_action: 建议的操作
            context: 上下文
            alternatives: 备选方案
            checkpoint_data: 检查点数据
            timeout_seconds: 超时时间（秒）

        Returns:
            ApprovalRequest: 批准请求对象
        """
        request_id = str(uuid.uuid4())
        timeout = timeout_seconds or self.default_timeout

        expires_at = datetime.fromtimestamp(
            get_utc_now().timestamp() + timeout
        ).isoformat()

        request = ApprovalRequest(
            request_id=request_id,
            agent_id=agent_id,
            user_id=user_id,
            title=title,
            description=description,
            proposed_action=proposed_action,
            alternatives=alternatives or [],
            context=context or {},
            checkpoint_data=checkpoint_data or {},
            created_at=get_utc_now().isoformat(),
            expires_at=expires_at
        )

        # 保存到Redis
        key = f"hitl:request:{request_id}"
        self.redis.setex(
            key,
            timeout,
            json.dumps(request.dict())
        )

        # 添加到用户的待处理列表
        user_list_key = f"hitl:user:{user_id}:pending"
        self.redis.lpush(user_list_key, request_id)
        self.redis.expire(user_list_key, timeout)

        return request

    def get_approval_request(
        self,
        request_id: str
    ) -> Optional[ApprovalRequest]:
        """
        获取批准请求

        Args:
            request_id: 请求ID

        Returns:
            Optional[ApprovalRequest]: 请求对象，如果不存在返回None
        """
        key = f"hitl:request:{request_id}"
        data = self.redis.get(key)

        if data:
            return ApprovalRequest(**json.loads(data))
        return None

    def get_pending_requests(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[ApprovalRequest]:
        """
        获取用户待处理的请求列表

        Args:
            user_id: 用户ID
            limit: 返回数量限制

        Returns:
            List[ApprovalRequest]: 请求列表
        """
        user_list_key = f"hitl:user:{user_id}:pending"
        request_ids = self.redis.lrange(user_list_key, 0, limit - 1)

        requests = []
        for req_id in request_ids:
            request = self.get_approval_request(req_id.decode())
            if request and request.status == ApprovalStatus.PENDING:
                # 检查是否超时
                if request.expires_at:
                    expires = datetime.fromisoformat(request.expires_at)
                    if get_utc_now() > expires:
                        self._mark_timeout(request.request_id)
                        continue
                requests.append(request)

        return requests

    # ==================== 用户响应处理 ====================

    async def submit_approval(
        self,
        request_id: str,
        status: ApprovalStatus,
        data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        提交批准响应（简化版本，用于SSE流式场景）

        Args:
            request_id: 请求ID
            status: 批准状态
            data: 额外数据（如selected_version, reason等）

        Returns:
            bool: 是否成功
        """
        # 保存到Redis，让等待的Agent可以读取
        key = f"hitl:response:{request_id}"
        response_data = {
            "request_id": request_id,
            "status": status.value,
            "data": data or {},
            "timestamp": get_utc_now().isoformat()
        }

        # 保存响应，30分钟过期
        self.redis.setex(
            key,
            1800,
            json.dumps(response_data)
        )

        return True

    def approve_request(
        self,
        request_id: str,
        user_id: str,
        modifications: Optional[Dict[str, Any]] = None,
        feedback: Optional[str] = None
    ) -> ApprovalResponse:
        """
        批准请求

        Args:
            request_id: 请求ID
            user_id: 用户ID
            modifications: 用户修改（如果有）
            feedback: 用户反馈

        Returns:
            ApprovalResponse: 响应对象
        """
        request = self.get_approval_request(request_id)
        if not request:
            raise ValueError(f"Request {request_id} not found")

        if request.user_id != user_id:
            raise ValueError("User not authorized")

        # 判定状态
        status = ApprovalStatus.MODIFIED if modifications else ApprovalStatus.APPROVED

        response = ApprovalResponse(
            request_id=request_id,
            status=status,
            modifications=modifications,
            feedback=feedback,
            timestamp=get_utc_now().isoformat()
        )

        # 更新请求状态
        request.status = status
        request.user_response = response.dict()
        request.responded_at = response.timestamp

        self._save_request(request)
        self._remove_from_pending(user_id, request_id)

        return response

    def reject_request(
        self,
        request_id: str,
        user_id: str,
        reason: Optional[str] = None
    ) -> ApprovalResponse:
        """
        拒绝请求

        Args:
            request_id: 请求ID
            user_id: 用户ID
            reason: 拒绝原因

        Returns:
            ApprovalResponse: 响应对象
        """
        request = self.get_approval_request(request_id)
        if not request:
            raise ValueError(f"Request {request_id} not found")

        if request.user_id != user_id:
            raise ValueError("User not authorized")

        response = ApprovalResponse(
            request_id=request_id,
            status=ApprovalStatus.REJECTED,
            feedback=reason,
            timestamp=get_utc_now().isoformat()
        )

        # 更新请求状态
        request.status = ApprovalStatus.REJECTED
        request.user_response = response.dict()
        request.responded_at = response.timestamp

        self._save_request(request)
        self._remove_from_pending(user_id, request_id)

        return response

    def modify_and_approve(
        self,
        request_id: str,
        user_id: str,
        modified_action: Dict[str, Any],
        feedback: Optional[str] = None
    ) -> ApprovalResponse:
        """
        修改后批准

        Args:
            request_id: 请求ID
            user_id: 用户ID
            modified_action: 修改后的操作
            feedback: 反馈说明

        Returns:
            ApprovalResponse: 响应对象
        """
        return self.approve_request(
            request_id,
            user_id,
            modifications=modified_action,
            feedback=feedback
        )

    def select_alternative(
        self,
        request_id: str,
        user_id: str,
        alternative_index: int,
        feedback: Optional[str] = None
    ) -> ApprovalResponse:
        """
        选择备选方案

        Args:
            request_id: 请求ID
            user_id: 用户ID
            alternative_index: 备选方案索引
            feedback: 反馈说明

        Returns:
            ApprovalResponse: 响应对象
        """
        request = self.get_approval_request(request_id)
        if not request:
            raise ValueError(f"Request {request_id} not found")

        if alternative_index >= len(request.alternatives):
            raise ValueError("Invalid alternative index")

        selected_alternative = request.alternatives[alternative_index]

        return self.approve_request(
            request_id,
            user_id,
            modifications={"selected_alternative": alternative_index, **selected_alternative},
            feedback=feedback
        )

    # ==================== 等待批准 ====================

    async def wait_for_approval(
        self,
        request_id: str,
        check_interval: int = 5,
        max_wait: int = None
    ) -> ApprovalResponse:
        """
        等待用户批准（异步）

        Args:
            request_id: 请求ID
            check_interval: 检查间隔（秒）
            max_wait: 最大等待时间（秒）

        Returns:
            ApprovalResponse: 用户响应

        Raises:
            TimeoutError: 如果超时
        """
        import asyncio

        start_time = get_utc_now().timestamp()
        max_wait_time = max_wait or self.default_timeout

        while True:
            request = self.get_approval_request(request_id)

            if not request:
                raise ValueError(f"Request {request_id} not found")

            # 检查是否已响应
            if request.status != ApprovalStatus.PENDING:
                return ApprovalResponse(**request.user_response)

            # 检查是否超时
            elapsed = get_utc_now().timestamp() - start_time
            if elapsed > max_wait_time:
                self._mark_timeout(request_id)
                raise TimeoutError(f"Approval request {request_id} timed out")

            # 等待后再检查
            await asyncio.sleep(check_interval)

    # ==================== Checkpoint管理 ====================

    def save_checkpoint(
        self,
        agent_id: str,
        user_id: str,
        checkpoint_name: str,
        agent_state: Dict[str, Any],
        metadata: Dict[str, Any] = None
    ) -> str:
        """
        保存Agent状态检查点

        Args:
            agent_id: Agent ID
            user_id: 用户ID
            checkpoint_name: 检查点名称
            agent_state: Agent状态
            metadata: 元数据

        Returns:
            str: 检查点ID
        """
        checkpoint_id = str(uuid.uuid4())

        checkpoint = {
            "checkpoint_id": checkpoint_id,
            "agent_id": agent_id,
            "user_id": user_id,
            "checkpoint_name": checkpoint_name,
            "agent_state": agent_state,
            "metadata": metadata or {},
            "created_at": get_utc_now().isoformat()
        }

        # 保存检查点
        key = f"hitl:checkpoint:{checkpoint_id}"
        self.redis.setex(
            key,
            60 * 60 * 24 * 7,  # 7天过期
            json.dumps(checkpoint)
        )

        # 添加到Agent的检查点列表
        list_key = f"hitl:agent:{agent_id}:checkpoints"
        self.redis.lpush(list_key, checkpoint_id)
        self.redis.ltrim(list_key, 0, 19)  # 保留最近20个
        self.redis.expire(list_key, 60 * 60 * 24 * 7)

        return checkpoint_id

    def load_checkpoint(
        self,
        checkpoint_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        加载检查点

        Args:
            checkpoint_id: 检查点ID

        Returns:
            Optional[Dict]: 检查点数据
        """
        key = f"hitl:checkpoint:{checkpoint_id}"
        data = self.redis.get(key)

        if data:
            return json.loads(data)
        return None

    def get_agent_checkpoints(
        self,
        agent_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        获取Agent的检查点列表

        Args:
            agent_id: Agent ID
            limit: 返回数量限制

        Returns:
            List[Dict]: 检查点列表
        """
        list_key = f"hitl:agent:{agent_id}:checkpoints"
        checkpoint_ids = self.redis.lrange(list_key, 0, limit - 1)

        checkpoints = []
        for cp_id in checkpoint_ids:
            checkpoint = self.load_checkpoint(cp_id.decode())
            if checkpoint:
                checkpoints.append(checkpoint)

        return checkpoints

    # ==================== 辅助方法 ====================

    def _save_request(self, request: ApprovalRequest):
        """保存请求"""
        key = f"hitl:request:{request.request_id}"
        ttl = self.redis.ttl(key)
        if ttl > 0:
            self.redis.setex(key, ttl, json.dumps(request.dict()))

    def _remove_from_pending(self, user_id: str, request_id: str):
        """从待处理列表移除"""
        user_list_key = f"hitl:user:{user_id}:pending"
        self.redis.lrem(user_list_key, 0, request_id)

    def _mark_timeout(self, request_id: str):
        """标记为超时"""
        request = self.get_approval_request(request_id)
        if request:
            request.status = ApprovalStatus.TIMEOUT
            self._save_request(request)

    # ==================== 统计信息 ====================

    def get_stats(self, user_id: str = None) -> Dict[str, Any]:
        """
        获取HITL统计信息

        Args:
            user_id: 用户ID（可选）

        Returns:
            Dict: 统计信息
        """
        if user_id:
            pending = self.get_pending_requests(user_id)
            return {
                "pending_count": len(pending),
                "pending_requests": [
                    {
                        "request_id": r.request_id,
                        "title": r.title,
                        "created_at": r.created_at
                    }
                    for r in pending
                ]
            }
        else:
            return {"message": "Global stats not implemented"}
