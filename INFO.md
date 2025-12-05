• 发现的问题

  - High — 导入向量化在请求内同步执行：import_service 现在在 JSON/TXT/MD 导入后逐章调用
    ChapterVectorService.store_chapter_vector，每章都会跑 sentence-transformers、分段、存库并 commit。大作品（多章
    或长章）导入会被完全阻塞，容易拖超请求/网关超时；与章节 API 的后台任务风格不一致。
  - Medium — 章节向量分块无上限：ChapterVectorService._split_content 按句 + 500 字符切片，没有 chunk 上限或大小动
    态调整；10MB 文本可能产生上千块，embedding/内存/数据库压力无法控制。
  - Low — 新的 10MB 文本上限和 UTF-8 限制尚未同步到前端提示，用户可能仍尝试大文件或其他编码，体验落差。

  已解决/效果

  - 导入时携带 create_new=true + work_id 会 400 拒绝，避免误追加。
  - 导入章节内容保持纯文本（不再拼接 HTML），降低未清洗内容的风险。
  - 删除章节时会顺带删除章节向量，避免悬挂数据。
  - 导入的章节现在会生成向量（>100 字符），Agent 的章节 RAG 能覆盖导入内容。

  建议后续修正

  1. 将导入的章节向量化改成后台任务或队列（类似 chapters.py 的 BackgroundTasks），导入接口先返回，再异步生成向量；
     必要时在响应中返回“向量化已排队”标志。
  2. 给 ChapterVectorService._split_content 增加 chunk 上限或自适应分块逻辑，避免极端长文本生成过多向量；超限时返
     回 warning 或拒绝导入。
  3. 前端 ImportDialog 增加 “TXT/MD 最大 10MB，需 UTF-8 编码” 文案，降低失败率。