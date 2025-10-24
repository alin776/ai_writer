"""
设备信息解析工具
从 User-Agent 字符串中提取浏览器、操作系统、设备类型等信息
"""
import re
from typing import Dict, Optional


def parse_user_agent(user_agent: Optional[str]) -> Dict[str, Optional[str]]:
    """
    解析 User-Agent 字符串

    Args:
        user_agent: User-Agent 字符串

    Returns:
        包含设备信息的字典
    """
    if not user_agent:
        return {
            'browser': None,
            'browser_version': None,
            'operating_system': None,
            'device_type': 'desktop',
            'device_name': None,
        }

    ua = user_agent.lower()

    # 解析浏览器
    browser, browser_version = _parse_browser(ua, user_agent)

    # 解析操作系统
    operating_system = _parse_os(ua)

    # 解析设备类型
    device_type = _parse_device_type(ua)

    # 生成设备名称
    device_name = _generate_device_name(browser, operating_system, device_type)

    return {
        'browser': browser,
        'browser_version': browser_version,
        'operating_system': operating_system,
        'device_type': device_type,
        'device_name': device_name,
    }


def _parse_browser(ua: str, original_ua: str) -> tuple[Optional[str], Optional[str]]:
    """解析浏览器名称和版本"""
    # Chrome/Chromium
    if 'edg/' in ua:
        match = re.search(r'edg/([\d.]+)', ua)
        return 'Edge', match.group(1) if match else None
    elif 'chrome/' in ua and 'edg/' not in ua:
        match = re.search(r'chrome/([\d.]+)', ua)
        return 'Chrome', match.group(1) if match else None

    # Firefox
    elif 'firefox/' in ua:
        match = re.search(r'firefox/([\d.]+)', ua)
        return 'Firefox', match.group(1) if match else None

    # Safari
    elif 'safari/' in ua and 'chrome' not in ua:
        match = re.search(r'version/([\d.]+)', ua)
        return 'Safari', match.group(1) if match else None

    # Opera
    elif 'opr/' in ua or 'opera/' in ua:
        match = re.search(r'(?:opr|opera)/([\d.]+)', ua)
        return 'Opera', match.group(1) if match else None

    # IE
    elif 'msie' in ua or 'trident/' in ua:
        match = re.search(r'(?:msie |rv:)([\d.]+)', ua)
        return 'Internet Explorer', match.group(1) if match else None

    return 'Unknown', None


def _parse_os(ua: str) -> Optional[str]:
    """解析操作系统"""
    # Windows
    if 'windows nt 10.0' in ua:
        return 'Windows 10/11'
    elif 'windows nt 6.3' in ua:
        return 'Windows 8.1'
    elif 'windows nt 6.2' in ua:
        return 'Windows 8'
    elif 'windows nt 6.1' in ua:
        return 'Windows 7'
    elif 'windows' in ua:
        return 'Windows'

    # macOS
    elif 'mac os x' in ua:
        match = re.search(r'mac os x ([\d_]+)', ua)
        if match:
            version = match.group(1).replace('_', '.')
            return f'macOS {version}'
        return 'macOS'

    # Linux
    elif 'linux' in ua:
        if 'android' in ua:
            match = re.search(r'android ([\d.]+)', ua)
            if match:
                return f'Android {match.group(1)}'
            return 'Android'
        return 'Linux'

    # iOS
    elif 'iphone' in ua or 'ipad' in ua:
        match = re.search(r'os ([\d_]+)', ua)
        if match:
            version = match.group(1).replace('_', '.')
            return f'iOS {version}'
        return 'iOS'

    return None


def _parse_device_type(ua: str) -> str:
    """解析设备类型"""
    # Mobile
    if any(keyword in ua for keyword in ['iphone', 'android', 'mobile']):
        return 'mobile'

    # Tablet
    elif any(keyword in ua for keyword in ['ipad', 'tablet']):
        return 'tablet'

    # Desktop
    return 'desktop'


def _generate_device_name(
    browser: Optional[str],
    os: Optional[str],
    device_type: str
) -> str:
    """生成设备名称"""
    parts = []

    if browser and browser != 'Unknown':
        parts.append(browser)

    if os:
        parts.append(os)

    if device_type == 'mobile':
        parts.append('手机')
    elif device_type == 'tablet':
        parts.append('平板')
    else:
        parts.append('桌面')

    return ' · '.join(parts) if parts else '未知设备'


def get_client_ip(request) -> Optional[str]:
    """
    从 FastAPI Request 中获取客户端 IP

    Args:
        request: FastAPI Request 对象

    Returns:
        客户端 IP 地址
    """
    # 优先从代理头获取真实 IP
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        # X-Forwarded-For 可能包含多个 IP，取第一个
        return forwarded_for.split(',')[0].strip()

    real_ip = request.headers.get('X-Real-IP')
    if real_ip:
        return real_ip

    # 直接连接的客户端 IP
    if request.client:
        return request.client.host

    return None
