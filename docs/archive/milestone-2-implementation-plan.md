# Milestone 2 实现计划 - AI 增强功能

## 📋 项目概览

**版本:** v2.0
**开始日期:** 2025-10
**预计工期:** 4-6 周
**负责人:** 开发团队

### 功能模块

1. 去AI痕迹功能
2. AI交互式反馈系统
3. 小说评审功能增强
4. AI写作竞技场

---

## 🎯 功能一：去AI痕迹功能

### 功能描述
将AI生成的文本转化为更自然、更人性化的表达，消除机械感和明显的AI写作特征。

### 技术方案
**实现方式:** 原生实现（Prompt Engineering + 多轮改写）

### 核心特性
- 多维度检测AI痕迹（句式、词汇、节奏）
- 三阶段改写流程
- 风格保持一致性
- 实时流式输出

---

## 📁 文件结构

### 后端新增文件

```
backend/
├── app/
│   ├── api/v1/
│   │   └── ai.py                          # 现有文件，需扩展
│   ├── services/ai/
│   │   ├── humanize_service.py            # 新增：去AI痕迹服务
│   │   ├── feedback_service.py            # 新增：交互反馈服务
│   │   ├── review_service.py              # 新增：评审服务
│   │   ├── arena_service.py               # 新增：竞技场服务
│   │   └── prompts/
│   │       ├── humanize_prompts.py        # 新增：去痕迹提示词库
│   │       ├── feedback_prompts.py        # 新增：反馈提示词库
│   │       └── review_prompts.py          # 新增：评审提示词库
│   ├── models/
│   │   ├── feedback_session.py            # 新增：反馈会话模型
│   │   └── review_result.py               # 新增：评审结果模型
│   └── schemas/
│       ├── humanize.py                    # 新增：去痕迹请求/响应模型
│       ├── feedback.py                    # 新增：反馈请求/响应模型
│       ├── review.py                      # 新增：评审请求/响应模型
│       └── arena.py                       # 新增：竞技场请求/响应模型
```

### 前端新增文件

```
src/
├── components/
│   ├── editor/
│   │   ├── AIHumanizeDialog.tsx           # 新增：去AI痕迹对话框
│   │   ├── AIFeedbackPanel.tsx            # 新增：AI反馈面板
│   │   └── AIMenu.tsx                     # 现有文件，需扩展
│   ├── review/
│   │   ├── ReviewPanel.tsx                # 新增：评审面板
│   │   ├── ReviewResult.tsx               # 新增：评审结果展示
│   │   └── ReviewHistory.tsx              # 新增：评审历史
│   └── arena/
│       ├── ArenaPanel.tsx                 # 新增：竞技场面板
│       ├── ModelSelector.tsx              # 新增：模型选择器
│       └── ResultComparison.tsx           # 新增：结果对比
├── services/
│   └── AIService.ts                       # 现有文件，需扩展
├── hooks/
│   ├── useAIHumanize.ts                   # 新增：去痕迹Hook
│   ├── useAIFeedback.ts                   # 新增：反馈Hook
│   ├── useNovelReview.ts                  # 新增：评审Hook
│   └── useAIArena.ts                      # 新增：竞技场Hook
└── types/
    ├── humanize.ts                        # 新增：去痕迹类型定义
    ├── feedback.ts                        # 新增：反馈类型定义
    ├── review.ts                          # 新增：评审类型定义
    └── arena.ts                           # 新增：竞技场类型定义
```

---

## 🔧 详细实现计划

## 功能一：去AI痕迹功能

### 后端实现

#### 1. 创建 Pydantic 数据模型
**文件:** `backend/app/schemas/humanize.py`

```python
from pydantic import BaseModel, Field
from typing import Optional, Literal

class HumanizeRequest(BaseModel):
    """去AI痕迹请求"""
    text: str = Field(..., description="待处理的文本", min_length=1)
    style: Optional[str] = Field(None, description="目标风格（如：轻松、严肃、幽默）")
    intensity: Literal["light", "medium", "strong"] = Field(
        default="medium",
        description="去痕迹强度"
    )

class HumanizeResponse(BaseModel):
    """去AI痕迹响应"""
    original_text: str
    humanized_text: str
    changes: list[dict]  # 记录具体改动
    ai_score_before: float  # 处理前AI特征评分 0-100
    ai_score_after: float   # 处理后AI特征评分 0-100
```

#### 2. 创建 Prompts 库
**文件:** `backend/app/services/ai/prompts/humanize_prompts.py`

