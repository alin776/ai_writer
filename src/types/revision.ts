export type ChapterRevisionStatus = 'pending' | 'accepted' | 'discarded' | 'conflict';

export interface ChapterRevision {
  id: string;
  requestId: string;
  workId: string;
  chapterId: string;
  status: ChapterRevisionStatus;
  operation: string;
  originalText?: string;
  newText: string;
  position?: { from: number; to: number };
  beforeAnchor?: string;
  afterAnchor?: string;
  nodeId?: string;
  paragraphIndex?: number;
  description?: string;
  createdAt: string;
}
