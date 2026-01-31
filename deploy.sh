#!/bin/bash

# ============================================
# 文枢AI 一键部署脚本
# ============================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的信息
info() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# 检查是否为root用户
check_root() {
    if [ "$EUID" -ne 0 ]; then
        error "请使用 root 用户运行此脚本: sudo ./deploy.sh"
    fi
}

# 检查并安装Docker
install_docker() {
    if ! command -v docker &> /dev/null; then
        info "正在安装 Docker..."
        curl -fsSL https://get.docker.com | sh
        systemctl start docker
        systemctl enable docker
        success "Docker 安装完成"
    else
        success "Docker 已安装: $(docker --version)"
    fi
}

# 检查并安装Docker Compose
install_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        info "正在安装 Docker Compose..."
        curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
        success "Docker Compose 安装完成"
    else
        success "Docker Compose 已安装: $(docker-compose --version)"
    fi
}

# 检查配置文件
check_config() {
    info "检查配置文件..."

    if [ ! -f "backend/.env.prod" ]; then
        warning "未找到 backend/.env.prod，正在从模板创建..."
        if [ -f "backend/.env.example" ]; then
            cp backend/.env.example backend/.env.prod
            warning "请编辑 backend/.env.prod 配置文件后重新运行脚本"
            warning "特别注意修改: SECRET_KEY, OPENAI_API_KEY, ADMIN_PASSWORD, CORS_ORIGINS"
            exit 1
        else
            error "未找到 backend/.env.example 模板文件"
        fi
    fi

    if [ ! -f "docker-compose.prod.yml" ]; then
        error "未找到 docker-compose.prod.yml 文件"
    fi

    if [ ! -f "nginx.conf" ]; then
        error "未找到 nginx.conf 文件"
    fi

    if [ ! -f "Dockerfile" ]; then
        error "未找到前端 Dockerfile 文件"
    fi

    success "配置文件检查完成"
}

# 构建并启动服务
deploy() {
    info "开始部署..."

    # 停止旧容器（如果存在）
    info "停止旧容器..."
    docker-compose -f docker-compose.prod.yml down 2>/dev/null || true

    # 构建镜像
    info "构建 Docker 镜像（可能需要几分钟）..."
    docker-compose -f docker-compose.prod.yml build --no-cache

    # 启动服务
    info "启动服务..."
    docker-compose -f docker-compose.prod.yml up -d

    # 等待数据库就绪
    info "等待数据库就绪..."
    sleep 10

    # 执行数据库迁移
    info "执行数据库迁移..."
    docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head

    success "部署完成！"
}

# 显示服务状态
show_status() {
    echo ""
    info "服务状态："
    docker-compose -f docker-compose.prod.yml ps
    echo ""
    success "=========================================="
    success "  文枢AI 部署成功！"
    success "=========================================="
    echo ""
    info "访问地址: http://$(curl -s ifconfig.me 2>/dev/null || echo '服务器IP')"
    info "API文档:  http://$(curl -s ifconfig.me 2>/dev/null || echo '服务器IP')/api/v1/docs"
    echo ""
    info "常用命令："
    echo "  查看日志:   docker-compose -f docker-compose.prod.yml logs -f"
    echo "  重启服务:   docker-compose -f docker-compose.prod.yml restart"
    echo "  停止服务:   docker-compose -f docker-compose.prod.yml down"
    echo "  查看状态:   docker-compose -f docker-compose.prod.yml ps"
    echo ""
}

# 主函数
main() {
    echo ""
    echo "============================================"
    echo "       文枢AI 云服务器部署脚本"
    echo "============================================"
    echo ""

    check_root
    install_docker
    install_docker_compose
    check_config
    deploy
    show_status
}

# 执行主函数
main "$@"