```python
"""去AI痕迹专用提示词库"""

DETECTION_PROMPT = """
你是一个AI文本检测专家。分析以下文本，识别AI写作的典型特征：

文本：
{text}

请从以下维度评估（0-100分）：
1. 句式多样性（AI倾向使用固定句式）
2. 词汇丰富度（AI常用高频词汇）
3. 逻辑连接词过度使用（如"因此"、"综上所述"）
4. 缺乏个人化表达和口语化元素
5. 段落结构过于工整

返回JSON格式：
{{
  "overall_score": 总体AI特征得分,
  "dimensions": {{
    "sentence_variety": 得分,
    "vocabulary_richness": 得分,
    "connector_overuse": 得分,
    "personalization": 得分,
    "structure_rigidity": 得分
  }},
  "detected_patterns": ["具体AI痕迹1", "具体AI痕迹2"]
}}
"""

HUMANIZE_LIGHT_PROMPT = """
你是一个文本润色师。对以下文本进行轻度人性化改写：

原文：
{text}

风格要求：{style}

改写要点：
1. 适度调整句式，增加1-2个短句
2. 替换2-3个过于"AI化"的词汇
3. 保持原意和整体结构

只输出改写后的文本，不要添加任何解释。
"""

HUMANIZE_MEDIUM_PROMPT = """
你是一个专业的人性化文本改写专家。对以下文本进行中度人性化改写：

原文：
{text}

风格要求：{style}

改写要点：
1. 打破固定句式，增加长短句变化
2. 加入1-2个口语化表达或个性化细节
3. 减少逻辑连接词的使用
4. 适当增加情感色彩
5. 保持核心观点和信息完整

只输出改写后的文本，不要添加任何解释。
"""

HUMANIZE_STRONG_PROMPT = """
你是一个高级人性化文本改写大师。对以下文本进行深度人性化改写：

原文：
{text}

风格要求：{style}

改写要点：
1. 完全重构句式，创造自然的节奏变化
2. 加入口语化、个性化表达
3. 使用更丰富的修辞手法
4. 添加细节和情感元素
5. 打破过于工整的段落结构
6. 可以适当重新组织内容顺序
7. 确保读起来像是人类自然创作

只输出改写后的文本，不要添加任何解释。
"""

def get_humanize_prompt(intensity: str, text: str, style: str = "") -> str:
    """根据强度获取对应的提示词"""
    prompts = {
        "light": HUMANIZE_LIGHT_PROMPT,
        "medium": HUMANIZE_MEDIUM_PROMPT,
        "strong": HUMANIZE_STRONG_PROMPT
    }
    return prompts[intensity].format(text=text, style=style or "自然流畅")
```

#### 3. 创建核心服务类
**文件:** `backend/app/services/ai/humanize_service.py`

```python
"""去AI痕迹服务"""

import json
import logging
from typing import AsyncGenerator
from app.services.ai.http_ai_service import HTTPAIService
from app.services.ai.prompts.humanize_prompts import (
    DETECTION_PROMPT,
    get_humanize_prompt
)

logger = logging.getLogger(__name__)


class HumanizeService:
    """去AI痕迹服务 - 三阶段处理"""

    def __init__(self):
        self.http_ai = HTTPAIService()

    async def detect_ai_traces(self, text: str) -> dict:
        """
        阶段1：检测AI痕迹

        Returns:
            {
                "overall_score": float,
                "dimensions": dict,
                "detected_patterns": list
            }
        """
        logger.info("开始检测AI痕迹...")

        messages = [
            {"role": "system", "content": "你是AI文本检测专家。"},
            {"role": "user", "content": DETECTION_PROMPT.format(text=text)}
        ]

        # 非流式调用，获取完整JSON
        result = ""
        async for chunk in self.http_ai._stream_chat(
            messages,
            max_tokens=500,
            temperature=0.3
        ):
            result += chunk

        # 解析JSON
        try:
            detection_result = json.loads(result)
            logger.info(f"AI特征检测完成，得分: {detection_result['overall_score']}")
            return detection_result
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}, 原始结果: {result}")
            # 返回默认值
            return {
                "overall_score": 50.0,
                "dimensions": {},
                "detected_patterns": []
            }

    async def humanize_stream(
        self,
        text: str,
        intensity: str = "medium",
        style: str = ""
    ) -> AsyncGenerator[str, None]:
        """
        阶段2：流式人性化改写

        Args:
            text: 原始文本
            intensity: 强度 light/medium/strong
            style: 风格要求

        Yields:
            改写后的文本片段
        """
        logger.info(f"开始人性化改写，强度: {intensity}")

        prompt = get_humanize_prompt(intensity, text, style)
        messages = [
            {"role": "system", "content": "你是专业的人性化文本改写专家。"},
            {"role": "user", "content": prompt}
        ]

        async for chunk in self.http_ai._stream_chat(
            messages,
            max_tokens=2000,
            temperature=0.8  # 较高温度增加创造性
        ):
            yield chunk

    async def verify_humanization(self, original: str, humanized: str) -> dict:
        """
        阶段3：验证改写效果

        Returns:
            {
                "ai_score_before": float,
                "ai_score_after": float,
                "improvement": float,
                "changes": list
            }
        """
        logger.info("验证人性化效果...")

        # 分别检测原文和改写后的AI特征
        before = await self.detect_ai_traces(original)
        after = await self.detect_ai_traces(humanized)

        improvement = before["overall_score"] - after["overall_score"]

        return {
            "ai_score_before": before["overall_score"],
            "ai_score_after": after["overall_score"],
            "improvement": improvement,
            "changes": self._extract_changes(original, humanized)
        }

    def _extract_changes(self, original: str, humanized: str) -> list[dict]:
        """提取具体改动（简化版，实际可用diff算法）"""
        # TODO: 实现更精确的diff算法
        return [
            {
                "type": "humanization",
                "description": "文本已进行人性化改写"
            }
        ]
```

