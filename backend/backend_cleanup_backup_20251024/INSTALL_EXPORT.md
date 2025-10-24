# 导入导出功能安装说明

## Python 依赖安装

导入导出功能需要安装 `beautifulsoup4` 库用于HTML到Markdown的转换。

### 安装命令

```bash
cd backend
pip install beautifulsoup4
```

或者使用虚拟环境：

```bash
cd backend
.venv/bin/pip install beautifulsoup4   # Linux/Mac
# 或
.venv\Scripts\pip install beautifulsoup4  # Windows
```

### 验证安装

```bash
python -c "import bs4; print('beautifulsoup4已安装')"
```

## 功能测试

### 1. 启动后端

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 测试导出API

```bash
# 导出为JSON
curl -X POST http://localhost:8000/api/v1/works/{work_id}/export \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"format": "json", "includeChapters": true, "includeWorldview": true}'

# 导出为Markdown
curl -X POST http://localhost:8000/api/v1/works/{work_id}/export \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"format": "markdown", "includeChapters": true, "includeWorldview": true}'
```

### 3. 测试导入API

```bash
# 预览导入
curl -X POST http://localhost:8000/api/v1/works/import/preview \
  -H "Authorization: Bearer {token}" \
  -F "file=@export.json" \
  -F "format=json"

# 执行导入
curl -X POST http://localhost:8000/api/v1/works/import \
  -H "Authorization: Bearer {token}" \
  -F "file=@export.json" \
  -F "format=json" \
  -F "create_new=true" \
  -F "include_worldview=true"
```

## 功能说明

### 导出功能

**支持格式**：
- **JSON**: 完整数据备份（作品+章节+世界观+规范+分析）
- **Markdown**: 可读格式（正文+世界观附录）
- **DOCX**: 出版格式（待实现）

**导出内容**：
- ✅ 章节内容（支持选择章节）
- ✅ 世界观数据（人物/地点/设定）
- ✅ 创作规范（作品规范+AI规范）
- ✅ 分析报告（可选）

**临时文件管理**：
- 导出文件保存24小时后自动清理
- 下载链接格式：`/api/v1/downloads/{file_id}`

### 导入功能

**支持格式**：
- **JSON**: 完整导入（自动创建作品和关联数据）
- **TXT/Markdown**: 智能导入（自动分割章节）

**导入选项**：
- ✅ 选择性导入世界观数据
- ✅ 选择性导入创作规范
- ✅ 导入前预览（章节数量、总字数等）

**章节分割规则**：
- 识别 "第X章" 模式
- 识别 "Chapter X" 模式
- 识别 Markdown 标题（##）
- 如无明确标记，将整个文本作为单章导入

## 前端集成

### WorkDetailView（作品详情页）
- 左侧章节树顶部新增"导出作品"按钮
- 点击弹出ExportDialog对话框
- 支持选择导出格式和内容选项

### WorksView（作品列表页）
- 操作栏新增"导入作品"按钮（绿色）
- 点击弹出ImportDialog对话框
- 支持文件上传、预览、确认导入
- 导入成功后自动跳转到新作品

## 注意事项

1. **文件大小限制**：最大50MB
2. **临时文件清理**：建议定期执行清理任务
3. **权限验证**：所有API都需要JWT Token认证
4. **错误处理**：导入失败会自动回滚事务

## 后续优化

- [ ] 添加DOCX导出支持（需要python-docx）
- [ ] 支持批量导出（多个作品）
- [ ] 添加导出进度显示
- [ ] 支持云端备份（阿里云OSS）
