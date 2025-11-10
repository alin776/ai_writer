(venv) PS D:\Java\ai_writer\backend> python -m tests.test_connection_leak
12:06:42 __main__ INFO
================================================================================
12:06:42 __main__ INFO   ReAct 模式工具连接泄漏测试
12:06:42 __main__ INFO   ================================================================================

12:06:42 __main__ INFO
============================================================
12:06:42 __main__ INFO   测试工具: read_chapter_tool
12:06:42 __main__ INFO   测试次数: 50
12:06:42 __main__ INFO   ============================================================

12:06:42 __main__ INFO   初始连接池状态: {'total': 10, 'checked_out': 0, 'available': 10}
12:06:42 __main__ INFO   进度: 20/50, 成功: 20, 失败: 0, 连接池: {'total': 10, 'checked_out': 0, 'available': 10}
12:06:42 __main__ INFO   进度: 40/50, 成功: 40, 失败: 0, 连接池: {'total': 10, 'checked_out': 0, 'available': 10}
12:06:45 __main__ INFO
最终连接池状态: {'total': 10, 'checked_out': 0, 'available': 10}
12:06:45 __main__ INFO   ✅ read_chapter_tool - 连接泄漏已修复！
12:06:45 __main__ INFO
============================================================
12:06:45 __main__ INFO   测试工具: get_chapter_by_order_tool
12:06:45 __main__ INFO   测试次数: 50
12:06:45 __main__ INFO   ============================================================

12:06:45 __main__ INFO   初始连接池状态: {'total': 10, 'checked_out': 0, 'available': 10}
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 __main__ INFO   进度: 20/50, 成功: 20, 失败: 0, 连接池: {'total': 10, 'checked_out': 0, 'available': 10}
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 __main__ INFO   进度: 40/50, 成功: 40, 失败: 0, 连接池: {'total': 10, 'checked_out': 0, 'available': 10}
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:06:47 __main__ INFO
最终连接池状态: {'total': 10, 'checked_out': 0, 'available': 10}
12:06:47 __main__ INFO   ✅ get_chapter_by_order_tool - 连接泄漏已修复！
12:06:47 __main__ INFO
============================================================
12:06:47 __main__ INFO   测试工具: search_analysis_fragments_tool
12:06:47 __main__ INFO   测试次数: 50
12:06:47 __main__ INFO   ============================================================

