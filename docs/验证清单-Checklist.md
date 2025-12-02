# 缓存系统验证清单

**日期**: 2025-12-02
**目的**: 验证所有修复是否生效
**执行人**: 待定
**状态**: 待测试

---

## 🔐 安全性验证

### 1. 权限绕过漏洞修复验证

#### 测试1: 跨用户访问
```bash
# 场景：用户B尝试访问用户A的数据

# Step 1: 用户A登录，访问自己的角色
curl -X GET "http://localhost:8000/api/v1/worldview/works/{work_id_A}/characters" \
  -H "Authorization: Bearer {token_A}"

# 预期：200 OK，返回角色列表
# ✅ 缓存已保存

# Step 2: 用户B尝试访问work_id_A
curl -X GET "http://localhost:8000/api/v1/worldview/works/{work_id_A}/characters" \
  -H "Authorization: Bearer {token_B}"

# 预期：403 Forbidden
# ✅ 权限验证在缓存检查之前
```

**验证点**：
- [ ] 用户B无法访问用户A的数据
- [ ] 返回403错误
- [ ] 日志显示权限验证失败

#### 测试2-6: 其他4个GET端点
```bash
# 重复测试以下端点：
GET /works/{id}/locations
GET /works/{id}/settings
GET /works/{id}/guidelines
GET /works/{id}/ai-guidelines
```

**验证点**：
- [ ] 所有GET端点都先验证权限
- [ ] 跨用户访问全部被拒绝

---

## 📊 数据一致性验证

### 2. 章节列表缓存失效验证

#### 测试1: 创建章节
```bash
# Step 1: 获取章节列表（缓存）
GET /api/v1/chapters/work/{work_id}
# 返回：3个章节

# Step 2: 创建新章节
POST /api/v1/chapters
{
  "work_id": "{work_id}",
  "title": "第四章",
  "content": "..."
}

# Step 3: 再次获取列表
GET /api/v1/chapters/work/{work_id}

# 预期：返回4个章节（包含新创建的）
```

**验证点**：
- [ ] 创建后立即能看到新章节
- [ ] 缓存已失效

#### 测试2: 更新章节
```bash
# Step 1: 更新章节内容
PUT /api/v1/chapters/{chapter_id}
{
  "title": "第一章（修改）"
}

# Step 2: 获取列表
GET /api/v1/chapters/work/{work_id}

# 预期：章节标题已更新
```

**验证点**：
- [ ] 更新后立即看到修改
- [ ] 缓存已失效

#### 测试3: 删除章节
```bash
# Step 1: 删除章节
DELETE /api/v1/chapters/{chapter_id}

# Step 2: 获取列表
GET /api/v1/chapters/work/{work_id}

# 预期：章节已不存在
```

**验证点**：
- [ ] 删除后立即看不到该章节
- [ ] 缓存已失效

#### 测试4: 章节排序（遗漏修复验证）⭐
```bash
# Step 1: 获取列表（观察当前顺序）
GET /api/v1/chapters/work/{work_id}
# 当前顺序：[A, B, C]

# Step 2: 重新排序
POST /api/v1/chapters/reorder
{
  "work_id": "{work_id}",
  "chapter_ids": ["C", "A", "B"]
}

# Step 3: 再次获取列表
GET /api/v1/chapters/work/{work_id}

# 预期：新顺序 [C, A, B]
```

**验证点**：
- [ ] 排序后立即看到新顺序
- [ ] 缓存已失效 ⭐（遗漏修复点）

#### 测试5: 生成章节概括（遗漏修复验证）⭐
```bash
# Step 1: 生成概括
POST /api/v1/chapters/{chapter_id}/summary
{
  "regenerate": true
}

# Step 2: 获取列表
GET /api/v1/chapters/work/{work_id}

# 预期：章节对象包含新生成的summary字段
```

**验证点**：
- [ ] 生成后立即能看到summary
- [ ] 缓存已失效 ⭐（遗漏修复点）

---

### 3. 世界观数据缓存失效验证

