# NovelAIde 项目文档索引

> 📚 **完整文档导航** | 最后更新: 2025-10-28 v2.21

## 📁 文档结构总览

```
docs/
├── 核心文档/ (11个)
│   ├── README.md - 文档总览 ⭐⭐⭐
│   ├── 01-overview.md - 项目概述
│   ├── 02-tech-stack.md - 技术栈规划
│   ├── 03-current-status.md - 当前项目状态 ⭐
│   ├── 04-milestones.md - 开发路线图 🔥
│   ├── 05-tasks.md - 开发任务清单
│   ├── 06-frontend-specs.md - 前端开发规范
│   ├── 07-api-reference.md - API参考文档 🔥
│   ├── 08-deployment.md - 部署运维指南
│   ├── 09-references.md - 参考资源
│   └── core-workflow.md - 核心流程图
├── AI功能文档/ (3个)
│   ├── 14-ai-evaluation-summary.md - AI评价功能总结 ⭐⭐
│   ├── 15-feature-ai-book-breakdown.md - AI拆书功能设计 ⭐⭐ 🔥
│   └── 16-feature-knowledge-base.md - 个人知识库功能设计 ⭐⭐ 🔥
├── 性能优化/ (1个)
│   └── performance-optimization-2025-10-28.md - Redis缓存性能优化 ⭐⭐⭐ 🔥
├── 历史文档/ (archive/)
│   └── 30+ 个已归档的历史文档
└── 索引文档/
    └── DOCS_INDEX.md - 本文档 🔥
```

---

## 🎯 按用途分类

### 新手入门 (必读)

1. **[README.md](./README.md)** - 从这里开始 ⭐⭐⭐
2. **[01-overview.md](./01-overview.md)** - 了解项目背景
3. **[02-tech-stack.md](./02-tech-stack.md)** - 熟悉技术栈
4. **[03-current-status.md](./03-current-status.md)** - 掌握当前进度
5. **[08-deployment.md](./08-deployment.md)** - 搭建开发环境

### 前端开发

**核心文档**:
- [06-frontend-specs.md](./06-frontend-specs.md) - 前端开发规范
- [07-api-reference.md](./07-api-reference.md) - API调用文档

### 后端开发

**核心文档**:
- [02-tech-stack.md](./02-tech-stack.md) - 后端技术栈
- [performance-optimization-2025-10-28.md](./performance-optimization-2025-10-28.md) - 性能优化实践 ⭐⭐⭐

### AI功能开发

**核心AI功能**:
- [14-ai-evaluation-summary.md](./14-ai-evaluation-summary.md) - AI评价功能总结 ⭐⭐
- [15-feature-ai-book-breakdown.md](./15-feature-ai-book-breakdown.md) - AI拆书功能设计 ⭐⭐ 🔥
- [16-feature-knowledge-base.md](./16-feature-knowledge-base.md) - 个人知识库设计 ⭐⭐ 🔥

### 产品规划

- [04-milestones.md](./04-milestones.md) - 开发路线图
- [05-tasks.md](./05-tasks.md) - 任务清单
- [03-current-status.md](./03-current-status.md) - 当前状态

### 运维部署

- [08-deployment.md](./08-deployment.md) - 部署指南

---

## 📊 文档统计

| 分类 | 文档数量 |
|------|---------|
| 核心文档 | 11个 |
| AI功能文档 | 3个 |
| 性能优化 | 1个 |
| 历史归档 | 30+个 |
| **总计** | **15个核心 + 30+归档** |

---

## ⭐ 重点文档标记

| 标记 | 含义 |
|------|------|
| ⭐⭐⭐ | 必读文档 |
| ⭐⭐ | 重要文档 |
| ⭐ | 推荐阅读 |
| 🔥 | 最新更新 |
| 📦 | 已归档 |

---

## 🔄 最近更新

### 2025-10-28 (v2.21) 🔥
- 🔥 **Redis缓存性能优化完成** ⭐⭐⭐
- 🔥 性能提升16.7x (目标3-4x)
- 🔥 支持章节解析、AI分析、向量缓存三级缓存
- 🔥 支持部分缓存命中优化
- 🔥 新增缓存统计监控
- 🔥 新增 performance-optimization-2025-10-28.md
- 📝 大规模文档整理: 30+个历史文档归档
- 📝 核心文档精简至15个

### 2025-10-26 (v2.19)
- 🔥 **知识库MVP后端完成** (Day 4完成) ⭐⭐⭐
- 🔥 7个REST API端点全部实现 ✅
- 🔥 自动化测试100%通过 (9/9) ✅

### 2025-10-26 (v2.18)
- 🔥 **新增Milestone 2.5: 个人知识库 + AI拆书系统** ⭐⭐⭐
- 🔥 新增2个功能设计文档 (15/16)

---

## 📝 文档贡献指南

### 如何更新文档

1. **修改文档** - 直接编辑对应的.md文件
2. **更新版本** - 修改文档顶部的更新日期
3. **更新索引** - 如有新增文档,更新本索引

### 文档规范

- **格式**: Markdown
- **编码**: UTF-8
- **换行**: LF (Unix风格)
- **标题**: 使用中文或英文,保持一致性
- **代码块**: 注明语言类型

---

**维护者**: NovelAIde 团队
**最后更新**: 2025-10-28
**版本**: v2.21
