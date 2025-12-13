import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { Button } from '../../components/ui/button';
import ReactMarkdown from 'react-markdown';

/**
 * TermsView 组件 - 服务条款展示页面
 */
const TermsView: React.FC = () => {
  const navigate = useNavigate();
  const [content, setContent] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch('/terms-of-service.md')
      .then(res => res.text())
      .then(text => {
        setContent(text);
        setLoading(false);
      })
      .catch(() => {
        setContent('# 加载失败\n\n服务条款内容加载失败，请稍后重试。');
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
          <article className="text-gray-800 leading-relaxed space-y-4">
            <ReactMarkdown
              components={{
                h1: ({children}) => <h1 className="text-3xl font-bold text-gray-900 mb-6">{children}</h1>,
                h2: ({children}) => <h2 className="text-2xl font-bold text-gray-900 mt-8 mb-4">{children}</h2>,
                h3: ({children}) => <h3 className="text-xl font-semibold text-gray-900 mt-6 mb-3">{children}</h3>,
                p: ({children}) => <p className="text-gray-700 leading-relaxed mb-4">{children}</p>,
                ul: ({children}) => <ul className="text-gray-700 list-disc list-inside my-4 space-y-2">{children}</ul>,
                li: ({children}) => <li className="text-gray-700">{children}</li>,
                strong: ({children}) => <strong className="text-gray-900 font-semibold">{children}</strong>,
                a: ({children, href}) => <a href={href} className="text-blue-600 underline hover:text-blue-800">{children}</a>,
                hr: () => <hr className="border-gray-200 my-8" />,
                blockquote: ({children}) => <blockquote className="border-l-4 border-gray-300 pl-4 italic text-gray-600">{children}</blockquote>,
              }}
            >
              {content}
            </ReactMarkdown>
          </article>
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

export default TermsView;
