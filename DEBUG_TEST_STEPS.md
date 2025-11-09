# Debug测试步骤

## 🎯 目标
确认后端是否发送progress事件，前端是否接收到

## ✅ 步骤1：重启后端
```bash
# 停止当前后端（Ctrl+C）
# 重新启动
cd D:\Java\ai_writer\backend
python -m uvicorn app.main:app --reload
```

## ✅ 步骤2：打开前端
前端已经在运行：http://localhost:5174/

## ✅ 步骤3：打开浏览器控制台
F12 → Console（清空旧日志）

## ✅ 步骤4：切换到ReAct模式
1. 点击 `∞` 按钮
2. 选择 **⚡ ReAct**
3. 确认看到 ✓ 标记

## ✅ 步骤5：发送测试消息
输入：`你好`（简单消息，快速测试）

## 🔍 步骤6：检查日志

### **前端日志（浏览器控制台）**
应该看到：
```
🟢 [API] 收到 progress 事件: {type: "progress", step: "intent_analysis", ...}
🔵 [DEBUG] onProgress 被调用了！ {type: "progress", ...}
🔵 [DEBUG] progress.step = intent_analysis
🔵 [DEBUG] 创建的 activity = {id: "...", type: "intent_analysis", ...}
🔵 [DEBUG] 更新后的 activities 数组长度 = 1
```

如果看到这些日志，说明前端接收到了事件！

### **后端日志（终端）**
应该看到：
```
[Stream Event] 节点: intent_classifier
[Stream Event] progress_event = {'type': 'progress', 'step': 'intent_analysis', ...}
[Stream Event] on_progress 回调已调用
```

如果看到这些日志，说明后端正确发送了事件！

## 🐛 问题诊断

### **情况1：后端有日志，前端没有日志**
**原因**：SSE传输问题
**解决**：检查 `agent.py` 中的事件队列发送逻辑

### **情况2：后端没有日志**
**原因**：`_parse_node_event()` 返回了 None
**解决**：检查节点映射表是否覆盖了所有节点

### **情况3：前端有日志，但界面没显示**
**原因**：ActivityStream 组件渲染问题
**解决**：检查 `activities.length > 0` 条件

## 📝 请提供

测试后，请提供：
1. **后端终端完整日志**（从发送消息到完成）
2. **前端控制台截图**（显示所有 🟢 🔵 标记的日志）
3. **界面截图**（显示是否有ActivityStream）

我会根据这些信息进一步诊断！
