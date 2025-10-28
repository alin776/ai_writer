# 评审系统性能优化 - 快速参考

## 🎯 优化目标

将作品级评审性能提升**2倍**,并改善用户体验

## 📊 当前状态

### 实测性能 (5章评审)
- **总耗时**: 2分59秒
- **瓶颈**: AI调用串行执行
  - 情节: 31秒
  - 人物: 35秒
  - 世界观: 35秒
  - 文风: 33秒
  - 建议: 45秒

### 推算性能
- 10章: ~6分钟
- 20章: ~12分钟 ❌ 不可接受

---

## 🚀 优化方案 (3天)

### Day 1: 并发优化 ⭐⭐⭐⭐⭐
**任务**: 4个分析器并发执行
**文件**: `backend/app/services/review/book_review_analyzer.py`
**技术**: `asyncio.gather()`
**效果**: 性能提升2x

**核心代码**:
```python
# 并发执行
plot, char, world, style = await asyncio.gather(
    self._analyze_plot_structure(...),
    self._analyze_characters(...),
    self._analyze_worldview(...),
    self._analyze_writing_style(...)
)
```

**预期**: 5章 3分钟 → **1.5分钟**

---

### Day 2上午: 快速模式 ⭐⭐⭐
**任务**: 仅分析情节+人物
**文件**: `backend/app/services/review/book_review_service.py`
**API**: `POST /api/v1/review/books/quick`
**效果**: 1分钟快速评审

**使用场景**:
- 快速预览
- 多作品对比
- 初步筛选

---

### Day 2下午: 进度提示 ⭐⭐⭐⭐
**任务**: SSE实时推送进度
**技术**: Server-Sent Events
**API**:
- `POST /books/async` - 提交任务
- `GET /books/review/{id}/progress` - 监听进度

**前端示例**:
```javascript
const eventSource = new EventSource('/api/v1/review/books/review/{id}/progress')
eventSource.onmessage = (e) => {
  const {progress, step} = JSON.parse(e.data)
  updateUI(progress, step)
}
```

---

### Day 3: 完善和文档
- 错误处理
- API文档
- 集成测试
- 性能总结

---

## 📈 预期成果

| 章节数 | 优化前 | 优化后 | 提升 |
|--------|--------|--------|------|
| 5章 | 3分钟 | **1.5分钟** | 2x |
| 10章 | 6分钟 | **3分钟** | 2x |
| 20章 | 12分钟 | **6分钟** | 2x |
| 快速模式 | - | **1分钟** | 新功能 |

---

## ✅ 执行清单

### Day 1
- [ ] 修改`book_review_analyzer.py`支持并发
- [ ] 添加异常处理和默认值
- [ ] 性能测试验证
- [ ] 更新文档

### Day 2
- [ ] 实现快速评审模式
- [ ] 实现异步任务和进度追踪
- [ ] 实现SSE接口
- [ ] 前端集成示例

### Day 3
- [ ] 完善错误处理
- [ ] 编写API文档
- [ ] 集成测试
- [ ] 性能优化总结

---

## 📝 关键文件

| 文件 | 作用 |
|------|------|
| `backend/app/services/review/book_review_analyzer.py` | 并发执行4个分析器 |
| `backend/app/services/review/book_review_service.py` | 快速模式 + 进度追踪 |
| `backend/app/api/v1/review.py` | API接口 |
| `backend/tests/test_concurrent_performance.py` | 性能测试 |

---

## 🎯 验收标准

- ✅ 5章评审 < 90秒
- ✅ 快速模式 < 60秒
- ✅ SSE进度 < 1秒延迟
- ✅ 加速比 > 2x
- ✅ 错误率 < 1%

---

## 📖 详细文档

完整计划见: `tasks/review_performance_optimization_plan.md`

---

*快速参考 v1.0 - 2025-10-28*
