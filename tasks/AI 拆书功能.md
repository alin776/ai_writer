# NovelAIde - AI 拆书功能技术实现完整文档

> 生成时间: 2025-10-26
> 版本: v1.0
> 作者: Claude Code Analysis

---

## 📚 目录

1. [系统架构概览](#1-系统架构概览)
2. [核心数据模型](#2-核心数据模型)
3. [AI 拆书工作流程](#3-ai-拆书工作流程)
4. [番茄小说拆书策略详解](#4-番茄小说拆书策略详解)
5. [API 接口完整说明](#5-api-接口完整说明)
6. [前后端交互流程](#6-前后端交互流程)
7. [提示词工程详解](#7-提示词工程详解)
8. [数据持久化机制](#8-数据持久化机制)
9. [扩展开发指南](#9-扩展开发指南)
10. [性能优化与监控](#10-性能优化与监控)

---

## 1. 系统架构概览

### 1.1 技术栈

```yaml
后端框架: Spring Boot 3.4.1 (Java 21)
数据库: MongoDB (响应式驱动)
AI 集成: LangChain4j 1.0.0-beta3
消息流: Server-Sent Events (SSE)
响应式编程: Project Reactor (Flux/Mono)
API 风格: RESTful + WebFlux
```

### 1.2 模块结构

```
AINovalServer/
├── domain/model/              # 数据模型层
│   ├── setting/
│   │   ├── generation/
│   │   │   ├── SettingNode.java              # 设定节点（树形结构）
│   │   │   ├── SettingGenerationSession.java # 生成会话
│   │   │   └── SettingGenerationEvent.java   # SSE 事件
│   │   └── NovelSettingHistory.java          # 历史快照
│   └── Novel.java                            # 小说主模型
│
├── service/                   # 业务逻辑层
│   ├── setting/
│   │   ├── generation/
│   │   │   ├── ISettingGenerationService.java        # 服务接口
│   │   │   ├── SettingGenerationService.java         # 核心服务实现
│   │   │   ├── InMemorySessionManager.java           # 会话管理器
│   │   │   ├── StrategyManagementService.java        # 策略管理
│   │   │   ├── SystemStrategyInitializationService.java  # 系统策略初始化
│   │   │   └── strategy/
│   │   │       ├── ISettingGenerationStrategy.java   # 策略接口
│   │   │       ├── TomatoWebNovelStrategy.java       # 番茄小说策略 ⭐
│   │   │       └── BaseSettingGenerationStrategy.java
│   │   ├── SettingComposeService.java        # 编排服务
│   │   └── NovelSettingHistoryService.java   # 历史管理
│   └── impl/
│       ├── ImportServiceImpl.java            # 小说导入服务
│       └── TxtNovelParser.java               # TXT 解析器
│
├── controller/                # API 控制层
│   ├── SettingGenerationController.java      # 设定生成 API
│   └── NovelController.java                  # 小说导入 API
│
├── repository/                # 数据访问层
│   ├── NovelSettingHistoryRepository.java
│   └── NovelRepository.java
│
└── config/                    # 配置层
    ├── ChatLanguageModelConfig.java          # LLM 模型配置
    └── MongoConfig.java                      # MongoDB 配置
```

---

## 2. 核心数据模型

### 2.1 SettingNode（设定节点）

**文件路径**: `domain/model/setting/generation/SettingNode.java`

```java
@Data
@Builder
public class SettingNode {
    // 基础信息
    private String id;                    // 节点唯一标识
    private String parentId;              // 父节点ID（树形结构）
    private String name;                  // 节点名称
    private SettingType type;             // 设定类型（世界观/角色/情节等）
    private String description;           // 详细描述内容

    // 扩展属性
    private Map<String, Object> attributes;         // 自定义属性
    private Map<String, Object> strategyMetadata;   // 策略特定元数据

    // 生成追踪
    private GenerationStatus generationStatus;      // 生成状态
    private String errorMessage;                    // 错误信息
    private String generationPrompt;                // 使用的提示词

    // 树形结构
    private List<SettingNode> children;             // 子节点列表

    // 生成状态枚举
    public enum GenerationStatus {
        PENDING,        // 待生成
        GENERATING,     // 生成中
        COMPLETED,      // 已完成
        FAILED,         // 失败
        MODIFIED        // 已修改
    }
}
```

**设计亮点**:
- **树形结构**: 通过 `parentId` 和 `children` 实现多层级设定
- **元数据分离**: `attributes` 存储业务属性，`strategyMetadata` 存储策略相关数据
- **状态追踪**: 每个节点都有独立的生成状态，方便错误恢复

### 2.2 SettingGenerationSession（生成会话）

**文件路径**: `domain/model/setting/generation/SettingGenerationSession.java`

```java
@Data
@Builder
public class SettingGenerationSession {
    // 会话标识
    private String sessionId;             // 会话唯一ID
    private String userId;                // 用户ID
    private String novelId;               // 关联小说ID（可选）

    // 生成配置
    private String initialPrompt;         // 初始提示词
    private String strategy;              // 生成策略ID
    private String promptTemplateId;      // 提示词模板ID

    // 会话状态
    private SessionStatus status;         // 会话状态
    private boolean fromExistingHistory;  // 是否从历史创建
    private String sourceHistoryId;       // 源历史记录ID

    // 生成数据（内存临时存储）
    private Map<String, SettingNode> generatedNodes;  // 已生成节点
    private List<String> rootNodeIds;                 // 根节点ID列表

    // 时间戳
    private LocalDateTime createdAt;      // 创建时间
    private LocalDateTime updatedAt;      // 更新时间
    private LocalDateTime expiresAt;      // 过期时间

    // 元数据
    private Map<String, Object> metadata; // 会话元数据
    private String errorMessage;          // 错误信息

    // 会话状态枚举
    public enum SessionStatus {
        INITIALIZING,   // 初始化
        GENERATING,     // 生成中
        COMPLETED,      // 已完成
        ERROR,          // 错误
        CANCELLED,      // 已取消
        SAVED           // 已保存
    }
}
```

**核心方法**:

```java
// 添加节点
public void addNode(SettingNode node) {
    generatedNodes.put(node.getId(), node);
    if (node.getParentId() == null) {
        rootNodeIds.add(node.getId());
    }
}

// 删除节点及其所有子孙
public void removeNodeAndDescendants(String nodeId) {
    Set<String> toRemove = new HashSet<>();
    collectDescendants(nodeId, toRemove);
    toRemove.add(nodeId);

    toRemove.forEach(id -> {
        generatedNodes.remove(id);
        rootNodeIds.remove(id);
    });
}
```

### 2.3 NovelSettingHistory（历史快照）

**作用**: 保存用户每次生成的设定树版本，支持版本管理和恢复。

**关键字段**:
```java
- historyId: String              // 历史记录ID
- userId: String                 // 用户ID
- novelId: String (可选)         // 关联小说ID（独立快照时为null）
- snapshotName: String           // 快照名称
- strategyId: String             // 使用的策略ID
- rootSettings: List<String>     // 根设定ID列表
- createdAt: LocalDateTime       // 创建时间
- metadata: Map<String, Object>  // 元数据
```

**设计模式**: **快照模式** - 每次保存生成一个不可变的快照，保留完整的设定树结构。

---

## 3. AI 拆书工作流程

### 3.1 完整流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                   1. 用户上传小说 TXT                             │
└──────────────────────┬──────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│         2. TxtNovelParser 智能章节识别                            │
│    - 正则匹配: "第X章"、"Chapter N"、"序章"等                      │
│    - 备用策略: 基于空行和长度的启发式识别                           │
│    - 输出: List<ParsedSceneData>                                 │
└──────────────────────┬──────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│              3. ImportServiceImpl 保存到数据库                     │
│    - 创建 Novel 文档                                              │
│    - 为每章创建 Scene 文档                                         │
│    - 生成章节索引和元数据                                          │
└──────────────────────┬──────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│      4. 用户选择"番茄小说拆书"策略，发起 AI 分析请求                │
│    POST /api/v1/setting-generation/start                        │
│    Body: {                                                       │
│      "initialPrompt": "分析这本小说的核心设定",                    │
│      "promptTemplateId": "tomato-web-novel",                     │
│      "novelId": "xxx",                                           │
│      "modelConfigId": "gpt-4"                                    │
│    }                                                             │
└──────────────────────┬──────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│        5. SettingGenerationService 创建生成会话                   │
│    - 生成 sessionId                                              │
│    - 初始化 SettingGenerationSession                             │
│    - 选择策略: TomatoWebNovelStrategy                            │
└──────────────────────┬──────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│         6. TomatoWebNovelStrategy 执行生成策略                    │
│    Step 1: 构建系统提示词（内置番茄小说创作理念）                   │
│    Step 2: 构建用户提示词（包含小说内容摘要）                       │
│    Step 3: 调用 LLM 生成 11 个维度的设定                          │
│    Step 4: 解析 LLM 返回的 JSON 结构                              │
│    Step 5: 构建 SettingNode 树形结构                             │
└──────────────────────┬──────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│         7. SSE 事件流实时推送生成进度                              │
│    - NodeGeneratedEvent: 节点生成完成                             │
│    - GenerationProgressEvent: 进度更新                            │
│    - GenerationCompletedEvent: 全部完成                           │
└──────────────────────┬──────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│         8. 用户保存设定 & 自动创建历史快照                          │
│    POST /api/v1/setting-generation/{sessionId}/save             │
│    - 保存 SettingNode 到 MongoDB (settings 集合)                 │
│    - 创建 NovelSettingHistory 快照                               │
│    - 关联到 Novel 文档                                            │
└──────────────────────┬──────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│              9. 前端展示树形分析结果                               │
│    - 11 个根节点（核心卖点、主角设定等）                            │
│    - 每个节点包含详细描述和子节点                                   │
│    - 支持在线编辑、AI 续写、导出等功能                              │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 关键步骤详解

#### Step 2: TxtNovelParser 智能章节识别

**文件路径**: `service/impl/TxtNovelParser.java`

**章节标题正则表达式**:

```java
private static final Pattern CHAPTER_TITLE_PATTERN = Pattern.compile(
    "^\\s*(?:" +
        "(?:(?:正文|番外)(?:\\s+)?(?:第[一二三四五六七八九十百千万零〇\\d]+章)?)|" +
        "(?:序章|楔子|尾声|后记|(?:第[一二三四五六七八九十百千万零〇\\d]+[章卷节部回集]))|" +
        "(?:[\\(（【]?\\s*[一二三四五六七八九十百千万零〇\\d]+\\s*[\\)）】]?[\\s.、：:])|" +
        "(?:Chapter\\s+\\d+)|(?:[IVXLCDM]+)" +
    ")[\\s.、.:：]*(.*)$"
);
```

**支持的格式**:
- ✅ 中文正式: "第一章 初遇"、"第十五章 决战"
- ✅ 中文简化: "序章"、"楔子"、"尾声"、"后记"
- ✅ 数字括号: "(1) 开始"、"【2】崛起"
- ✅ 英文格式: "Chapter 1 Beginning"
- ✅ 罗马数字: "I"、"II"、"III"

**备用识别策略**:

```java
private ParsedSceneData createFallbackScene(String content, int index) {
    // 基于空行和段落长度的启发式识别
    String[] lines = content.split("\n");
    String potentialTitle = lines[0].trim();

    // 如果第一行短于50字，可能是标题
    if (potentialTitle.length() < 50) {
        return ParsedSceneData.builder()
            .title(potentialTitle)
            .content(content.substring(potentialTitle.length()).trim())
            .sequence(index)
            .build();
    }

    return ParsedSceneData.builder()
        .title("第 " + (index + 1) + " 部分")
        .content(content)
        .sequence(index)
        .build();
}
```

#### Step 6: TomatoWebNovelStrategy 执行生成

**文件路径**: `service/setting/generation/strategy/TomatoWebNovelStrategy.java`

**策略定义的 11 个分析维度**:

```java
@Override
public List<ElementDefinition> defineElements() {
    return Arrays.asList(
        // 1. 核心卖点（最高优先级）
        ElementDefinition.builder()
            .id("core_selling_point")
            .name("核心卖点")
            .description("一句话概括小说的最大吸引力点")
            .settingType(SettingType.THEME)
            .priority(1)
            .expectedOutputLength("50-80字")
            .build(),

        // 2. 主角设定
        ElementDefinition.builder()
            .id("protagonist_setting")
            .name("主角设定")
            .description("主角的身份背景、性格标签、初始困境")
            .settingType(SettingType.CHARACTER)
            .priority(2)
            .expectedOutputLength("100-200字")
            .children(Arrays.asList("identity", "personality", "initial_crisis"))
            .build(),

        // 3. 金手指系统（网文核心）
        ElementDefinition.builder()
            .id("cheat_system")
            .name("金手指系统")
            .description("主角的外挂、系统或核心优势")
            .settingType(SettingType.MAGIC_SYSTEM)
            .priority(3)
            .expectedOutputLength("150-250字")
            .children(Arrays.asList("mechanism", "growth_path", "usage_examples"))
            .build(),

        // 4. 世界观框架
        ElementDefinition.builder()
            .id("world_framework")
            .name("世界观框架")
            .description("故事发生的时代背景与底层规则")
            .settingType(SettingType.WORLD_SETTING)
            .priority(4)
            .expectedOutputLength("100-200字")
            .build(),

        // 5. 等级/力量体系
        ElementDefinition.builder()
            .id("power_system")
            .name("等级力量体系")
            .description("角色成长的分层体系与战力规则")
            .settingType(SettingType.MAGIC_SYSTEM)
            .priority(5)
            .expectedOutputLength("100-200字")
            .build(),

        // 6. 反派势力
        ElementDefinition.builder()
            .id("antagonist_forces")
            .name("反派势力")
            .description("敌对体系，层级递进的反派设计")
            .settingType(SettingType.CHARACTER)
            .priority(6)
            .expectedOutputLength("100-200字")
            .build(),

        // 7. 情感线设定
        ElementDefinition.builder()
            .id("romance_line")
            .name("情感线设定")
            .description("情感关系的发展路径")
            .settingType(SettingType.RELATIONSHIP)
            .priority(7)
            .expectedOutputLength("100-150字")
            .build(),

        // 8. 爽点布局（网文核心）
        ElementDefinition.builder()
            .id("satisfaction_points")
            .name("爽点布局")
            .description("打脸、反差、碾压、绝境翻盘等爽点设计")
            .settingType(SettingType.PLOT)
            .priority(8)
            .expectedOutputLength("150-250字")
            .children(Arrays.asList("chapter_1_10", "chapter_10_30", "chapter_30_plus"))
            .build(),

        // 9. 期待感钩子（网文核心）
        ElementDefinition.builder()
            .id("anticipation_hooks")
            .name("期待感钩子")
            .description("悬念、伏笔、预告等拉期待的设计")
            .settingType(SettingType.PLOT)
            .priority(9)
            .expectedOutputLength("150-250字")
            .build(),

        // 10. 支线剧情
        ElementDefinition.builder()
            .id("sub_plots")
            .name("支线剧情")
            .description("增强可读性的副线")
            .settingType(SettingType.PLOT)
            .priority(10)
            .expectedOutputLength("100-200字")
            .build(),

        // 11. 特色设定
        ElementDefinition.builder()
            .id("unique_features")
            .name("特色设定")
            .description("差异化卖点与母题")
            .settingType(SettingType.THEME)
            .priority(11)
            .expectedOutputLength("100-150字")
            .build()
    );
}
```

---

## 4. 番茄小说拆书策略详解

### 4.1 策略初始化

**文件路径**: `service/setting/generation/SystemStrategyInitializationService.java:324-374`

**系统提示词（AI 角色定位）**:

```
你是一位在番茄小说平台孵化多本爆款的白金大神作家兼策划。

核心理念（必须贯彻）：
- 金手指：独特且具成长性的优势/系统，避免平庸或单纯数值堆砌
- 爽点：反差、打脸、扮猪吃虎、绝境翻盘、信息差等，每隔几章必须有一波"大爽"
- 期待感：悬念、伏笔、信息差形成闭环，每一章都让读者想看下一章
- 网感：始终围绕"读者体验"与"商业化结果"思考

输出要求：
1. 严格遵循JSON Schema结构
2. 根节点（11个维度）每个50-80字精炼概括
3. 叶子节点（详细内容）每个100-200字深度阐述
4. 必须体现"拉期待—给爽点—再拉期待"的循环结构
5. 所有内容必须可落地执行，避免空洞理论
```

**用户提示词模板**:

```
小说创意或已有内容：
{{input}}

根节点清单（必须包含）：
1. 核心卖点：≤50字一句话说清最大吸引力
2. 主角设定：身份背景/性格标签、初始困境
3. 金手指系统：核心机理、成长路径、至少2个具体用法示例
4. 世界观框架：时代背景、底层规则、社会结构
5. 等级力量体系：分层体系、战力对比、晋升条件
6. 反派势力：至少3层递进反派、每层代表性角色
7. 情感线设定：女主/男主设定、感情发展阶段
8. 爽点布局：前3章内的第一个"大爽点"详细描述
9. 期待感钩子：前5章的核心悬念/伏笔
10. 支线剧情：至少2条副线，说明与主线的关联
11. 特色设定：区别于同类小说的差异化卖点

要求：
- 每个根节点生成独立的JSON对象
- 必须包含 id、name、description、children（如有）
- description 为核心内容，50-80字
- children 为子节点数组，每个100-200字
```

### 4.2 AI 生成流程

**Hybrid 流程（文本阶段 + 工具直通）**:

```java
// 1. 文本阶段：让 LLM 分析并规划设定结构
String textPhasePrompt = buildTextPhasePrompt(novelContent, userInput);
Mono<String> textResponse = chatLanguageModel.generate(textPhasePrompt);

// 2. 工具调用阶段：让 LLM 使用 Tool 输出结构化 JSON
Mono<Map<String, Object>> toolResponse = textResponse.flatMap(textResult -> {
    String toolPhasePrompt = buildToolPhasePrompt(textResult);
    return chatLanguageModel.generateWithTools(toolPhasePrompt, generateSettingTool);
});

// 3. 解析 Tool 返回的 JSON，构建 SettingNode 树
Mono<List<SettingNode>> settingTree = toolResponse.map(json -> {
    return parseJsonToSettingNodes(json, strategy.defineElements());
});
```

### 4.3 JSON Schema 定义

**Tool 定义**（供 LLM 调用）:

```json
{
  "name": "generate_setting_tree",
  "description": "生成结构化的小说设定树",
  "parameters": {
    "type": "object",
    "properties": {
      "root_nodes": {
        "type": "array",
        "description": "11个根节点的数组",
        "items": {
          "type": "object",
          "properties": {
            "id": { "type": "string", "description": "节点唯一标识，如 core_selling_point" },
            "name": { "type": "string", "description": "节点名称，如 核心卖点" },
            "description": { "type": "string", "description": "节点核心内容，50-80字" },
            "children": {
              "type": "array",
              "description": "子节点数组（可选）",
              "items": {
                "type": "object",
                "properties": {
                  "id": { "type": "string" },
                  "name": { "type": "string" },
                  "description": { "type": "string", "description": "子节点详细内容，100-200字" }
                },
                "required": ["id", "name", "description"]
              }
            }
          },
          "required": ["id", "name", "description"]
        }
      }
    },
    "required": ["root_nodes"]
  }
}
```

### 4.4 实际生成示例

**输入**:
```
小说创意：重生都市，系统加身，从小厨师逆袭成商业大亨
```

**AI 生成的 JSON**（简化版）:

```json
{
  "root_nodes": [
    {
      "id": "core_selling_point",
      "name": "核心卖点",
      "description": "重生+美食系统，30岁失败厨师重回20岁，用未来记忆+神级味觉系统，从街边小摊逆袭成餐饮帝国掌控者。"
    },
    {
      "id": "protagonist_setting",
      "name": "主角设定",
      "description": "林逸，30岁因餐厅倒闭跳楼，重生回20岁。性格：谨慎、有野心、擅长烹饪。",
      "children": [
        {
          "id": "identity",
          "name": "身份背景",
          "description": "出身贫困农村，父母欠债50万，在三流餐厅打工3年。重生后拥有未来10年的餐饮市场记忆。"
        },
        {
          "id": "personality",
          "name": "性格标签",
          "description": "外表低调内心骄傲，擅长隐藏实力，对食材有近乎偏执的追求，对仇人绝不手软。"
        },
        {
          "id": "initial_crisis",
          "name": "初始困境",
          "description": "重生当天，原餐厅老板因嫉妒陷害，面临被开除+赔偿10万的危机。三天后父亲住院需要30万手术费。"
        }
      ]
    },
    {
      "id": "cheat_system",
      "name": "金手指系统",
      "description": "【美食评鉴系统】：品尝任何食物后可复制并优化配方，获得'美食点数'解锁新技能。",
      "children": [
        {
          "id": "mechanism",
          "name": "核心机理",
          "description": "吃任何食物后，系统自动分析并生成'完美配方'。消耗美食点数可解锁：神级刀工、极致火候、食材溯源、味觉预判等能力。美食点数通过制作料理、顾客好评、击败对手获得。"
        },
        {
          "id": "growth_path",
          "name": "成长路径",
          "description": "LV1-LV3：初级厨师（复制家常菜）→ LV4-LV7：高级厨师（复制星级料理）→ LV8-LV10：美食大师（创造新菜系）→ LV10+：商业帝国（控制供应链）。"
        },
        {
          "id": "usage_1",
          "name": "开局爽点",
          "description": "第1章：被老板刁难做'佛跳墙'，用系统复制米其林三星配方，震惊全场，反手打脸老板，被五星酒店挖走。"
        },
        {
          "id": "usage_2",
          "name": "中期爽点",
          "description": "第30章：参加全国烹饪大赛，对手使用名贵食材，林逸用普通食材+系统优化，做出'化腐朽为神奇'的料理，逆转夺冠。"
        }
      ]
    },
    {
      "id": "satisfaction_points",
      "name": "爽点布局",
      "description": "第1-3章：打脸刁难老板，震惊同行；第10章：开店首日爆满，原老板求合作被拒；第30章：收购仇人餐饮集团。",
      "children": [
        {
          "id": "chapter_1_10",
          "name": "第1-10章爽点",
          "description": "第1章：系统复制佛跳墙打脸老板 → 第3章：五星酒店高薪挖角 → 第5章：初恋女友后悔求复合被拒 → 第8章：用一道菜征服美食评论家 → 第10章：自己开店首日排队500米。"
        },
        {
          "id": "chapter_10_30",
          "name": "第10-30章爽点",
          "description": "第15章：原老板餐厅倒闭求收购 → 第20章：击败米其林二星厨师 → 第25章：被餐饮协会特邀入会 → 第30章：全国大赛夺冠，成为最年轻的'国宴大师'。"
        }
      ]
    },
    {
      "id": "anticipation_hooks",
      "name": "期待感钩子",
      "description": "第1章结尾：系统提示'检测到传说级食材，距离XX公里'；第5章结尾：神秘老人说'你的味觉天赋，是我们组织寻找了30年的...'"
    }
    // ... 其他6个维度省略
  ]
}
```

---

## 5. API 接口完整说明

### 5.1 启动设定生成

**接口**: `POST /api/v1/setting-generation/start`

**请求体**:
```json
{
  "initialPrompt": "分析这本小说的核心设定",
  "promptTemplateId": "tomato-web-novel",
  "novelId": "67d67d6833335f5166782e6f",
  "modelConfigId": "gpt-4-config-id",
  "userId": "user-123",
  "usePublicTextModel": false
}
```

**参数说明**:
- `initialPrompt`: 用户输入的分析指令或小说创意
- `promptTemplateId`: 策略模板ID（如 `tomato-web-novel`）
- `novelId`: 小说ID（可选，如果是分析现有小说）
- `modelConfigId`: AI 模型配置ID（指定使用的 LLM）
- `userId`: 用户ID（开发环境可选，默认使用测试用户）
- `usePublicTextModel`: 是否在文本阶段使用公共模型（省钱）

**响应**: SSE 事件流

```
event: SessionCreatedEvent
data: {"sessionId":"session-123","status":"INITIALIZING"}

event: GenerationProgressEvent
data: {"sessionId":"session-123","progress":10,"currentStep":"分析小说内容"}

event: NodeGeneratedEvent
data: {
  "sessionId":"session-123",
  "node":{
    "id":"core_selling_point",
    "name":"核心卖点",
    "description":"重生+美食系统，30岁失败厨师重回20岁..."
  }
}

event: NodeGeneratedEvent
data: {
  "sessionId":"session-123",
  "node":{
    "id":"protagonist_setting",
    "name":"主角设定",
    "description":"林逸，30岁因餐厅倒闭跳楼...",
    "children":[...]
  }
}

... (共11个 NodeGeneratedEvent)

event: GenerationCompletedEvent
data: {"sessionId":"session-123","totalNodes":11,"message":"设定生成完成"}

event: complete
data: {"data":"[DONE]"}
```

**事件类型**:
- `SessionCreatedEvent`: 会话创建成功
- `GenerationProgressEvent`: 进度更新（10%, 20%, ...100%）
- `NodeGeneratedEvent`: 单个节点生成完成
- `GenerationCompletedEvent`: 全部生成完成
- `GenerationErrorEvent`: 生成错误（recoverable=true 时客户端不应显示）
- `complete`: SSE 连接结束标志

### 5.2 保存生成的设定

**接口**: `POST /api/v1/setting-generation/{sessionId}/save`

**请求体**:
```json
{
  "novelId": "67d67d6833335f5166782e6f",
  "updateExisting": false,
  "targetHistoryId": null
}
```

**参数说明**:
- `novelId`: 保存到哪个小说（可选，为 null 时保存为独立快照）
- `updateExisting`: 是否更新现有历史记录（true=更新，false=新建）
- `targetHistoryId`: 目标历史记录ID（updateExisting=true 时必填）

**响应**:
```json
{
  "code": 200,
  "data": {
    "success": true,
    "message": "设定已成功保存，并已创建历史记录",
    "rootSettingIds": [
      "setting-001",
      "setting-002",
      // ... 11个根设定ID
    ],
    "historyId": "history-20251026-001"
  }
}
```

**后端处理流程**:
1. 从会话中获取所有 `SettingNode`
2. 保存每个节点到 MongoDB `settings` 集合
3. 如果有 `novelId`，关联到 Novel 文档
4. **自动创建** `NovelSettingHistory` 快照
5. 清理会话（可选，保留一段时间供查看）

### 5.3 修改设定节点（AI 增强）

**接口**: `POST /api/v1/setting-generation/{sessionId}/update-node`

**请求体**:
```json
{
  "nodeId": "core_selling_point",
  "modificationPrompt": "核心卖点改为：加入修仙元素，主角不仅会做饭还能炼丹",
  "modelConfigId": "gpt-4-config-id",
  "scope": "self_and_children",
  "publicModel": false,
  "publicModelConfigId": null
}
```

**参数说明**:
- `nodeId`: 要修改的节点ID
- `modificationPrompt`: 修改指令（AI 会根据指令重新生成）
- `modelConfigId`: 模型配置ID
- `scope`: 修改范围
  - `self`: 仅修改当前节点
  - `children_only`: 仅修改子节点
  - `self_and_children`: 修改当前节点及其所有子节点
- `publicModel`: 是否使用公共模型（省钱）
- `publicModelConfigId`: 公共模型配置ID

**响应**: SSE 事件流（同 start 接口）

### 5.4 整体调整会话

**接口**: `POST /api/v1/setting-generation/{sessionId}/adjust`

**用途**: 在不破坏现有层级结构的前提下，对整个设定树进行整体调整。

**请求体**:
```json
{
  "adjustmentPrompt": "将整体风格从'热血爽文'调整为'智斗谋略'，降低打脸情节，增加商战智谋",
  "modelConfigId": "gpt-4-config-id",
  "promptTemplateId": "tomato-web-novel"
}
```

**后端处理**:
```java
// 1. 读取当前会话的所有节点
Map<String, SettingNode> currentNodes = session.getGeneratedNodes();

// 2. 构建"调整提示词"（包含现有结构）
String enhancedPrompt =
    "请在不破坏现有层级结构与父子关联关系的前提下，对设定进行整体调整。" +
    "保留节点的层级与引用关系（使用名称/路径表达），避免包含任何UUID或无意义的内部ID。" +
    "\n当前设定结构：\n" + serializeNodesToText(currentNodes) +
    "\n\n调整说明：\n" + request.getAdjustmentPrompt();

// 3. 调用 LLM 重新生成（保持ID不变，仅更新description）
Mono<Map<String, SettingNode>> adjustedNodes =
    chatLanguageModel.generateWithTools(enhancedPrompt, adjustSettingTool);

// 4. 合并到会话（更新现有节点，不删除）
adjustedNodes.subscribe(nodes -> {
    nodes.forEach((id, node) -> {
        if (session.getGeneratedNodes().containsKey(id)) {
            session.getGeneratedNodes().get(id).setDescription(node.getDescription());
            session.getGeneratedNodes().get(id).setGenerationStatus(GenerationStatus.MODIFIED);
        }
    });
});
```

### 5.5 开始写作（关联小说）

**接口**: `POST /api/v1/setting-generation/start-writing`

**请求体**:
```json
{
  "sessionId": "session-123",
  "novelId": "novel-456",
  "historyId": "history-789",
  "fork": true,
  "reuseNovel": false
}
```

**参数说明**:
- `sessionId`: 会话ID（优先使用）
- `novelId`: 明确指定的小说ID（可选）
- `historyId`: 历史记录ID（如果是从历史快照开始写作）
- `fork`: 是否创建新小说（true=新建，false=复用）
- `reuseNovel`: 是否复用会话中的 novelId（已废弃，被 fork 取代）

**优先级逻辑**:
```
1. 请求体中的 novelId（最高优先级）
2. 会话中的 novelId
3. 根据 fork 参数决定：
   - fork=true → 创建新草稿小说
   - fork=false → 创建新草稿小说（不再使用历史记录的 novelId）
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "novelId": "novel-456"
  }
}
```

**后端处理流程**（SettingComposeService.orchestrateStartWriting）:

```java
public Mono<String> orchestrateStartWriting(
    String userId, String username,
    String sessionId, String novelId, String historyId
) {
    return Mono.defer(() -> {
        // 1. 确定数据源（会话 or 历史记录）
        if (sessionId != null && !sessionId.isBlank()) {
            return sessionManager.getSession(sessionId)
                .flatMap(session -> {
                    // 检查会话是否完成
                    if (session.getStatus() != SessionStatus.COMPLETED) {
                        return Mono.error(new IllegalStateException(
                            "Session not completed: " + sessionId
                        ));
                    }
                    // 保存设定到小说
                    return saveSessionSettings(session, novelId);
                });
        } else if (historyId != null && !historyId.isBlank()) {
            // 从历史记录加载设定
            return historyService.getHistory(historyId)
                .flatMap(history -> loadHistorySettings(history, novelId));
        } else {
            return Mono.error(new IllegalArgumentException(
                "必须提供 sessionId 或 historyId"
            ));
        }
    }).map(savedNovelId -> {
        // 2. 标记小说为"已就绪"
        return novelService.updateNovelStatus(savedNovelId, true)
            .thenReturn(savedNovelId);
    }).flatMap(id -> id);
}
```

### 5.6 获取会话状态

**接口**: `GET /api/v1/setting-generation/{sessionId}/status`

**响应**:
```json
{
  "code": 200,
  "data": {
    "sessionId": "session-123",
    "status": "GENERATING",
    "progress": 45,
    "currentStep": "正在生成爽点布局",
    "totalSteps": 11,
    "errorMessage": null
  }
}
```

### 5.7 轻量状态查询

**接口**: `GET /api/v1/setting-generation/status-lite/{id}`

**用途**: 快速判断一个 ID 是会话还是历史记录。

**响应**:
```json
{
  "code": 200,
  "data": {
    "exists": true,
    "type": "session",  // 或 "history"
    "status": "COMPLETED",
    "hasNovel": true,
    "novelId": "novel-456"
  }
}
```

---

## 6. 前后端交互流程

### 6.1 前端订阅 SSE 事件

**前端代码示例**（JavaScript/TypeScript）:

```typescript
// 1. 创建 SSE 连接
const eventSource = new EventSource(
  '/api/v1/setting-generation/start',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      initialPrompt: '分析这本小说的核心设定',
      promptTemplateId: 'tomato-web-novel',
      novelId: novelId,
      modelConfigId: modelConfigId
    })
  }
);

// 2. 监听不同类型的事件
eventSource.addEventListener('SessionCreatedEvent', (e) => {
  const data = JSON.parse(e.data);
  console.log('会话已创建:', data.sessionId);
  setSessionId(data.sessionId);
});

eventSource.addEventListener('GenerationProgressEvent', (e) => {
  const data = JSON.parse(e.data);
  console.log('生成进度:', data.progress);
  setProgress(data.progress);
  setCurrentStep(data.currentStep);
});

eventSource.addEventListener('NodeGeneratedEvent', (e) => {
  const data = JSON.parse(e.data);
  console.log('节点已生成:', data.node.name);

  // 实时更新树形结构
  setSettingTree(prevTree => {
    if (data.node.parentId) {
      // 子节点：添加到父节点的 children
      return addChildNode(prevTree, data.node.parentId, data.node);
    } else {
      // 根节点：直接添加
      return [...prevTree, data.node];
    }
  });
});

eventSource.addEventListener('GenerationCompletedEvent', (e) => {
  const data = JSON.parse(e.data);
  console.log('生成完成，共', data.totalNodes, '个节点');
  setIsGenerating(false);
});

eventSource.addEventListener('GenerationErrorEvent', (e) => {
  const data = JSON.parse(e.data);
  if (!data.recoverable) {
    console.error('生成失败:', data.errorMessage);
    setError(data.errorMessage);
    eventSource.close();
  }
});

eventSource.addEventListener('complete', (e) => {
  console.log('SSE 连接关闭');
  eventSource.close();
});

// 3. 错误处理
eventSource.onerror = (err) => {
  console.error('SSE 连接错误:', err);
  eventSource.close();
};
```

### 6.2 前端展示设定树

**推荐 UI 库**: Ant Design Tree / Element Plus Tree

```vue
<template>
  <div class="setting-tree-container">
    <!-- 进度条 -->
    <a-progress
      v-if="isGenerating"
      :percent="progress"
      :status="error ? 'exception' : 'active'"
      :format="() => currentStep"
    />

    <!-- 树形结构 -->
    <a-tree
      v-if="!isGenerating"
      :tree-data="settingTree"
      :field-names="{
        title: 'name',
        key: 'id',
        children: 'children'
      }"
      show-line
      :show-icon="true"
      default-expand-all
    >
      <template #title="{ name, description }">
        <div class="tree-node">
          <span class="node-name">{{ name }}</span>
          <a-tooltip :title="description">
            <info-circle-outlined class="node-icon" />
          </a-tooltip>
        </div>
      </template>
    </a-tree>

    <!-- 详情面板 -->
    <a-drawer
      v-model:visible="showNodeDetail"
      title="节点详情"
      width="600"
    >
      <div v-if="selectedNode">
        <h3>{{ selectedNode.name }}</h3>
        <a-typography-paragraph>
          {{ selectedNode.description }}
        </a-typography-paragraph>

        <!-- 编辑按钮 -->
        <a-space>
          <a-button @click="editNode">
            <edit-outlined /> 手动编辑
          </a-button>
          <a-button @click="aiModifyNode">
            <robot-outlined /> AI 修改
          </a-button>
        </a-space>
      </div>
    </a-drawer>

    <!-- 保存按钮 -->
    <div class="action-bar">
      <a-button
        type="primary"
        size="large"
        :loading="isSaving"
        @click="saveSettings"
      >
        保存设定
      </a-button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

const settingTree = ref([]);
const isGenerating = ref(false);
const progress = ref(0);
const currentStep = ref('');
const error = ref(null);
const selectedNode = ref(null);
const showNodeDetail = ref(false);

// 添加子节点到树形结构
function addChildNode(tree, parentId, childNode) {
  return tree.map(node => {
    if (node.id === parentId) {
      return {
        ...node,
        children: [...(node.children || []), childNode]
      };
    } else if (node.children) {
      return {
        ...node,
        children: addChildNode(node.children, parentId, childNode)
      };
    }
    return node;
  });
}

// 保存设定
async function saveSettings() {
  isSaving.value = true;
  try {
    const response = await fetch(
      `/api/v1/setting-generation/${sessionId.value}/save`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          novelId: novelId.value,
          updateExisting: false
        })
      }
    );
    const result = await response.json();
    if (result.code === 200) {
      message.success('设定已保存');
      historyId.value = result.data.historyId;
    }
  } catch (err) {
    message.error('保存失败: ' + err.message);
  } finally {
    isSaving.value = false;
  }
}
</script>
```

### 6.3 前端修改节点（AI 增强）

```typescript
// AI 修改节点
async function aiModifyNode() {
  const modificationPrompt = await showPromptModal();

  const eventSource = new EventSource(
    `/api/v1/setting-generation/${sessionId}/update-node`,
    {
      method: 'POST',
      body: JSON.stringify({
        nodeId: selectedNode.value.id,
        modificationPrompt: modificationPrompt,
        modelConfigId: modelConfigId,
        scope: 'self_and_children'
      })
    }
  );

  eventSource.addEventListener('NodeGeneratedEvent', (e) => {
    const data = JSON.parse(e.data);
    // 更新节点内容
    updateNodeInTree(data.node);
  });

  eventSource.addEventListener('complete', () => {
    message.success('修改完成');
    eventSource.close();
  });
}
```

---

## 7. 提示词工程详解

### 7.1 提示词模板变量

**系统支持的变量**:

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `{{input}}` | 用户输入的创意或指令 | "分析这本小说的核心设定" |
| `{{novel_content}}` | 小说内容（前 N 章摘要） | "第一章：林逸重生到20岁..." |
| `{{novel_title}}` | 小说标题 | "重生之美食系统" |
| `{{novel_genre}}` | 小说类型 | "都市重生" |
| `{{user_preferences}}` | 用户偏好设置 | "喜欢爽文风格" |
| `{{existing_settings}}` | 现有设定内容（编辑模式） | 已生成的设定树JSON |

### 7.2 番茄小说策略提示词完整版

**系统提示词**（324-350 行）:

```
你是一位在番茄小说平台孵化多本爆款的白金大神作家兼策划。你的核心能力是：
1. 深刻理解网文读者心理与付费逻辑
2. 精通"金手指-爽点-期待感"三位一体的节奏设计
3. 擅长将抽象创意转化为可执行的章节大纲与设定体系

核心理念（必须贯彻）：
- 金手指：独特且具成长性的优势/系统，避免平庸或单纯数值堆砌。必须有"用法示例"而非空洞描述。
- 爽点：反差、打脸、扮猪吃虎、绝境翻盘、信息差、碾压等。每隔几章必须有一波"大爽"，小爽点穿插。
- 期待感：悬念、伏笔、信息差形成闭环，每一章都让读者想看下一章。前几章必须埋下"长线钩子"（如终极反派、隐藏身份、世界真相等）。
- 网感：始终围绕"读者体验"与"商业化结果"思考，而非文学性或艺术性。

输出要求：
1. 严格遵循JSON Schema结构，不得偏离
2. 根节点（11个维度）每个50-80字精炼概括，突出核心卖点
3. 叶子节点（详细内容）每个100-200字深度阐述，必须包含具体示例
4. 必须体现"拉期待—给爽点—再拉期待"的循环结构
5. 所有内容必须可落地执行，避免"需要深入挖掘"之类的空洞理论
6. 反派/情感线/支线等必须有层级递进，不能一笔带过

禁止行为：
- 生成与网文商业逻辑脱节的"文学化"设定
- 使用模糊词汇（"可能"、"也许"、"或许"）
- 重复已有网文的套路而不加创新
- 忽略"爽点密度"与"期待感钩子"的布局
```

**用户提示词**（351-374 行）:

```
小说创意或已有内容：
{{input}}

{{#if novel_content}}
小说前几章内容摘要：
{{novel_content}}
{{/if}}

根节点清单（必须包含，顺序不可变）：
1. 核心卖点（core_selling_point）：≤50字一句话说清最大吸引力点，必须包含"差异化元素"
2. 主角设定（protagonist_setting）：身份背景/性格标签、初始困境，必须有"反差感"
   - 子节点：identity（身份背景）、personality（性格标签）、initial_crisis（初始困境）
3. 金手指系统（cheat_system）：核心机理、成长路径、至少2个具体用法示例
   - 子节点：mechanism（核心机理）、growth_path（成长路径）、usage_1（开局爽点）、usage_2（中期爽点）
4. 世界观框架（world_framework）：时代背景、底层规则、社会结构，必须为"力量体系"铺垫
5. 等级力量体系（power_system）：分层体系、战力对比、晋升条件，必须有"阶层跨越爽点"
6. 反派势力（antagonist_forces）：至少3层递进反派（小BOSS→中BOSS→终极BOSS），每层代表性角色
   - 子节点：tier_1（前期反派）、tier_2（中期反派）、tier_3（后期反派）
7. 情感线设定（romance_line）：女主/男主设定、感情发展阶段（初遇→暧昧→确认→虐恋→圆满）
   - 子节点：heroine（女主设定）、stages（发展阶段）
8. 爽点布局（satisfaction_points）：前3章内的第一个"大爽点"详细描述，10-30章爽点规划
   - 子节点：chapter_1_10（前期爽点）、chapter_10_30（中期爽点）
9. 期待感钩子（anticipation_hooks）：前5章的核心悬念/伏笔，必须形成"问题链"
10. 支线剧情（sub_plots）：至少2条副线，说明与主线的关联与交织点
    - 子节点：subplot_1（副线1）、subplot_2（副线2）
11. 特色设定（unique_features）：区别于同类小说的差异化卖点，必须有"记忆点"

输出格式要求：
- 使用 generate_setting_tree 工具输出结构化JSON
- 每个节点必须包含：id、name、description、children（如有）
- description 为核心内容，根节点50-80字，叶子节点100-200字
- 所有子节点必须在 children 数组中，不得遗漏
- 必须包含所有11个根节点，不得擅自合并或删减

特别提醒：
- 番茄小说读者偏好"快节奏+高爽点密度"，前3章必须有至少2个爽点
- 金手指必须"独特+可成长+有具体用法"，不能只是"系统赋予能力"这种泛泛而谈
- 反派必须有"层级递进"，不能一开始就是"宇宙级大BOSS"
- 情感线不能"无脑倒贴"，必须有"追妻火葬场"或"误会虐恋"等情感张力
```

### 7.3 提示词优化技巧

**技巧 1: 使用"角色扮演"增强 AI 理解**

```
✅ 好的提示词：
"你是一位在番茄小说平台孵化多本爆款的白金大神作家兼策划。"

❌ 差的提示词：
"你是一个AI助手，帮我分析小说。"
```

**技巧 2: 使用"禁止行为"减少错误输出**

```
✅ 好的提示词：
"禁止使用模糊词汇（'可能'、'也许'、'或许'）"

❌ 差的提示词：
（不提及禁止行为，导致 AI 输出不确定内容）
```

**技巧 3: 使用"具体示例"引导输出格式**

```
✅ 好的提示词：
"金手指系统示例：
- mechanism: '吃任何食物后，系统自动分析并生成完美配方...'
- usage_1: '第1章：被老板刁难做佛跳墙，用系统复制米其林三星配方...'"

❌ 差的提示词：
"请生成金手指系统的详细描述。"
```

**技巧 4: 使用"Chain-of-Thought"提升复杂推理**

```
✅ 好的提示词：
"请按以下步骤思考：
1. 分析小说的核心冲突是什么？
2. 主角需要什么能力才能解决冲突？
3. 这个能力如何设计才能既独特又合理？
4. 最终输出金手指系统的设定。"

❌ 差的提示词：
"生成金手指系统。"
```

---

## 8. 数据持久化机制

### 8.1 MongoDB 集合设计

**集合清单**:

| 集合名 | 说明 | 关键字段 |
|--------|------|---------|
| `novels` | 小说主文档 | _id, title, author, settings[] |
| `scenes` | 场景/章节文档 | _id, novelId, chapterId, content |
| `settings` | 设定节点文档 | _id, novelId, type, parentId, children[] |
| `novel_setting_histories` | 设定历史快照 | _id, userId, novelId, rootSettings[], createdAt |
| `ai_requests` | AI 请求日志 | _id, userId, model, inputTokens, cost |
| `users` | 用户信息 | _id, username, credits |

### 8.2 Settings 集合 Schema

**文档结构**:

```json
{
  "_id": "setting-001",
  "novelId": "novel-123",
  "userId": "user-456",
  "name": "核心卖点",
  "type": "THEME",
  "description": "重生+美食系统，30岁失败厨师重回20岁...",
  "parentId": null,
  "children": [
    "setting-002",
    "setting-003"
  ],
  "attributes": {
    "priority": 1,
    "elementId": "core_selling_point"
  },
  "strategyMetadata": {
    "strategyId": "tomato-web-novel",
    "expectedLength": "50-80字",
    "generatedBy": "gpt-4"
  },
  "version": 1,
  "createdAt": "2025-10-26T10:00:00Z",
  "updatedAt": "2025-10-26T10:00:00Z"
}
```

**索引设计**:

```javascript
// 复合索引：按小说查询所有设定
db.settings.createIndex({ "novelId": 1, "parentId": 1 });

// 用户索引：查询用户的所有设定
db.settings.createIndex({ "userId": 1, "createdAt": -1 });

// 类型索引：按类型筛选
db.settings.createIndex({ "type": 1 });

// 全文搜索索引
db.settings.createIndex({
  "name": "text",
  "description": "text"
});
```

### 8.3 Novel Setting History Schema

**文档结构**:

```json
{
  "_id": "history-20251026-001",
  "userId": "user-456",
  "novelId": "novel-123",
  "snapshotName": "初版设定",
  "strategyId": "tomato-web-novel",
  "promptTemplateId": "template-001",
  "rootSettings": [
    "setting-001",
    "setting-011",
    "setting-021"
    // ... 11个根设定ID
  ],
  "metadata": {
    "totalNodes": 43,
    "strategyVersion": "v1.0",
    "modelUsed": "gpt-4",
    "generationTime": "2025-10-26T10:00:00Z"
  },
  "createdAt": "2025-10-26T10:05:00Z"
}
```

**查询示例**:

```java
// 1. 查询用户的所有历史记录
Flux<NovelSettingHistory> histories = historyRepository
    .findByUserIdOrderByCreatedAtDesc(userId);

// 2. 查询小说的所有历史记录（版本管理）
Flux<NovelSettingHistory> novelHistories = historyRepository
    .findByNovelIdOrderByCreatedAtDesc(novelId);

// 3. 加载历史记录的完整设定树
Mono<List<SettingNode>> loadHistorySettings(String historyId) {
    return historyRepository.findById(historyId)
        .flatMapMany(history ->
            Flux.fromIterable(history.getRootSettings())
        )
        .flatMap(settingId -> settingRepository.findById(settingId))
        .collectList();
}
```

### 8.4 响应式持久化流程

**保存会话到数据库**:

```java
@Transactional
public Mono<List<String>> saveSessionSettings(
    String sessionId,
    String novelId
) {
    return sessionManager.getSession(sessionId)
        .flatMapMany(session -> {
            // 1. 获取所有根节点
            List<String> rootNodeIds = session.getRootNodeIds();

            // 2. 递归保存所有节点（深度优先）
            return Flux.fromIterable(rootNodeIds)
                .flatMap(rootId -> {
                    SettingNode rootNode = session.getGeneratedNodes().get(rootId);
                    return saveNodeRecursively(rootNode, novelId, null);
                });
        })
        .collectList()
        .flatMap(savedIds -> {
            // 3. 创建历史快照
            return createHistorySnapshot(sessionId, novelId, savedIds)
                .thenReturn(savedIds);
        });
}

// 递归保存节点及其子节点
private Mono<String> saveNodeRecursively(
    SettingNode node,
    String novelId,
    String parentId
) {
    // 1. 保存当前节点
    Setting setting = Setting.builder()
        .novelId(novelId)
        .name(node.getName())
        .type(node.getType())
        .description(node.getDescription())
        .parentId(parentId)
        .attributes(node.getAttributes())
        .strategyMetadata(node.getStrategyMetadata())
        .build();

    return settingRepository.save(setting)
        .flatMap(savedSetting -> {
            // 2. 递归保存所有子节点
            if (node.getChildren() != null && !node.getChildren().isEmpty()) {
                return Flux.fromIterable(node.getChildren())
                    .flatMap(child ->
                        saveNodeRecursively(child, novelId, savedSetting.getId())
                    )
                    .collectList()
                    .flatMap(childIds -> {
                        // 3. 更新父节点的 children 字段
                        savedSetting.setChildren(childIds);
                        return settingRepository.save(savedSetting);
                    })
                    .map(Setting::getId);
            }
            return Mono.just(savedSetting.getId());
        });
}
```

---

## 9. 扩展开发指南

### 9.1 如何添加新的拆书策略

**步骤 1: 创建策略类**

```java
// 文件路径: service/setting/generation/strategy/QidianFantasyStrategy.java
@Component
public class QidianFantasyStrategy implements ISettingGenerationStrategy {

    @Override
    public String getStrategyId() {
        return "qidian-fantasy";
    }

    @Override
    public String getStrategyName() {
        return "起点玄幻策略";
    }

    @Override
    public String getDescription() {
        return "专为起点玄幻小说设计的拆书分析策略，侧重修炼体系、宗门势力、天材地宝等元素";
    }

    @Override
    public List<ElementDefinition> defineElements() {
        return Arrays.asList(
            ElementDefinition.builder()
                .id("cultivation_system")
                .name("修炼体系")
                .description("境界划分、突破条件、战力对比")
                .settingType(SettingType.MAGIC_SYSTEM)
                .priority(1)
                .expectedOutputLength("200-300字")
                .children(Arrays.asList("realms", "breakthrough", "power_comparison"))
                .build(),

            ElementDefinition.builder()
                .id("sect_forces")
                .name("宗门势力")
                .description("主要宗门、势力关系、地盘划分")
                .settingType(SettingType.FACTION)
                .priority(2)
                .expectedOutputLength("200-300字")
                .build(),

            // ... 其他8-10个维度
        );
    }

    @Override
    public String buildSystemPrompt(Map<String, Object> context) {
        return """
            你是一位起点玄幻小说的资深编辑，擅长分析修真体系和世界观设定。

            核心理念：
            - 修炼体系必须"层级分明+合理递进"
            - 宗门势力必须"有等级+有矛盾"
            - 天材地宝必须"稀缺+有用+有争夺"
            - 主角机缘必须"合理+爽点+推动剧情"

            输出要求：
            1. 严格遵循 JSON Schema 结构
            2. 修炼境界至少5个大境界，每个大境界3个小境界
            3. 宗门势力至少3个层级（小宗门→大宗门→圣地）
            4. 所有设定必须相互关联，形成完整世界观
            """;
    }

    @Override
    public String buildUserPrompt(String userInput, Map<String, Object> context) {
        StringBuilder prompt = new StringBuilder();
        prompt.append("小说创意或内容：\n");
        prompt.append(userInput).append("\n\n");

        if (context.containsKey("novel_content")) {
            prompt.append("小说前几章内容：\n");
            prompt.append(context.get("novel_content")).append("\n\n");
        }

        prompt.append("根节点清单（必须包含）：\n");
        prompt.append("1. 修炼体系（cultivation_system）\n");
        prompt.append("2. 宗门势力（sect_forces）\n");
        // ... 其他维度

        return prompt.toString();
    }
}
```

**步骤 2: 注册策略到系统**

```java
// 文件路径: service/setting/generation/SystemStrategyInitializationService.java
@Service
public class SystemStrategyInitializationService {

    private final QidianFantasyStrategy qidianFantasyStrategy;

    @PostConstruct
    public void initializeSystemStrategies() {
        // 注册番茄小说策略
        registerStrategy(tomatoWebNovelStrategy);

        // 注册起点玄幻策略（新增）
        registerStrategy(qidianFantasyStrategy);
    }

    private Mono<Void> registerStrategy(ISettingGenerationStrategy strategy) {
        // 1. 创建提示词模板
        EnhancedUserPromptTemplate template = EnhancedUserPromptTemplate.builder()
            .name(strategy.getStrategyName())
            .description(strategy.getDescription())
            .category("system")
            .content(strategy.buildUserPrompt("{{input}}", Map.of()))
            .systemPrompt(strategy.buildSystemPrompt(Map.of()))
            .isPublic(true)
            .build();

        // 2. 设置生成配置
        SettingGenerationConfig config = new SettingGenerationConfig();
        config.setStrategyId(strategy.getStrategyId());
        config.setExpectedRootNodes(strategy.defineElements().size());
        config.setMaxDepth(3);

        template.setSettingGenerationConfig(config);

        // 3. 保存到数据库
        return promptTemplateRepository.save(template).then();
    }
}
```

**步骤 3: 前端调用新策略**

```typescript
// 前端选择策略
const strategies = await fetchStrategies();
// 返回: [
//   { id: 'tomato-web-novel', name: '番茄小说策略' },
//   { id: 'qidian-fantasy', name: '起点玄幻策略' }
// ]

// 用户选择后发起请求
startGeneration({
  initialPrompt: '分析这本修真小说',
  promptTemplateId: 'qidian-fantasy',
  novelId: novelId,
  modelConfigId: modelConfigId
});
```

### 9.2 如何集成新的 AI 模型

**步骤 1: 创建模型提供者**

```java
// 文件路径: service/ai/DeepSeekModelProvider.java
@Component
public class DeepSeekModelProvider implements AIModelProvider {

    @Value("${ai.deepseek.api-key}")
    private String apiKey;

    @Value("${ai.deepseek.base-url}")
    private String baseUrl;

    @Override
    public String getProviderId() {
        return "deepseek";
    }

    @Override
    public Mono<String> generate(String prompt, Map<String, Object> params) {
        // 实现 DeepSeek API 调用
        return webClient.post()
            .uri(baseUrl + "/chat/completions")
            .header("Authorization", "Bearer " + apiKey)
            .bodyValue(buildRequestBody(prompt, params))
            .retrieve()
            .bodyToMono(DeepSeekResponse.class)
            .map(response -> response.getChoices().get(0).getMessage().getContent());
    }

    @Override
    public Flux<String> generateStream(String prompt, Map<String, Object> params) {
        // 实现流式响应
        return webClient.post()
            .uri(baseUrl + "/chat/completions")
            .header("Authorization", "Bearer " + apiKey)
            .bodyValue(buildRequestBody(prompt, params, true))
            .retrieve()
            .bodyToFlux(ServerSentEvent.class)
            .map(sse -> parseStreamChunk(sse.data()));
    }

    private Map<String, Object> buildRequestBody(
        String prompt,
        Map<String, Object> params,
        boolean stream
    ) {
        return Map.of(
            "model", params.getOrDefault("model", "deepseek-chat"),
            "messages", List.of(Map.of("role", "user", "content", prompt)),
            "temperature", params.getOrDefault("temperature", 0.7),
            "max_tokens", params.getOrDefault("max_tokens", 2000),
            "stream", stream
        );
    }
}
```

**步骤 2: 注册到配置**

```java
// 文件路径: config/ChatLanguageModelConfig.java
@Configuration
public class ChatLanguageModelConfig {

    private final DeepSeekModelProvider deepSeekProvider;

    @Bean
    public ChatLanguageModel chatLanguageModel(
        @Value("${ai.default-provider}") String defaultProvider
    ) {
        return switch (defaultProvider) {
            case "openai" -> openAIProvider.createModel();
            case "anthropic" -> anthropicProvider.createModel();
            case "deepseek" -> deepSeekProvider.createModel(); // 新增
            default -> throw new IllegalArgumentException("Unknown provider: " + defaultProvider);
        };
    }
}
```

**步骤 3: 配置文件**

```yaml
# application.yml
ai:
  default-provider: deepseek
  deepseek:
    api-key: ${DEEPSEEK_API_KEY}
    base-url: https://api.deepseek.com/v1
    model: deepseek-chat
    temperature: 0.7
    max-tokens: 4000
```

### 9.3 如何添加自动爬虫功能

**⚠️ 法律风险警告**: 爬取番茄小说等平台的内容可能违反版权法，仅供个人学习使用，不得用于商业用途。

**步骤 1: 创建爬虫服务**

```java
// 文件路径: service/crawler/NovelCrawlerService.java
@Service
public class NovelCrawlerService {

    private final WebClient webClient;

    /**
     * 爬取番茄小说热门榜单
     *
     * ⚠️ 仅供学习参考，实际使用需获得授权
     */
    public Mono<List<NovelMetadata>> crawlTomatoHotList() {
        return webClient.get()
            .uri("https://fanqienovel.com/page/热门榜单")
            .retrieve()
            .bodyToMono(String.class)
            .map(html -> parseHotList(html));
    }

    /**
     * 爬取小说章节内容
     */
    public Mono<String> crawlNovelContent(String novelUrl) {
        return webClient.get()
            .uri(novelUrl)
            .retrieve()
            .bodyToMono(String.class)
            .map(html -> extractContent(html));
    }

    private List<NovelMetadata> parseHotList(String html) {
        // 使用 Jsoup 解析 HTML
        Document doc = Jsoup.parse(html);
        Elements novelElements = doc.select(".novel-item");

        return novelElements.stream()
            .map(element -> NovelMetadata.builder()
                .title(element.select(".title").text())
                .author(element.select(".author").text())
                .url(element.select("a").attr("href"))
                .description(element.select(".description").text())
                .build())
            .collect(Collectors.toList());
    }

    private String extractContent(String html) {
        Document doc = Jsoup.parse(html);
        Elements chapters = doc.select(".chapter-content");

        StringBuilder content = new StringBuilder();
        chapters.forEach(chapter -> {
            content.append(chapter.text()).append("\n\n");
        });

        return content.toString();
    }
}
```

**步骤 2: 创建定时任务**

```java
// 文件路径: task/scheduler/NovelCrawlerScheduler.java
@Component
@EnableScheduling
public class NovelCrawlerScheduler {

    private final NovelCrawlerService crawlerService;
    private final ImportServiceImpl importService;

    /**
     * 每天凌晨 2 点爬取热门榜单
     */
    @Scheduled(cron = "0 0 2 * * ?")
    public void crawlDailyHotList() {
        log.info("开始爬取热门榜单...");

        crawlerService.crawlTomatoHotList()
            .flatMapMany(Flux::fromIterable)
            .flatMap(novel -> {
                // 爬取前 3 章内容
                return crawlerService.crawlNovelContent(novel.getUrl())
                    .flatMap(content -> {
                        // 自动导入并分析
                        return importService.importFromText(
                            novel.getTitle(),
                            content,
                            "system-crawler"
                        );
                    });
            })
            .subscribe(
                result -> log.info("爬取并导入成功: {}", result.getTitle()),
                error -> log.error("爬取失败", error)
            );
    }
}
```

**步骤 3: 配置反爬策略**

```java
// 添加 User-Agent、延迟、代理等反爬措施
@Bean
public WebClient crawlerWebClient() {
    return WebClient.builder()
        .defaultHeader("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...")
        .defaultHeader("Referer", "https://fanqienovel.com")
        .filter((request, next) -> {
            // 添加随机延迟（500ms - 2000ms）
            return Mono.delay(Duration.ofMillis(
                ThreadLocalRandom.current().nextInt(500, 2000)
            )).flatMap(tick -> next.exchange(request));
        })
        .build();
}
```

**推荐方案**: 不使用爬虫，而是让用户手动上传 TXT 文件，或与平台合作获取 API 授权。

---

## 10. 性能优化与监控

### 10.1 性能优化策略

**优化 1: 使用缓存减少 AI 调用**

```java
@Cacheable(value = "setting-generation", key = "#promptHash")
public Mono<List<SettingNode>> generateWithCache(
    String promptHash,
    String prompt,
    String strategyId
) {
    // 如果缓存中有相同提示词的结果，直接返回
    return settingGenerationService.generate(prompt, strategyId);
}
```

**优化 2: 批量保存节点**

```java
// ❌ 差的实现（N 次数据库调用）
for (SettingNode node : nodes) {
    settingRepository.save(node).subscribe();
}

// ✅ 好的实现（1 次批量调用）
settingRepository.saveAll(nodes)
    .collectList()
    .subscribe();
```

**优化 3: 使用虚拟线程（Java 21）**

```yaml
# application.yml
spring:
  threads:
    virtual:
      enabled: true
```

```java
@Bean
public Executor taskExecutor() {
    return Executors.newVirtualThreadPerTaskExecutor();
}
```

**优化 4: 限制小说内容长度**

```java
// 只取前 5 章或前 10000 字作为上下文
String novelContext = scenes.stream()
    .limit(5)
    .map(Scene::getContent)
    .collect(Collectors.joining("\n"))
    .substring(0, Math.min(10000, totalLength));
```

### 10.2 监控指标

**关键指标**:

| 指标 | 说明 | 阈值 |
|------|------|------|
| `ai.generation.duration` | AI 生成耗时 | < 30s |
| `ai.generation.token_count` | Token 消耗量 | < 4000 tokens |
| `ai.generation.cost` | 单次成本 | < $0.5 |
| `session.active_count` | 活跃会话数 | < 1000 |
| `database.query.duration` | 数据库查询耗时 | < 100ms |

**Prometheus 监控配置**:

```java
@Component
public class SettingGenerationMetrics {

    private final Counter generationCounter;
    private final Timer generationTimer;
    private final Gauge activeSessionsGauge;

    public SettingGenerationMetrics(MeterRegistry registry) {
        this.generationCounter = Counter.builder("ai.generation.total")
            .description("AI 生成总次数")
            .tag("strategy", "")
            .register(registry);

        this.generationTimer = Timer.builder("ai.generation.duration")
            .description("AI 生成耗时")
            .register(registry);

        this.activeSessionsGauge = Gauge.builder("session.active.count",
            sessionManager, SessionManager::getActiveSessionCount)
            .description("活跃会话数")
            .register(registry);
    }

    public void recordGeneration(String strategyId, Duration duration) {
        generationCounter.increment();
        generationTimer.record(duration);
    }
}
```

### 10.3 错误处理与重试

**重试策略**:

```java
public Mono<List<SettingNode>> generateWithRetry(
    String prompt,
    String strategyId
) {
    return settingGenerationService.generate(prompt, strategyId)
        .retryWhen(Retry.backoff(3, Duration.ofSeconds(2))
            .filter(throwable -> throwable instanceof TimeoutException)
            .doBeforeRetry(signal ->
                log.warn("重试生成，第 {} 次", signal.totalRetries() + 1)
            )
        )
        .timeout(Duration.ofSeconds(60))
        .onErrorResume(error -> {
            log.error("生成失败，已达最大重试次数", error);
            return Mono.error(new GenerationFailedException("AI 生成失败，请稍后重试"));
        });
}
```

**错误分类**:

```java
public class GenerationException extends RuntimeException {
    private final ErrorCategory category;
    private final boolean recoverable;

    public enum ErrorCategory {
        RATE_LIMIT,      // 速率限制（可重试）
        TOKEN_LIMIT,     // Token 超限（不可重试，需用户调整）
        MODEL_ERROR,     // 模型错误（可重试）
        PARSE_ERROR,     // 解析错误（不可重试，提示词问题）
        TIMEOUT,         // 超时（可重试）
        NETWORK_ERROR    // 网络错误（可重试）
    }
}
```

---

## 📋 总结与检查清单

### ✅ 已实现的核心功能

- [x] 小说 TXT 导入与智能章节识别
- [x] 番茄小说拆书策略（11 个维度分析）
- [x] AI 驱动的设定生成（Hybrid 流程）
- [x] SSE 实时推送生成进度
- [x] 树形设定节点管理
- [x] 节点 AI 修改与整体调整
- [x] 历史快照与版本管理
- [x] 小说设定关联与保存
- [x] 响应式数据库持久化

### 🔧 待优化的功能

- [ ] 前端树形展示组件完善
- [ ] 更多拆书策略（起点、晋江、纵横）
- [ ] 爬虫功能（需考虑版权）
- [ ] 知识库 RAG 集成（Chroma 已配置）
- [ ] 用户自定义策略编辑器
- [ ] 设定导出（Markdown/PDF/Word）
- [ ] 多语言支持

### 🎯 关键文件速查

| 功能 | 文件路径 |
|------|---------|
| 番茄小说策略 | `service/setting/generation/strategy/TomatoWebNovelStrategy.java` |
| 核心生成服务 | `service/setting/generation/SettingGenerationService.java` |
| API 控制器 | `controller/SettingGenerationController.java` |
| 数据模型 | `domain/model/setting/generation/SettingNode.java` |
| 会话管理 | `service/setting/generation/InMemorySessionManager.java` |
| 历史管理 | `service/setting/NovelSettingHistoryService.java` |
| 小说导入 | `service/impl/ImportServiceImpl.java` |
| TXT 解析 | `service/impl/TxtNovelParser.java` |

---

## 🔗 相关资源

- [Spring WebFlux 官方文档](https://docs.spring.io/spring-framework/reference/web/webflux.html)
- [Project Reactor 文档](https://projectreactor.io/docs)
- [LangChain4j 文档](https://docs.langchain4j.dev)
- [MongoDB Reactive 驱动](https://mongodb.github.io/mongo-java-driver-reactivestreams/)
- [Server-Sent Events 规范](https://html.spec.whatwg.org/multipage/server-sent-events.html)

---

**文档版本**: v1.0
**最后更新**: 2025-10-26
**维护者**: Claude Code Analysis

---

## ⚖️ 法律声明

本文档中提及的"番茄小说"、"起点中文网"等平台名称及爬虫示例代码，仅用于技术说明和学习参考。任何爬取行为必须：

1. **遵守 robots.txt 协议**
2. **尊重版权，不得用于商业用途**
3. **控制请求频率，避免影响平台服务**
4. **优先考虑与平台合作，获取 API 授权**

推荐方案是让用户自行上传 TXT 文件，而非自动爬取。
