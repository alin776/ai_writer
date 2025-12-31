import { useState, useRef } from 'react';
import { X, Camera, Loader2 } from 'lucide-react';
import { createFangroup, uploadChannelCover } from '@/services/channelApi';
import { useToast } from '@/hooks/useToast';
import ImageCropper from '@/components/common/ImageCropper';

interface CreateFangroupDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export function CreateFangroupDialog({ isOpen, onClose, onSuccess }: CreateFangroupDialogProps) {
  const { showToast } = useToast();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
  });
  // 裁剪后的预览图（data URL）
  const [coverPreview, setCoverPreview] = useState<string | null>(null);
  // 裁剪后的 Blob（用于上传）
  const [coverBlob, setCoverBlob] = useState<Blob | null>(null);
  // 原始图片（用于裁剪器）
  const [originalImage, setOriginalImage] = useState<string>('');
  // 显示裁剪器
  const [showCropper, setShowCropper] = useState(false);

  const [isUploading, setIsUploading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!isOpen) return null;

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // 验证文件类型
    if (!file.type.startsWith('image/')) {
      showToast('error', '请选择图片文件');
      return;
    }

    // 验证文件大小 (10MB，裁剪后会变小)
    if (file.size > 10 * 1024 * 1024) {
      showToast('error', '图片大小不能超过 10MB');
      return;
    }

    // 读取文件并打开裁剪器
    const reader = new FileReader();
    reader.onload = () => {
      setOriginalImage(reader.result as string);
      setShowCropper(true);
    };
    reader.readAsDataURL(file);

    // 清空 input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // 裁剪完成
  const handleCropComplete = (croppedBlob: Blob) => {
    setCoverBlob(croppedBlob);
    // 生成预览 URL
    const previewUrl = URL.createObjectURL(croppedBlob);
    setCoverPreview(previewUrl);
    setShowCropper(false);
    setOriginalImage('');
  };

  // 关闭裁剪器
  const handleCropperClose = () => {
    setShowCropper(false);
    setOriginalImage('');
  };

  const handleRemoveCover = () => {
    if (coverPreview) {
      URL.revokeObjectURL(coverPreview);
    }
    setCoverPreview(null);
    setCoverBlob(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.name.trim()) {
      showToast('error', '请输入频道名称');
      return;
    }

    try {
      setIsSubmitting(true);

      // 如果有封面图片，先上传
      let coverUrl: string | undefined;
      if (coverBlob) {
        setIsUploading(true);
        try {
          // 将 Blob 转换为 File
          const file = new File([coverBlob], 'cover.png', { type: 'image/png' });
          const result = await uploadChannelCover(file);
          // ApiAdapter 会将 cover_url 转换为 coverUrl
          coverUrl = (result as any).coverUrl || (result as any).cover_url;
          console.log('[CreateFangroupDialog] 上传封面结果:', result, '封面URL:', coverUrl);
        } catch (error) {
          console.error('上传封面失败:', error);
          showToast('error', '上传封面失败');
          return;
        } finally {
          setIsUploading(false);
        }
      }

      // 创建粉丝群
      console.log('[CreateFangroupDialog] 创建粉丝群, coverUrl:', coverUrl);
      await createFangroup({
        name: formData.name.trim(),
        description: formData.description.trim() || undefined,
        cover_image: coverUrl,
      });

      showToast('success', '粉丝群创建成功！');
      resetForm();
      onSuccess();
      onClose();
    } catch (error) {
      console.error('创建粉丝群失败:', error);
      showToast('error', '创建粉丝群失败');
    } finally {
      setIsSubmitting(false);
    }
  };

  const resetForm = () => {
    setFormData({ name: '', description: '' });
    if (coverPreview) {
      URL.revokeObjectURL(coverPreview);
    }
    setCoverPreview(null);
    setCoverBlob(null);
  };

  const handleClose = () => {
    if (!isSubmitting) {
      resetForm();
      onClose();
    }
  };

  return (
    <>
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={handleClose}>
        <div
          className="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-md mx-4"
          onClick={(e) => e.stopPropagation()}
        >
          {/* 头部 */}
          <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              创建粉丝群
            </h2>
            <button
              onClick={handleClose}
              disabled={isSubmitting}
              className="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors disabled:opacity-50"
            >
              <X className="w-5 h-5 text-gray-500 dark:text-gray-400" />
            </button>
          </div>

          {/* 表单 */}
          <form onSubmit={handleSubmit} className="p-4 space-y-4">
            {/* 群头像 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                群头像
              </label>
              <div className="flex items-center gap-4">
                {/* 头像预览/上传区域 */}
                <div
                  onClick={() => !isSubmitting && fileInputRef.current?.click()}
                  className={`
                    relative w-20 h-20 rounded-full overflow-hidden cursor-pointer
                    border-2 border-dashed border-gray-300 dark:border-gray-600
                    hover:border-blue-500 dark:hover:border-blue-400
                    transition-colors flex items-center justify-center
                    ${isSubmitting ? 'opacity-50 cursor-not-allowed' : ''}
                  `}
                >
                  {coverPreview ? (
                    <>
                      <img
                        src={coverPreview}
                        alt="封面预览"
                        className="w-full h-full object-cover"
                      />
                      {/* 遮罩层 */}
                      <div className="absolute inset-0 bg-black/40 opacity-0 hover:opacity-100 transition-opacity flex items-center justify-center">
                        <Camera className="w-6 h-6 text-white" />
                      </div>
                    </>
                  ) : (
                    <div className="flex flex-col items-center text-gray-400 dark:text-gray-500">
                      <Camera className="w-6 h-6 mb-1" />
                      <span className="text-xs">上传</span>
                    </div>
                  )}
                  {isUploading && (
                    <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
                      <Loader2 className="w-6 h-6 text-white animate-spin" />
                    </div>
                  )}
                </div>

                {/* 说明文字和删除按钮 */}
                <div className="flex-1">
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    支持 JPG、PNG、WebP、GIF 格式
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    可裁剪调整，最大 10MB
                  </p>
                  {coverPreview && (
                    <button
                      type="button"
                      onClick={handleRemoveCover}
                      disabled={isSubmitting}
                      className="mt-2 text-xs text-red-500 hover:text-red-600 disabled:opacity-50"
                    >
                      移除头像
                    </button>
                  )}
                </div>
              </div>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                className="hidden"
              />
            </div>

            {/* 频道名称 */}
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                频道名称 <span className="text-red-500">*</span>
              </label>
              <input
                id="name"
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="例如：小明的创作空间"
                maxLength={50}
                disabled={isSubmitting}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 disabled:opacity-50"
              />
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                {formData.name.length}/50
              </p>
            </div>

            {/* 频道简介 */}
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                频道简介
              </label>
              <textarea
                id="description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                placeholder="介绍一下你的粉丝群..."
                maxLength={200}
                rows={3}
                disabled={isSubmitting}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 resize-none disabled:opacity-50"
              />
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                {formData.description.length}/200
              </p>
            </div>

            {/* 提示信息 */}
            <div className="bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-800 rounded-lg p-3">
              <p className="text-sm text-blue-800 dark:text-blue-300">
                💡 粉丝群功能：
              </p>
              <ul className="text-xs text-blue-700 dark:text-blue-400 mt-2 space-y-1 list-disc list-inside">
                <li>发送公告通知所有成员</li>
                <li>@全体成员功能</li>
                <li>永久频道，不会被折叠</li>
                <li>深度经营你的核心粉丝</li>
              </ul>
            </div>

            {/* 按钮组 */}
            <div className="flex gap-3 pt-2">
              <button
                type="button"
                onClick={handleClose}
                disabled={isSubmitting}
                className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50"
              >
                取消
              </button>
              <button
                type="submit"
                disabled={isSubmitting || !formData.name.trim()}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {isSubmitting && <Loader2 className="w-4 h-4 animate-spin" />}
                {isSubmitting ? (isUploading ? '上传中...' : '创建中...') : '创建'}
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* 图片裁剪器 */}
      <ImageCropper
        isOpen={showCropper}
        imageSrc={originalImage}
        onClose={handleCropperClose}
        onSave={handleCropComplete}
        aspect={1}
        cropShape="round"
      />
    </>
  );
}