12:06:47 __main__ INFO   初始连接池状态: {'total': 10, 'checked_out': 0, 'available': 10}
12:06:50 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:06:50 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:06:50 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:06:50 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:06:58 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  4.81it/s]
12:06:58 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:06:58 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:06:58 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:06:58 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:06:58 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:06:58 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:07:05 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 63.49it/s]
12:07:05 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:07:05 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:07:05 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:07:05 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:07:05 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:07:05 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:07:13 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 31.75it/s]
12:07:13 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:07:13 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:07:13 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:07:13 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:07:13 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:07:13 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:07:20 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 12.56it/s]
12:07:20 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:07:20 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:07:20 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:07:20 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:07:20 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:07:20 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:07:28 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.27it/s]
12:07:29 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:07:29 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:07:29 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:07:29 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:07:29 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:07:29 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:07:36 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 24.09it/s]
12:07:36 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:07:36 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:07:36 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:07:36 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:07:36 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:07:36 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:07:43 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 23.69it/s]
12:07:43 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:07:43 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:07:43 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:07:43 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:07:43 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:07:43 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:07:51 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 13.49it/s]
12:07:51 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:07:51 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:07:51 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:07:51 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:07:51 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:07:51 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:07:59 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.63it/s]
12:07:59 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:07:59 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:07:59 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:07:59 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:07:59 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:07:59 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:08:07 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 11.72it/s]
12:08:07 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:08:07 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:08:07 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:08:07 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:08:07 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:08:07 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:08:15 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 11.59it/s]
12:08:15 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:08:15 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:08:15 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:08:15 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:08:15 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:08:15 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:08:23 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 16.87it/s]
12:08:23 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:08:23 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:08:23 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:08:23 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:08:23 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:08:23 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:08:30 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 13.78it/s]
12:08:30 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:08:30 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:08:30 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:08:30 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:08:30 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:08:30 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:08:37 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 13.85it/s]
12:08:37 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:08:37 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:08:37 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:08:37 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:08:37 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:08:37 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:08:44 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 13.69it/s]
12:08:44 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:08:44 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:08:44 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:08:44 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:08:44 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:08:44 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:08:52 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.97it/s]
12:08:52 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:08:52 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:08:52 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:08:52 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:08:52 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:08:52 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:09:01 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 13.71it/s]
12:09:01 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:09:01 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:09:01 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:09:01 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:09:01 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:09:01 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:09:09 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  4.69it/s]
12:09:09 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:09:09 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:09:09 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:09:09 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:09:09 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:09:09 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:09:17 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.51it/s]
12:09:17 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:09:17 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:09:17 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:09:17 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:09:17 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:09:17 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:09:25 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.38it/s]
12:09:25 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:09:25 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:09:25 __main__ INFO   进度: 20/50, 成功: 20, 失败: 0, 连接池: {'total': 10, 'checked_out': 0, 'available': 10}
12:09:25 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:09:25 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:09:25 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:09:25 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:09:34 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.93it/s]
12:09:34 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:09:34 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:09:34 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:09:34 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:09:34 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:09:34 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:09:42 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.39it/s]
12:09:42 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:09:42 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:09:42 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:09:42 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:09:42 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:09:42 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:09:49 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 21.11it/s]
12:09:49 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:09:49 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:09:49 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:09:49 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:09:49 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:09:49 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:09:56 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 13.71it/s]
12:09:56 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:09:56 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:09:56 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:09:56 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:09:56 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:09:56 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:10:03 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 17.27it/s]
12:10:03 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:10:03 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:10:03 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:10:03 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:10:03 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:10:03 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:10:10 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 14.27it/s]
12:10:10 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:10:10 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:10:10 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:10:10 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:10:10 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:10:10 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:10:18 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.67it/s]
12:10:18 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:10:18 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:10:18 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:10:18 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:10:18 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:10:18 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:10:27 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 10.39it/s]
12:10:27 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:10:27 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:10:27 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:10:27 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:10:27 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:10:27 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:10:36 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.98it/s]
12:10:36 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:10:36 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:10:36 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:10:36 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:10:36 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:10:36 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:10:45 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.02it/s]
12:10:45 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:10:45 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:10:45 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:10:45 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:10:45 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:10:45 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:10:53 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 13.38it/s]
12:10:53 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:10:53 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:10:53 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:10:53 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:10:53 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:10:53 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:11:01 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 11.13it/s]
12:11:01 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:11:01 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:11:01 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:11:01 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:11:01 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:11:01 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:11:09 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.48it/s]
12:11:09 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:11:09 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:11:09 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:11:09 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:11:09 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:11:09 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:11:17 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 11.99it/s]
12:11:17 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:11:17 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:11:17 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:11:17 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:11:17 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:11:17 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:11:26 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.91it/s]
12:11:26 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:11:26 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:11:26 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:11:26 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:11:26 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:11:26 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:11:34 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.47it/s]
12:11:34 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:11:34 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:11:34 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:11:34 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:11:34 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:11:34 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:11:42 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 12.02it/s]
12:11:43 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:11:43 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:11:43 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:11:43 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:11:43 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:11:43 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:11:51 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  9.97it/s]
12:11:51 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:11:51 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:11:51 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:11:51 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:11:51 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:11:51 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:11:59 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  5.69it/s]
12:11:59 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:11:59 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:11:59 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:11:59 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:11:59 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:11:59 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:12:07 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  5.53it/s]
12:12:07 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:12:07 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:12:07 __main__ INFO   进度: 40/50, 成功: 40, 失败: 0, 连接池: {'total': 10, 'checked_out': 0, 'available': 10}
12:12:07 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:12:07 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:12:07 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:12:07 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:12:15 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  9.26it/s]
12:12:16 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:12:16 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:12:16 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:12:16 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:12:16 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:12:16 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:12:24 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.17it/s]
12:12:24 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:12:24 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:12:24 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:12:24 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:12:24 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:12:24 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:12:34 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 10.03it/s]
12:12:34 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:12:34 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:12:34 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:12:34 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:12:34 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:12:34 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:12:43 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 10.51it/s]
12:12:43 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:12:43 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:12:43 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:12:43 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:12:43 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:12:43 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:12:51 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.10it/s]
12:12:51 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:12:51 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:12:51 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:12:51 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:12:51 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:12:51 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:12:59 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.85it/s]
12:13:00 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:13:00 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:13:00 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:13:00 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:13:00 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:13:00 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:13:07 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.17it/s]
12:13:07 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:13:07 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:13:07 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:13:07 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:13:07 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:13:07 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:13:15 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 17.14it/s]
12:13:15 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:13:15 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:13:15 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:13:15 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:13:15 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:13:15 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:13:23 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.19it/s]
12:13:23 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:13:23 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:13:23 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=测试查询...
12:13:23 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:13:23 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:13:23 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:13:31 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 13.61it/s]
12:13:31 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:13:31 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:13:33 __main__ INFO
最终连接池状态: {'total': 10, 'checked_out': 0, 'available': 10}
12:13:33 __main__ INFO   ✅ search_analysis_fragments_tool - 连接泄漏已修复！
12:13:33 __main__ INFO
============================================================
12:13:33 __main__ INFO   测试工具: get_context_tool
12:13:33 __main__ INFO   测试次数: 50
12:13:33 __main__ INFO   ============================================================

