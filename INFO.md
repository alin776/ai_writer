• 下面是更详细、直白的缺点清单，每条都说明“问题 → 直接后果 → 证据”。

  1. 两条链路字段不一致，答案容易对不上
     自动注入带 role/relationships/guidelines 等字段，而工具链路只给 name/description 和少量字段；同一个问题（如“人物关系”）会因为走哪
     条链路得到不同答案。
     证据：自动注入字段 backend/app/api/v1/agent.py:1300、backend/app/api/v1/agent.py:1340；工具返回结构 backend/app/services/agent/
     langgraph_tools.py:1132
  2. 强制使用已废弃工具，技术债明显
     Prompt 里还要求“必须调用 get_worldview_summary”，但该工具已经标注 deprecated，内部只是转调 get_writing_context。这会让后续维护很
     痛：要改一次就得改 Prompt 和工具两个地方。
     证据：Prompt 强制调用 backend/app/services/agent/actions/general_chat_action.py:131；工具弃用标记 backend/app/services/agent/
     langgraph_tools.py:917
  3. 自动注入没有执行轨迹事件，用户看不到“世界观已加载”
     knowledge_loaded 只在工具调用后触发；自动注入没有任何 flow 事件，所以 UI 层看不到“世界观已加载”，用户会误以为没读取。
     证据：flow 事件生成 backend/app/services/agent/langgraph_agent.py:1676、事件结构 backend/app/services/agent/stream/
     flow_events.py:84
  4. 重复拉取、重复上下文，浪费成本
     /chat/stream 已自动注入世界观，用户再问“世界观里有什么”又被 Prompt 强制调用工具，再拉一次。结果是 DB 查询和上下文两头重复，成本上
     升、上下文更膨胀。
     证据：自动注入 backend/app/api/v1/agent.py:1291；Prompt 强制调用 backend/app/services/agent/actions/general_chat_action.py:131
  5. 没有分页/数量上限，只做字段截断，长作品容易爆上下文
     代码是“全量查询全部人物/地点/设定”，只对描述字段做 [:200/300/500]，但没有条目数量上限。大作品会塞满 prompt。
     证据：全量查询 backend/app/api/v1/agent.py:1300、backend/app/services/worldview_service.py:30；工具路径也无数量限制 backend/app/
     services/agent/langgraph_tools.py:1132
  6. 截断+无ID，导致“看得到但定位不到”
     返回里没有实体 id，只给截断后的 description，导致 Agent 无法精确指向或让前端跳到对应卡片，用户修正很困难。
     证据：自动注入字段结构 backend/app/api/v1/agent.py:1302；工具结构 backend/app/services/agent/langgraph_tools.py:1140
  7. 缓存带来“旧世界观”风险
     工具链路 get_writing_context 走工具缓存，worldview 默认 TTL 30 分钟；如果用户刚更新世界观，工具可能返回旧数据。
     证据：缓存别名与 TTL backend/app/services/agent/utils/tool_cache.py:33、backend/app/services/agent/utils/tool_cache.py:101
  8. 执行轨迹里角色标签容易出现“空角色”
     knowledge_loaded 拼装展示时用 name - role，但工具返回的角色列表没有 role 字段，最终 UI 可能展示成 “张三 - ” 这种空值。
     证据：拼接逻辑 backend/app/services/agent/langgraph_agent.py:1694；工具返回字段 backend/app/services/agent/
     langgraph_tools.py:1139
  9. 返回顺序不稳定
     WorldviewService 查询没有 order_by，数据库默认顺序不保证稳定；相同请求可能顺序变化，影响记忆与引用一致性。
     证据：查询无排序 backend/app/services/worldview_service.py:30
  10. 自动注入“无条件发生”，无法按意图精简
     只要 work_id 存在就注入世界观，即使用户只是闲聊或不需要世界观，也会塞进上下文；缺乏“按需加载”。
     证据：注入逻辑不做意图判断 backend/app/api/v1/agent.py:1291