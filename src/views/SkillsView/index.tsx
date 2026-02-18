import React, { useEffect, useMemo, useState } from 'react';
import { Zap, Loader2, AlertCircle } from 'lucide-react';
import { agentApi } from '@/services/agentApi';

interface Skill {
  name: string;
  description: string;
  group: string;
}

const GROUP_ORDER = ['质量检查', '创作分析', '创作辅助'];

export default function SkillsView() {
  const [skills, setSkills] = useState<Skill[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSkill, setSelectedSkill] = useState<Skill | null>(null);

  useEffect(() => {
    const fetchSkills = async () => {
      try {
        setLoading(true);
        const data = await agentApi.getSkills();
        setSkills(data);
      } catch (err: any) {
        setError(err?.message || '获取技能列表失败');
      } finally {
        setLoading(false);
      }
    };
    fetchSkills();
  }, []);

  const grouped = useMemo(() => {
    const map = new Map<string, Skill[]>();
    for (const skill of skills) {
      const list = map.get(skill.group) || [];
      list.push(skill);
      map.set(skill.group, list);
    }
    const sorted: [string, Skill[]][] = [];
    for (const g of GROUP_ORDER) {
      if (map.has(g)) sorted.push([g, map.get(g)!]);
    }
    for (const [g, list] of map) {
      if (!GROUP_ORDER.includes(g)) sorted.push([g, list]);
    }
    return sorted;
  }, [skills]);

  // Auto-select first visible skill after grouping
  useEffect(() => {
    if (grouped.length > 0 && grouped[0][1].length > 0 && !selectedSkill) {
      setSelectedSkill(grouped[0][1][0]);
    }
  }, [grouped, selectedSkill]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full py-32">
        <Loader2 className="w-6 h-6 animate-spin text-gray-400" />
        <span className="ml-2 text-gray-500">加载技能列表...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-full py-32 text-gray-500">
        <AlertCircle className="w-8 h-8 mb-2 text-red-400" />
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="px-6 py-5 border-b border-gray-200 dark:border-slate-700">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-amber-50 dark:bg-amber-900/30 flex items-center justify-center">
            <Zap className="w-5 h-5 text-amber-600 dark:text-amber-400" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-gray-900 dark:text-white">AI 技能</h1>
            <p className="text-sm text-gray-500 dark:text-slate-400">
              {skills.length} 个可用技能 · 在对话中使用 <code className="px-1.5 py-0.5 bg-gray-100 dark:bg-slate-800 rounded text-xs">/技能名</code> 快速调用
            </p>
          </div>
        </div>
      </div>

      {/* Body: left list + right detail */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left panel — grouped skill list */}
        <div className="w-72 border-r border-gray-200 dark:border-slate-700 overflow-y-auto py-4 px-3 space-y-5">
          {grouped.map(([group, items]) => (
            <div key={group}>
              <div className="px-3 pb-2 text-xs font-medium text-gray-400 dark:text-slate-500 uppercase tracking-wider">
                {group}
              </div>
              <div className="space-y-0.5">
                {items.map((skill) => {
                  const active = selectedSkill?.name === skill.name;
                  return (
                    <button
                      key={skill.name}
                      onClick={() => setSelectedSkill(skill)}
                      className={`w-full text-left px-3 py-2.5 rounded-lg transition-colors ${
                        active
                          ? 'bg-amber-50 dark:bg-amber-900/20 text-amber-800 dark:text-amber-300'
                          : 'hover:bg-gray-100 dark:hover:bg-slate-800 text-gray-700 dark:text-slate-300'
                      }`}
                    >
                      <div className="flex items-center gap-2">
                        <Zap className={`w-3.5 h-3.5 flex-shrink-0 ${active ? 'text-amber-500' : 'text-gray-400'}`} />
                        <span className="text-sm font-medium truncate">{skill.name}</span>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          ))}
        </div>

        {/* Right panel — skill detail */}
        <div className="flex-1 overflow-y-auto p-6">
          {selectedSkill ? (
            <div className="max-w-2xl">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-xl bg-amber-50 dark:bg-amber-900/30 flex items-center justify-center">
                  <Zap className="w-5 h-5 text-amber-500" />
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">{selectedSkill.name}</h2>
                  <span className="text-xs px-2 py-0.5 rounded-full bg-gray-100 dark:bg-slate-800 text-gray-500 dark:text-slate-400">
                    {selectedSkill.group}
                  </span>
                </div>
              </div>
              <div className="prose prose-sm dark:prose-invert max-w-none">
                <p className="text-gray-600 dark:text-slate-300 leading-relaxed whitespace-pre-wrap">
                  {selectedSkill.description}
                </p>
              </div>
              <div className="mt-6 p-4 rounded-xl bg-gray-50 dark:bg-slate-800/50 border border-gray-200 dark:border-slate-700">
                <p className="text-xs text-gray-500 dark:text-slate-400">
                  💡 在 AI 对话框中输入 <code className="px-1.5 py-0.5 bg-white dark:bg-slate-700 rounded text-amber-600 dark:text-amber-400">/{selectedSkill.name}</code> 即可调用此技能
                </p>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center h-full text-gray-400">
              <p>选择一个技能查看详情</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
