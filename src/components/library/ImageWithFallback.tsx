import React, { useState } from 'react';

// 默认封面图片 - 使用本地图片确保国内可访问
const DEFAULT_COVER_IMAGE = '/default-cover.jpg';

export function ImageWithFallback(props: React.ImgHTMLAttributes<HTMLImageElement>) {
  const [didError, setDidError] = useState(false);

  const handleError = () => {
    setDidError(true);
  };

  const { src, alt, style = {}, className, ...rest } = props;

  // 确保 objectFit 样式被应用
  const imgStyle = { ...style };

  // 如果图片加载失败，显示默认封面
  if (didError) {
    return (
      <img
        src={DEFAULT_COVER_IMAGE}
        alt={alt || '默认封面'}
        className={className}
        style={imgStyle}
        {...rest}
        data-original-url={src}
      />
    );
  }

  return (
    <img src={src} alt={alt} className={className} style={imgStyle} {...rest} onError={handleError} />
  );
}
