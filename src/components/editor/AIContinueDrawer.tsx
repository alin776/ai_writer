/**
 * AI 续写参数设置抽屉 (优化版)
 * 从右侧滑出，支持快速模式和专业模式
 * 严格遵循详细的 UI/UX 规范：圆角、焦点样式、颜色对比、动态数组管理、平滑动画。
 */
import React, { useState, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { X, Sparkles, ChevronDown, Plus, Trash2, Zap, Settings, Loader2 } from 'lucide-react';

// 保持原有的接口定义
export interface AIContinueConfig {
    lastChapterContext: string;
    focusCharacter: string;
    characterStatus: string;
    coreLocation: string;
    environmentStatus: string;
    settingConstraints: string;
    styleAdjectives: string;
    emotionalTone: string;
    narrativePerspective: '第一人称' | '第三人称受限视角' | '全知视角' | string; // 增加 string 以兼容初始空值
    perspectiveFocusCharacter: string;
    targetLength: number;
    endingStyle: string;
    plotPoints: string[];
    prohibitedContent: string[];
}

interface AIContinueDrawerProps {
    isOpen: boolean;
    onClose: () => void;
    onConfirm: (config: AIContinueConfig) => void;
    editorContent: string;
}

type Mode = 'quick' | 'professional';
type PanelKey = 'character' | 'style' | 'output' | 'context';

// 默认配置（更严谨的初始化）
const DEFAULT_CONFIG: AIContinueConfig = {
    lastChapterContext: '',
    focusCharacter: '',
    characterStatus: '',
    coreLocation: '',
    environmentStatus: '',
    settingConstraints: '',
    styleAdjectives: '',
    emotionalTone: '',
    narrativePerspective: '第三人称受限视角',
    perspectiveFocusCharacter: '',
    targetLength: 300,
    endingStyle: '',
    plotPoints: [''],
    prohibitedContent: [''],
};

const AIContinueDrawer: React.FC<AIContinueDrawerProps> = ({
    isOpen,
    onClose,
    onConfirm,
    editorContent,
}) => {
    const { t } = useTranslation();
    const [mode, setMode] = useState<Mode>('quick');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [errors, setErrors] = useState<{ [key: string]: string }>({});
    const [config, setConfig] = useState<AIContinueConfig>(DEFAULT_CONFIG);

    // 折叠面板状态 - 初始保持收起
    const [expandedPanels, setExpandedPanels] = useState<Record<PanelKey, boolean>>({
        character: false,
        style: false,
        output: false,
        context: false,
    });

    // 1. 自动提取最后1000字作为上下文
    useEffect(() => {
        if (isOpen && editorContent) {
            // 提取最后1000字
            const context = editorContent.length > 1000
                ? '...' + editorContent.slice(-1000)
                : editorContent;
            setConfig((prev) => ({ ...prev, lastChapterContext: context }));
        }
    }, [isOpen, editorContent]);

    // 2. 通用输入处理
    const handleInputChange = useCallback((field: keyof AIContinueConfig, value: any) => {
        setConfig((prev) => ({ ...prev, [field]: value }));
        // 焦点时清除错误
        if (errors[field]) {
            setErrors((prev) => {
                const newErrors = { ...prev };
                delete newErrors[field];
                return newErrors;
            });
        }
    }, [errors]);

    // 3. 数组输入处理 (Plot Points / Prohibited Content)
    const handleArrayChange = useCallback((field: 'plotPoints' | 'prohibitedContent', index: number, value: string) => {
        setConfig((prev) => ({
            ...prev,
            [field]: prev[field].map((item, i) => (i === index ? value : item)),
        }));
    }, []);

    const addArrayItem = useCallback((field: 'plotPoints' | 'prohibitedContent') => {
        setConfig((prev) => ({
            ...prev,
            [field]: [...prev[field].filter(Boolean), ''], // 添加前先清理空项
        }));
    }, []);

    const removeArrayItem = useCallback((field: 'plotPoints' | 'prohibitedContent', index: number) => {
        // 强制 Plot Points 至少保留一个
        if (field === 'plotPoints' && config.plotPoints.length === 1) return;
        
        setConfig((prev) => ({
            ...prev,
            [field]: prev[field].filter((_, i) => i !== index),
        }));
    }, [config.plotPoints.length]);

    // 4. 折叠面板切换
    const togglePanel = useCallback((panel: PanelKey) => {
        setExpandedPanels((prev) => ({ ...prev, [panel]: !prev[panel] }));
    }, []);

    // 5. 验证逻辑
    const validateConfig = (): boolean => {
        const newErrors: { [key: string]: string } = {};

        // 关键情节目标验证（无论模式，只要列表不为空，至少要有一个非空项）
        const hasValidPlotPoint = config.plotPoints.some(p => p.trim());
        if (!hasValidPlotPoint) {
            newErrors.plotPoints = t('editor.aiContinue.writingIntentRequired');
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    // 6. 提交逻辑
    const handleSubmit = async () => {
        if (!validateConfig()) {
            // 自动展开到错误面板
            if (errors.plotPoints) {
                setExpandedPanels(prev => ({ ...prev, output: true }));
            }
            return;
        }

        setIsSubmitting(true);
        try {
            // 提交前清理空字符串，只发送有效数据
            const finalConfig: AIContinueConfig = {
                ...config,
                plotPoints: config.plotPoints.filter(Boolean),
                prohibitedContent: config.prohibitedContent.filter(Boolean),
            };
            await onConfirm(finalConfig);
        } finally {
            setIsSubmitting(false);
        }
    };

    // 7. 文风标签逻辑
    const styleTagsKeys = ['tense', 'calm', 'humorous', 'romantic', 'suspense', 'relaxed', 'serious', 'emotional'];
    const MAX_TAGS = 3;

    const toggleStyleTag = useCallback((tag: string) => {
        // 使用 set 的方式处理标签，避免逗号分隔符带来的解析问题
        const currentTags = config.styleAdjectives.split('、').filter(t => t.trim());
        const tagSet = new Set(currentTags);

        if (tagSet.has(tag)) {
            tagSet.delete(tag);
        } else {
            if (tagSet.size < MAX_TAGS) {
                tagSet.add(tag);
            }
        }
        handleInputChange('styleAdjectives', Array.from(tagSet).join('、'));
    }, [config.styleAdjectives, handleInputChange]);

    const isStyleTagSelected = (tag: string) => {
        return config.styleAdjectives.split('、').includes(tag);
    };

    const isQuickModePlotError = mode === 'quick' && errors.plotPoints;
    const isProfessionalModePlotError = mode === 'professional' && errors.plotPoints;


    return (
        <>
            {/* 1. 半透明遮罩 - 增强视觉效果 */}
            <div
                className={`fixed inset-0 bg-gradient-to-br from-gray-900/60 to-gray-900/40 backdrop-blur-sm z-40 transition-opacity duration-300 ease-out ${
                    isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
                }`}
                onClick={onClose}
            />

            {/* 2. 抽屉容器 - 增强阴影和圆角 */}
            <div
                className={`fixed top-0 right-0 h-screen w-96 bg-gradient-to-b from-white to-gray-50/30 shadow-2xl z-50 flex flex-col transition-all duration-300 ease-out ${
                    isOpen ? 'translate-x-0' : 'translate-x-full'
                }`}
            >
                {/* 2.1 顶部操作区 (Header) - 增强渐变和阴影 */}
                <div className="flex items-center justify-between px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-blue-50/50 to-purple-50/30">
                    <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                        <Sparkles className="w-5 h-5 text-blue-600" />
                        {t('editor.aiContinue.settingsTitle')}
                    </h2>
                    <div className="flex items-center gap-3">
                        {/* 模式切换 - 优化的标签组样式 */}
                        <div className="inline-flex rounded-lg bg-gradient-to-br from-gray-100 to-gray-200/50 p-1 shadow-inner">
                            <button
                                onClick={() => setMode('quick')}
                                className={`px-3 py-1.5 text-sm font-medium rounded-md transition-all duration-200 flex items-center gap-1.5 transform ${
                                    mode === 'quick'
                                        ? 'bg-indigo-600 text-gray-100 shadow-lg scale-105' // <-- 修正: text-white -> text-gray-100
                                        : 'text-gray-700 hover:text-gray-900 hover:bg-white hover:shadow-sm'
                                }`}
                            >
                                <Zap className="w-4 h-4" />
                                {t('editor.aiContinue.quickMode')}
                            </button>
                            <button
                                onClick={() => setMode('professional')}
                                className={`px-3 py-1.5 text-sm font-medium rounded-md transition-all duration-200 flex items-center gap-1.5 transform ${
                                    mode === 'professional'
                                        ? 'bg-indigo-600 text-gray-100 shadow-lg scale-105' // <-- 修正: text-white -> text-gray-100
                                        : 'text-gray-700 hover:text-gray-900 hover:bg-white hover:shadow-sm'
                                }`}
                            >
                                <Settings className="w-4 h-4" />
                                {t('editor.aiContinue.professionalMode')}
                            </button>
                        </div>
                        {/* 关闭按钮 - 增强 hover 效果 */}
                        <button
                            onClick={onClose}
                            className="p-1.5 rounded-lg hover:bg-red-50 hover:text-red-600 text-gray-500 transition-all duration-200 transform hover:scale-110"
                            title={t('editor.aiContinue.close')}
                        >
                            <X className="w-5 h-5" />
                        </button>
                    </div>
                </div>

                {/* 2.2 内容区 - 可滚动，间距优化 */}
                <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6">
                    {mode === 'quick' ? (
                        /* ==================== 快速模式 ==================== */
                        <>
                            {/* 续写意图 (简版) - 增强视觉效果 */}
                            <div className="group">
                                <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center gap-1">
                                    <span className="w-1.5 h-1.5 rounded-full bg-blue-600"></span>
                                    {t('editor.aiContinue.writingIntent')} <span className="text-red-500">*</span>
                                </label>
                                <textarea
                                    value={config.plotPoints[0] || ''}
                                    onChange={(e) => handleArrayChange('plotPoints', 0, e.target.value)}
                                    className={`w-full px-4 py-3 text-sm bg-white border-2 rounded-xl focus:outline-none focus:ring-2 transition-all duration-200 resize-none shadow-sm ${
                                        isQuickModePlotError
                                            ? 'border-red-400 focus:ring-red-200 focus:border-red-500'
                                            : 'border-gray-200 focus:border-blue-500 focus:ring-blue-100 hover:border-gray-300'
                                    }`}
                                    rows={3}
                                    placeholder={t('editor.aiContinue.writingIntentPlaceholder')}
                                />
                                {isQuickModePlotError && (
                                    <p className="mt-2 text-sm text-red-500 flex items-center gap-1 animate-pulse">
                                        <span className="w-1 h-1 rounded-full bg-red-500"></span>
                                        {errors.plotPoints}
                                    </p>
                                )}
                            </div>

                            {/* 目标长度 (滑块 + 数字输入) - 增强视觉效果 */}
                            <div className="p-4 rounded-xl bg-gradient-to-br from-blue-50/50 to-purple-50/30 border border-blue-100">
                                <label className="block text-sm font-medium text-gray-700 mb-3 flex items-center gap-2">
                                    <span className="w-1.5 h-1.5 rounded-full bg-blue-600"></span>
                                    {t('editor.aiContinue.targetLengthLabel')}：<span className="font-bold text-blue-600 text-base">{config.targetLength} {t('editor.aiContinue.words')}</span>
                                </label>
                                <div className="space-y-3">
                                    <input
                                        type="range"
                                        min="100"
                                        max="1000"
                                        step="50"
                                        value={config.targetLength}
                                        onChange={(e) => handleInputChange('targetLength', parseInt(e.target.value))}
                                        className="w-full h-2.5 bg-gradient-to-r from-blue-200 to-purple-200 rounded-full appearance-none cursor-pointer shadow-inner
                                            [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-5 [&::-webkit-slider-thumb]:h-5
                                            [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-gradient-to-r [&::-webkit-slider-thumb]:from-blue-600 [&::-webkit-slider-thumb]:to-blue-500 [&::-webkit-slider-thumb]:cursor-pointer [&::-webkit-slider-thumb]:shadow-lg [&::-webkit-slider-thumb]:transition-transform [&::-webkit-slider-thumb]:hover:scale-110
                                            [&::-moz-range-thumb]:w-5 [&::-moz-range-thumb]:h-5 [&::-moz-range-thumb]:rounded-full [&::-moz-range-thumb]:bg-gradient-to-r [&::-moz-range-thumb]:from-blue-600 [&::-moz-range-thumb]:to-blue-500 [&::-moz-range-thumb]:cursor-pointer [&::-moz-range-thumb]:shadow-lg"
                                    />
                                    <div className="flex items-center justify-between">
                                        <span className="text-xs font-medium text-gray-600">100 {t('editor.aiContinue.words')}</span>
                                        <input
                                            type="number"
                                            value={config.targetLength}
                                            onChange={(e) => handleInputChange('targetLength', parseInt(e.target.value) || 300)}
                                            className="w-20 px-3 py-1.5 text-sm font-semibold bg-white border-2 border-blue-200 rounded-lg text-center focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition-all duration-200"
                                            min="100"
                                            max="1000"
                                        />
                                        <span className="text-xs font-medium text-gray-600">1000 {t('editor.aiContinue.words')}</span>
                                    </div>
                                </div>
                            </div>

                            {/* 文风微调 (标签组) - 增强动画效果 */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-3 flex items-center gap-1">
                                    <span className="w-1.5 h-1.5 rounded-full bg-blue-600"></span>
                                    {t('editor.aiContinue.styleTuning')} <span className="text-xs text-gray-500">({t('editor.aiContinue.styleTuningHint', { n: MAX_TAGS })})</span>
                                </label>
                                <div className="flex flex-wrap gap-2">
                                    {styleTagsKeys.map((tagKey) => {
                                        const tagLabel = t(`editor.aiContinue.styleOptions.${tagKey}`);
                                        return (
                                        <button
                                            key={tagKey}
                                            onClick={() => toggleStyleTag(tagLabel)}
                                            disabled={!isStyleTagSelected(tagLabel) && config.styleAdjectives.split('、').filter(t => t.trim()).length >= MAX_TAGS}
                                            className={`px-4 py-2 text-sm font-medium rounded-full transition-all duration-200 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 ${
                                                isStyleTagSelected(tagLabel)
                                                    ? 'bg-indigo-600 text-white shadow-md'
                                                    : 'bg-white text-gray-800 border-2 border-gray-200 hover:border-blue-400 hover:bg-blue-50 shadow-sm'
                                            }`}
                                        >
                                            {tagLabel}
                                        </button>
                                        );
                                    })}
                                </div>
                            </div>

                            {/* 叙事视角 (按钮组) - 增强视觉效果 */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-3 flex items-center gap-1">
                                    <span className="w-1.5 h-1.5 rounded-full bg-blue-600"></span>
                                    {t('editor.aiContinue.narrativePerspective')}
                                </label>
                                <div className="grid grid-cols-3 gap-2">
                                    {[
                                        { key: 'firstPerson', value: '第一人称' },
                                        { key: 'thirdPersonLimited', value: '第三人称受限视角' },
                                        { key: 'omniscient', value: '全知视角' }
                                    ].map(({ key, value }) => (
                                        <button
                                            key={key}
                                            onClick={() => handleInputChange('narrativePerspective', value)}
                                            className={`px-3 py-3 text-xs rounded-xl border-2 transition-all duration-200 font-semibold transform hover:scale-105 ${
                                                config.narrativePerspective === value
                                                    ? 'bg-indigo-600 text-white border-indigo-600 shadow-lg'
                                                    : 'bg-white text-gray-800 border-gray-200 hover:border-blue-400 hover:bg-blue-50 shadow-sm'
                                            }`}
                                        >
                                            {t(`editor.aiContinue.${key}`)}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </>
                    ) : (
                        /* ==================== 专业模式 ==================== */
                        <>
                            {/* 关键情节目标（必填高亮，动态列表） - 增强视觉效果 */}
                            <div className="p-5 bg-gradient-to-br from-blue-50 to-indigo-50/30 rounded-xl border-2 border-blue-200 shadow-sm">
                                <label className="block text-sm font-bold text-gray-900 mb-2 flex items-center gap-2">
                                    <Sparkles className="w-4 h-4 text-blue-600" />
                                    {t('editor.aiContinue.plotPoints')} <span className="text-red-500">*</span>
                                </label>
                                <p className="text-xs text-gray-600 mb-4">{t('editor.aiContinue.plotPointsRequired')}</p>
                                <div className="space-y-2">
                                    {config.plotPoints.map((point, index) => (
                                        <div key={index} className="flex gap-2 items-start">
                                            <span className="flex-shrink-0 w-6 h-10 pt-2 flex justify-center text-sm text-gray-600 font-medium">
                                                {index + 1}.
                                            </span>
                                            <div className="flex-1">
                                                <input
                                                    type="text"
                                                    value={point}
                                                    onChange={(e) => handleArrayChange('plotPoints', index, e.target.value)}
                                                    className={`w-full px-3 py-2.5 text-sm bg-white border rounded-lg focus:outline-none focus:ring-1 transition-colors duration-200 ${
                                                        isProfessionalModePlotError && !point.trim() && index === 0
                                                            ? 'border-red-500 focus:ring-red-500'
                                                            : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
                                                    }`}
                                                    placeholder={t('editor.aiContinue.plotPointPlaceholder', { n: index + 1 })}
                                                />
                                                {isProfessionalModePlotError && index === 0 && !point.trim() && (
                                                    <p className="mt-1 text-xs text-red-500">{errors.plotPoints}</p>
                                                )}
                                            </div>
                                            {config.plotPoints.length > 1 && (
                                                <button
                                                    onClick={() => removeArrayItem('plotPoints', index)}
                                                    className="flex-shrink-0 p-2.5 text-red-500 hover:bg-red-100 rounded-md transition-colors duration-200"
                                                    title="删除"
                                                >
                                                    <Trash2 className="w-4 h-4" />
                                                </button>
                                            )}
                                        </div>
                                    ))}
                                    {config.plotPoints.length < 5 && (
                                        <button
                                            onClick={() => addArrayItem('plotPoints')}
                                            className="w-full px-4 py-3 text-sm text-blue-600 font-semibold border-2 border-blue-300 border-dashed rounded-xl hover:bg-blue-100 hover:border-blue-400 transition-all duration-200 flex items-center justify-center gap-2 mt-3 transform hover:scale-[1.02]"
                                        >
                                            <Plus className="w-4 h-4" />
                                            {t('editor.aiContinue.addNewTarget')}
                                        </button>
                                    )}
                                </div>
                            </div>

                            {/* 折叠面板 A：核心角色状态与地点 */}
                            {renderAccordionPanel('character', t('editor.aiContinue.characterPanel'), expandedPanels.character, togglePanel, (
                                <div className="px-4 py-4 border-t border-gray-200 space-y-3">
                                    <div className="grid grid-cols-2 gap-3">
                                        {/* 焦点人物 */}
                                        <InputGroup label={t('editor.aiContinue.focusCharacter')} placeholder={t('editor.aiContinue.focusCharacterPlaceholder')} value={config.focusCharacter} onChange={(e) => handleInputChange('focusCharacter', e.target.value)} />
                                        {/* 当前情绪 */}
                                        <InputGroup label={t('editor.aiContinue.currentMood')} placeholder={t('editor.aiContinue.currentMoodPlaceholder')} value={config.characterStatus} onChange={(e) => handleInputChange('characterStatus', e.target.value)} />
                                    </div>
                                    <div className="grid grid-cols-2 gap-3">
                                        {/* 核心地点 */}
                                        <InputGroup label={t('editor.aiContinue.coreLocation')} placeholder={t('editor.aiContinue.coreLocationPlaceholder')} value={config.coreLocation} onChange={(e) => handleInputChange('coreLocation', e.target.value)} />
                                        {/* 环境状态 */}
                                        <InputGroup label={t('editor.aiContinue.environmentStatus')} placeholder={t('editor.aiContinue.environmentStatusPlaceholder')} value={config.environmentStatus} onChange={(e) => handleInputChange('environmentStatus', e.target.value)} />
                                    </div>
                                    {/* 关键设定限制 */}
                                    <div>
                                        <label className="block text-xs font-medium text-gray-700 mb-1.5">{t('editor.aiContinue.settingConstraints')}</label>
                                        <textarea
                                            value={config.settingConstraints}
                                            onChange={(e) => handleInputChange('settingConstraints', e.target.value)}
                                            className="w-full px-3 py-2 text-sm bg-gray-50 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-blue-500 resize-none"
                                            rows={2}
                                            placeholder={t('editor.aiContinue.settingConstraintsPlaceholder')}
                                        />
                                    </div>
                                </div>
                            ))}

                            {/* 折叠面板 B：风格、情绪与视角 */}
                            {renderAccordionPanel('style', t('editor.aiContinue.stylePanel'), expandedPanels.style, togglePanel, (
                                <div className="px-4 py-4 border-t border-gray-200 space-y-3">
                                    {/* 文风形容词 */}
                                    <InputGroup label={`${t('editor.aiContinue.styleAdjectives')} (${t('editor.aiContinue.styleAdjectivesHint')})`} placeholder={t('editor.aiContinue.styleAdjectivesPlaceholder')} value={config.styleAdjectives} onChange={(e) => handleInputChange('styleAdjectives', e.target.value)} />
                                    {/* 情绪基调 */}
                                    <InputGroup label={t('editor.aiContinue.emotionalTone')} placeholder={t('editor.aiContinue.emotionalTonePlaceholder')} value={config.emotionalTone} onChange={(e) => handleInputChange('emotionalTone', e.target.value)} />

                                    {/* 叙事视角 (下拉选择) */}
                                    <div>
                                        <label className="block text-xs font-medium text-gray-700 mb-1.5">{t('editor.aiContinue.narrativePerspective')}</label>
                                        <select
                                            value={config.narrativePerspective}
                                            onChange={(e) => handleInputChange('narrativePerspective', e.target.value)}
                                            className="w-full px-3 py-2.5 text-sm bg-gray-50 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-blue-500"
                                        >
                                            <option value="第一人称">{t('editor.aiContinue.firstPerson')}</option>
                                            <option value="第三人称受限视角">{t('editor.aiContinue.thirdPersonLimited')}</option>
                                            <option value="全知视角">{t('editor.aiContinue.omniscient')}</option>
                                        </select>
                                    </div>
                                    {/* 焦点角色（受限视角专属） */}
                                    {config.narrativePerspective === '第三人称受限视角' && (
                                        <InputGroup label={t('editor.aiContinue.perspectiveFocusCharacter')} placeholder={t('editor.aiContinue.perspectiveFocusCharacterPlaceholder')} value={config.perspectiveFocusCharacter} onChange={(e) => handleInputChange('perspectiveFocusCharacter', e.target.value)} />
                                    )}
                                </div>
                            ))}

                            {/* 折叠面板 C：输出控制与限制 */}
                            {renderAccordionPanel('output', t('editor.aiContinue.outputPanel'), expandedPanels.output, togglePanel, (
                                <div className="px-4 py-4 border-t border-gray-200 space-y-4">
                                    {/* 目标长度 (专业模式下的精确控制) */}
                                    <div>
                                        <label className="block text-xs font-medium text-gray-700 mb-2">
                                            {t('editor.aiContinue.targetLengthLabel')}：<span className="font-semibold text-blue-600">{config.targetLength} {t('editor.aiContinue.words')}</span>
                                        </label>
                                        {/* 滑块部分与快速模式保持一致，省略重复代码 */}
                                        <div className="space-y-2">
                                            <input
                                                type="range"
                                                min="100"
                                                max="1000"
                                                step="50"
                                                value={config.targetLength}
                                                onChange={(e) => handleInputChange('targetLength', parseInt(e.target.value))}
                                                className="w-full h-2 bg-gray-300 rounded-lg appearance-none cursor-pointer
                                                    [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4
                                                    [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-blue-600 [&::-webkit-slider-thumb]:cursor-pointer
                                                    [&::-moz-range-thumb]:w-4 [&::-moz-range-thumb]:h-4 [&::-moz-range-thumb]:rounded-full [&::-moz-range-thumb]:bg-blue-600 [&::-moz-range-thumb]:cursor-pointer"
                                            />
                                            <div className="flex items-center justify-center gap-2">
                                                <input
                                                    type="number"
                                                    value={config.targetLength}
                                                    onChange={(e) => handleInputChange('targetLength', parseInt(e.target.value) || 300)}
                                                    className="w-20 px-3 py-1.5 text-sm bg-gray-50 border border-gray-300 rounded-md text-center focus:outline-none focus:border-blue-500 focus:ring-blue-500"
                                                    min="100"
                                                    max="1000"
                                                />
                                                <span className="text-sm text-gray-600">{t('editor.aiContinue.words')}</span>
                                            </div>
                                        </div>
                                    </div>

                                    {/* 结尾形式 */}
                                    <InputGroup label={t('editor.aiContinue.endingStyle')} placeholder={t('editor.aiContinue.endingStylePlaceholder')} value={config.endingStyle} onChange={(e) => handleInputChange('endingStyle', e.target.value)} />

                                    {/* 禁止内容 (动态列表，高亮提示) */}
                                    <div>
                                        <label className="block text-xs font-medium text-gray-700 mb-1.5">
                                            {t('editor.aiContinue.prohibitedContent')} <span className="text-red-600 text-xs font-bold">({t('editor.aiContinue.absoluteRestriction')})</span>
                                        </label>
                                        <div className="space-y-2">
                                            {config.prohibitedContent.map((item, index) => (
                                                <div key={index} className="flex gap-2">
                                                    <input
                                                        type="text"
                                                        value={item}
                                                        onChange={(e) => handleArrayChange('prohibitedContent', index, e.target.value)}
                                                        className="flex-1 px-3 py-2 text-sm bg-gray-50 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-blue-500"
                                                        placeholder={t('editor.aiContinue.prohibitedPlaceholder', { n: index + 1 })}
                                                    />
                                                    {config.prohibitedContent.length > 1 && (
                                                        <button
                                                            onClick={() => removeArrayItem('prohibitedContent', index)}
                                                            className="flex-shrink-0 p-2 text-red-500 hover:bg-red-100 rounded-md transition-colors duration-200"
                                                            title={t('common.delete')}
                                                        >
                                                            <Trash2 className="w-4 h-4" />
                                                        </button>
                                                    )}
                                                </div>
                                            ))}
                                            <button
                                                onClick={() => addArrayItem('prohibitedContent')}
                                                className="w-full px-3 py-2 text-sm text-blue-600 font-medium border border-blue-300 border-dashed rounded-lg hover:bg-blue-50 transition-colors duration-200 flex items-center justify-center gap-2"
                                            >
                                                <Plus className="w-4 h-4" />
                                                {t('editor.aiContinue.addProhibited')}
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            ))}
                            
                            {/* 折叠面板 D：当前上下文预览 (只读) */}
                            {renderAccordionPanel('context', t('editor.aiContinue.contextPreview'), expandedPanels.context, togglePanel, (
                                <div className="px-4 py-4 border-t border-gray-200">
                                    <div className="p-3 bg-gray-100 rounded-lg text-xs text-gray-700 leading-relaxed max-h-40 overflow-y-auto font-mono border border-gray-300">
                                        {config.lastChapterContext || t('editor.aiContinue.noContextContent')}
                                    </div>
                                </div>
                            ))}
                        </>
                    )}
                </div>

                {/* 2.3 底部操作区 (Footer) - 增强视觉效果和互动 */}
                <div className="flex items-center justify-end gap-3 px-6 py-5 border-t border-gray-200 shadow-lg bg-gradient-to-r from-white to-gray-50/50">
                    <button
                        onClick={onClose}
                        disabled={isSubmitting}
                        className="px-6 py-2.5 text-sm font-semibold text-gray-700 bg-white border-2 border-gray-300 rounded-xl hover:bg-gray-50 hover:border-gray-400 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105"
                    >
                        {t('editor.aiContinue.cancel')}
                    </button>
                    <button
                        onClick={handleSubmit}
                        disabled={isSubmitting}
                        // 移除了 text-white，确保子级 span 的 text-gray-100 生效
                        className="px-8 py-3 bg-indigo-600 text-sm font-bold rounded-xl shadow-lg hover:shadow-xl hover:bg-indigo-700 transition-all duration-200 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 disabled:hover:scale-100"
                    >
                        {isSubmitting ? (
                            <>
                              <Loader2 className="w-5 h-5 animate-spin text-blue-200" />
                              <span className="text-gray-100">{t('editor.aiContinue.generating')}</span>
                            </>
                          ) : (
                            <>
                              <Sparkles className="w-5 h-5 text-blue-200" />
                              <span className="text-gray-100">{t('editor.aiContinue.generate')}</span>
                            </>
                          )}
                    </button>
                </div>
            </div>
        </>
    );
};

export default AIContinueDrawer;


// =================================================================
// 辅助组件：简化代码
// =================================================================

// 辅助组件：用于渲染带标签的输入框
interface InputGroupProps {
    label: string;
    placeholder: string;
    value: string;
    onChange: React.ChangeEventHandler<HTMLInputElement | HTMLTextAreaElement>;
}
const InputGroup: React.FC<InputGroupProps> = ({ label, placeholder, value, onChange }) => (
    <div>
        <label className="block text-xs font-semibold text-gray-700 mb-2">{label}</label>
        <input
            type="text"
            value={value}
            onChange={onChange}
            className="w-full px-3 py-2.5 text-sm bg-white border-2 border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 hover:border-gray-300 transition-all duration-200 shadow-sm"
            placeholder={placeholder}
        />
    </div>
);

// 辅助组件：用于渲染折叠面板 - 增强视觉效果
const renderAccordionPanel = (
    panelKey: PanelKey,
    title: string,
    isExpanded: boolean,
    toggleFn: (key: PanelKey) => void,
    children: React.ReactNode
) => (
    <div className="border-2 border-gray-200 rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow duration-200">
        <button
            onClick={() => toggleFn(panelKey)}
            className="w-full flex items-center justify-between px-5 py-4 bg-gradient-to-r from-white to-gray-50/50 hover:from-blue-50/30 hover:to-purple-50/20 transition-all duration-200 group"
        >
            <span className="text-sm font-bold text-gray-800 group-hover:text-blue-700 transition-colors duration-200">{title}</span>
            <ChevronDown
                className={`w-5 h-5 text-gray-500 group-hover:text-blue-600 transition-all duration-300 ${
                    isExpanded ? 'rotate-180' : ''
                }`}
            />
        </button>
        <div
            className={`transition-all duration-300 ease-in-out ${
                isExpanded ? 'max-h-[500px] opacity-100' : 'max-h-0 opacity-0'
            } overflow-hidden`}
        >
            {children}
        </div>
    </div>
);
