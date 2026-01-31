import React from 'react';
import { AlertCircle } from 'lucide-react';
import i18n from '@/i18n';

interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

/**
 * 捕获后代组件运行时错误的容器，避免整页崩溃。
 */
class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = {
    hasError: false,
    error: undefined,
  };

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void {
    // 记录错误详情，便于调试
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  private handleRetry = (): void => {
    this.setState({ hasError: false, error: undefined });
  };

  render(): React.ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="min-h-[200px] bg-white border border-red-100 rounded-lg p-6 flex flex-col space-y-3">
          <div className="flex items-center text-red-600 font-semibold">
            <AlertCircle className="w-5 h-5 mr-2" />
            <span>{i18n.t('errors.pageError')}</span>
          </div>
          <p className="text-sm text-gray-600">
            {this.state.error?.message || i18n.t('errors.unknownError')}
          </p>
          <div className="flex items-center space-x-3">
            <button
              type="button"
              onClick={this.handleRetry}
              className="px-3 py-2 text-sm rounded-md bg-blue-600 text-white hover:bg-blue-700 transition-colors"
            >
              {i18n.t('common.retry')}
            </button>
            <button
              type="button"
              onClick={() => window.location.reload()}
              className="px-3 py-2 text-sm rounded-md border border-gray-300 text-gray-700 hover:bg-gray-50 transition-colors"
            >
              {i18n.t('common.refreshPage')}
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
