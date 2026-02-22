import React, { useEffect, useMemo, useState } from 'react';
import { Search, Zap, ChevronDown, ChevronLeft, ChevronRight, X } from 'lucide-react';
import SkillEditor from '@/components/editor/SkillEditor';
import { agentApi } from '@/services/agentApi';
import type { Skill } from '@/types/agent';

const GROUP_ORDER = [
    '故事诊断', '角色塑造', '结构设计',
    '写作技法', '世界构建',
];

// ── channel-style section header ──────────────────────────────────────────────
function SectionHeader({
  title, count, expanded, onToggle,
}: {
  title: string; count: number; expanded: boolean; onToggle: () => void;
}) {
  return (
    <button
      onClick={onToggle}
      className="w-full flex items-center gap-1.5 px-2 py-2
                 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg transition-colors"
    >
      {expanded
        ? <ChevronDown  className="w-4 h-4 shrink-0 text-gray-400 dark:text-gray-500" />
        : <ChevronRight className="w-4 h-4 shrink-0 text-gray-400 dark:text-gray-500" />
      }
      <span className="flex-1 text-left text-gray-500 dark:text-gray-400 text-sm uppercase tracking-wide">
        {title}
      </span>
      <span className="text-xs text-gray-400 dark:text-gray-500">{count}</span>
    </button>
  );
}

