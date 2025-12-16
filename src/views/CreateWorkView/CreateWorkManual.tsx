import React, { useState, useEffect } from 'react';
import { ArrowLeft, Save } from 'lucide-react';
import { motion } from 'motion/react';
import type { CreateWorkData } from '../../types';
import type { WorldViewData } from './index';

interface CreateWorkManualProps {
  onSubmit: (data: CreateWorkData, worldView: WorldViewData) => void;
  onBack: () => void;
}

/**
 * CreateWorkManual 组件 - 手动创建作品表单
 * 
 * 包含：
 * - 作品基本信息（标题、简介）
 * - 世界观设定（类型、背景、力量体系等）
 */
const CreateWorkManual: React.FC<CreateWorkManualProps> = ({ onSubmit, onBack }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    genre: '',
    // 世界观简介
    worldIntro: '',
    // 主要地点（逗号分隔）
    mainLocations: '',
    // 力量体系
    powerSystemName: '',
    powerSystemDesc: '',
    // 主角设定
    protagonistName: '',
    protagonistDesc: '',
    // 剧情与规则
    plotIdea: '',
    worldRules: '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  /**
   * 组件加载时滚动到顶部
   */
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  /**
   * 处理输入变化
   */
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // 清除错误
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  /**
   * 验证表单
   */
  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = '请输入作品标题';
    } else if (formData.title.length < 2) {
      newErrors.title = '标题至少需要2个字符';
    }

    if (!formData.description.trim()) {
      newErrors.description = '请输入作品简介';
    } else if (formData.description.length < 10) {
      newErrors.description = '简介至少需要10个字符';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  /**
   * 处理提交
   */
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    // 分离基本信息和世界观数据
    const workData: CreateWorkData = {
      title: formData.title.trim(),
      description: formData.description.trim(),
    };

    // 将手动输入的世界观信息对齐为 AI Guidelines 字段，便于后端自动分发到人物/地点/设定
    const worldViewData: WorldViewData = {
      // 小说类型
      primaryGenre: formData.genre,
      // 世界观简介
      worldIntro: formData.worldIntro,
      // 世界规则
      worldRules: formData.worldRules,
      // 主要地点（逗号分隔）
      mainLocations: formData.mainLocations,
      // 力量体系
      powerSystemName: formData.powerSystemName,
      powerLevels: formData.powerSystemDesc,  // 用描述填充等级划分字段
      // 主角信息
      protagonistName: formData.protagonistName,
      protagonistIdentity: formData.protagonistDesc,
      protagonistTraits: formData.protagonistDesc,
      // 剧情构思
      conflictDesign: formData.plotIdea,
    };

    onSubmit(workData, worldViewData);
  };

  return (
    <div className="min-h-screen bg-[#faf8f5] dark:bg-slate-900 overflow-y-auto">
      {/* 背景墨迹渐变 */}
      <div className="absolute inset-0 opacity-[0.02] dark:opacity-[0.05] pointer-events-none">
        <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-radial from-gray-900 dark:from-gray-100 to-transparent blur-3xl"></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-gradient-radial from-gray-900 dark:from-gray-100 to-transparent blur-3xl"></div>
      </div>

      <div className="relative z-10 max-w-4xl mx-auto px-8 py-12">
        {/* 返回按钮 */}
        <button
          onClick={onBack}
          className="mb-8 w-10 h-10 rounded-full border-2 border-gray-300 dark:border-gray-600 bg-[#faf8f5] dark:bg-slate-800 flex items-center justify-center hover:border-gray-600 dark:hover:border-gray-400 transition-colors group"
        >
          <ArrowLeft className="w-4 h-4 text-gray-400 group-hover:text-gray-800 dark:group-hover:text-gray-200 transition-colors" />
        </button>

        {/* 标题区域 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl text-gray-800 dark:text-gray-100 mb-3 tracking-wide">创建你的作品</h1>
          <div className="w-24 h-px bg-gradient-to-r from-transparent via-gray-300 dark:via-gray-600 to-transparent mx-auto mb-4"></div>
          <p className="text-gray-500 dark:text-gray-400">详细描述你的创作世界，让故事更加立体生动</p>
        </motion.div>

        {/* 表单区域 */}
        <motion.form
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          onSubmit={handleSubmit}
          className="space-y-10"
        >
          {/* 基本信息 */}
          <div className="space-y-6">
            <div className="border-l-2 border-gray-800 dark:border-gray-200 pl-4">
              <h2 className="text-xl text-gray-800 dark:text-gray-100 mb-1">基本信息</h2>
            </div>

            <div className="space-y-6 pl-6">
              {/* 作品标题 */}
              <div className="space-y-2">
                <label htmlFor="title" className="block text-gray-700 dark:text-gray-300">
                  作品标题 <span className="text-gray-400 dark:text-gray-500">*</span>
                </label>
                <input
                  id="title"
                  name="title"
                  type="text"
                  value={formData.title}
                  onChange={handleChange}
                  placeholder="请输入作品标题"
                  className={`w-full px-4 py-2 border ${errors.title ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'} bg-white/50 dark:bg-slate-800/50 text-gray-900 dark:text-gray-100 focus:border-gray-600 dark:focus:border-gray-400 focus:ring-1 focus:ring-gray-600/20 dark:focus:ring-gray-400/20 outline-none rounded transition-colors placeholder:text-gray-400 dark:placeholder:text-gray-500`}
                />
                {errors.title && <span className="text-sm text-red-500">{errors.title}</span>}
              </div>

              {/* 作品简介 */}
              <div className="space-y-2">
                <label htmlFor="description" className="block text-gray-700 dark:text-gray-300">
                  作品简介 <span className="text-gray-400 dark:text-gray-500">*</span>
                </label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  placeholder="简要描述您的作品内容、主题或特色"
                  rows={4}
                  className={`w-full px-4 py-2 border ${errors.description ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'} bg-white/50 dark:bg-slate-800/50 text-gray-900 dark:text-gray-100 focus:border-gray-600 dark:focus:border-gray-400 focus:ring-1 focus:ring-gray-600/20 dark:focus:ring-gray-400/20 outline-none rounded resize-none transition-colors placeholder:text-gray-400 dark:placeholder:text-gray-500`}
                />
                {errors.description && <span className="text-sm text-red-500">{errors.description}</span>}
              </div>
            </div>
          </div>

          {/* 分隔线 */}
          <div className="w-full h-px bg-gradient-to-r from-transparent via-gray-300 dark:via-gray-600 to-transparent"></div>

          {/* 世界观设定 */}
          <div className="space-y-6">
            <div className="border-l-2 border-gray-800 dark:border-gray-200 pl-4">
              <h2 className="text-xl text-gray-800 dark:text-gray-100 mb-1">
                世界观设定<span className="text-gray-400 dark:text-gray-500">（选填）</span>
              </h2>
              <p className="text-sm text-gray-400 dark:text-gray-500 mt-2">详细的世界观设定能让你的故事更加立体和真实，这些信息可以随时补充和修改</p>
            </div>

            <div className="space-y-6 pl-6">
              {/* 小说类型 */}
              <div className="space-y-2">
                <label htmlFor="genre" className="block text-gray-700 dark:text-gray-300">小说类型</label>
                <select
                  id="genre"
                  name="genre"
                  value={formData.genre}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white/50 dark:bg-slate-800/50 text-gray-900 dark:text-gray-100 focus:border-gray-600 dark:focus:border-gray-400 focus:ring-1 focus:ring-gray-600/20 dark:focus:ring-gray-400/20 outline-none rounded transition-colors"
                >
                  <option value="">请选择类型</option>
                  <option value="xuanhuan">玄幻</option>
                  <option value="xianxia">仙侠</option>
                  <option value="wuxia">武侠</option>
                  <option value="dushi">都市</option>
                  <option value="lishi">历史</option>
                  <option value="junshi">军事</option>
                  <option value="kehuan">科幻</option>
                  <option value="youxi">游戏</option>
                  <option value="qihuan">奇幻</option>
                  <option value="other">其他</option>
                </select>
              </div>

              {/* 世界观简介 - 跨两列 */}
              <div className="space-y-2">
                <label htmlFor="worldIntro" className="block text-gray-700 dark:text-gray-300">世界观简介</label>
                <textarea
                  id="worldIntro"
                  name="worldIntro"
                  value={formData.worldIntro}
                  onChange={handleChange}
                  placeholder="描述故事发生的时代、社会背景、世界观设定..."
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white/50 dark:bg-slate-800/50 text-gray-900 dark:text-gray-100 focus:border-gray-600 dark:focus:border-gray-400 focus:ring-1 focus:ring-gray-600/20 dark:focus:ring-gray-400/20 outline-none rounded resize-none transition-colors placeholder:text-gray-400 dark:placeholder:text-gray-500"
                />
              </div>

              {/* 两列布局的字段 */}
              <div className="grid grid-cols-2 gap-6">
                {/* 主要地点 */}
                <div className="space-y-2">
                  <label htmlFor="mainLocations" className="block text-gray-700 dark:text-gray-300">主要地点</label>
                  <textarea
                    id="mainLocations"
                    name="mainLocations"
                    value={formData.mainLocations}
                    onChange={handleChange}
                    placeholder="用逗号分隔，如：天元城、魔法学院、暗影森林..."
                    rows={3}
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white/50 dark:bg-slate-800/50 text-gray-900 dark:text-gray-100 focus:border-gray-600 dark:focus:border-gray-400 focus:ring-1 focus:ring-gray-600/20 dark:focus:ring-gray-400/20 outline-none rounded resize-none transition-colors placeholder:text-gray-400 dark:placeholder:text-gray-500"
                  />
                </div>

                {/* 世界规则 */}
                <div className="space-y-2">
                  <label htmlFor="worldRules" className="block text-gray-700 dark:text-gray-300">世界规则</label>
                  <textarea
                    id="worldRules"
                    name="worldRules"
                    value={formData.worldRules}
                    onChange={handleChange}
                    placeholder="特殊的世界规则、法则、限制、禁忌..."
                    rows={3}
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white/50 dark:bg-slate-800/50 text-gray-900 dark:text-gray-100 focus:border-gray-600 dark:focus:border-gray-400 focus:ring-1 focus:ring-gray-600/20 dark:focus:ring-gray-400/20 outline-none rounded resize-none transition-colors placeholder:text-gray-400 dark:placeholder:text-gray-500"
                  />
                </div>

                {/* 力量体系名称 */}
                <div className="space-y-2">
                  <label htmlFor="powerSystemName" className="block text-gray-700 dark:text-gray-300">力量体系名称</label>
                  <input
                    id="powerSystemName"
                    name="powerSystemName"
                    type="text"
                    value={formData.powerSystemName}
                    onChange={handleChange}
                    placeholder="如：修仙、魔法、斗气..."
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white/50 dark:bg-slate-800/50 text-gray-900 dark:text-gray-100 focus:border-gray-600 dark:focus:border-gray-400 focus:ring-1 focus:ring-gray-600/20 dark:focus:ring-gray-400/20 outline-none rounded transition-colors placeholder:text-gray-400 dark:placeholder:text-gray-500"
                  />
                </div>

                {/* 力量体系描述 */}
                <div className="space-y-2">
                  <label htmlFor="powerSystemDesc" className="block text-gray-700 dark:text-gray-300">力量体系描述</label>
                  <input
                    id="powerSystemDesc"
                    name="powerSystemDesc"
                    type="text"
                    value={formData.powerSystemDesc}
                    onChange={handleChange}
                    placeholder="等级划分、修炼方式、代价限制..."
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white/50 dark:bg-slate-800/50 text-gray-900 dark:text-gray-100 focus:border-gray-600 dark:focus:border-gray-400 focus:ring-1 focus:ring-gray-600/20 dark:focus:ring-gray-400/20 outline-none rounded transition-colors placeholder:text-gray-400 dark:placeholder:text-gray-500"
                  />
                </div>

                {/* 主角名字 */}
                <div className="space-y-2">
                  <label htmlFor="protagonistName" className="block text-gray-700 dark:text-gray-300">主角名字</label>
                  <input
                    id="protagonistName"
                    name="protagonistName"
                    type="text"
                    value={formData.protagonistName}
                    onChange={handleChange}
                    placeholder="主角的名字"
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white/50 dark:bg-slate-800/50 text-gray-900 dark:text-gray-100 focus:border-gray-600 dark:focus:border-gray-400 focus:ring-1 focus:ring-gray-600/20 dark:focus:ring-gray-400/20 outline-none rounded transition-colors placeholder:text-gray-400 dark:placeholder:text-gray-500"
                  />
                </div>

                {/* 主角描述 */}
                <div className="space-y-2">
                  <label htmlFor="protagonistDesc" className="block text-gray-700 dark:text-gray-300">主角描述</label>
                  <input
                    id="protagonistDesc"
                    name="protagonistDesc"
                    type="text"
                    value={formData.protagonistDesc}
                    onChange={handleChange}
                    placeholder="性格、背景、特殊能力..."
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white/50 dark:bg-slate-800/50 text-gray-900 dark:text-gray-100 focus:border-gray-600 dark:focus:border-gray-400 focus:ring-1 focus:ring-gray-600/20 dark:focus:ring-gray-400/20 outline-none rounded transition-colors placeholder:text-gray-400 dark:placeholder:text-gray-500"
                  />
                </div>

                {/* 剧情构思 - 跨两列 */}
                <div className="space-y-2 col-span-2">
                  <label htmlFor="plotIdea" className="block text-gray-700 dark:text-gray-300">剧情构思</label>
                  <textarea
                    id="plotIdea"
                    name="plotIdea"
                    value={formData.plotIdea}
                    onChange={handleChange}
                    placeholder="主线剧情、重要事件、故事走向、情节发展..."
                    rows={3}
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white/50 dark:bg-slate-800/50 text-gray-900 dark:text-gray-100 focus:border-gray-600 dark:focus:border-gray-400 focus:ring-1 focus:ring-gray-600/20 dark:focus:ring-gray-400/20 outline-none rounded resize-none transition-colors placeholder:text-gray-400 dark:placeholder:text-gray-500"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* 底部按钮 */}
          <div className="flex justify-center gap-6 pt-8 pb-12">
            <motion.button
              type="button"
              onClick={onBack}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="px-12 py-3 border border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:border-gray-600 dark:hover:border-gray-400 hover:text-gray-800 dark:hover:text-gray-100 transition-all duration-300"
            >
              取消
            </motion.button>
            <motion.button
              type="submit"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="px-12 py-3 bg-gray-800 dark:bg-gray-200 text-white dark:text-slate-900 hover:bg-gray-900 dark:hover:bg-gray-100 transition-all duration-300 flex items-center gap-2"
            >
              <Save size={18} />
              <span>创建作品</span>
            </motion.button>
          </div>
        </motion.form>
      </div>
    </div>
  );
};

export default CreateWorkManual;