#### 4. 扩展 API 路由
**文件:** `backend/app/api/v1/ai.py`（在现有文件末尾添加）

```python
# ==================== 新增：去AI痕迹功能 ====================

from app.services.ai.humanize_service import HumanizeService
from app.schemas.humanize import HumanizeRequest

@router.post("/ai/humanize")
async def humanize_text(
    request: HumanizeRequest,
    current_user: User = Depends(get_current_active_user),
):
    """
    去AI痕迹 - 流式响应

    三阶段处理：
    1. 检测AI痕迹（返回评分）
    2. 人性化改写（流式输出）
    3. 验证效果（返回对比）
    """
    try:
        service = HumanizeService()

        async def generate():
            # 阶段1：检测
            yield f"data: [PHASE]检测AI痕迹中...\n\n"
            detection = await service.detect_ai_traces(request.text)
            yield f"data: [DETECTION]{json.dumps(detection, ensure_ascii=False)}\n\n"

            # 阶段2：改写
            yield f"data: [PHASE]开始人性化改写...\n\n"
            humanized_text = ""
            async for chunk in service.humanize_stream(
                request.text,
                request.intensity,
                request.style
            ):
                humanized_text += chunk
                yield f"data: {chunk}\n\n"

            # 阶段3：验证
            yield f"data: [PHASE]验证改写效果...\n\n"
            verification = await service.verify_humanization(
                request.text,
                humanized_text
            )
            yield f"data: [VERIFICATION]{json.dumps(verification, ensure_ascii=False)}\n\n"

            yield "data: [DONE]\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )

    except Exception as e:
        logger.error(f"去AI痕迹失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"去AI痕迹失败: {str(e)}"
        )
```

### 前端实现

#### 1. 创建类型定义
**文件:** `src/types/humanize.ts`

```typescript
export interface HumanizeRequest {
  text: string;
  style?: string;
  intensity: 'light' | 'medium' | 'strong';
}

export interface AIDetectionResult {
  overall_score: number;
  dimensions: {
    sentence_variety: number;
    vocabulary_richness: number;
    connector_overuse: number;
    personalization: number;
    structure_rigidity: number;
  };
  detected_patterns: string[];
}

export interface HumanizeVerification {
  ai_score_before: number;
  ai_score_after: number;
  improvement: number;
  changes: Array<{
    type: string;
    description: string;
  }>;
}

export type HumanizePhase = 'detecting' | 'humanizing' | 'verifying' | 'done';
```

#### 2. 扩展 AIService
**文件:** `src/services/AIService.ts`（添加新方法）

