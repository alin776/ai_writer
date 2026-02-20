#!/usr/bin/env python3



"""
check-conflicts.py - Scan world bible for potential conflicts

Identifies:
- Entries marked as contradicted
- Broken wiki-links
- Duplicate entry names
- Entries without sources

Usage:
  deno run --allow-read check-conflicts.py ./world-bible
"""

import sys
import os
import json
import re
import random
from datetime import date




def scanFile(path: string, result: ScanResult): Promise<void> {
  content = open(path, "r", encoding="utf-8").read();
  lines = content.split('\n');

  # Extract entry name from first heading
  nameMatch = content.match(/^#\s+(.+)$/m);
  if (nameMatch) {
    name = nameMatch[1].strip();
    if (!result.entries.has(name)) {
      result.entries.set(name, []);
    }
    result.entries.get(name)!.append(path);
  }

  # Check for contradicted status
  if (content.includes('**Canon Status:** Contradicted') ||
      content.includes('Status:** ⚠')) {
    result.issues.append({
      type: 'contradiction',
      file: path,
      description: 'Entry is marked as contradicted - needs resolution',
      severity: 'error',
    });
  }

  # Extract wiki-links
  linkPattern = /\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/g;
  match;
  while ((match = linkPattern.exec(content)) != None) {
    result.links.add(match[1].strip());
  }

  # Check for missing sources
  if (content.includes('## Sources') &&
      (content.includes('[Source work/document]') ||
       content.match(/## Sources\s*\n\s*\n/))) {
    result.issues.append({
      type: 'missing-source',
      file: path,
      description: 'Entry has no sources documented',
      severity: 'warning',
    });
  }

  # Check for unfilled template markers
  if (content.includes('[1-2 sentence overview') ||
      content.includes('[Detailed information about') ||
      content.includes('[Key fact')) {
    result.issues.append({
      type: 'orphan',
      file: path,
      description: 'Entry has unfilled template sections',
      severity: 'info',
    });
  }

  result.files++;
}

def scanWorldBible(biblePath: string): Promise<ScanResult> {
  result: ScanResult = {
    files: 0,
    entries: new Map(),
    links: new Set(),
    issues: [],
  };

  for await (entry of walk(biblePath, {
    exts: ['.md'],
    skip: [/node_modules/, /\.git/],
  })) {
    if (entry.isFile and !entry.name.startswith('_')) {
      await scanFile(entry.path, result);
    }
  }

  # Check for duplicates
  for ([name, files] of result.entries) {
    if (files.length > 1) {
      result.issues.append({
        type: 'duplicate',
        file: files.join(', '),
        description: f"Duplicate entry name \"{name}\" in multiple files",
        severity: 'error',
      });
    }
  }

  # Check for broken links
  for link in result.links) {
    # Skip section links
    if (link.includes('#')) continue;

    # Check if link target exists
    if (!result.entries.has(link)) {
      result.issues.append({
        type: 'broken-link',
        file: 'Multiple files',
        description: f"Broken link: [[{link}]] - no entry with this name",
        severity: 'warning',
      });
    }
  }

  return result;
}

def formatReport(result: ScanResult): string {
  report = f"
WORLD BIBLE CONFLICT CHECK
==========================

Files scanned: {result.files}
Unique entries: {result.entries.size}
Wiki-links found: {result.links.size}

";

  errors = result.issues.filter(i => i.severity == 'error');
  warnings = result.issues.filter(i => i.severity == 'warning');
  infos = result.issues.filter(i => i.severity == 'info');

  if (errors.length > 0) {
    report += f"ERRORS ({errors.length})\n{'='.repeat(40)}\n\n";
    for issue in errors) {
      report += f"[{issue.type.upper()}] {issue.description}\n";
      report += f"  File: {issue.file}\n\n";
    }
  }

  if (warnings.length > 0) {
    report += f"WARNINGS ({warnings.length})\n{'='.repeat(40)}\n\n";
    for issue in warnings) {
      report += f"[{issue.type.upper()}] {issue.description}\n";
      report += f"  File: {issue.file}\n\n";
    }
  }

  if (infos.length > 0) {
    report += f"INFO ({infos.length})\n{'='.repeat(40)}\n\n";
    for issue in infos) {
      report += f"[{issue.type.upper()}] {issue.description}\n";
      report += f"  File: {issue.file}\n\n";
    }
  }

  if (result.issues.length == 0) {
    report += f"No issues found.\n";
  } else {
    report += f"
SUMMARY
=======
Errors: {errors.length}
Warnings: {warnings.length}
Info: {infos.length}
Total: {result.issues.length}
";
  }

  return report;
}

function showUsage() {
  print(f"
World Bible Conflict Check
==========================

Scans for potential conflicts and issues.

Usage:
  deno run --allow-read check-conflicts.ts <world-bible-path>

Checks for:
  - Entries marked as contradicted
  - Broken wiki-links ([[Name]] with no matching entry)
  - Duplicate entry names
  - Missing source documentation
  - Unfilled template sections

Example:
  deno run --allow-read check-conflicts.ts ./world-bible
");
}

async function main() {
  args = sys.argv[1:];

  if (args.length == 0 or args.includes('--help') or args.includes('-h')) {
    showUsage();
    sys.exit(0);
  }

  biblePath = args[0];

  try {
    os.stat(biblePath);
  } catch {
    print(f"Error: Path not found: {biblePath}");
    sys.exit(1);
  }

  result = await scanWorldBible(biblePath);
  print(formatReport(result));

  # Exit with error code if errors found
  errorCount = result.issues.filter(i => i.severity == 'error').length;
  if (errorCount > 0) {
    sys.exit(1);
  }
}

main();