// ── main component ────────────────────────────────────────────────────────────
export default function SkillsView() {
  const [skills,  setSkills]  = useState<Skill[]>([]);
  const [loading, setLoading] = useState(true);
  const [error,   setError]   = useState<string | null>(null);
  const [selected, setSelected] = useState<Skill | null>(null);
  const [search,  setSearch]  = useState('');
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>(
    Object.fromEntries(GROUP_ORDER.map(g => [g, true]))
  );
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [enabledMap, setEnabledMap] = useState<Record<string, boolean>>({});
  const [toggling, setToggling] = useState<string | null>(null);

  useEffect(() => {
    agentApi.getSkills()
      .then(data => {
        setSkills(data);
        // 从 API 响应构建 enabledMap
        const map: Record<string, boolean> = {};
        for (const s of data) {
          map[s.name] = s.enabled ?? false;
        }
        setEnabledMap(map);
        setLoading(false);
      })
      .catch(err  => { setError(err?.message || '获取技能列表失败'); setLoading(false); });
  }, []);

  const handleToggleSkill = async (skillName: string) => {
    if (toggling) return;
    setToggling(skillName);
    const prev = enabledMap[skillName];
    setEnabledMap(m => ({ ...m, [skillName]: !prev }));
    try {
      await agentApi.toggleSkill(skillName);
    } catch (err: any) {
      setEnabledMap(m => ({ ...m, [skillName]: prev }));
      setError(err?.message || '切换技能状态失败');
    } finally {
      setToggling(null);
    }
  };

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase();
    if (!q) return skills;
    return skills.filter(s =>
      s.name.toLowerCase().includes(q) || s.description.toLowerCase().includes(q)
    );
  }, [skills, search]);

  const grouped = useMemo(() => {
    const map = new Map<string, Skill[]>();
    for (const s of filtered) {
      const arr = map.get(s.group) ?? [];
      arr.push(s);
      map.set(s.group, arr);
    }
    const out: [string, Skill[]][] = [];
    for (const g of GROUP_ORDER)   { if (map.has(g)) out.push([g, map.get(g)!]); }
    for (const [g, list] of map)   { if (!GROUP_ORDER.includes(g)) out.push([g, list]); }
    return out;
  }, [filtered]);

  // auto-select first skill on load
  useEffect(() => {
    if (!selected && grouped.length > 0 && grouped[0][1].length > 0) {
      setSelected(grouped[0][1][0]);
    }
  }, [grouped, selected]);

  // YAML 作为首个代码块，与正文一起在编辑器里
  const editorContent = useMemo(() => {
    if (!selected) return '';
    const yaml = [
      '```yaml',
      `name: ${selected.name}`,
      `category: ${selected.group}`,
      `description: ${selected.description}`,
      ...(selected.allowed_tools?.length
        ? [`allowed-tools: [${selected.allowed_tools.join(', ')}]`]
        : []),
      '```',
    ].join('\n');
    return selected.content ? yaml + '\n\n' + selected.content : yaml;
  }, [selected]);

  return (
    <div className="h-full flex flex-col bg-white dark:bg-gray-950 text-gray-900 dark:text-white">

      {/* ── body ──────────────────────────────────────────────────────────── */}
      <div className="flex-1 flex overflow-hidden">

        {/* ── left panel wrapper ────────────────────────────────────────── */}
        <div className="relative flex-shrink-0">
          <div
            className={`h-full ${
              isSidebarCollapsed ? 'w-0' : 'w-56 min-w-56'
            } transition-all duration-300 ease-in-out overflow-hidden border-r border-gray-100 dark:border-gray-700 flex flex-col bg-white dark:bg-gray-900`}
          >

            {/* search */}
            <div className="p-2">
              <div className="relative">
                <Search className="absolute left-2 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-gray-400 dark:text-gray-500" />
                <input
                  value={search}
                  onChange={e => setSearch(e.target.value)}
                  placeholder="搜索技能…"
                  className="w-full pl-7 pr-7 py-1.5 text-xs border border-gray-200 dark:border-gray-600
                             rounded-lg bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-gray-100
                             focus:outline-none focus:border-gray-300 dark:focus:border-gray-500"
                />
                {search && (
                  <button
                    onClick={() => setSearch('')}
                    className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300"
                  >
                    <X className="w-3 h-3" />
                  </button>
                )}
              </div>
            </div>

            {/* skill list */}
            <div className="flex-1 overflow-y-auto p-1.5 pb-3">
              {loading && (
                <p className="p-4 text-center text-xs text-gray-400 dark:text-gray-500">加载中…</p>
              )}
              {error && (
                <p className="p-4 text-center text-xs text-red-500 dark:text-red-400">{error}</p>
              )}

              {grouped.map(([group, items]) => {
                const isExpanded = expandedSections[group] ?? true;
                return (
                  <div key={group} className="mb-1">
                    <SectionHeader
                      title={group}
                      count={items.length}
                      expanded={isExpanded}
                      onToggle={() =>
                        setExpandedSections(prev => ({ ...prev, [group]: !prev[group] }))
                      }
                    />

                    {isExpanded && items.map(skill => {
                      const active = selected?.name === skill.name;
                      const isEnabled = enabledMap[skill.name] ?? false;
                      return (
                        <button
                          key={skill.name}
                          onClick={() => setSelected(skill)}
                          className={`w-full flex items-center gap-2 px-2 py-2 rounded-lg transition-colors ${
                            active
                              ? 'bg-gray-200 text-gray-900 dark:bg-zinc-700 dark:text-gray-100'
                              : 'hover:bg-gray-50 dark:hover:bg-zinc-800 text-gray-700 dark:text-gray-300'
                          } ${!isEnabled ? 'opacity-50' : ''}`}
                        >
                          <Zap className="shrink-0 w-4 h-4 opacity-60" />
                          <span className="flex-1 w-0 text-left truncate text-sm">{skill.name}</span>
                          {isEnabled && (
                            <span className="w-1.5 h-1.5 rounded-full bg-green-500 flex-shrink-0" />
                          )}
                        </button>
                      );
                    })}
                  </div>
                );
              })}
            </div>
          </div>

          {/* ── sidebar toggle button ─────────────────────────────────────── */}
          <button
            onClick={() => setIsSidebarCollapsed(prev => !prev)}
            className="absolute top-1/2 -translate-y-1/2 -right-3 z-10
                       w-6 h-6 rounded-full flex items-center justify-center
                       bg-white dark:bg-gray-800
                       border border-gray-200 dark:border-gray-600
                       shadow-sm hover:shadow
                       text-gray-400 dark:text-gray-500
                       hover:text-gray-600 dark:hover:text-gray-300
                       transition-colors"
          >
            {isSidebarCollapsed
              ? <ChevronRight className="w-3.5 h-3.5" />
              : <ChevronLeft  className="w-3.5 h-3.5" />
            }
          </button>
        </div>

        {/* ── right panel ───────────────────────────────────────────────── */}
        <div className="flex-1 flex flex-col overflow-hidden bg-white dark:bg-gray-950">
          {selected ? (
            <>
              {/* path bar */}
              <div className="flex items-center justify-between px-5 py-2.5 border-b border-gray-200 dark:border-slate-700 bg-gray-50 dark:bg-slate-900/30 flex-shrink-0">
                <div className="flex items-center gap-2 min-w-0">
                  <span className="text-gray-400 dark:text-slate-600 text-sm">/</span>
                  <span className="text-sm font-medium text-gray-900 dark:text-white truncate">
                    {selected.name}
                  </span>
                  <span className="text-[9px] px-1.5 py-0.5 rounded-full flex-shrink-0 bg-gray-100 dark:bg-slate-800 text-gray-500 dark:text-slate-400 border border-gray-200 dark:border-slate-700">
                    {selected.group}
                  </span>
                </div>

                <div className="flex items-center gap-3 flex-shrink-0">
                  {/* Toggle switch */}
                  <button
                    onClick={() => handleToggleSkill(selected.name)}
                    disabled={toggling === selected.name}
                    className={`relative w-9 h-5 rounded-full transition-colors ${
                      enabledMap[selected.name]
                        ? 'bg-green-500 dark:bg-green-600'
                        : 'bg-gray-300 dark:bg-slate-600'
                    } ${toggling === selected.name ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
                    aria-label={enabledMap[selected.name] ? '禁用技能' : '启用技能'}
                  >
                    <span className={`absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full shadow-sm transition-transform duration-200 ${
                      enabledMap[selected.name] ? 'translate-x-4' : 'translate-x-0'
                    }`} />
                  </button>
                </div>
              </div>

              {/* 统一滚动区：YAML 代码块 + 正文，全在同一个编辑器里 */}
              <div className="flex-1 overflow-hidden min-h-0">
                <SkillEditor
                  key={selected.name}
                  content={editorContent}
                  placeholder="在此编写技能文档…"
                />
              </div>
            </>
          ) : (
            !loading && (
              <div className="flex flex-col items-center justify-center h-full gap-3 text-gray-300 dark:text-slate-600">
                <span className="text-sm text-gray-400 dark:text-slate-500">选择一个技能查看详情</span>
              </div>
            )
          )}
        </div>
      </div>

    </div>
  );
}
