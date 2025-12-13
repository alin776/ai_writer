import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { Button } from '../../components/ui/button';
import ReactMarkdown from 'react-markdown';

/**
 * PrivacyView 组件 - 隐私政策展示页面
 */
const PrivacyView: React.FC = () => {
  const navigate = useNavigate();
  const [content, setContent] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch('/privacy-policy.md')
      .then(res => res.text())
      .then(text => {
        setContent(text);
        setLoading(false);
      })
      .catch(() => {
        setContent('# 加载失败\n\n隐私政策内容加载失败，请稍后重试。');
        setLoading(false);
      });
  }, []);

  const handleBack = () => {
    navigate(-1);
  };

  const handleAccept = () => {
    navigate(-1);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-600">加载中...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* 返回按钮 */}
        <Button
          variant="outline"
          onClick={handleBack}
          className="mb-6 border-gray-200 hover:border-gray-900"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          返回
        </Button>

        {/* 文档内容 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 md:p-12">
          <div className="prose prose-lg max-w-none
            [&_h1]:text-3xl [&_h1]:font-bold [&_h1]:text-gray-900 [&_h1]:mb-6
            [&_h2]:text-2xl [&_h2]:font-bold [&_h2]:text-gray-900 [&_h2]:mt-8 [&_h2]:mb-4
            [&_h3]:text-xl [&_h3]:font-semibold [&_h3]:text-gray-900 [&_h3]:mt-6 [&_h3]:mb-3
            [&_p]:text-gray-700 [&_p]:leading-relaxed [&_p]:mb-4
            [&_ul]:text-gray-700 [&_ul]:my-4
            [&_li]:text-gray-700 [&_li]:mb-2
            [&_strong]:text-gray-900 [&_strong]:font-semibold
            [&_a]:text-blue-600 [&_a]:underline [&_a]:hover:text-blue-800
            [&_hr]:border-gray-200 [&_hr]:my-8
            [&_blockquote]:border-l-4 [&_blockquote]:border-gray-300 [&_blockquote]:pl-4 [&_blockquote]:italic [&_blockquote]:text-gray-600
            [&_table]:border-collapse [&_table]:w-full [&_table]:my-4
            [&_th]:bg-gray-50 [&_th]:text-gray-900 [&_th]:font-semibold [&_th]:p-3 [&_th]:border [&_th]:border-gray-200
            [&_td]:text-gray-700 [&_td]:p-3 [&_td]:border [&_td]:border-gray-200
          ">
            <ReactMarkdown>{content}</ReactMarkdown>
          </div>
        </div>

        {/* 底部操作 */}
        <div className="mt-8 text-center">
          <Button
            onClick={handleAccept}
            className="bg-gray-900 hover:bg-gray-800 text-white px-8 py-3"
          >
            我已了解
          </Button>
        </div>
      </div>
    </div>
  );
};

export default PrivacyView;