```typescript
/**
 * 去AI痕迹（流式）
 */
async humanizeText(
  request: HumanizeRequest,
  callbacks: {
    onPhaseChange?: (phase: HumanizePhase) => void;
    onDetection?: (result: AIDetectionResult) => void;
    onChunk?: (chunk: string) => void;
    onVerification?: (result: HumanizeVerification) => void;
  }
): Promise<string> {
  try {
    const apiUrl = `${this.baseUrl}/ai/humanize`;
    const token = this.getAuthToken();

    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        'Accept': 'text/event-stream',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`API请求失败: ${response.status}`);
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('无法读取响应流');
    }

    const decoder = new TextDecoder();
    let humanizedText = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n').filter(line => line.trim() !== '');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);

          if (data === '[DONE]') {
            callbacks.onPhaseChange?.('done');
            continue;
          }

          // 阶段切换
          if (data.startsWith('[PHASE]')) {
            const phase = data.slice(7);
            if (phase.includes('检测')) callbacks.onPhaseChange?.('detecting');
            if (phase.includes('改写')) callbacks.onPhaseChange?.('humanizing');
            if (phase.includes('验证')) callbacks.onPhaseChange?.('verifying');
            continue;
          }

          // 检测结果
          if (data.startsWith('[DETECTION]')) {
            const detection = JSON.parse(data.slice(11));
            callbacks.onDetection?.(detection);
            continue;
          }

          // 验证结果
          if (data.startsWith('[VERIFICATION]')) {
            const verification = JSON.parse(data.slice(14));
            callbacks.onVerification?.(verification);
            continue;
          }

          // 改写内容
          humanizedText += data;
          callbacks.onChunk?.(data);
        }
      }
    }

    return humanizedText;
  } catch (error) {
    console.error('去AI痕迹失败:', error);
    throw error;
  }
}
```

#### 3. 创建自定义 Hook
**文件:** `src/hooks/useAIHumanize.ts`

```typescript
import { useState } from 'react';
import AIService from '@/services/AIService';
import type {
  HumanizeRequest,
  HumanizePhase,
  AIDetectionResult,
  HumanizeVerification,
} from '@/types/humanize';

export function useAIHumanize() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [phase, setPhase] = useState<HumanizePhase>('detecting');
  const [detection, setDetection] = useState<AIDetectionResult | null>(null);
  const [humanizedText, setHumanizedText] = useState('');
  const [verification, setVerification] = useState<HumanizeVerification | null>(null);
  const [error, setError] = useState<string | null>(null);

  const humanize = async (request: HumanizeRequest) => {
    setIsProcessing(true);
    setError(null);
    setHumanizedText('');
    setDetection(null);
    setVerification(null);

    try {
      const result = await AIService.humanizeText(request, {
        onPhaseChange: setPhase,
        onDetection: setDetection,
        onChunk: (chunk) => {
          setHumanizedText((prev) => prev + chunk);
        },
        onVerification: setVerification,
      });

      return result;
    } catch (err) {
      const message = err instanceof Error ? err.message : '未知错误';
      setError(message);
      throw err;
    } finally {
      setIsProcessing(false);
    }
  };

  return {
    humanize,
    isProcessing,
    phase,
    detection,
    humanizedText,
    verification,
    error,
  };
}
```

#### 4. 创建 UI 组件
**文件:** `src/components/editor/AIHumanizeDialog.tsx`

