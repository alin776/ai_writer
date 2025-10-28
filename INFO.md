(venv) PS D:\Java\ai_writer\backend> python tests/test_database_performance.py

🚀 开始数据库性能审查...

======================================================================
📊 数据库索引审查
======================================================================

📋 表: ai_call_logs
   索引数量: 13
   - ai_call_logs_pkey: id
   - ix_ai_call_logs_analysis_id: analysis_id
   - ix_ai_call_logs_chapter_id: chapter_id
   - ix_ai_call_logs_created_at: created_at
   - ix_ai_call_logs_id: id
   - ix_ai_call_logs_model_name: model_name
   - ix_ai_call_logs_operation_type: operation_type
   - ix_ai_call_logs_user_id: user_id
   - ix_ai_call_logs_work_id: work_id
   - ix_ai_logs_model_created: model_name, created_at
   - ix_ai_logs_operation_created: operation_type, created_at
   - ix_ai_logs_user_created: user_id, created_at
   - ix_ai_logs_work_created: work_id, created_at

📋 表: ai_guidelines
   索引数量: 3
   - ai_guidelines_pkey: id
   - ix_ai_guidelines_id: id
   - ix_ai_guidelines_work_id: work_id

📋 表: alembic_version
   索引数量: 1
   - alembic_version_pkc: version_num

📋 表: book_analysis_jobs
   索引数量: 4
   - book_analysis_jobs_pkey: id
   - ix_book_analysis_jobs_file_hash: file_hash
   - ix_book_analysis_jobs_status: status
   - ix_book_analysis_jobs_user_id: user_id

📋 表: chapter_versions
   索引数量: 6
   - chapter_versions_pkey: id
   - ix_chapter_versions_chapter_id: chapter_id
   - ix_chapter_versions_id: id
   - ix_chapter_versions_is_milestone: is_milestone
   - ix_chapter_versions_review_session_id: review_session_id
   - ix_chapter_versions_user_id: user_id

📋 表: chapters
   索引数量: 5
   - chapters_pkey: id
   - ix_chapters_id: id
   - ix_chapters_order: "order"
   - ix_chapters_status: status
   - ix_chapters_work_id: work_id

📋 表: characters
   索引数量: 3
   - characters_pkey: id
   - ix_characters_id: id
   - ix_characters_work_id: work_id

📋 表: entity_groups
   索引数量: 2
   - entity_groups_pkey: id
   - ix_entity_groups_work_id: work_id

📋 表: entity_relationships
   索引数量: 1
   - entity_relationships_pkey: id

📋 表: evaluation_records
   索引数量: 11
   - evaluation_records_pkey: id
   - ix_eval_operation_created: operation_type, created_at
   - ix_eval_user_created: user_id, created_at
   - ix_eval_work_created: work_id, created_at
   - ix_evaluation_records_ai_call_log_id: ai_call_log_id
   - ix_evaluation_records_chapter_id: chapter_id
   - ix_evaluation_records_created_at: created_at
   - ix_evaluation_records_id: id
   - ix_evaluation_records_operation_type: operation_type
   - ix_evaluation_records_user_id: user_id
   - ix_evaluation_records_work_id: work_id

📋 表: group_members
   索引数量: 3
   - group_members_pkey: id
   - ix_group_members_entity_id: entity_id
   - ix_group_members_group_id: group_id

📋 表: humanize_session_details
   索引数量: 3
   - humanize_session_details_pkey: id
   - ix_humanize_session_details_expires_at: expires_at
   - ix_humanize_session_details_session_id: session_id

📋 表: humanize_sessions
   索引数量: 5
   - humanize_sessions_pkey: id
   - ix_humanize_sessions_ai_function: ai_function
   - ix_humanize_sessions_created_at: created_at
   - ix_humanize_sessions_id: id
   - ix_humanize_sessions_user_id: user_id

📋 表: knowledge_items
   索引数量: 7
   - ix_knowledge_items_category: category
   - ix_knowledge_items_chapter_id: chapter_id
   - ix_knowledge_items_id: id
   - ix_knowledge_items_title: title
   - ix_knowledge_items_user_id: user_id
   - ix_knowledge_items_work_id: work_id
   - knowledge_items_pkey: id

📋 表: locations
   索引数量: 3
   - ix_locations_id: id
   - ix_locations_work_id: work_id
   - locations_pkey: id

📋 表: novel_analyses
   索引数量: 4
   - ix_novel_analyses_id: id
   - ix_novel_analyses_status: status
   - ix_novel_analyses_work_id: work_id
   - novel_analyses_pkey: id

📋 表: novel_analysis_vectors
   索引数量: 9
   - idx_novel_vectors_analysis_id: analysis_id
   - idx_novel_vectors_chapter_id: chapter_id
   - idx_novel_vectors_source: source_type, source_id
   - idx_novel_vectors_user_source: user_id, source_type
   - idx_novel_vectors_work_id: work_id
   - ix_novel_analysis_vectors_source_id: source_id
   - ix_novel_analysis_vectors_source_type: source_type
   - ix_novel_analysis_vectors_user_id: user_id
   - novel_analysis_vectors_pkey: id