#### 测试1: 角色CRUD
```bash
# 创建角色
POST /api/v1/worldview/characters
GET /api/v1/worldview/works/{id}/characters
# 预期：立即看到新角色

# 更新角色
PUT /api/v1/worldview/characters/{id}
GET /api/v1/worldview/works/{id}/characters
# 预期：立即看到修改

# 删除角色
DELETE /api/v1/worldview/characters/{id}
GET /api/v1/worldview/works/{id}/characters
# 预期：立即看不到该角色
```

**验证点**：
- [ ] 创建后立即可见
- [ ] 更新后立即可见
- [ ] 删除后立即不可见

#### 测试2-4: 地点、设定、规范
```bash
# 重复测试：
- locations CRUD
- settings CRUD
- guidelines CRUD
- ai-guidelines CRUD
```

**验证点**：
- [ ] 所有写操作后缓存立即失效

---

### 4. 聚合缓存失效验证 ⭐

#### 测试1: 角色变更 → worlddata失效
```bash
# Step 1: 获取完整世界观（缓存）
GET /api/v1/worldview/works/{id}/worlddata
# 返回：{characters: [A, B], locations: [X, Y], ...}

# Step 2: 创建新角色C
POST /api/v1/worldview/characters
{
  "name": "角色C"
}

# Step 3: 再次获取worlddata
GET /api/v1/worldview/works/{id}/worlddata

# 预期：返回 {characters: [A, B, C], ...}
```

**验证点**：
- [ ] 创建角色后，worlddata立即包含新角色 ⭐
- [ ] 级联失效机制生效

#### 测试2-4: 其他数据变更
```bash
# 测试：
- 创建地点 → worlddata包含新地点
- 创建设定 → worlddata包含新设定
- 更新规范 → worlddata包含新规范
```

**验证点**：
- [ ] 所有子数据变更后，worlddata都失效 ⭐

---

## ⚡ 性能验证

### 5. 缓存命中率验证

#### 测试1: 章节列表缓存
```bash
# Step 1: 首次请求（缓存未命中）
GET /api/v1/chapters/work/{work_id}
# 观察日志：⚠️ [GET chapters] 缓存未命中
# 响应时间：~50ms

# Step 2: 第二次请求（缓存命中）
GET /api/v1/chapters/work/{work_id}
# 观察日志：✅ [GET chapters] 缓存命中
# 响应时间：~5ms

# Step 3: 60秒后（缓存过期）
sleep 61
GET /api/v1/chapters/work/{work_id}
# 观察日志：⚠️ [GET chapters] 缓存未命中
```

**验证点**：
- [ ] 第一次查询缓存未命中
- [ ] 第二次查询缓存命中
- [ ] 缓存TTL=60秒生效
- [ ] 响应时间提升明显

#### 测试2: 世界观数据缓存
```bash
# 测试：
GET /works/{id}/characters (TTL=300s)
GET /works/{id}/locations (TTL=300s)
GET /works/{id}/settings (TTL=300s)
GET /works/{id}/guidelines (TTL=300s)
GET /works/{id}/ai-guidelines (TTL=300s)
```

**验证点**：
- [ ] TTL=300秒（5分钟）
- [ ] 缓存命中时响应快

#### 测试3: worlddata聚合端点 ⭐
```bash
# Step 1: 首次请求（4次DB查询）
GET /api/v1/worldview/works/{id}/worlddata
# 响应时间：~120ms

# Step 2: 第二次请求（缓存命中）
GET /api/v1/worldview/works/{id}/worlddata
# 响应时间：~10ms

# 预期：性能提升 90%+
```

**验证点**：
- [ ] 缓存生效 ⭐
- [ ] 响应时间显著降低
- [ ] 减少4次数据库查询

---

## 🛡️ 稳定性验证

### 6. Redis降级验证

