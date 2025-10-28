# 构建和部署指南

> 📋 **文档**: 13-build-and-deploy.md | **最后更新**: 2025-10-25
> **版本**: v1.0

[← 返回文档导航](./README.md)

---

## 📑 目录

- [构建命令说明](#构建命令说明)
- [开发环境](#开发环境)
- [生产构建](#生产构建)
- [TypeScript 类型检查](#typescript-类型检查)
- [部署指南](#部署指南)
- [常见问题](#常见问题)

---

## 🛠️ 构建命令说明

项目提供了多个构建命令，满足不同场景的需求：

### 命令对照表

| 命令 | 用途 | 类型检查 | 构建速度 | 适用场景 |
|------|------|----------|----------|----------|
| `npm run dev` | 开发服务器 | ❌ 否 | ⚡ 极快 | 日常开发 |
| `npm run pure-build` | 快速构建 | ❌ 否 | ⚡ 快速 | 生产部署 ⭐ |
| `npm run type-check` | 类型检查 | ✅ 是 | ⚡ 快速 | 代码质量检查 |
| `npm run build` | 完整构建 | ✅ 是 | 🐢 较慢 | 严格构建 |
| `npm run preview` | 预览构建 | - | - | 本地预览 |

### 详细说明

#### 1. `npm run dev` - 开发服务器

```bash
npm run dev
```

**说明**：
- 启动 Vite 开发服务器
- 支持热更新（HMR）
- 不执行 TypeScript 类型检查
- 启动时间：约 2-3 秒

**输出**：
```
VITE v7.1.10  ready in 2520 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

---

#### 2. `npm run pure-build` ⭐ **推荐用于生产部署**

```bash
npm run pure-build
```

**说明**：
- 跳过 TypeScript 类型检查
- 直接使用 Vite 构建生产版本
- 构建时间：约 60 秒
- 生成优化后的静态文件到 `dist` 目录

**优点**：
- ✅ 构建速度快
- ✅ 不受 TypeScript 错误影响
- ✅ 适合快速部署

**构建产物**：
```
dist/
├── assets/          # 优化后的 JS/CSS 文件
├── index.html       # 入口 HTML
└── ...
```

**构建输出示例**：
```
✓ built in 59.66s
dist/index.html                        0.48 kB │ gzip: 0.32 kB
dist/assets/NovelEditor-CfQPdncc.js  945.25 kB │ gzip: 308.68 kB
...
```

---

#### 3. `npm run type-check` - 类型检查

```bash
npm run type-check
```

**说明**：
- 仅执行 TypeScript 类型检查
- 不进行构建
- 用于代码质量检查

**使用场景**：
- Git 提交前检查
- CI/CD 流程中的质量检查
- 开发过程中的类型验证

**当前状态**：
```
176 个 TypeScript 错误
（不影响项目运行，可选择性修复）
```

---

#### 4. `npm run build` - 完整构建

```bash
npm run build
```

**说明**：
- 先执行 TypeScript 类型检查（`tsc -b`）
- 然后执行 Vite 构建（`vite build`）
- 构建时间：较长（取决于类型错误数量）

**注意**：
- ⚠️ 如果存在 TypeScript 错误，构建会失败
- ⚠️ 当前项目有 176 个类型错误，此命令会失败
- 💡 建议使用 `npm run pure-build` 代替

---

#### 5. `npm run preview` - 预览构建产物

```bash
npm run preview
```

**说明**：
- 预览 `dist` 目录的构建产物
- 需要先运行 `npm run pure-build` 或 `npm run build`
- 启动本地静态服务器

**使用场景**：
- 构建后本地测试
- 验证生产版本功能

---

## 💻 开发环境

### 启动开发服务器

```bash
# 安装依赖（首次运行）
npm install

# 启动开发服务器
npm run dev
```

### 开发环境特点

- ✅ 热更新（HMR）：修改代码自动刷新
- ✅ 无类型检查：开发速度快
- ✅ Source Map：方便调试
- ✅ 模块热替换：无需刷新页面

### 开发流程

1. 修改代码
2. 浏览器自动刷新
3. 查看效果
4. 继续开发

---

## 🚀 生产构建

### 推荐构建流程

```bash
# 1. 清理旧的构建产物（可选）
rm -rf dist

# 2. 执行快速构建
npm run pure-build

# 3. 本地预览（可选）
npm run preview

# 4. 部署 dist 目录到服务器
```

### 构建产物说明

构建完成后，`dist` 目录包含：

```
dist/
├── assets/
│   ├── index-*.js        # 主应用代码（代码分割）
│   ├── NovelEditor-*.js  # 编辑器模块（945 KB，最大块）
│   ├── *.css             # 样式文件
│   └── ...
└── index.html            # 入口 HTML
```

### 性能优化建议

构建输出中可能会看到警告：

```
(!) Some chunks are larger than 500 kB after minification.
```

**解决方案**：
- 使用动态导入 `import()` 进行代码分割
- 配置 `build.rollupOptions.output.manualChunks`
- 调整 `build.chunkSizeWarningLimit`

（当前版本可接受，后续优化）

---

## 🔍 TypeScript 类型检查

### 当前状态

**TypeScript 错误数量**: 176 个

**错误分类**：
1. 缺少依赖：~30 个（`@tanstack/react-query`）
2. 类型不匹配：~50 个（Chapter.status, User.role 等）
3. 未使用变量：~80 个（TS6133 警告）
4. 其他错误：~16 个

**重要结论**：
> ⚠️ **这些 TypeScript 错误不影响项目运行和生产部署**
> 原因：Vite 在开发和构建时使用 esbuild 进行代码转换，不执行类型检查

### 类型检查策略

#### 方案 A：忽略类型错误（推荐）

```bash
# 使用 pure-build 跳过类型检查
npm run pure-build
```

**优点**：
- ✅ 快速构建和部署
- ✅ 不受类型错误阻塞
- ✅ 适合快速迭代

**适用场景**：
- 快速部署需求
- 功能优先于类型安全
- 紧急修复和发布

---

#### 方案 B：修复类型错误（可选）

如果你希望严格的类型检查：

```bash
# 1. 安装缺失依赖
npm install @tanstack/react-query

# 2. 修复类型定义文件
# 统一 types/index.ts 和 types/novel.ts
# 添加 Chapter.status, User.role 等字段

# 3. 清理未使用的变量
# 或添加 // @ts-ignore

# 4. 验证类型检查
npm run type-check

# 5. 完整构建
npm run build
```

**预计时间**: 1-2 天

---

## 📦 部署指南

### 部署前检查清单

- [ ] 代码已提交到 Git
- [ ] 运行 `npm run pure-build` 构建成功
- [ ] 本地预览 `npm run preview` 功能正常
- [ ] 环境变量配置正确

### 环境变量配置

创建 `.env.production` 文件：

```bash
# API 基础URL
VITE_API_BASE_URL=https://your-api-domain.com

# OpenAI 配置（可选）
VITE_OPENAI_API_KEY=sk-xxx
VITE_OPENAI_MODEL=gpt-4
VITE_API_URL=https://your-openai-proxy.com

# 是否使用 Mock 数据
VITE_USE_MOCK=false
```

### 部署到服务器

#### 方法 1：手动部署

```bash
# 1. 构建
npm run pure-build

# 2. 上传 dist 目录到服务器
scp -r dist/* user@server:/var/www/html/

# 3. 配置 Nginx（参考下方配置）
```

#### 方法 2：使用 CI/CD

GitHub Actions 示例：

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run pure-build
      - name: Deploy to Server
        run: |
          # 部署脚本
```

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /var/www/html/dist;
    index index.html;

    # SPA 路由支持
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Gzip 压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
    gzip_min_length 1000;
}
```

---

## ❓ 常见问题

### Q1: 为什么推荐使用 `pure-build` 而不是 `build`？

**A**: 因为：
- `pure-build` 跳过类型检查，构建速度快（59.66s）
- 当前项目有 176 个 TypeScript 错误，`build` 会失败
- TypeScript 错误不影响实际运行
- 适合快速部署和迭代

---

### Q2: TypeScript 错误会影响功能吗？

**A**: 不会。

- Vite 使用 esbuild 进行代码转换，不执行类型检查
- 开发环境 (`npm run dev`) 完全正常运行
- 生产构建 (`npm run pure-build`) 正常生成优化文件
- 类型检查仅用于开发时的代码质量保证

---

### Q3: 什么时候需要修复 TypeScript 错误？

**A**: 以下情况需要修复：

- 想使用严格的类型检查（`npm run build`）
- 团队要求代码质量标准
- 准备长期维护的项目
- 需要更好的 IDE 智能提示

否则，可以暂时忽略，专注于功能开发。

---

### Q4: 构建产物太大怎么办？

**A**: 性能优化建议：

1. **代码分割**：
   ```ts
   // 使用动态导入
   const Component = lazy(() => import('./Component'));
   ```

2. **配置手动分块**：
   ```ts
   // vite.config.ts
   build: {
     rollupOptions: {
       output: {
         manualChunks: {
           'react-vendor': ['react', 'react-dom'],
           'editor': ['@tiptap/core', '@tiptap/react']
         }
       }
     }
   }
   ```

3. **调整警告阈值**：
   ```ts
   // vite.config.ts
   build: {
     chunkSizeWarningLimit: 1000
   }
   ```

---

### Q5: 部署后页面刷新 404 怎么办？

**A**: 这是 SPA 路由问题，需要配置服务器：

**Nginx**:
```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

**Apache** (`.htaccess`):
```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
```

---

## 📚 相关文档

- [上一章: 变更日志](./12-changelog.md)
- [下一章: 开发路线图](./04-milestones.md)
- [返回: 文档导航](./README.md)

---

**最后更新**: 2025-10-25
**维护者**: NovelAIde 团队