📋 表: review_sessions
   索引数量: 5
   - ix_review_sessions_id: id
   - ix_review_sessions_review_level: review_level
   - ix_review_sessions_target_id: target_id
   - ix_review_sessions_user_id: user_id
   - review_sessions_pkey: id

📋 表: review_tasks
   索引数量: 7
   - ix_review_tasks_chapter_id: chapter_id
   - ix_review_tasks_id: id
   - ix_review_tasks_priority: priority
   - ix_review_tasks_review_session_id: review_session_id
   - ix_review_tasks_status: status
   - ix_review_tasks_user_id: user_id
   - review_tasks_pkey: id

📋 表: rewrite_results
   索引数量: 3
   - ix_rewrite_results_id: id
   - ix_rewrite_results_session_id: session_id
   - rewrite_results_pkey: id

📋 表: rewrite_sessions
   索引数量: 4
   - ix_rewrite_sessions_created_at: created_at
   - ix_rewrite_sessions_id: id
   - ix_rewrite_sessions_user_id: user_id
   - rewrite_sessions_pkey: id

📋 表: settings
   索引数量: 3
   - ix_settings_id: id
   - ix_settings_work_id: work_id
   - settings_pkey: id

📋 表: timeline_events
   索引数量: 1
   - timeline_events_pkey: id

📋 表: user_profiles
   索引数量: 2
   - ix_user_profiles_user_id: user_id
   - user_profiles_pkey: id

📋 表: user_sessions
   索引数量: 4
   - ix_user_sessions_id: id
   - ix_user_sessions_user_id: user_id
   - user_sessions_pkey: id
   - user_sessions_session_token_key: session_token

📋 表: users
   索引数量: 4
   - ix_users_email: email
   - ix_users_id: id
   - ix_users_username: username
   - users_pkey: id

📋 表: work_guidelines
   索引数量: 3
   - ix_work_guidelines_id: id
   - ix_work_guidelines_work_id: work_id
   - work_guidelines_pkey: id

📋 表: works
   索引数量: 4
   - ix_works_author_id: author_id
   - ix_works_id: id
   - ix_works_title: title
   - works_pkey: id

📋 表: worldview_suggestions
   索引数量: 4
   - ix_worldview_suggestions_job_id: job_id
   - ix_worldview_suggestions_status: status
   - ix_worldview_suggestions_user_id: user_id
   - worldview_suggestions_pkey: id

======================================================================
🔍 缺失索引检测
======================================================================

⚠️ 发现缺失的索引:

   - chapters.author_id
   - relationships.work_id
   - relationships.source_id
   - relationships.target_id
   - timeline_events.work_id

======================================================================
⏱️ 查询性能测试
======================================================================

📊 作品列表查询 (带章节)
   耗时: 22.57ms
   行数: 17
   ✅ 查询快速 (<50ms)

📊 章节列表查询
   耗时: 0.00ms
   行数: 0
   ✅ 查询快速 (<50ms)

📊 AI日志统计查询
   耗时: 15.92ms
   行数: 1
   ✅ 查询快速 (<50ms)

======================================================================
💾 表大小分析
======================================================================

表名                             大小              行数
----------------------------------------------------------------------
chapters                       1064 kB                713
novel_analysis_vectors         688 kB                 120
ai_call_logs                   264 kB                  17
novel_analyses                 232 kB                   4
knowledge_items                216 kB                  60
evaluation_records             192 kB                   1
user_sessions                  176 kB                  91
review_tasks                   128 kB                  15
users                          112 kB                  78
chapter_versions               112 kB                   9
review_sessions                112 kB                   5
book_analysis_jobs             112 kB                   5
humanize_sessions              88 kB                   22
worldview_suggestions          88 kB                    0
works                          80 kB                   17
user_profiles                  80 kB                   39
settings                       64 kB                    1
locations                      64 kB                    1
humanize_session_details       64 kB                   13
characters                     64 kB                    2
ai_guidelines                  64 kB                    1
rewrite_sessions               40 kB                    0
work_guidelines                32 kB                    0
entity_relationships           32 kB                    1
rewrite_results                32 kB                    0
entity_groups                  24 kB                    0
alembic_version                24 kB                    1
group_members                  24 kB                    0
timeline_events                16 kB                    0

======================================================================
🔍 N+1查询模式检测
======================================================================

检查 Service 文件中的 selectinload/joinedload 使用情况...

⚠️ 无法执行 grep 命令: [WinError 2] 系统找不到指定的文件。

📝 N+1查询优化建议:

1. ✅ 在查询作品时预加载章节:
   .options(selectinload(Work.chapters))

2. ✅ 在查询世界观时预加载关系:
   .options(selectinload(Character.relationships))

3. ⚠️ 避免在循环中查询关联数据:
   # ❌ 错误
   for work in works:
       chapters = await get_chapters(work.id)

   # ✅ 正确
   works = await db.execute(
       select(Work).options(selectinload(Work.chapters))
   )

======================================================================
📊 性能审查总结
======================================================================

⚠️ 发现 5 个缺失的索引
   建议创建这些索引以提升查询性能

📝 下一步建议:
   1. 如有缺失索引,运行 Day2 索引优化脚本
   2. 监控慢查询日志
   3. 定期运行性能测试

======================================================================
✅ 审查完成!
======================================================================
(venv) PS D:\Java\ai_writer\backend>