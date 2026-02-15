/**
 * Shared Markdown normalization for agent outputs.
 *
 * Goals:
 * 1. Normalize common non-Markdown ordered-list prefixes to `1. ...`.
 * 2. Optionally remove leading indent for plain paragraphs.
 * 3. Repair pseudo-table text (`| ... || ...`) into valid GFM tables.
 */

interface NormalizeOptions {
  stripLeadingIndent?: boolean;
}

const CJK_NUMBER_MAP: Record<string, number> = {
  '零': 0,
  '一': 1,
  '二': 2,
  '两': 2,
  '三': 3,
  '四': 4,
  '五': 5,
  '六': 6,
  '七': 7,
  '八': 8,
  '九': 9,
  '十': 10
};

function toNumber(value: string): number | null {
  const cleaned = value.trim();
  if (!cleaned) return null;
  if (/^\d+$/.test(cleaned)) return parseInt(cleaned, 10);

  if (cleaned === '十') return 10;
  if (cleaned.includes('十')) {
    const parts = cleaned.split('十');
    const tens = parts[0] ? (CJK_NUMBER_MAP[parts[0]] ?? 0) : 1;
    const ones = parts[1] ? (CJK_NUMBER_MAP[parts[1]] ?? 0) : 0;
    return tens * 10 + ones;
  }

  const single = CJK_NUMBER_MAP[cleaned];
  if (single === undefined) return null;
  return single;
}

function isYearish(value: string): boolean {
  const trimmed = value.trim();
  if (!/^(19|20)\d{2}$/.test(trimmed)) return false;
  const year = parseInt(trimmed, 10);
  return year >= 1900 && year <= 2100;
}

function isNoticeLine(text: string): boolean {
  if (!text) return false;
  const haystack = text.trim();
  return /(公告|编号|版本|通知|更新|修订|说明|通告|第[一二三四五六七八九十]+号)/.test(haystack);
}

function shouldPreserveIndent(trimmed: string): boolean {
  if (!trimmed) return false;
  if (/^#{1,6}\s/.test(trimmed)) return true;
  if (/^>/.test(trimmed)) return true;
  if (/^[-*+]\s/.test(trimmed)) return true;
  if (/^\d+[.)]\s/.test(trimmed)) return true;
  if (/^\|/.test(trimmed)) return true;
  if (/^(\*{3,}|-{3,}|_{3,})$/.test(trimmed)) return true;
  return false;
}

function stripLeadingIndent(line: string): string {
  if (!line) return line;
  const trimmed = line.trimStart();
  if (shouldPreserveIndent(trimmed)) return line;
  return line.replace(/^[\s\u00a0\u2000-\u200b\u202f\u205f\u3000\uFEFF]+/, '');
}

function fixOrderedListPrefix(line: string): string {
  const bracketed = line.match(/^(\s*)[（(]\s*([0-9]+)\s*[）)]\s*(.+)$/);
  if (bracketed) {
    if (isYearish(bracketed[2]) || isNoticeLine(bracketed[3])) return line;
    return `${bracketed[1]}${bracketed[2]}. ${bracketed[3]}`;
  }

  const numbered = line.match(/^(\s*)([0-9]+|[一二三四五六七八九十两]+)\s*[、.．)\]）:：]\s*(.+)$/);
  if (!numbered) return line;

  const value = toNumber(numbered[2]);
  if (value === null) return line;
  if (isYearish(String(value)) || isNoticeLine(numbered[3])) return line;
  if (/^\s*[0-9]+\s*[.．]\s*[0-9]/.test(line)) return line;
  return `${numbered[1]}${value}. ${numbered[3]}`;
}

function isFenceLine(line: string): boolean {
  return line.trim().startsWith('```');
}

function isPseudoTableLine(line: string): boolean {
  const t = line.trim();
  if (!t) return false;
  if (t.includes('||')) {
    const segments = t.split('||').map((part) => part.trim()).filter(Boolean);
    // Guardrail: avoid converting plain logical-or text like "A || B".
    if (!segments.some((segment) => segment.includes('|'))) {
      return false;
    }
    return true;
  }
  const pipeCount = (t.match(/\|/g) || []).length;
  return pipeCount >= 2 && (t.startsWith('|') || t.endsWith('|'));
}

function isBridgeDashLine(line: string): boolean {
  return /^[-=]{3,}$/.test(line.trim());
}

