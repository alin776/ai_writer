  - backend/app/services/agent/langgraph_agent.py 仍有约 5,094 行（命令 python -c "..." 实测），仅从 6,133 行缩到
执行、规划、任务执行、反思编排、响应组装、工具派发、JSON 解析、记忆读写等多重职责，未形成清晰的模块边界。
  - 虽已把少量工具/上下文辅助函数移到 langgraph_tools.py 和 utils/context_builder.py（见文件头部拆分说明），但主体
控制流、回调、错误处理仍集中在本文件，耦合度高，拆解尚未真正完成。
  建议的拆分方向（按可操作性排序）
  2. 按横切拆：history.py（checkpointer/记忆装配与清理）、json_utils.py（统一 JSON 提取与健壮解析）、
 callbacks.py（on_plan/on_task_* 事件封装）。
  3. 将 DeepAgent 相关入口从主类分离，只保留策略开关和结果接入点。
  4. 维持现有已拆出的 langgraph_tools、context_builder，再逐步迁移剩余纯工具型方法（如 quick path、Intent 决策组
 装、progress tracker 包装）。