#### 测试1: Redis不可用
```bash
# Step 1: 停止Redis
docker stop redis

# Step 2: 请求数据
GET /api/v1/chapters/work/{work_id}

# 预期：
# - 请求正常返回（从数据库查询）
# - 日志：[缓存装饰器] Redis不可用,直接执行函数
```

**验证点**：
- [ ] 请求不受影响
- [ ] 降级到数据库查询
- [ ] 有警告日志

#### 测试2: Redis恢复
```bash
# Step 1: 启动Redis
docker start redis

# Step 2: 请求数据
GET /api/v1/chapters/work/{work_id}

# 预期：
# - 缓存功能恢复
# - 日志：💾 [Worldview] 缓存已保存
```

**验证点**：
- [ ] 缓存自动恢复
- [ ] 无需重启服务

---

### 7. 序列化稳定性验证

#### 测试1: 空列表
```bash
# Step 1: 查询一个没有角色的作品
GET /api/v1/worldview/works/{empty_work_id}/characters

# 预期：
# - 返回 {total: 0, items: []}
# - 不会报错（IndexError）
```

**验证点**：
- [ ] 空列表不报错 ⭐
- [ ] 正常返回空数组

#### 测试2: Pydantic版本兼容
```bash
# 检查日志，确认：
# - 使用 model_dump() 或 dict()
# - 无序列化错误
```

**验证点**：
- [ ] 无序列化异常
- [ ] 日志无ERROR

---

## 📝 日志验证

### 8. 缓存日志完整性

#### 检查项：
```bash
# 查看后端日志，应包含：

# 缓存命中
✅ [Worldview] 缓存命中: worldview:characters:{work_id}

# 缓存未命中
⚠️ [Worldview] 缓存未命中: worldview:characters:{work_id}

# 缓存保存
💾 [Worldview] 缓存已保存: worldview:characters:{work_id} (expire=300s)

# 缓存失效
🗑️ [Worldview] 缓存已失效: worldview:characters:{work_id}

# 聚合缓存失效
🗑️ [Worldview] 聚合缓存已失效: worldview:worlddata:{work_id}

# 章节缓存失效
🗑️ [Chapters] 缓存已失效: chapters:work:{work_id}
```

**验证点**：
- [ ] 所有缓存操作都有日志
- [ ] 日志包含完整信息
- [ ] Emoji标记清晰

---

## ✅ 总体验证清单

### 必须验证（P0）
- [ ] 1. 权限绕过漏洞已修复（5个GET端点）
- [ ] 2. 章节CRUD缓存失效（3个端点）
- [ ] 3. 章节排序缓存失效 ⭐（遗漏修复）
- [ ] 4. 章节概括缓存失效 ⭐（遗漏修复）
- [ ] 5. 世界观CRUD缓存失效（13个端点）
- [ ] 6. worlddata聚合缓存失效 ⭐（级联机制）
- [ ] 7. Redis降级正常

### 推荐验证（P1）
- [ ] 8. 缓存命中率符合预期（70-90%）
- [ ] 9. 响应时间显著提升
- [ ] 10. 空列表不报错
- [ ] 11. 日志完整清晰

### 可选验证（P2）
- [ ] 12. worlddata性能优化生效 ⭐
- [ ] 13. 并发场景测试
- [ ] 14. 压力测试

---

## 📋 执行记录

| 测试项 | 执行日期 | 执行人 | 结果 | 备注 |
|--------|---------|--------|------|------|
| 权限绕过漏洞 | | | | |
| 章节CRUD缓存 | | | | |
| 章节排序缓存 | | | | ⭐ 遗漏修复点 |
| 章节概括缓存 | | | | ⭐ 遗漏修复点 |
| 世界观CRUD缓存 | | | | |
| worlddata缓存 | | | | ⭐ 新增优化 |
| Redis降级 | | | | |
| 性能测试 | | | | |

---

## 🚨 发现问题记录

| 日期 | 问题描述 | 严重性 | 状态 | 负责人 |
|------|---------|--------|------|--------|
| | | | | |

---

**创建时间**: 2025-12-02
**版本**: V1.0
**状态**: 待执行