12:13:33 __main__ INFO   初始连接池状态: {'total': 10, 'checked_out': 0, 'available': 10}
12:13:33 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:13:33 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:13:33 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:13:33 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:13:33 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:13:41 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.04it/s]
12:13:41 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:13:41 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:13:41 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:13:41 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:13:41 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:13:41 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:13:41 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:14:23 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.79it/s]
12:14:23 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:14:23 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:14:23 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:14:23 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:14:23 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:14:23 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:14:23 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:14:31 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.61it/s]
12:14:32 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:14:32 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:14:32 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:14:32 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:14:32 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:14:32 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:14:32 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:14:40 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 10.53it/s]
12:14:40 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:14:40 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:14:40 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:14:40 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:14:40 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:14:40 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:14:40 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:14:48 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.88it/s]
12:14:48 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:14:48 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:14:48 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:14:48 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:14:48 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:14:48 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:14:48 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:14:57 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.28it/s]
12:14:57 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:14:57 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:14:57 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:14:57 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:14:57 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:14:57 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:14:57 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:15:05 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.38it/s]
12:15:05 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:15:05 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:15:05 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:15:05 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:15:05 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:15:05 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:15:05 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:15:13 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.22it/s]
12:15:14 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:15:14 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:15:14 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:15:14 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:15:14 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:15:14 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:15:14 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:15:22 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.75it/s]
12:15:22 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:15:22 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:15:22 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:15:22 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:15:22 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:15:22 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:15:22 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:15:29 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.42it/s]
12:15:29 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:15:29 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:15:29 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:15:29 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:15:29 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:15:29 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:15:29 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:15:37 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  9.62it/s]
12:15:38 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:15:38 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:15:38 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:15:38 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:15:38 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:15:38 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:15:38 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:15:45 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 16.24it/s]
12:15:45 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:15:45 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:15:45 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:15:45 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:15:45 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:15:45 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:15:45 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:15:52 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 21.21it/s]
12:15:52 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:15:52 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:15:52 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:15:52 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:15:52 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:15:52 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:15:52 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:15:59 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 30.73it/s]
12:15:59 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:15:59 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:15:59 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:15:59 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:15:59 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:15:59 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:15:59 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:16:06 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.99it/s]
12:16:07 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:16:07 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:16:07 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:16:07 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:16:07 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:16:07 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:16:07 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:16:14 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  9.73it/s]
12:16:15 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:16:15 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:16:15 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:16:15 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:16:15 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:16:15 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:16:15 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:16:22 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 11.31it/s]
12:16:22 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:16:22 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:16:22 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:16:22 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:16:22 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:16:22 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:16:22 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:16:30 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 10.31it/s]
12:16:30 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:16:30 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:16:30 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:16:30 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:16:30 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:16:30 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:16:30 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:16:44 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.56it/s]
12:16:44 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:16:44 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:16:44 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:16:44 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:16:44 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:16:44 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:16:44 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:16:52 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  9.02it/s]
12:16:52 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:16:52 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:16:52 __main__ INFO   进度: 20/50, 成功: 20, 失败: 0, 连接池: {'total': 10, 'checked_out': 0, 'available': 10}
12:16:52 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:16:52 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:16:52 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:16:52 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:16:52 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:17:00 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.19it/s]
12:17:00 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:17:00 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:17:00 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:17:00 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:17:00 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:17:00 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:17:00 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:17:08 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.34it/s]
12:17:08 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:17:08 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:17:08 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:17:08 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:17:08 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:17:08 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:17:08 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:17:15 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  4.96it/s]
12:17:16 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:17:16 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:17:16 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:17:16 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:17:16 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:17:16 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:17:16 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:17:23 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.57it/s]
12:17:24 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:17:24 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:17:24 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:17:24 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:17:24 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:17:24 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:17:24 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:17:31 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.38it/s]
12:17:31 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:17:31 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:17:31 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:17:31 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:17:31 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:17:31 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:17:31 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:17:39 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 10.99it/s]
12:17:39 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:17:39 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:17:39 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:17:39 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:17:39 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:17:39 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:17:39 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:17:46 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.85it/s]
12:17:47 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:17:47 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:17:47 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:17:47 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:17:47 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:17:47 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:17:47 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:17:54 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.86it/s]
12:17:54 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:17:54 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:17:54 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:17:54 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:17:54 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:17:54 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:17:54 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:18:02 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  5.59it/s]
12:18:02 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:18:02 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:18:02 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:18:02 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:18:02 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:18:02 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:18:02 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:18:10 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  5.23it/s]
12:18:10 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:18:10 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:18:10 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:18:10 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:18:10 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:18:10 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:18:10 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:18:18 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  4.99it/s]
12:18:18 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:18:18 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:18:18 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:18:18 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:18:18 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:18:18 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:18:18 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:18:26 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.57it/s]
12:18:26 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:18:26 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:18:26 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:18:26 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:18:26 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:18:26 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:18:26 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:18:34 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.12it/s]
12:18:34 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:18:34 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:18:34 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:18:34 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:18:34 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:18:34 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:18:34 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:18:42 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.79it/s]
12:18:42 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:18:42 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:18:42 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:18:42 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:18:42 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:18:42 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:18:42 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:18:50 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.84it/s]
12:18:50 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:18:50 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:18:50 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:18:50 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:18:50 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:18:50 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:18:50 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:18:58 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.97it/s]
12:18:58 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:18:58 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:18:58 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:18:58 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:18:58 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:18:58 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:18:58 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:19:06 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.63it/s]
12:19:06 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:19:06 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:19:06 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:19:06 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:19:06 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:19:06 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:19:06 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:19:13 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.63it/s]
12:19:13 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:19:13 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:19:13 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:19:13 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:19:13 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:19:13 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:19:13 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:19:21 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.87it/s]
12:19:21 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:19:21 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:19:21 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:19:21 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:19:21 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:19:21 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:19:21 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:19:29 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.09it/s]
12:19:29 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:19:29 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:19:29 __main__ INFO   进度: 40/50, 成功: 40, 失败: 0, 连接池: {'total': 10, 'checked_out': 0, 'available': 10}
12:19:29 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:19:29 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:19:29 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:19:29 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:19:29 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:19:36 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 21.10it/s]
12:19:36 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:19:36 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:19:36 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:19:36 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:19:36 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:19:36 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:19:36 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:19:43 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 15.80it/s]
12:19:43 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:19:43 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:19:43 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:19:43 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:19:43 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:19:43 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:19:43 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:19:50 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 13.06it/s]
12:19:50 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:19:50 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:19:50 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:19:50 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:19:50 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:19:50 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:19:50 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:19:58 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.14it/s]
12:19:58 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:19:58 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:19:58 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:19:58 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:19:58 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:19:58 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:19:58 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:20:06 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.29it/s]
12:20:07 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:20:07 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:20:07 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:20:07 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:20:07 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:20:07 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:20:07 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:20:15 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.58it/s]
12:20:15 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:20:15 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:20:15 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:20:15 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:20:15 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:20:15 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:20:15 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:20:23 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.97it/s]
12:20:23 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:20:23 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:20:23 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:20:23 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:20:23 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:20:23 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:20:23 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:20:31 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.06it/s]
12:20:31 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:20:31 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:20:31 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:20:31 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:20:31 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:20:31 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:20:31 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:20:39 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  5.44it/s]
12:20:40 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:20:40 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:20:40 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:20:40 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:20:40 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:20:40 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:20:40 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:20:47 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.09it/s]
12:20:48 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:20:48 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:20:50 __main__ INFO
最终连接池状态: {'total': 10, 'checked_out': 0, 'available': 10}
12:20:50 __main__ INFO   ✅ get_context_tool - 连接泄漏已修复！
12:20:50 __main__ INFO
================================================================================
12:20:50 __main__ INFO   测试总结
12:20:50 __main__ INFO   ================================================================================
12:20:50 __main__ INFO   ✅ read_chapter_tool: 通过
12:20:50 __main__ INFO   ✅ get_chapter_by_order_tool: 通过
12:20:50 __main__ INFO   ✅ search_analysis_fragments_tool: 通过
12:20:50 __main__ INFO   ✅ get_context_tool: 通过
12:20:50 __main__ INFO
总计: 4 通过, 0 失败, 0 未知
12:20:50 __main__ INFO
🎉 所有测试通过！连接泄漏已修复！
12:20:50 __main__ INFO
================================================================================
12:20:50 __main__ INFO   压力测试：100 个并发工具调用
12:20:50 __main__ INFO   ================================================================================

