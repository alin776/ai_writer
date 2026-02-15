/**
 * ExecutionFlow component (v7.1)
 *
 * Renders step cards and related flow cards in execution order.
 */

import type { FlowItem, TextFlowData, ToolFlowData, ContentFlowData, StepFlowData, OutputFlowData, AgentHeaderFlowData, CompletionFlowData, SummarizationFlowData, RevisionFlowData, ExploreRoundFlowData, ExploreSummaryFlowData, OperateFlowData } from '@/types/agent';
import { TextBlock } from './TextBlock';
import { ToolCard } from './ToolCard';
import { ContentBlock } from './ContentBlock';
import { StepCard } from './StepCard';
import { OutputCard } from './OutputCard';
import { AgentHeader } from './AgentHeader';
import { CompletionStatus } from './CompletionStatus';
import { SummarizationCard } from './SummarizationCard';
import { RevisionCard } from './RevisionCard';
import { ExploreRoundCard, ExploreSummaryCard } from './ExploreCard';
import { OperateCard } from './OperateCard';

interface ExecutionFlowProps {
  items: FlowItem[];
  onApplyContent?: (content: string) => void;
  onAddToKnowledge?: (title: string, content: string) => void;
  onAcceptRevision?: (itemId: string, requestId: string | undefined, selectedVersion?: number) => void;
  onDiscardRevision?: (itemId: string, requestId: string | undefined) => void;
  onJumpRevision?: (itemId: string, requestId: string | undefined) => void;
  onAcceptAllRevisions?: (itemIds: string[]) => void;
  onDiscardAllRevisions?: (itemIds: string[]) => void;
  // v7.2: undo/redo callbacks
  onUndoRevision?: (itemId: string) => void;
  onRedoRevision?: (itemId: string) => void;
}

export function ExecutionFlow({
  items,
  onApplyContent,
  onAddToKnowledge,
  onAcceptRevision,
  onDiscardRevision,
  onJumpRevision,
  onAcceptAllRevisions,
  onDiscardAllRevisions,
  onUndoRevision,
  onRedoRevision
}: ExecutionFlowProps) {
  if (!items || items.length === 0) {
    return null;
  }

  const stepIds = new Set(
    items
      .filter((item) => item.type === 'step')
      .map((item) => (item.data as StepFlowData).stepId)
  );

  const exploreItemsByStep = new Map<number, FlowItem[]>();
  items.forEach((item) => {
    if (item.type !== 'explore_round' && item.type !== 'explore_summary') {
      return;
    }
    const stepId = (item.data as ExploreRoundFlowData | ExploreSummaryFlowData).stepId;
    if (!stepIds.has(stepId)) {
      return;
    }
    const grouped = exploreItemsByStep.get(stepId) || [];
    grouped.push(item);
    exploreItemsByStep.set(stepId, grouped);
  });

  return (
    <div>
      {items.map((item) => {
        switch (item.type) {
          case 'text':
            // Do not render TextBlock here; StepCard carries the context.
            return null;
          case 'tool':
            // Do not render ToolCard here; StepCard is the single timeline unit.
            return null;
          case 'content':
            return (
              <ContentBlock
                key={item.id}
                content={(item.data as ContentFlowData).content}
              />
            );
          case 'step': {
            const stepData = item.data as StepFlowData;
            const exploreItems = exploreItemsByStep.get(stepData.stepId) || [];
            const isExploreStep = exploreItemsByStep.has(stepData.stepId)
              || stepData.toolCall?.name === 'explore_content';
            // v7.4: fallback to item.id to keep callbacks stable.
            const revisionId = stepData.revisionItemId || item.id;
            return (
              <StepCard
                key={item.id}
                {...stepData}
                revisionEventTimestamp={item.timestamp}
                description={isExploreStep ? undefined : stepData.description}
                onAcceptRevision={stepData.revision ? (selectedVersion) => onAcceptRevision?.(revisionId, (stepData.revision as any)?.requestId, selectedVersion) : undefined}
                onDiscardRevision={stepData.revision ? () => onDiscardRevision?.(revisionId, (stepData.revision as any)?.requestId) : undefined}
                onUndoRevision={stepData.revision ? () => onUndoRevision?.(revisionId) : undefined}
                onRedoRevision={stepData.revision ? () => onRedoRevision?.(revisionId) : undefined}
                onJumpRevision={stepData.revision ? () => onJumpRevision?.(revisionId, (stepData.revision as any)?.requestId) : undefined}
              >
                {exploreItems.length > 0 && (
                  <div className="space-y-2">
                    {exploreItems.map((exploreItem) => {
                      if (exploreItem.type === 'explore_round') {
                        return (
                          <ExploreRoundCard
                            key={exploreItem.id}
                            {...(exploreItem.data as ExploreRoundFlowData)}
                          />
                        );
                      }
                      if (exploreItem.type === 'explore_summary') {
                        return (
                          <ExploreSummaryCard
                            key={exploreItem.id}
                            {...(exploreItem.data as ExploreSummaryFlowData)}
                          />
                        );
                      }
                      return null;
                    })}
                  </div>
                )}
              </StepCard>
            );
          }
          case 'output':
            return (
              <OutputCard
                key={item.id}
                {...(item.data as OutputFlowData)}
                onApply={onApplyContent ? () => onApplyContent((item.data as OutputFlowData).content) : undefined}
                onAddToKnowledge={onAddToKnowledge ? () => onAddToKnowledge(
                  (item.data as OutputFlowData).title,
                  (item.data as OutputFlowData).content
                ) : undefined}
              />
            );
          case 'agent_header':
            return (
              <AgentHeader
                key={item.id}
                {...(item.data as AgentHeaderFlowData)}
              />
            );
          case 'completion':
            return (
              <CompletionStatus
                key={item.id}
                {...(item.data as CompletionFlowData)}
              />
            );
          case 'summarization':
            return (
              <SummarizationCard
                key={item.id}
                {...(item.data as SummarizationFlowData)}
              />
            );
          case 'revision': {
            const revisionData = item.data as RevisionFlowData;
            return (
              <RevisionCard
                key={item.id}
                {...revisionData}
                eventTimestamp={item.timestamp}
                onAccept={(selectedVersion) => onAcceptRevision?.(item.id, revisionData.requestId, selectedVersion)}
                onDiscard={() => onDiscardRevision?.(item.id, revisionData.requestId)}
                onUndo={() => onUndoRevision?.(item.id)}
                onRedo={() => onRedoRevision?.(item.id)}
                onJump={() => onJumpRevision?.(item.id, revisionData.requestId)}
              />
            );
          }
          case 'explore_round':
            if (stepIds.has((item.data as ExploreRoundFlowData).stepId)) {
              return null;
            }
            return (
              <ExploreRoundCard
                key={item.id}
                {...(item.data as ExploreRoundFlowData)}
              />
            );
          case 'explore_summary':
            if (stepIds.has((item.data as ExploreSummaryFlowData).stepId)) {
              return null;
            }
            return (
              <ExploreSummaryCard
                key={item.id}
                {...(item.data as ExploreSummaryFlowData)}
              />
            );
          case 'operate':
            return (
              <OperateCard
                key={item.id}
                data={item.data as OperateFlowData}
              />
            );
          default:
            return null;
        }
      })}
    </div>
  );
}

export default ExecutionFlow;