```typescript
import { useState } from 'react';
import { useAIHumanize } from '@/hooks/useAIHumanize';
import type { HumanizeRequest } from '@/types/humanize';

interface Props {
  open: boolean;
  onClose: () => void;
  selectedText: string;
  onApply: (humanizedText: string) => void;
}

export function AIHumanizeDialog({ open, onClose, selectedText, onApply }: Props) {
  const [intensity, setIntensity] = useState<'light' | 'medium' | 'strong'>('medium');
  const [style, setStyle] = useState('');

  const { humanize, isProcessing, phase, detection, humanizedText, verification } = useAIHumanize();

  const handleHumanize = async () => {
    const request: HumanizeRequest = {
      text: selectedText,
      intensity,
      style,
    };

    try {
      await humanize(request);
    } catch (error) {
      console.error('去AI痕迹失败:', error);
    }
  };

  const handleApply = () => {
    onApply(humanizedText);
    onClose();
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg w-[800px] max-h-[80vh] overflow-auto p-6">
        <h2 className="text-xl font-bold mb-4">去AI痕迹</h2>

        {/* 强度选择 */}
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">改写强度</label>
          <div className="flex gap-2">
            {(['light', 'medium', 'strong'] as const).map((level) => (
              <button
                key={level}
                onClick={() => setIntensity(level)}
                className={`px-4 py-2 rounded ${
                  intensity === level ? 'bg-blue-500 text-white' : 'bg-gray-200'
                }`}
              >
                {level === 'light' && '轻度'}
                {level === 'medium' && '中度'}
                {level === 'strong' && '强度'}
              </button>
            ))}
          </div>
        </div>

        {/* 风格输入 */}
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">风格要求（可选）</label>
          <input
            type="text"
            value={style}
            onChange={(e) => setStyle(e.target.value)}
            placeholder="如：轻松幽默、严肃专业..."
            className="w-full px-3 py-2 border rounded"
          />
        </div>

        {/* 原文预览 */}
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">原文</label>
          <div className="p-3 bg-gray-50 rounded max-h-32 overflow-auto">
            {selectedText}
          </div>
        </div>

        {/* 处理阶段指示 */}
        {isProcessing && (
          <div className="mb-4">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
              <span>
                {phase === 'detecting' && '正在检测AI痕迹...'}
                {phase === 'humanizing' && '正在人性化改写...'}
                {phase === 'verifying' && '正在验证效果...'}
              </span>
            </div>
          </div>
        )}

        {/* AI特征检测结果 */}
        {detection && (
          <div className="mb-4 p-3 bg-yellow-50 rounded">
            <div className="font-medium mb-2">
              AI特征评分: {detection.overall_score.toFixed(1)}分
            </div>
            {detection.detected_patterns.length > 0 && (
              <div className="text-sm">
                <div>检测到的AI痕迹:</div>
                <ul className="list-disc list-inside">
                  {detection.detected_patterns.map((pattern, i) => (
                    <li key={i}>{pattern}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* 改写结果 */}
        {humanizedText && (
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">改写后</label>
            <div className="p-3 bg-green-50 rounded max-h-48 overflow-auto">
              {humanizedText}
            </div>
          </div>
        )}

        {/* 验证结果 */}
        {verification && (
          <div className="mb-4 p-3 bg-blue-50 rounded">
            <div className="flex justify-between items-center">
              <div>
                <span className="font-medium">改进效果: </span>
                <span className={verification.improvement > 0 ? 'text-green-600' : 'text-red-600'}>
                  {verification.improvement > 0 ? '+' : ''}
                  {verification.improvement.toFixed(1)}分
                </span>
              </div>
              <div className="text-sm text-gray-600">
                {verification.ai_score_before.toFixed(1)} → {verification.ai_score_after.toFixed(1)}
              </div>
            </div>
          </div>
        )}

        {/* 操作按钮 */}
        <div className="flex justify-end gap-2">
          <button
            onClick={onClose}
            className="px-4 py-2 border rounded hover:bg-gray-50"
          >
            取消
          </button>
          {!isProcessing && !humanizedText && (
            <button
              onClick={handleHumanize}
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              开始处理
            </button>
          )}
          {humanizedText && (
            <button
              onClick={handleApply}
              className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
            >
              应用改写
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
```

#### 5. 集成到编辑器菜单
**文件:** `src/components/editor/AIMenu.tsx`（在现有菜单中添加）

```typescript
// 在 AIMenu 组件中添加新按钮
<button
  onClick={() => {
    const selectedText = editor.state.doc.textBetween(
      editor.state.selection.from,
      editor.state.selection.to
    );
    if (selectedText) {
      setHumanizeDialogOpen(true);
      setSelectedText(selectedText);
    }
  }}
  className="flex items-center gap-2 px-3 py-2 hover:bg-gray-100 rounded"
>
  <WandIcon className="w-4 h-4" />
  <span>去AI痕迹</span>
</button>

{/* 添加对话框 */}
<AIHumanizeDialog
  open={humanizeDialogOpen}
  onClose={() => setHumanizeDialogOpen(false)}
  selectedText={selectedText}
  onApply={(humanizedText) => {
    editor.chain().focus().insertContent(humanizedText).run();
  }}
/>
```

---

## 功能二：AI交互式反馈系统

### 功能描述
为作者提供持续的AI写作指导和反馈，支持多轮对话，根据小说上下文提供针对性建议。

### 技术方案
**实现方式:** 原生实现 + LangChain Memory（对话历史管理）

### 核心特性
- 会话管理（支持多个独立反馈会话）
- 上下文感知（自动读取当前章节/世界观）
- 持续性反馈（保留历史对话）
- 多种反馈模式（剧情建议、人物发展、冲突设计等）

### 实现步骤

#### 后端实现

##### 1. 安装 LangChain 核心库
```bash
cd backend
pip install langchain-core==0.3.0
pip freeze > requirements.txt
```

##### 2. 创建数据库模型
**文件:** `backend/app/models/feedback_session.py`

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class FeedbackSession(Base):
    """AI反馈会话"""
    __tablename__ = "feedback_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    work_id = Column(Integer, ForeignKey("works.id"), nullable=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=True)

    title = Column(String(200), default="新建反馈会话")
    mode = Column(String(50), default="general")  # general, plot, character, conflict, etc.

    context = Column(JSON, default=dict)  # 存储世界观等上下文信息

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    user = relationship("User", back_populates="feedback_sessions")
    messages = relationship("FeedbackMessage", back_populates="session", cascade="all, delete-orphan")