12:20:50 __main__ INFO   初始连接池: {'total': 10, 'checked_out': 0, 'available': 10}
12:20:50 __main__ INFO   开始执行 100 个并发任务...
12:20:50 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:20:50 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:20:50 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:20:50 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:20:58 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  5.98it/s]
12:20:58 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:20:58 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:20:58 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:20:58 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:20:58 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:21:06 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  5.33it/s]
12:21:06 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:21:06 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:21:06 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:21:06 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:21:06 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:21:15 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  5.41it/s]
12:21:15 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:21:15 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:21:15 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:21:15 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:21:15 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:21:24 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 10.84it/s]
12:21:24 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:21:24 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:21:24 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:21:24 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:21:24 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:21:32 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  5.68it/s]
12:21:32 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:21:32 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:21:32 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:21:32 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:21:32 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:21:40 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.58it/s]
12:21:41 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:21:41 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:21:41 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:21:41 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:21:41 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:22:01 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.99it/s]
12:22:01 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:22:01 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:22:01 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:22:01 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:22:01 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:22:09 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.67it/s]
12:22:09 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:22:09 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:22:09 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:22:09 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:22:09 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:22:17 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.45it/s]
12:22:17 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:22:17 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:22:17 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:22:17 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:22:17 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:22:25 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  9.01it/s]
12:22:25 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:22:25 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:22:25 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:22:25 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:22:25 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:22:33 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.69it/s]
12:22:33 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:22:33 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:22:33 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:22:33 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:22:33 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:22:41 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.33it/s]
12:22:42 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:22:42 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:22:42 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:22:42 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:22:42 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:22:50 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.27it/s]
12:22:50 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:22:50 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:22:50 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:22:50 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:22:50 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:22:58 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  5.95it/s]
12:22:58 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:22:58 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:22:58 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:22:58 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:22:58 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:23:06 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.15it/s]
12:23:06 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:23:06 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:23:06 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:23:06 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:23:06 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:23:14 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 10.87it/s]
12:23:14 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:23:14 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:23:14 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:23:14 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:23:14 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:23:21 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 15.20it/s]
12:23:21 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:23:21 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:23:21 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:23:21 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:23:21 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:23:28 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 17.22it/s]
12:23:28 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:23:28 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:23:28 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:23:28 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:23:28 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:23:35 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 21.05it/s]
12:23:35 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:23:35 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:23:35 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:23:35 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:23:35 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:23:42 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 16.67it/s]
12:23:42 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:23:42 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:23:42 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:23:42 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:23:42 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:23:49 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 10.54it/s]
12:23:49 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:23:49 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:23:49 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:23:49 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:23:49 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:23:57 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.56it/s]
12:23:57 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:23:57 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:23:57 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:23:57 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:23:57 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:24:05 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  5.39it/s]
12:24:05 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:24:05 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:24:05 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:24:05 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:24:05 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:24:13 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.88it/s]
12:24:13 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:24:13 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=test...
12:24:13 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:24:13 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:24:13 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:24:23 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  4.96it/s]
12:24:23 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=
12:24:23 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:23 app.services.vector_store_service ERROR   RAG检索失败:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2329, in connect
    return await connect_utils._connect(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 991, in _connect
    conn = await _connect_addr(
           ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 828, in _connect_addr
    return await __connect_addr(params, True, *args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 873, in __connect_addr
    tr, pr = await connector
             ^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 744, in _create_ssl_connection
    tr, pr = await loop.create_connection(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 1080, in create_connection
    infos = await self._ensure_resolved(
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 1456, in _ensure_resolved
    return await loop.getaddrinfo(host, port, family=family, type=type,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 901, in getaddrinfo
    return await self.run_in_executor(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncio.exceptions.CancelledError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 169, in _do_get
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 167, in _do_get
    return self._create_connection()
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 393, in _create_connection
    return _ConnectionRecord(self)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 678, in __init__
    self.__connect()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 902, in __connect
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 898, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\create.py", line 645, in connect
    return dialect.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 616, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 941, in connect
    await_only(creator_fn(*arg, **kw)),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2328, in connect
    async with compat.timeout(timeout):
  File "C:\Program Files\Python312\Lib\asyncio\timeouts.py", line 115, in __aexit__
    raise TimeoutError from exc_val
TimeoutError
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2):
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:24 app.services.vector_store_service ERROR   RAG检索失败:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2329, in connect
    return await connect_utils._connect(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 991, in _connect
    conn = await _connect_addr(
           ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 828, in _connect_addr
    return await __connect_addr(params, True, *args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 873, in __connect_addr
    tr, pr = await connector
             ^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 744, in _create_ssl_connection
    tr, pr = await loop.create_connection(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 1080, in create_connection
    infos = await self._ensure_resolved(
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 1456, in _ensure_resolved
    return await loop.getaddrinfo(host, port, family=family, type=type,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 901, in getaddrinfo
    return await self.run_in_executor(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncio.exceptions.CancelledError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 169, in _do_get
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 167, in _do_get
    return self._create_connection()
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 393, in _create_connection
    return _ConnectionRecord(self)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 678, in __init__
    self.__connect()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 902, in __connect
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 898, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\create.py", line 645, in connect
    return dialect.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 616, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 941, in connect
    await_only(creator_fn(*arg, **kw)),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2328, in connect
    async with compat.timeout(timeout):
  File "C:\Program Files\Python312\Lib\asyncio\timeouts.py", line 115, in __aexit__
    raise TimeoutError from exc_val
TimeoutError
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2):
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:24 app.services.vector_store_service ERROR   RAG检索失败:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2329, in connect
    return await connect_utils._connect(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 991, in _connect
    conn = await _connect_addr(
           ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 828, in _connect_addr
    return await __connect_addr(params, True, *args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 873, in __connect_addr
    tr, pr = await connector
             ^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 744, in _create_ssl_connection
    tr, pr = await loop.create_connection(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 1080, in create_connection
    infos = await self._ensure_resolved(
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 1456, in _ensure_resolved
    return await loop.getaddrinfo(host, port, family=family, type=type,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 901, in getaddrinfo
    return await self.run_in_executor(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncio.exceptions.CancelledError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 169, in _do_get
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 167, in _do_get
    return self._create_connection()
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 393, in _create_connection
    return _ConnectionRecord(self)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 678, in __init__
    self.__connect()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 902, in __connect
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 898, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\create.py", line 645, in connect
    return dialect.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 616, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 941, in connect
    await_only(creator_fn(*arg, **kw)),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2328, in connect
    async with compat.timeout(timeout):
  File "C:\Program Files\Python312\Lib\asyncio\timeouts.py", line 115, in __aexit__
    raise TimeoutError from exc_val
TimeoutError
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2):
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:24 app.services.vector_store_service ERROR   RAG检索失败:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2329, in connect
    return await connect_utils._connect(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 991, in _connect
    conn = await _connect_addr(
           ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 828, in _connect_addr
    return await __connect_addr(params, True, *args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 873, in __connect_addr
    tr, pr = await connector
             ^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 744, in _create_ssl_connection
    tr, pr = await loop.create_connection(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 1080, in create_connection
    infos = await self._ensure_resolved(
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 1456, in _ensure_resolved
    return await loop.getaddrinfo(host, port, family=family, type=type,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 901, in getaddrinfo
    return await self.run_in_executor(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncio.exceptions.CancelledError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 169, in _do_get
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 167, in _do_get
    return self._create_connection()
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 393, in _create_connection
    return _ConnectionRecord(self)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 678, in __init__
    self.__connect()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 902, in __connect
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 898, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\create.py", line 645, in connect
    return dialect.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 616, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 941, in connect
    await_only(creator_fn(*arg, **kw)),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2328, in connect
    async with compat.timeout(timeout):
  File "C:\Program Files\Python312\Lib\asyncio\timeouts.py", line 115, in __aexit__
    raise TimeoutError from exc_val
TimeoutError
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2):
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:24 app.services.vector_store_service ERROR   RAG检索失败:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2329, in connect
    return await connect_utils._connect(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 991, in _connect
    conn = await _connect_addr(
           ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 828, in _connect_addr
    return await __connect_addr(params, True, *args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 873, in __connect_addr
    tr, pr = await connector
             ^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 744, in _create_ssl_connection
    tr, pr = await loop.create_connection(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 1080, in create_connection
    infos = await self._ensure_resolved(
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 1456, in _ensure_resolved
    return await loop.getaddrinfo(host, port, family=family, type=type,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 901, in getaddrinfo
    return await self.run_in_executor(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncio.exceptions.CancelledError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 169, in _do_get
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 167, in _do_get
    return self._create_connection()
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 393, in _create_connection
    return _ConnectionRecord(self)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 678, in __init__
    self.__connect()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 902, in __connect
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 898, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\create.py", line 645, in connect
    return dialect.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 616, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 941, in connect
    await_only(creator_fn(*arg, **kw)),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2328, in connect
    async with compat.timeout(timeout):
  File "C:\Program Files\Python312\Lib\asyncio\timeouts.py", line 115, in __aexit__
    raise TimeoutError from exc_val
TimeoutError
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2):
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:24 app.services.vector_store_service ERROR   RAG检索失败:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2329, in connect
    return await connect_utils._connect(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 991, in _connect
    conn = await _connect_addr(
           ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 828, in _connect_addr
    return await __connect_addr(params, True, *args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 873, in __connect_addr
    tr, pr = await connector
             ^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 744, in _create_ssl_connection
    tr, pr = await loop.create_connection(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 1080, in create_connection
    infos = await self._ensure_resolved(
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 1456, in _ensure_resolved
    return await loop.getaddrinfo(host, port, family=family, type=type,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 901, in getaddrinfo
    return await self.run_in_executor(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncio.exceptions.CancelledError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 169, in _do_get
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 167, in _do_get
    return self._create_connection()
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 393, in _create_connection
    return _ConnectionRecord(self)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 678, in __init__
    self.__connect()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 902, in __connect
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 898, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\create.py", line 645, in connect
    return dialect.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 616, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 941, in connect
    await_only(creator_fn(*arg, **kw)),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2328, in connect
    async with compat.timeout(timeout):
  File "C:\Program Files\Python312\Lib\asyncio\timeouts.py", line 115, in __aexit__
    raise TimeoutError from exc_val
TimeoutError
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2):
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:24 app.services.vector_store_service ERROR   RAG检索失败:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2329, in connect
    return await connect_utils._connect(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 991, in _connect
    conn = await _connect_addr(
           ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 828, in _connect_addr
    return await __connect_addr(params, True, *args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 873, in __connect_addr
    tr, pr = await connector
             ^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 744, in _create_ssl_connection
    tr, pr = await loop.create_connection(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 1080, in create_connection
    infos = await self._ensure_resolved(
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 1456, in _ensure_resolved
    return await loop.getaddrinfo(host, port, family=family, type=type,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 901, in getaddrinfo
    return await self.run_in_executor(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncio.exceptions.CancelledError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 169, in _do_get
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 167, in _do_get
    return self._create_connection()
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 393, in _create_connection
    return _ConnectionRecord(self)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 678, in __init__
    self.__connect()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 902, in __connect
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 898, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\create.py", line 645, in connect
    return dialect.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 616, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 941, in connect
    await_only(creator_fn(*arg, **kw)),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2328, in connect
    async with compat.timeout(timeout):
  File "C:\Program Files\Python312\Lib\asyncio\timeouts.py", line 115, in __aexit__
    raise TimeoutError from exc_val
TimeoutError
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2):
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:24 app.services.vector_store_service ERROR   RAG检索失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.vector_store_service ERROR   RAG检索失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.vector_store_service ERROR   RAG检索失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.vector_store_service ERROR   RAG检索失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.vector_store_service ERROR   RAG检索失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.vector_store_service ERROR   RAG检索失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.vector_store_service ERROR   RAG检索失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:24 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:24:24 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:24:24 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:24:24 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:24:24 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:24:24 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:24:32 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.56it/s]
12:24:32 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:32 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:32 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:24:32 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:24:35 app.services.vector_store_service ERROR   RAG检索失败:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2329, in connect
    return await connect_utils._connect(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 991, in _connect
    conn = await _connect_addr(
           ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 828, in _connect_addr
    return await __connect_addr(params, True, *args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 876, in __connect_addr
    await connected
asyncio.exceptions.CancelledError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 169, in _do_get
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 167, in _do_get
    return self._create_connection()
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 393, in _create_connection
    return _ConnectionRecord(self)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 678, in __init__
    self.__connect()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 902, in __connect
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 898, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\create.py", line 645, in connect
    return dialect.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 616, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 941, in connect
    await_only(creator_fn(*arg, **kw)),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2328, in connect
    async with compat.timeout(timeout):
  File "C:\Program Files\Python312\Lib\asyncio\timeouts.py", line 115, in __aexit__
    raise TimeoutError from exc_val
TimeoutError
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2):
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2):
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:35 app.services.vector_store_service ERROR   RAG检索失败:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2329, in connect
    return await connect_utils._connect(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 991, in _connect
    conn = await _connect_addr(
           ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 828, in _connect_addr
    return await __connect_addr(params, True, *args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 876, in __connect_addr
    await connected
asyncio.exceptions.CancelledError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 169, in _do_get
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 167, in _do_get
    return self._create_connection()
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 393, in _create_connection
    return _ConnectionRecord(self)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 678, in __init__
    self.__connect()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 902, in __connect
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 898, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\create.py", line 645, in connect
    return dialect.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 616, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 941, in connect
    await_only(creator_fn(*arg, **kw)),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2328, in connect
    async with compat.timeout(timeout):
  File "C:\Program Files\Python312\Lib\asyncio\timeouts.py", line 115, in __aexit__
    raise TimeoutError from exc_val
TimeoutError
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2):
12:24:35 app.services.vector_store_service ERROR   RAG检索失败:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2329, in connect
    return await connect_utils._connect(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 991, in _connect
    conn = await _connect_addr(
           ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 828, in _connect_addr
    return await __connect_addr(params, True, *args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 876, in __connect_addr
    await connected
asyncio.exceptions.CancelledError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 169, in _do_get
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 167, in _do_get
    return self._create_connection()
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 393, in _create_connection
    return _ConnectionRecord(self)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 678, in __init__
    self.__connect()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 902, in __connect
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 898, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\create.py", line 645, in connect
    return dialect.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 616, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 941, in connect
    await_only(creator_fn(*arg, **kw)),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2328, in connect
    async with compat.timeout(timeout):
  File "C:\Program Files\Python312\Lib\asyncio\timeouts.py", line 115, in __aexit__
    raise TimeoutError from exc_val
TimeoutError
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2):
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2):
12:24:35 app.services.vector_store_service ERROR   RAG检索失败:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2329, in connect
    return await connect_utils._connect(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 991, in _connect
    conn = await _connect_addr(
           ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 828, in _connect_addr
    return await __connect_addr(params, True, *args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 876, in __connect_addr
    await connected
asyncio.exceptions.CancelledError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 169, in _do_get
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 167, in _do_get
    return self._create_connection()
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 393, in _create_connection
    return _ConnectionRecord(self)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 678, in __init__
    self.__connect()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 902, in __connect
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 898, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\create.py", line 645, in connect
    return dialect.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 616, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 941, in connect
    await_only(creator_fn(*arg, **kw)),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2328, in connect
    async with compat.timeout(timeout):
  File "C:\Program Files\Python312\Lib\asyncio\timeouts.py", line 115, in __aexit__
    raise TimeoutError from exc_val
TimeoutError
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2):
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:35 app.services.vector_store_service ERROR   RAG检索失败:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2329, in connect
    return await connect_utils._connect(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 991, in _connect
    conn = await _connect_addr(
           ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 828, in _connect_addr
    return await __connect_addr(params, True, *args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 876, in __connect_addr
    await connected
asyncio.exceptions.CancelledError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 169, in _do_get
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 167, in _do_get
    return self._create_connection()
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 393, in _create_connection
    return _ConnectionRecord(self)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 678, in __init__
    self.__connect()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 902, in __connect
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 898, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\create.py", line 645, in connect
    return dialect.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 616, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 941, in connect
    await_only(creator_fn(*arg, **kw)),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2328, in connect
    async with compat.timeout(timeout):
  File "C:\Program Files\Python312\Lib\asyncio\timeouts.py", line 115, in __aexit__
    raise TimeoutError from exc_val
TimeoutError
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:35 app.services.vector_store_service ERROR   RAG检索失败:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2329, in connect
    return await connect_utils._connect(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 991, in _connect
    conn = await _connect_addr(
           ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 828, in _connect_addr
    return await __connect_addr(params, True, *args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 876, in __connect_addr
    await connected
asyncio.exceptions.CancelledError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 169, in _do_get
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 167, in _do_get
    return self._create_connection()
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 393, in _create_connection
    return _ConnectionRecord(self)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 678, in __init__
    self.__connect()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 902, in __connect
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 898, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\create.py", line 645, in connect
    return dialect.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 616, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 941, in connect
    await_only(creator_fn(*arg, **kw)),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2328, in connect
    async with compat.timeout(timeout):
  File "C:\Program Files\Python312\Lib\asyncio\timeouts.py", line 115, in __aexit__
    raise TimeoutError from exc_val
TimeoutError
12:24:35 app.services.vector_store_service ERROR   RAG检索失败:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2329, in connect
    return await connect_utils._connect(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 991, in _connect
    conn = await _connect_addr(
           ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 828, in _connect_addr
    return await __connect_addr(params, True, *args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connect_utils.py", line 876, in __connect_addr
    await connected
asyncio.exceptions.CancelledError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\vector_store_service.py", line 251, in retrieve_relevant_analysis
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 169, in _do_get
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 167, in _do_get
    return self._create_connection()
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 393, in _create_connection
    return _ConnectionRecord(self)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 678, in __init__
    self.__connect()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 902, in __connect
    with util.safe_reraise():
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 898, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\create.py", line 645, in connect
    return dialect.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 616, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 941, in connect
    await_only(creator_fn(*arg, **kw)),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 2328, in connect
    async with compat.timeout(timeout):
  File "C:\Program Files\Python312\Lib\asyncio\timeouts.py", line 115, in __aexit__
    raise TimeoutError from exc_val
TimeoutError
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 1/2):
12:24:35 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2):
12:24:35 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:24:35 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:24:35 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:24:35 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:24:35 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:24:43 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  9.70it/s]
12:24:44 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 1/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:24:44 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:24:44 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:24:44 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:24:44 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:24:46 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:24:46 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:24:46 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:24:46 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:24:54 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  5.03it/s]
12:24:54 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:24:54 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:24:55 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:24:55 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:24:55 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:24:55 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
12:24:55 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] ✅ RAG检索成功: 找到5个相关片段
12:24:55 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:24:55 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:24:55 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:24:55 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:24:55 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:25:03 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.76it/s]
12:25:03 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:25:03 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:25:03 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:25:03 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:25:03 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:25:03 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:25:11 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.10it/s]
12:25:11 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:25:11 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:25:11 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:25:11 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:25:11 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:25:18 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 17.68it/s]
12:25:18 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [read_chapter_tool] ❌ 读取章节失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 429, in read_chapter_tool
    chapter = await _retry_on_failure(
              ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\chapter_service.py", line 50, in get_chapter_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [read_chapter_tool] ❌ 读取章节失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 429, in read_chapter_tool
    chapter = await _retry_on_failure(
              ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\chapter_service.py", line 50, in get_chapter_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [get_chapter_by_order_tool] ❌ 查询失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 519, in get_chapter_by_order_tool
    work = await _retry_on_failure(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\work_service.py", line 31, in get_work_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [get_context_tool] ❌ 获取上下文失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 753, in get_context_tool
    work = await _retry_on_failure(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\work_service.py", line 31, in get_work_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [read_chapter_tool] ❌ 读取章节失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 429, in read_chapter_tool
    chapter = await _retry_on_failure(
              ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\chapter_service.py", line 50, in get_chapter_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [get_chapter_by_order_tool] ❌ 查询失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 519, in get_chapter_by_order_tool
    work = await _retry_on_failure(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\work_service.py", line 31, in get_work_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [read_chapter_tool] ❌ 读取章节失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 429, in read_chapter_tool
    chapter = await _retry_on_failure(
              ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\chapter_service.py", line 50, in get_chapter_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [get_context_tool] ❌ 获取上下文失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 753, in get_context_tool
    work = await _retry_on_failure(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\work_service.py", line 31, in get_work_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [read_chapter_tool] ❌ 读取章节失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 429, in read_chapter_tool
    chapter = await _retry_on_failure(
              ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\chapter_service.py", line 50, in get_chapter_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [get_chapter_by_order_tool] ❌ 查询失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 519, in get_chapter_by_order_tool
    work = await _retry_on_failure(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\work_service.py", line 31, in get_work_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [get_context_tool] ❌ 获取上下文失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 753, in get_context_tool
    work = await _retry_on_failure(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\work_service.py", line 31, in get_work_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [read_chapter_tool] ❌ 读取章节失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 429, in read_chapter_tool
    chapter = await _retry_on_failure(
              ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\chapter_service.py", line 50, in get_chapter_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [get_context_tool] ❌ 获取上下文失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 753, in get_context_tool
    work = await _retry_on_failure(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\work_service.py", line 31, in get_work_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [get_chapter_by_order_tool] ❌ 查询失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 519, in get_chapter_by_order_tool
    work = await _retry_on_failure(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\work_service.py", line 31, in get_work_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [get_context_tool] ❌ 获取上下文失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 753, in get_context_tool
    work = await _retry_on_failure(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\work_service.py", line 31, in get_work_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [read_chapter_tool] ❌ 读取章节失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 429, in read_chapter_tool
    chapter = await _retry_on_failure(
              ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\chapter_service.py", line 50, in get_chapter_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [get_chapter_by_order_tool] ❌ 查询失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 519, in get_chapter_by_order_tool
    work = await _retry_on_failure(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\work_service.py", line 31, in get_work_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [read_chapter_tool] ❌ 读取章节失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 429, in read_chapter_tool
    chapter = await _retry_on_failure(
              ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\chapter_service.py", line 50, in get_chapter_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [get_chapter_by_order_tool] ❌ 查询失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 519, in get_chapter_by_order_tool
    work = await _retry_on_failure(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\work_service.py", line 31, in get_work_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [read_chapter_tool] ❌ 读取章节失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 429, in read_chapter_tool
    chapter = await _retry_on_failure(
              ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\chapter_service.py", line 50, in get_chapter_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_chapter_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [read_chapter_tool] ❌ 读取章节失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 429, in read_chapter_tool
    chapter = await _retry_on_failure(
              ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\chapter_service.py", line 50, in get_chapter_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [get_chapter_by_order_tool] ❌ 查询失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 519, in get_chapter_by_order_tool
    work = await _retry_on_failure(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\work_service.py", line 31, in get_work_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [get_chapter_by_order_tool] ❌ 查询失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 519, in get_chapter_by_order_tool
    work = await _retry_on_failure(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\work_service.py", line 31, in get_work_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [get_context_tool] ❌ 获取上下文失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 753, in get_context_tool
    work = await _retry_on_failure(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\work_service.py", line 31, in get_work_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [get_chapter_by_order_tool] ❌ 查询失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 519, in get_chapter_by_order_tool
    work = await _retry_on_failure(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\work_service.py", line 31, in get_work_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [get_context_tool] ❌ 获取上下文失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 753, in get_context_tool
    work = await _retry_on_failure(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\work_service.py", line 31, in get_work_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [Retry] get_work_by_id 失败 (尝试 2/2): QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent ERROR   [get_context_tool] ❌ 获取上下文失败: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 753, in get_context_tool
    work = await _retry_on_failure(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 109, in _retry_on_failure
    result = await func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\app\services\work_service.py", line 31, in get_work_by_id
    result = await self.db.execute(
             ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2180, in _execute_internal
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2047, in _connection_for_bind
    return trans._connection_for_bind(engine, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in _connection_for_bind
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
                ^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 1143, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3269, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 3293, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 1269, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 716, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\impl.py", line 158, in _do_get
    raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
12:25:18 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:25:18 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:25:18 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:25:18 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:25:18 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:25:18 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:25:25 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 20.80it/s]
12:25:25 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:25:25 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:25:25 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:25:25 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:25:25 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:25:32 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 15.89it/s]
12:25:33 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:25:33 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:25:33 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:25:33 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:25:40 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 28.67it/s]
12:25:40 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:25:40 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:25:40 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:25:40 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:25:47 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 15.57it/s]
12:25:47 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:25:47 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:25:47 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:25:47 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:25:54 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 21.03it/s]
12:25:54 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:25:54 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:25:54 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:25:54 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:25:54 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:26:01 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 13.34it/s]
12:26:01 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:26:01 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:26:01 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:26:01 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:26:01 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:26:01 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:26:01 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:26:02 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:26:02 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:26:02 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:26:02 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:26:02 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:26:02 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:26:02 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:26:02 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:26:02 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:26:02 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:26:02 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:26:02 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:26:02 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:26:02 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:26:02 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:26:09 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 19.02it/s]
12:26:09 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:26:40 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:26:40 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:26:40 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:26:40 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:26:48 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.97it/s]
12:26:48 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:26:48 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:26:48 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:26:48 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:26:48 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:26:48 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:26:55 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  5.67it/s]
12:26:56 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:26:56 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:26:56 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:26:56 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:26:56 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:27:03 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 11.41it/s]
12:27:03 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=作品背景和设定...
12:27:03 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:27:03 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:27:03 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:27:11 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.01it/s]
12:27:11 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
12:27:11 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:27:11 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:27:11 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:27:11 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:27:11 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:27:11 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:27:11 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:27:11 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:27:11 app.services.vector_store_service INFO   检索到 3 个相关结果（阈值=0.4）
12:27:11 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
12:27:11 __main__ INFO   完成: 100 成功, 0 失败
12:27:13 __main__ INFO   最终连接池: {'total': 10, 'checked_out': 0, 'available': 10}
12:27:13 __main__ INFO   ✅ 压力测试通过！无连接泄漏
12:27:13 __main__ INFO
================================================================================
12:27:13 __main__ INFO   🎉 所有测试通过！ReAct 模式连接泄漏已修复！
12:27:13 __main__ INFO   ================================================================================
(venv) PS D:\Java\ai_writer\backend>