function parseCells(row: string): string[] {
  let t = row.trim();
  if (t.startsWith('|')) t = t.slice(1);
  if (t.endsWith('|')) t = t.slice(0, -1);

  const raw = t.split('|').map((c) => c.trim());
  while (raw.length > 0 && raw[0] === '') raw.shift();
  while (raw.length > 0 && raw[raw.length - 1] === '') raw.pop();

  if (raw.length <= 1) {
    const source = raw[0] || t.trim();
    const kv = source.match(/^(.{1,80}?)[：:]\s*(.+)$/);
    if (kv) {
      return [kv[1].trim(), kv[2].trim()];
    }
  }
  return raw;
}

function isSeparatorRow(cells: string[]): boolean {
  return cells.length > 0 && cells.every((cell) => /^:?-{3,}:?$/.test(cell.trim()));
}

function normalizeRow(cells: string[], columns: number): string {
  const padded = [...cells];
  if (padded.length < columns) padded.push(...new Array(columns - padded.length).fill(''));
  if (padded.length > columns) padded.length = columns;
  return `| ${padded.join(' | ')} |`;
}

function buildSeparator(columns: number): string {
  return `| ${new Array(columns).fill('---').join(' | ')} |`;
}

function formatPseudoTableBlock(lines: string[]): string[] {
  const candidateRows: string[] = [];
  const plainSegments: string[] = [];

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    if (isBridgeDashLine(trimmed)) continue;

    const segments = trimmed.includes('||')
      ? trimmed.split('||').map((part) => part.trim()).filter(Boolean)
      : [trimmed];

    for (let segment of segments) {
      if (!segment.includes('|')) {
        // Keep non-pipe segments as plain text (usually notes/citations after `||`).
        plainSegments.push(segment);
        continue;
      }

      if (!segment.startsWith('|')) segment = `| ${segment}`;
      if (!segment.endsWith('|')) segment = `${segment} |`;
      candidateRows.push(segment);
    }
  }

  const textFallback = candidateRows.length > 0 ? [...candidateRows, ...plainSegments] : lines;
  const dataRows: string[][] = [];
  const trailingText: string[] = [...plainSegments];
  let hasExplicitSeparator = false;

  for (const row of candidateRows) {
    const cells = parseCells(row);
    if (cells.length === 0) continue;
    if (isSeparatorRow(cells)) {
      hasExplicitSeparator = true;
      continue;
    }
    if (cells.length >= 2) {
      dataRows.push(cells);
    } else {
      trailingText.push(cells[0] || row);
    }
  }

  if (dataRows.length === 0) {
    return textFallback;
  }

  const columns = Math.max(2, ...dataRows.map((r) => r.length));
  const output: string[] = [];
  output.push(normalizeRow(dataRows[0], columns));
  output.push(hasExplicitSeparator ? normalizeRow(new Array(columns).fill('---'), columns) : buildSeparator(columns));
  for (let i = 1; i < dataRows.length; i += 1) {
    output.push(normalizeRow(dataRows[i], columns));
  }

  if (trailingText.length > 0) {
    output.push('', ...trailingText);
  }

  return output;
}

function repairPseudoTables(value: string): string {
  const lines = value.split(/\r?\n/);
  const out: string[] = [];
  let inCode = false;

  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i];
    if (isFenceLine(line)) {
      inCode = !inCode;
      out.push(line);
      continue;
    }

    if (inCode) {
      out.push(line);
      continue;
    }

    if (!isPseudoTableLine(line)) {
      out.push(line);
      continue;
    }

    const block: string[] = [line];
    let j = i + 1;
    while (j < lines.length) {
      const next = lines[j];
      if (isFenceLine(next)) break;
      if (!next.trim()) break;
      if (!isPseudoTableLine(next) && !isBridgeDashLine(next)) break;
      block.push(next);
      j += 1;
    }

    out.push(...formatPseudoTableBlock(block));
    i = j - 1;
  }

  return out.join('\n');
}

export function normalizeAgentMarkdown(value: string, options: NormalizeOptions = {}): string {
  const { stripLeadingIndent: shouldStripLeadingIndent = false } = options;
  const lines = value.split(/\r?\n/);

  const firstPass = lines.reduce(
    (state, line) => {
      const trimmed = line.trim();
      const fence = trimmed.startsWith('```');
      if (fence) {
        return { inCode: !state.inCode, lines: [...state.lines, line] };
      }
      if (state.inCode) {
        return { inCode: true, lines: [...state.lines, line] };
      }

      const fixed = fixOrderedListPrefix(line);
      const finalLine = shouldStripLeadingIndent ? stripLeadingIndent(fixed) : fixed;
      return { inCode: false, lines: [...state.lines, finalLine] };
    },
    { inCode: false, lines: [] as string[] }
  );

  return repairPseudoTables(firstPass.lines.join('\n'));
}
