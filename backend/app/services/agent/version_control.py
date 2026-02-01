"""
版本控制服务 - 补丁式版本管理

借鉴 pulpgen 的补丁式版本管理理念，实现：
- 补丁式版本控制（只存储变更差异）
- 版本回滚
- 版本分支
- 变更历史追踪

Author: AI Writer Agent System
Created: 2025-10-31
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import redis
import json
import uuid
from app.utils.datetime_utils import get_utc_now


# ==================== 数据模型 ====================

class PatchOperation(str, Enum):
    """补丁操作类型"""
    INSERT = "insert"      # 在指定位置插入文本
    DELETE = "delete"      # 删除指定位置的文本
    REPLACE = "replace"    # 替换指定位置的文本
    REORDER = "reorder"    # 重新排序段落


class Patch(BaseModel):
    """补丁定义

    记录单次内容变更操作
    """
    patch_id: str = Field(..., description="补丁唯一ID")
    operation: PatchOperation = Field(..., description="操作类型")
    position: int = Field(..., description="操作位置（字符索引或段落索引）")
    content: str = Field(default="", description="新内容（INSERT/REPLACE时使用）")
    length: int = Field(default=0, description="删除/替换长度")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="额外元数据")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    created_by: str = Field(..., description="创建者 (user_id 或 agent_name)")
    description: str = Field(default="", description="变更描述")



class Version(BaseModel):
    """版本定义

    一个版本包含一个或多个补丁
    """
    version_id: str = Field(..., description="版本唯一ID")
    parent_version_id: Optional[str] = Field(None, description="父版本ID")
    patches: List[Patch] = Field(default_factory=list, description="该版本包含的补丁列表")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    created_by: str = Field(..., description="创建者")
    tag: Optional[str] = Field(None, description="版本标签（如'初稿'、'修订版1'）")
    description: str = Field(default="", description="版本描述")



class VersionedContent(BaseModel):
    """版本化内容

    管理一份内容的所有版本历史
    """
    content_id: str = Field(..., description="内容唯一ID")
    base_content: str = Field(..., description="基础版本内容")
    versions: List[Version] = Field(default_factory=list, description="版本列表")
    current_version_id: str = Field(..., description="当前版本ID")
    branches: Dict[str, str] = Field(default_factory=dict, description="分支映射 (branch_name -> version_id)")



# ==================== 版本控制服务 ====================

class VersionControlService:
    """版本控制服务

    提供补丁式版本管理功能：
    - 创建版本化内容
    - 应用补丁创建新版本
    - 获取任意版本的内容
    - 版本回滚
    - 分支管理
    - 版本对比
    """

    def __init__(self, redis_client: redis.Redis):
        """初始化版本控制服务

        Args:
            redis_client: Redis客户端实例
        """
        self.redis = redis_client

    # ========== 1. 创建内容 ==========

    def create_content(
        self,
        content_id: str,
        initial_content: str,
        created_by: str
    ) -> VersionedContent:
        """创建版本化内容

        Args:
            content_id: 内容唯一ID
            initial_content: 初始内容
            created_by: 创建者ID

        Returns:
            VersionedContent: 版本化内容对象
        """
        # 创建初始版本（没有补丁）
        base_version = Version(
            version_id=self._generate_version_id(),
            parent_version_id=None,
            patches=[],
            created_at=get_utc_now(),
            created_by=created_by,
            tag="base",
            description="初始版本"
        )

        # 创建版本化内容
        versioned = VersionedContent(
            content_id=content_id,
            base_content=initial_content,
            versions=[base_version],
            current_version_id=base_version.version_id,
            branches={"main": base_version.version_id}
        )

        # 保存到Redis
        self._save(versioned)
        return versioned

    # ========== 2. 应用补丁 ==========

    def apply_patch(
        self,
        content_id: str,
        patch: Patch
    ) -> Version:
        """应用补丁（创建新版本）

        Args:
            content_id: 内容ID
            patch: 补丁对象

        Returns:
            Version: 新创建的版本
        """
        versioned = self._load(content_id)

        # 创建新版本
        new_version = Version(
            version_id=self._generate_version_id(),
            parent_version_id=versioned.current_version_id,
            patches=[patch],
            created_at=get_utc_now(),
            created_by=patch.created_by,
            description=patch.description or "应用补丁"
        )

        # 添加到版本列表
        versioned.versions.append(new_version)
        versioned.current_version_id = new_version.version_id

        # 保存
        self._save(versioned)
        return new_version

    # ========== 3. 获取内容 ==========

    def get_content_at_version(
        self,
        content_id: str,
        version_id: Optional[str] = None
    ) -> str:
        """获取指定版本的内容

        Args:
            content_id: 内容ID
            version_id: 版本ID（None表示当前版本）

        Returns:
            str: 该版本的完整内容
        """
        versioned = self._load(content_id)

        # 使用当前版本
        if not version_id:
            version_id = versioned.current_version_id

        # 从base_content开始应用所有补丁
        content = versioned.base_content
        patches = self._collect_patches_to_version(versioned, version_id)

        for patch in patches:
            content = self._apply_single_patch(content, patch)

        return content

    # ========== 4. 回滚版本 ==========

    def rollback_to_version(
        self,
        content_id: str,
        version_id: str
    ) -> str:
        """回滚到指定版本

        Args:
            content_id: 内容ID
            version_id: 目标版本ID

        Returns:
            str: 回滚后的内容
        """
        versioned = self._load(content_id)

        # 验证版本存在
        version_ids = {v.version_id for v in versioned.versions}
        if version_id not in version_ids:
            raise ValueError(f"版本 '{version_id}' 不存在")

        # 更新当前版本
        versioned.current_version_id = version_id
        self._save(versioned)

        return self.get_content_at_version(content_id, version_id)

    # ========== 5. 分支管理 ==========

    def create_branch(
        self,
        content_id: str,
        branch_name: str,
        from_version_id: Optional[str] = None
    ) -> str:
        """创建分支

        Args:
            content_id: 内容ID
            branch_name: 分支名称
            from_version_id: 基于哪个版本创建（None表示当前版本）

        Returns:
            str: 分支的base版本ID
        """
        versioned = self._load(content_id)

        # 确定分支base版本
        base_version = from_version_id or versioned.current_version_id

        # 验证版本存在
        version_ids = {v.version_id for v in versioned.versions}
        if base_version not in version_ids:
            raise ValueError(f"版本 '{base_version}' 不存在")

        # 保存分支
        versioned.branches[branch_name] = base_version
        self._save(versioned)

        return base_version

    def switch_branch(
        self,
        content_id: str,
        branch_name: str
    ) -> str:
        """切换到分支

        Args:
            content_id: 内容ID
            branch_name: 分支名称

        Returns:
            str: 分支的当前内容
        """
        versioned = self._load(content_id)

        if branch_name not in versioned.branches:
            raise ValueError(f"分支 '{branch_name}' 不存在")

        version_id = versioned.branches[branch_name]
        return self.rollback_to_version(content_id, version_id)

    # ========== 6. 版本历史和对比 ==========

    def get_version_history(
        self,
        content_id: str
    ) -> List[Dict[str, Any]]:
        """获取版本历史

        Args:
            content_id: 内容ID

        Returns:
            List[Dict]: 版本历史列表
        """
        versioned = self._load(content_id)

        history = []
        for version in versioned.versions:
            history.append({
                "version_id": version.version_id,
                "parent_version_id": version.parent_version_id,
                "created_at": version.created_at.isoformat(),
                "created_by": version.created_by,
                "tag": version.tag,
                "description": version.description,
                "patch_count": len(version.patches)
            })

        return history

    def compare_versions(
        self,
        content_id: str,
        version_id_1: str,
        version_id_2: str
    ) -> Dict[str, Any]:
        """对比两个版本

        Args:
            content_id: 内容ID
            version_id_1: 版本1 ID
            version_id_2: 版本2 ID

        Returns:
            Dict: 对比结果
        """
        content_1 = self.get_content_at_version(content_id, version_id_1)
        content_2 = self.get_content_at_version(content_id, version_id_2)

        # 简单的差异统计
        return {
            "version_1": version_id_1,
            "version_2": version_id_2,
            "length_diff": len(content_2) - len(content_1),
            "content_1_length": len(content_1),
            "content_2_length": len(content_2),
            "content_1_preview": content_1[:200],
            "content_2_preview": content_2[:200],
        }

    # ========== 辅助方法 ==========

    def _apply_single_patch(self, content: str, patch: Patch) -> str:
        """应用单个补丁

        Args:
            content: 当前内容
            patch: 补丁对象

        Returns:
            str: 应用补丁后的内容
        """
        if patch.operation == PatchOperation.INSERT:
            # 在指定位置插入内容
            return content[:patch.position] + patch.content + content[patch.position:]

        elif patch.operation == PatchOperation.DELETE:
            # 删除指定长度的内容
            return content[:patch.position] + content[patch.position + patch.length:]

        elif patch.operation == PatchOperation.REPLACE:
            # 替换指定长度的内容
            return content[:patch.position] + patch.content + content[patch.position + patch.length:]

        elif patch.operation == PatchOperation.REORDER:
            # 重排序（简化实现，直接返回）
            # 实际实现需要解析段落并重新排序
            return content

        return content

    def _collect_patches_to_version(
        self,
        versioned: VersionedContent,
        target_version_id: str
    ) -> List[Patch]:
        """收集到达目标版本的所有补丁

        Args:
            versioned: 版本化内容对象
            target_version_id: 目标版本ID

        Returns:
            List[Patch]: 按顺序排列的补丁列表（从base到target）
        """
        # 构建版本映射
        version_map = {v.version_id: v for v in versioned.versions}

        # 从目标版本往回追溯到base
        path = []
        current_id = target_version_id

        while current_id:
            if current_id not in version_map:
                break

            version = version_map[current_id]
            path.append(version)
            current_id = version.parent_version_id

        # 反转路径（从base到target）
        path.reverse()

        # 收集所有补丁
        patches = []
        for version in path:
            patches.extend(version.patches)

        return patches

    def _save(self, versioned: VersionedContent):
        """保存到Redis

        Args:
            versioned: 版本化内容对象
        """
        key = f"version:{versioned.content_id}"
        self.redis.set(key, versioned.json())

    def _load(self, content_id: str) -> VersionedContent:
        """从Redis加载

        Args:
            content_id: 内容ID

        Returns:
            VersionedContent: 版本化内容对象

        Raises:
            ValueError: 内容不存在
        """
        key = f"version:{content_id}"
        data = self.redis.get(key)

        if not data:
            raise ValueError(f"内容 '{content_id}' 不存在")

        return VersionedContent.parse_raw(data)

    def _generate_version_id(self) -> str:
        """生成版本ID

        Returns:
            str: 新的版本ID
        """
        return f"v_{uuid.uuid4().hex[:12]}"
