# ============================================
# 文枢AI 前端 Dockerfile
# ============================================

# 阶段1：构建前端
FROM node:22-alpine AS builder

WORKDIR /app

# 复制依赖文件
COPY package*.json ./

# 安装依赖（使用国内镜像加速）
RUN npm ci --registry=https://registry.npmmirror.com

# 复制源代码
COPY . .

# 设置环境变量（构建时使用，API地址为空表示使用相对路径）
ARG VITE_API_URL=""
ENV VITE_API_URL=$VITE_API_URL

# 构建
RUN npm run build

# 阶段2：Nginx服务
FROM nginx:alpine

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制Nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