class FeedbackMessage(Base):
    """反馈会话消息"""
    __tablename__ = "feedback_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("feedback_sessions.id"), nullable=False)

    role = Column(String(20), nullable=False)  # user / assistant
    content = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    session = relationship("FeedbackSession", back_populates="messages")
```

##### 3. 创建数据库迁移
```bash
cd backend
alembic revision --autogenerate -m "add_feedback_session_tables"
alembic upgrade head
```

##### 4. 创建 Pydantic Schema
**文件:** `backend/app/schemas/feedback.py`

```python
from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime


class FeedbackSessionCreate(BaseModel):
    """创建反馈会话"""
    work_id: Optional[int] = None
    chapter_id: Optional[int] = None
    title: str = "新建反馈会话"
    mode: Literal["general", "plot", "character", "conflict", "pacing"] = "general"


class FeedbackMessageCreate(BaseModel):
    """创建反馈消息"""
    content: str = Field(..., min_length=1)


class FeedbackMessageResponse(BaseModel):
    """反馈消息响应"""
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class FeedbackSessionResponse(BaseModel):
    """反馈会话响应"""
    id: int
    title: str
    mode: str
    created_at: datetime
    updated_at: datetime
    messages: List[FeedbackMessageResponse] = []

    class Config:
        from_attributes = True
```

##### 5. 创建反馈服务
**文件:** `backend/app/services/ai/feedback_service.py`

```python
"""AI交互式反馈服务"""

import logging
from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from langchain_core.messages import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory

from app.services.ai.http_ai_service import HTTPAIService
from app.models.feedback_session import FeedbackSession, FeedbackMessage
from app.models.work import Work
from app.models.chapter import Chapter

logger = logging.getLogger(__name__)


class FeedbackService:
    """AI反馈服务 - 支持多轮对话"""

    def __init__(self):
        self.http_ai = HTTPAIService()
        # 内存中的会话Memory（可以考虑用Redis存储）
        self._memories: dict[int, ConversationBufferMemory] = {}

    def _get_memory(self, session_id: int) -> ConversationBufferMemory:
        """获取会话Memory"""
        if session_id not in self._memories:
            self._memories[session_id] = ConversationBufferMemory(
                return_messages=True,
                memory_key="chat_history"
            )
        return self._memories[session_id]

    async def _load_context(
        self,
        db: AsyncSession,
        work_id: Optional[int],
        chapter_id: Optional[int]
    ) -> str:
        """加载小说上下文"""
        context_parts = []

        if work_id:
            result = await db.execute(
                select(Work).where(Work.id == work_id)
            )
            work = result.scalar_one_or_none()
            if work:
                context_parts.append(f"作品：{work.title}")
                if work.description:
                    context_parts.append(f"简介：{work.description}")

        if chapter_id:
            result = await db.execute(
                select(Chapter).where(Chapter.id == chapter_id)
            )
            chapter = result.scalar_one_or_none()
            if chapter:
                context_parts.append(f"当前章节：{chapter.title}")
                if chapter.content:
                    # 只取前500字作为上下文
                    preview = chapter.content[:500]
                    context_parts.append(f"章节内容预览：{preview}...")

        return "\n".join(context_parts)

    async def _get_system_prompt(self, mode: str) -> str:
        """根据模式获取系统提示词"""
        prompts = {
            "general": """你是一位专业的小说创作导师。你将与作者进行持续的对话，提供有针对性的写作建议和反馈。

请注意：
1. 根据作者提供的上下文理解小说背景
2. 提供具体、可操作的建议
3. 鼓励作者的创意，同时指出潜在问题
4. 保持对话的连贯性，记住之前讨论的内容""",

            "plot": """你是一位剧情设计专家。专注于帮助作者：
- 构建引人入胜的情节
- 设置合理的冲突和转折
- 优化叙事节奏
- 避免剧情漏洞""",

            "character": """你是一位人物塑造专家。专注于帮助作者：
- 创造立体鲜活的角色
- 设计合理的人物成长弧
- 处理人物关系和互动
- 避免人物OOC（Out of Character）""",

            "conflict": """你是一位冲突设计专家。专注于帮助作者：
- 设计多层次的冲突
- 平衡外部冲突和内心冲突
- 提升戏剧张力
- 让冲突推动剧情发展""",

            "pacing": """你是一位节奏控制专家。专注于帮助作者：
- 优化叙事节奏
- 平衡快慢节奏
- 设置悬念和高潮
- 避免拖沓或过快"""
        }

        return prompts.get(mode, prompts["general"])

    async def chat_stream(
        self,
        db: AsyncSession,
        session_id: int,
        user_message: str
    ) -> AsyncGenerator[str, None]:
        """
        流式对话

        Args:
            db: 数据库会话
            session_id: 反馈会话ID
            user_message: 用户消息

        Yields:
            AI回复的文本片段
        """
        # 获取会话信息
        result = await db.execute(
            select(FeedbackSession).where(FeedbackSession.id == session_id)
        )
        session = result.scalar_one_or_none()
        if not session:
            raise ValueError(f"会话 {session_id} 不存在")

        # 获取Memory
        memory = self._get_memory(session_id)

        # 构建系统提示词
        system_prompt = await self._get_system_prompt(session.mode)

        # 加载小说上下文
        context = await self._load_context(db, session.work_id, session.chapter_id)
        if context:
            system_prompt += f"\n\n当前小说上下文：\n{context}"

        # 构建消息列表
        messages = [
            {"role": "system", "content": system_prompt}
        ]

        # 添加历史消息（从Memory获取）
        history = memory.chat_memory.messages
        for msg in history:
            if isinstance(msg, HumanMessage):
                messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                messages.append({"role": "assistant", "content": msg.content})

        # 添加当前用户消息
        messages.append({"role": "user", "content": user_message})

        logger.info(f"反馈会话 {session_id}, 消息数: {len(messages)}")

        # 流式调用AI
        ai_response = ""
        async for chunk in self.http_ai._stream_chat(
            messages,
            max_tokens=1500,
            temperature=0.7
        ):
            ai_response += chunk
            yield chunk

        # 保存消息到Memory
        memory.chat_memory.add_user_message(user_message)
        memory.chat_memory.add_ai_message(ai_response)

        # 保存到数据库
        user_msg = FeedbackMessage(
            session_id=session_id,
            role="user",
            content=user_message
        )
        ai_msg = FeedbackMessage(
            session_id=session_id,
            role="assistant",
            content=ai_response
        )

        db.add(user_msg)
        db.add(ai_msg)
        await db.commit()

        logger.info(f"反馈消息已保存到数据库")
