import fs from 'fs';

const filePath = 'D:/Java/ai_writer/src/components/editor/AIPanel.tsx';
let content = fs.readFileSync(filePath, 'utf-8');
const lines = content.split('\n');

// 在第1249行后插入新代码（onAddToKnowledge 行后面）
const insertAfterLine = 1249;  // 0-indexed: 1248

// 要插入的新行
const newLines = [
  '                        onApplyContent={(content) => {',
  '                          // 派发 agent-show-revision 事件到编辑器，显示修订标记',
  "                          window.dispatchEvent(new CustomEvent('agent-show-revision', {",
  '                            detail: {',
  "                              type: 'continue',",
  '                              replacement: content,',
  '                              revisionId: `output-${Date.now()}`',
  '                            }',
  '                          }));',
  '                        }}'
];

// 检查是否已经添加过（避免重复）
if (lines[insertAfterLine - 1].includes('onAddToKnowledge={handleOpenAddKnowledge}') &&
    !lines[insertAfterLine].includes('onApplyContent')) {
  lines.splice(insertAfterLine, 0, ...newLines);
  // 使用 UTF-8 编码写入，保留 BOM
  fs.writeFileSync(filePath, lines.join('\n'), { encoding: 'utf-8' });
  console.log('Modified successfully');
} else if (lines[insertAfterLine].includes('onApplyContent')) {
  console.log('Already modified');
} else {
  console.log('Pattern not found at expected line');
  console.log('Line 1249:', lines[1248]);
  console.log('Line 1250:', lines[1249]);
}
