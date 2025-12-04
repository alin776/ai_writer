- 已完成 humanize 系列文档复审与修订，清理了乱码/emoji。
- 关键修复：路由示例与现有 AuthLayout 结构对齐；侧边栏菜单位置明确；补充 showToast 依赖说明；部署指南改为复用 src/utils/formatDate.ts；提醒按后端前缀配置 VITE_API_BASE_URL。
- 详细说明见 docs/humanize/REVIEW_REPORT.md。
21:43:30 app.services.ai.http_ai_service INFO   API 响应完成，共接收 31 个数据块，总长度: 4607
21:43:30 app.services.ai.http_ai_service INFO   流式响应Token统计: 6662 (prompt=4635, completion=2027)
21:43:30 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
21:43:30 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=6662, cost=$0.026064, time=23479ms
21:43:30 app.services.redis_cache_service INFO   ✓ 结果已缓存: novel_analysis:v2:micro:6a55fa4c... (TTL: 604800秒)
21:43:30 app.services.ai.novel_micro_analysis INFO   章节 6481bdc8-3657-4aca-a638-af31744a57cf 分析成功，提取事件数: 6
21:43:30 app.services.ai.novel_analysis_orchestrator INFO   [1/1] ✓ 分析完成: 百年关，天机变 (24.1秒)
21:43:30 app.services.ai.novel_analysis_orchestrator INFO   ⚡ 并行分析完成: 成功 1/1 章
21:43:30 app.services.ai.novel_analysis_orchestrator INFO   💾 开始批量保存 1 个分析结果...
21:43:30 app.services.novel_analysis_service INFO   Batch saved 1 micro results for analysis bc6a3696-335c-4ba9-960a-ef48e5659f7f, total: 1
21:43:30 app.services.ai.novel_analysis_orchestrator INFO   ✅ 批量保存完成: 1 个结果
21:43:30 app.services.ai.novel_analysis_orchestrator INFO   🔍 开始批量存储向量...
21:43:30 app.services.vector_store_service INFO   开始向量化章节 6481bdc8-3657-4aca-a638-af31744a57cf 的微观分析数据
21:43:30 app.services.vector_store_service INFO   生成向量维度: 384
21:43:30 app.services.vector_store_service INFO   向量存储成功: vector_id=10b6829b-802a-4c1d-b5c0-fe377c312c4e
21:43:30 app.services.ai.novel_analysis_orchestrator INFO   ✅ 批量向量存储完成
21:43:30 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
21:43:30 app.services.ai.novel_analysis_orchestrator INFO   微观分析完成统计:
21:43:30 app.services.ai.novel_analysis_orchestrator INFO     成功: 1/1 章节 (100.0%)
21:43:30 app.services.ai.novel_analysis_orchestrator INFO     失败: 0 章节
21:43:30 app.services.ai.novel_analysis_orchestrator INFO     总耗时: 27.2秒 (平均 27.2秒/章)
21:43:30 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
21:43:30 app.services.novel_analysis_service INFO   Updated analysis bc6a3696-335c-4ba9-960a-ef48e5659f7f progress: 1/1, stage: AnalysisStage.MACRO_ANALYSIS, status: None
21:43:30 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
21:43:30 app.services.ai.novel_analysis_orchestrator INFO   开始宏观分析...
21:43:30 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
21:43:30 app.services.ai.novel_macro_analysis INFO   开始宏观分析，共 1 个章节的数据，6 个事件
21:43:30 app.services.ai.novel_macro_analysis INFO   第 1/3 次尝试调用AI宏观分析
21:43:30 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
21:43:30 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
21:43:30 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=6000, temp=0.5, task_type=TaskType.SUMMARIZATION
INFO:     127.0.0.1:62074 - "OPTIONS /api/v1/humanize/rewrite/stream HTTP/1.1" 200 OK
21:43:33 app.api.v1.humanize ERROR   流式去痕迹失败: NameError: name 'HTTPAIService' is not defined
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\api\v1\humanize.py", line 652, in generate
    ai_service = HTTPAIService(user_id=str(current_user.id))
                 ^^^^^^^^^^^^^
NameError: name 'HTTPAIService' is not defined
21:43:33 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite/stream
INFO:     127.0.0.1:50402 - "POST /api/v1/humanize/rewrite/stream HTTP/1.1" 200 OK
21:43:34 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:43:41 app.services.ai.http_ai_service INFO   API 响应完成，共接收 18 个数据块，总长度: 1073
21:43:41 app.services.ai.http_ai_service INFO   流式响应Token统计: 4069 (prompt=3228, completion=841)
21:43:41 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
21:43:41 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=4069, cost=$0.012445, time=10709ms
21:43:41 app.services.ai.novel_macro_analysis INFO   宏观分析完成，报告长度: 1073 字符
21:43:41 app.services.ai.novel_analysis_orchestrator INFO   宏观分析完成，报告长度: 1073 字符，耗时: 10.7秒
21:43:41 app.services.novel_analysis_service INFO   Saved macro result for analysis bc6a3696-335c-4ba9-960a-ef48e5659f7f, marked as completed
21:43:41 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
21:43:41 app.services.ai.novel_analysis_orchestrator INFO   作品 9398f47b-1e74-4e1c-93dd-e837e51dbaaf 分析全部完成！
21:43:41 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
21:43:41 app.services.ai.novel_analysis_orchestrator INFO   📊 分析统计:
21:43:41 app.services.ai.novel_analysis_orchestrator INFO     微观分析: 1/1 章 (成功率 100.0%)
21:43:41 app.services.ai.novel_analysis_orchestrator INFO     宏观报告: 1073 字符
21:43:41 app.services.ai.novel_analysis_orchestrator INFO     总耗时: 38.0秒 (0.6分钟)
21:43:41 app.services.ai.novel_analysis_orchestrator INFO     平均速度: 38.0秒/章
21:43:41 app.services.ai.novel_analysis_orchestrator INFO     向量存储: 1 条，覆盖 1 章
21:43:41 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
21:43:41 app.services.ai.novel_analysis_orchestrator INFO   AI服务资源已清理
21:43:41 app.services.ai.novel_analysis_orchestrator INFO   AI服务资源已清理
21:43:41 app.api.v1.novel_analysis INFO   后台任务完成：作品 9398f47b-1e74-4e1c-93dd-e837e51dbaaf 分析成功