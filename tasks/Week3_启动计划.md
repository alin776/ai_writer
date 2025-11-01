# Week 3 启动计划：版本管理系统

> **开始日期**: 2025-10-31
> **预计工期**: 3-5个工作日
> **目标**: 完成补丁式版本控制系统

---

## ✅ 前置条件检查

### Week 1-2 完成情况
- ✅ Week 1: Memory系统增强完成 (EnhancedMemoryManager)
- ✅ Week 2: 工具系统标准化完成 (StandardTool框架, 5个工具, 监控系统)

### 技术准备
- ✅ Redis 可用 (用于版本存储)
- ✅ Pydantic 可用 (用于数据验证)
- ✅ pytest 可用 (用于测试)

---

## 🎯 Week 3 核心目标

### 功能目标
1. **补丁式版本控制**: 只存储变更差异,节省存储空间
2. **版本回滚**: 快速回滚到任意历史版本 (< 200ms)
3. **版本分支**: 支持并行创作多个版本
4. **变更历史**: 完整追踪每次修改

### 技术指标
- ✅ 版本创建成功率 100%
- ✅ 补丁应用正确率 100%
- ✅ 版本回滚耗时 < 200ms
- ✅ 存储空间节省 > 80%

---

## 📋 详细任务分解

### Day 1: 数据模型设计 (2-3小时)

#### 任务1.1: 创建核心数据结构
- [ ] 创建文件 `backend/app/services/agent/version_control.py`
- [ ] 定义 `PatchOperation` 枚举
  - INSERT (插入文本)
  - DELETE (删除文本)
  - REPLACE (替换文本)
  - REORDER (重排序段落)

- [ ] 定义 `Patch` 数据模型
  ```python
  class Patch(BaseModel):
      patch_id: str
      operation: PatchOperation
      position: int
      content: str = ""
      length: int = 0
      metadata: Dict[str, Any] = {}
      created_at: datetime
      created_by: str
      description: str = ""
  ```

- [ ] 定义 `Version` 数据模型
  ```python
  class Version(BaseModel):
      version_id: str
      parent_version_id: Optional[str]
      patches: List[Patch]
      created_at: datetime
      created_by: str
      tag: Optional[str]
      description: str
  ```

- [ ] 定义 `VersionedContent` 数据模型
  ```python
  class VersionedContent(BaseModel):
      content_id: str
      base_content: str
      versions: List[Version]
      current_version_id: str
      branches: Dict[str, str]
  ```

#### 任务1.2: 测试数据模型
- [ ] 创建测试文件 `backend/tests/test_version_control/test_models.py`
- [ ] 测试Pydantic模型序列化/反序列化
- [ ] 测试datetime的JSON编码

#### 验收标准
- [x] 所有数据模型定义完成
- [x] 模型可以正常序列化为JSON
- [x] 单元测试通过

---

### Day 2: 核心服务实现 (4-5小时)

#### 任务2.1: 实现VersionControlService基础功能
- [ ] 实现 `create_content()` 方法
  - 创建初始版本
  - 保存到Redis

- [ ] 实现 `apply_patch()` 方法
  - 创建新版本
  - 应用补丁
  - 更新current_version_id

- [ ] 实现 `get_content_at_version()` 方法
  - 收集从base到target的所有patches
  - 顺序应用补丁
  - 返回最终内容

- [ ] 实现 `rollback_to_version()` 方法
  - 更新current_version_id
  - 返回回滚后内容

#### 任务2.2: 实现补丁应用逻辑
- [ ] 实现 `_apply_single_patch()` 方法
  - INSERT: 在position插入content
  - DELETE: 删除position开始的length个字符
  - REPLACE: 替换position开始的length个字符
  - REORDER: 重新排序(简化实现)

- [ ] 实现 `_collect_patches_to_version()` 方法
  - 从target回溯到base
  - 反转路径
  - 收集所有patches

#### 任务2.3: 实现存储逻辑
- [ ] 实现 `_save()` 方法 (保存到Redis)
- [ ] 实现 `_load()` 方法 (从Redis加载)
- [ ] 实现 `_generate_version_id()` 方法

#### 验收标准
- [x] create_content可以创建新内容
- [x] apply_patch可以创建新版本
- [x] get_content_at_version可以正确还原内容
- [x] rollback_to_version可以回滚

---

### Day 3: 分支管理和高级功能 (3-4小时)

#### 任务3.1: 实现分支管理
- [ ] 实现 `create_branch()` 方法
  - 保存分支名称和对应version_id

- [ ] 实现 `switch_branch()` 方法
  - 切换current_version_id到分支版本

#### 任务3.2: 实现版本对比
- [ ] 实现 `get_version_history()` 方法
  - 返回所有版本信息列表

- [ ] 实现 `compare_versions()` 方法
  - 对比两个版本的内容
  - 返回差异统计

#### 验收标准
- [x] 可以创建和切换分支
- [x] 可以查看版本历史
- [x] 可以对比版本

---

### Day 4: 单元测试 (4-5小时)

#### 任务4.1: 创建测试框架
- [ ] 创建 `backend/tests/test_version_control/conftest.py`
  - Redis fixture (使用fakeredis模拟)
  - VersionControlService fixture
  - 测试数据fixture