```

##### 6. 创建 API 路由
**文件:** `backend/app/api/v1/feedback.py`（新建文件）

```python
"""AI反馈 API"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import logging

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.feedback_session import FeedbackSession
from app.schemas.feedback import (
    FeedbackSessionCreate,
    FeedbackSessionResponse,
    FeedbackMessageCreate
)
from app.services.ai.feedback_service import FeedbackService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/feedback/sessions", response_model=FeedbackSessionResponse)
async def create_feedback_session(
    data: FeedbackSessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """创建反馈会话"""
    session = FeedbackSession(
        user_id=current_user.id,
        work_id=data.work_id,
        chapter_id=data.chapter_id,
        title=data.title,
        mode=data.mode
    )

    db.add(session)
    await db.commit()
    await db.refresh(session)

    return session


@router.get("/feedback/sessions", response_model=List[FeedbackSessionResponse])
async def list_feedback_sessions(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用户的所有反馈会话"""
    result = await db.execute(
        select(FeedbackSession)
        .where(FeedbackSession.user_id == current_user.id)
        .order_by(FeedbackSession.updated_at.desc())
    )
    sessions = result.scalars().all()
    return sessions


@router.get("/feedback/sessions/{session_id}", response_model=FeedbackSessionResponse)
async def get_feedback_session(
    session_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取单个反馈会话"""
    result = await db.execute(
        select(FeedbackSession)
        .where(
            FeedbackSession.id == session_id,
            FeedbackSession.user_id == current_user.id
        )
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在"
        )

    return session


@router.post("/feedback/sessions/{session_id}/chat")
async def chat_with_ai(
    session_id: int,
    data: FeedbackMessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """与AI进行对话（流式）"""
    # 验证会话权限
    result = await db.execute(
        select(FeedbackSession)
        .where(
            FeedbackSession.id == session_id,
            FeedbackSession.user_id == current_user.id
        )
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在"
        )

    service = FeedbackService()

    async def generate():
        try:
            async for chunk in service.chat_stream(db, session_id, data.content):
                yield f"data: {chunk}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            logger.error(f"对话失败: {e}", exc_info=True)
            yield f"data: [ERROR]{str(e)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.delete("/feedback/sessions/{session_id}")
async def delete_feedback_session(
    session_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """删除反馈会话"""
    result = await db.execute(
        select(FeedbackSession)
        .where(
            FeedbackSession.id == session_id,
            FeedbackSession.user_id == current_user.id
        )
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在"
        )

    await db.delete(session)
    await db.commit()

    return {"message": "会话已删除"}
```

##### 7. 注册路由
**文件:** `backend/app/api/v1/__init__.py`（添加）

```python
from app.api.v1 import feedback

# 在 router 中添加
router.include_router(feedback.router, tags=["AI Feedback"])
```

#### 前端实现（简化版，可参考去AI痕迹的实现方式）

1. 创建类型定义 `src/types/feedback.ts`
2. 扩展 AIService `src/services/AIService.ts`
3. 创建 Hook `src/hooks/useAIFeedback.ts`
4. 创建 UI 组件 `src/components/editor/AIFeedbackPanel.tsx`
5. 集成到编辑器侧边栏

---

## 功能三：小说评审功能增强

### 核心改进
- 结构化输出（使用 Pydantic Parser）
- 多维度评分
- 具体改进建议
- 问题标注

### 实现方式
原生实现 + Pydantic 结构化输出

**实现步骤类似功能一、二，包含：**
1. 创建 Schema（评分维度、问题类型）
2. 创建 ReviewService（评审逻辑）
3. API 路由
4. 前端组件

---

## 功能四：AI写作竞技场

### 核心特性
- 多模型并发调用
- 实时对比展示
- 性能指标（速度、质量、成本）
- 投票和评分

### 技术实现
纯原生 `asyncio.gather()` 并发

**关键代码：**
```python
async def arena_battle(prompt: str, models: List[str]):
    async def call_model(model: str):
        start = time.time()
        result = await http_ai.generate(prompt, model=model)
        elapsed = time.time() - start
        return {"model": model, "result": result, "time": elapsed}

    results = await asyncio.gather(*[call_model(m) for m in models])
    return results
```

---

## 📅 实施时间表

| 阶段 | 任务 | 工期 | 责任人 |
|-----|------|------|--------|
| **Week 1** | 去AI痕迹功能 | 5天 | 后端2天 + 前端3天 |
| **Week 2** | AI交互式反馈系统 | 5天 | 后端3天 + 前端2天 |
| **Week 3** | 小说评审增强 | 3天 | 后端1.5天 + 前端1.5天 |
| **Week 3** | AI写作竞技场 | 2天 | 后端1天 + 前端1天 |
| **Week 4** | 集成测试和优化 | 5天 | 全栈 |
| **Week 5** | 内测和Bug修复 | 5天 | 全栈 |
| **Week 6** | 正式上线准备 | 3天 | 运维 + 全栈 |

**总计:** 4-6周

---

## 🔍 技术风险和应对

| 风险 | 影响 | 应对方案 |
|-----|------|---------|
| API调用频繁导致成本上升 | 高 | 添加速率限制、实现缓存策略 |
| LangChain Memory 内存泄漏 | 中 | 设置会话过期时间，定期清理 |
| 多模型竞技场响应慢 | 中 | 设置超时时间，提供提示 |
| 结构化输出解析失败 | 低 | 添加重试机制和降级方案 |

---

## ✅ 验收标准

### 功能验收
- [ ] 去AI痕迹功能可正常使用，改进效果明显
- [ ] 反馈系统支持多轮对话，上下文理解准确
- [ ] 评审功能提供结构化报告
- [ ] 竞技场支持至少3个模型对比

### 性能验收
- [ ] 流式响应延迟 < 500ms
- [ ] 并发用户支持 > 100
- [ ] API调用成功率 > 99%

### 代码质量
- [ ] 测试覆盖率 > 80%
- [ ] 类型检查通过
- [ ] 无严重 Bug

---

## 📦 依赖更新清单

### 后端
```bash
langchain-core==0.3.0  # 新增
```

### 前端
无新增依赖（复用现有）

---

## 🚀 部署注意事项

1. **数据库迁移**
   ```bash
   alembic upgrade head
   ```

2. **环境变量**
   确保配置了：
   - OPENAI_API_KEY
   - OPENAI_BASE_URL
   - OPENAI_MODEL

3. **性能监控**
   - 监控 API 调用次数和成本
   - 监控 Memory 使用情况

---

## 📝 后续优化建议

1. **Phase 2 之后可考虑：**
   - 引入 RAG（检索增强）提供历史评审参考
   - 添加 Agent 自主决策能力
   - 支持更多第三方 LLM（Claude、Gemini 等）

2. **性能优化：**
   - 使用 Redis 存储 Memory
   - 实现 Prompt 缓存
   - 添加 CDN 加速

---

**文档版本:** v1.0
**最后更新:** 2025-10-25
**维护者:** 开发团队
