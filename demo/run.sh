#!/bin/bash

echo "=========================================="
echo "🎬 文本到视频 Demo"
echo "=========================================="
echo ""

# 检查FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ 警告: FFmpeg 未安装"
    echo ""
    echo "安装 FFmpeg:"
    echo "  Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    echo ""
fi

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: Python3 未找到"
    exit 1
fi

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📚 安装/更新依赖..."
pip install -q -r requirements.txt

echo ""
echo "=========================================="
echo "🚀 启动应用中..."
echo "📱 请访问: http://localhost:8501"
echo "=========================================="
echo ""

# 启动Streamlit
streamlit run app.py
