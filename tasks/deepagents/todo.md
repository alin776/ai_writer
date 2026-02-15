# Preview.html 前端 UI 优化计划

## 设计方向：「墨色月华」
一个融合中国水墨意境的精致暗色主题。深墨色背景搭配翡翠/月光色点缀，营造出"月下执笔"的沉浸写作氛围。与仙侠题材内容相呼应。

## 待办事项

- [x] 1. 字体升级 — 引入 Google Fonts（"Noto Serif SC" 标题 + "LXGW WenKai" 正文 + "JetBrains Mono" 代码），替换 system-ui
- [x] 2. 配色方案 — 从冷蓝调改为墨色暖调：深墨底色 + 翡翠绿/琥珀金 accent 替代蓝色
- [x] 3. 背景氛围 — 添加 CSS 噪点纹理叠加 (SVG feTurbulence) 和微妙径向渐变，增加画面深度
- [x] 4. 页面加载动画 — 三个面板交错淡入 + 上移效果（纯 CSS animation-delay: 0.05s/0.15s/0.25s）
- [x] 5. 左面板精化 — 章节列表 hover/active 状态用翡翠色渐变，数字徽章翡翠渐变，进度条发光效果
- [x] 6. 中间面板精化 — 聊天输入框 focus 发光边框、用户消息琥珀顶部光线、事件组左侧装饰条、strong 标签琥珀色
- [x] 7. 右面板精化 — 编辑器标签页底部翡翠高亮条、diff 行 hover 交互、关闭按钮朱砂色
- [x] 8. 滚动条与细节 — 5px 窄滚动条、翡翠色 selection 选中、面板分隔线渐变淡出效果

## 审核

### 变更总结
仅修改 CSS 样式和 `<head>` 部分（添加 Google Fonts 引用），HTML 结构和 JavaScript 逻辑完全保持不变。

### 核心改动
| 改动项 | 旧 | 新 |
|--------|-----|-----|
| 正文字体 | system-ui / Segoe UI | LXGW WenKai (书法风格) |
| 标题字体 | 同上 | Noto Serif SC (宋体衬线) |
| 代码字体 | SF Mono / Cascadia Code | JetBrains Mono |
| 主色调 | #3b82f6 冷蓝 | #4d9f7f 翡翠绿 |
| 强调色 | 无 | #c9a84e 琥珀金 |
| 文字色 | #f1f5f9 冷白 | #e6ddd0 暖羊皮纸 |
| 删除色 | #ef4444 亮红 | #c4524e 朱砂 |
| 背景 | 纯色 #0c1222 | #090d12 + 噪点纹理 + 径向渐变 |
| 加载动画 | 无 | 三面板交错淡入 (panelReveal) |
| 输入框 | 无 focus 效果 | focus 时翡翠发光边框 |
| 标签页高亮 | 无底线 | 活跃标签页底部翡翠色指示条 |