#### 任务4.2: 编写核心功能测试
- [ ] `test_create_content.py`
  - 测试创建新内容
  - 测试初始版本

- [ ] `test_apply_patch.py`
  - 测试INSERT操作
  - 测试DELETE操作
  - 测试REPLACE操作
  - 测试REORDER操作

- [ ] `test_version_retrieval.py`
  - 测试get_content_at_version
  - 测试多次补丁应用

- [ ] `test_rollback.py`
  - 测试版本回滚
  - 测试回滚正确性

#### 任务4.3: 编写高级功能测试
- [ ] `test_branches.py`
  - 测试创建分支
  - 测试切换分支
  - 测试分支独立性

- [ ] `test_version_history.py`
  - 测试版本历史查询
  - 测试版本对比

#### 验收标准
- [x] 测试覆盖率 > 80%
- [x] 所有测试通过
- [x] 边界情况测试通过

---

### Day 5: 性能测试和集成 (3-4小时)

#### 任务5.1: 性能测试
- [ ] 创建 `backend/tests/test_version_control/test_performance.py`
- [ ] 测试版本回滚速度
  - 10个版本回滚 < 200ms
  - 50个版本回滚 < 500ms
  - 100个版本回滚 < 1000ms

- [ ] 测试存储空间节省
  - 对比完整副本 vs 补丁式
  - 验证节省 > 80%

#### 任务5.2: 集成到章节创作流程(可选)
- [ ] 在 `writing_agent.py` 中集成
  - create_chapter 时创建版本化内容
  - continue_writing 时应用补丁
  - 支持undo操作

#### 任务5.3: 创建API端点(可选,可推迟到后续)
- [ ] `POST /api/v1/agent/versions/create`
- [ ] `POST /api/v1/agent/versions/apply-patch`
- [ ] `GET /api/v1/agent/versions/{version_id}`
- [ ] `POST /api/v1/agent/versions/rollback`

#### 验收标准
- [x] 版本回滚速度 < 200ms
- [x] 存储空间节省 > 80%
- [x] 基本集成完成(可选)

---

## 📦 交付物清单

### 核心代码
1. ✅ `backend/app/services/agent/version_control.py` (~400-500行)
   - PatchOperation, Patch, Version, VersionedContent
   - VersionControlService类

### 测试代码
2. ✅ `backend/tests/test_version_control/` (新目录)
   - conftest.py (pytest配置)
   - test_models.py (数据模型测试)
   - test_create_content.py
   - test_apply_patch.py
   - test_version_retrieval.py
   - test_rollback.py
   - test_branches.py
   - test_version_history.py
   - test_performance.py

### 文档
3. ⬜ `docs/Agent/intermediate-state/Week3_实施记录.md` (可选)
   - 实施过程记录
   - 遇到的问题和解决方案
   - 性能测试结果

---

## 📊 验收标准

### 功能完整性
- [x] 补丁式版本控制完成
- [x] 版本回滚功能正常
- [x] 分支管理功能正常
- [x] 版本历史查询正常

### 性能指标
- [x] 版本创建成功率 100%
- [x] 补丁应用正确率 100%
- [x] 版本回滚耗时 < 200ms
- [x] 存储空间节省 > 80%

### 质量指标
- [x] 单元测试通过
- [x] 测试覆盖率 > 80%
- [x] 代码可正常运行
- [x] 向后兼容(独立模块,不影响现有功能)

---

## 🔍 关键技术点

### 1. 补丁应用顺序
```python
# 从base到target的正确顺序
patches = _collect_patches_to_version(versioned, target_version_id)
content = base_content
for patch in patches:  # 按创建时间顺序应用
    content = _apply_single_patch(content, patch)
```

### 2. 版本树遍历
```python
# 从target回溯到base
path = []
current = target_version
while current.parent_version_id:
    path.append(current)
    current = version_map[current.parent_version_id]

path.reverse()  # 反转得到base -> target的路径
```

### 3. Redis存储
```python
# 键设计
key = f"version:{content_id}"
redis.set(key, versioned.json())

# 读取
data = redis.get(key)
versioned = VersionedContent.parse_raw(data)
```

---

## 💡 最佳实践

### 设计原则
1. **简洁优先**: 保持补丁操作简单(INSERT/DELETE/REPLACE)
2. **类型安全**: 使用Pydantic确保数据正确
3. **独立模块**: 不依赖其他Agent模块,可独立测试
4. **向后兼容**: 不影响现有功能

### 测试策略
1. **先写测试**: 明确需求和边界
2. **覆盖边界**: 测试空内容、大量版本等极端情况
3. **性能基准**: 建立性能基线,防止退化

### 实施建议
1. **Day 1完成数据模型** - 打好基础
2. **Day 2-3完成核心功能** - 保证质量
3. **Day 4完成测试** - 确保可靠
4. **Day 5性能优化** - 达到指标

---

## 🚀 开始检查清单

在开始实施前,请确认:
- [x] 已阅读 `05_版本管理设计.md`
- [x] 理解补丁式版本控制原理
- [x] Redis可用
- [x] 开发环境就绪

**准备开始Week 3开发!** 🎯

---

**文档创建**: 2025-10-31
**状态**: 待开始
