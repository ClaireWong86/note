#!/usr/bin/env python3
"""
简单的视频生成测试 - 直接生成一个测试视频
"""

print("=" * 60)
print("🎬 视频生成测试")
print("=" * 60)
print()

import sys

# 检查依赖
try:
    import gtts
    print("✅ gTTS 已安装")
except ImportError:
    print("❌ gTTS 未安装，请运行: pip install gTTS")
    sys.exit(1)

try:
    from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip
    print("✅ MoviePy 已安装")
except ImportError:
    print("❌ MoviePy 未安装，请运行: pip install moviepy")
    sys.exit(1)

try:
    import numpy as np
    print("✅ NumPy 已安装")
except ImportError:
    print("❌ NumPy 未安装，请运行: pip install numpy")
    sys.exit(1)

try:
    from PIL import Image
    print("✅ Pillow 已安装")
except ImportError:
    print("❌ Pillow 未安装，请运行: pip install Pillow")
    sys.exit(1)

# 检查FFmpeg
import subprocess
try:
    subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    print("✅ FFmpeg 已安装")
except (subprocess.CalledProcessError, FileNotFoundError):
    print("❌ FFmpeg 未安装")
    print("   macOS安装: brew install ffmpeg")
    print("   或者下载: https://ffmpeg.org/download.html")
    sys.exit(1)

print()
print("✅ 所有依赖检查通过！")
print()

# 开始测试生成视频
print("🚀 开始生成测试视频...")
print()

import os
import tempfile
import textwrap
import random
from gtts import gTTS

def create_gradient_background(width, height):
    """创建渐变背景"""
    start_color = (30, 144, 255)
    end_color = (0, 71, 171)
    
    gradient = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        ratio = y / height
        for c in range(3):
            gradient[y, :, c] = int(start_color[c] * (1 - ratio) + end_color[c] * ratio)
    
    return gradient

def generate_test_video():
    test_text = "欢迎使用文本到视频Demo。这是一个简单的测试，展示如何将文字转换为视频。"
    
    print("📝 测试文本:", test_text)
    print()
    
    # 1. 生成TTS
    print("🎤 正在生成语音...")
    tts = gTTS(text=test_text, lang='zh', slow=False)
    audio_path = "temp_audio.mp3"
    tts.save(audio_path)
    print("✅ 语音已生成")
    
    # 获取音频时长
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration
    print(f"⏱️ 音频时长: {duration:.1f}秒")
    
    # 2. 创建背景
    print("🎨 创建背景...")
    width, height = 1280, 720
    gradient = create_gradient_background(width, height)
    
    temp_img_path = "temp_bg.png"
    img = Image.fromarray(gradient)
    img.save(temp_img_path)
    
    background_clip = ImageClip(temp_img_path).set_duration(duration)
    
    # 3. 创建文字
    from moviepy.editor import TextClip
    print("📝 添加文字...")
    
    wrapped_text = textwrap.fill(test_text, width=30)
    
    # 使用更兼容的字体
    text_clip = TextClip(
        wrapped_text,
        fontsize=50,
        color='white',
        size=(width - 200, height - 200),
        method='caption',
        align='center'
    ).set_duration(duration)
    
    text_clip = text_clip.set_position('center')
    
    # 4. 合成
    print("🎬 合成视频...")
    final_clip = CompositeVideoClip([background_clip, text_clip], size=(width, height))
    final_clip = final_clip.set_audio(audio_clip)
    
    # 5. 导出
    output_path = "test_output.mp4"
    print(f"📤 导出到: {output_path}")
    final_clip.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        logger='bar'
    )
    
    # 清理
    audio_clip.close()
    os.remove(audio_path)
    os.remove(temp_img_path)
    
    return output_path

try:
    output_path = generate_test_video()
    print()
    print("=" * 60)
    print(f"✅ 成功！视频已生成: {output_path}")
    print("=" * 60)
    print()
    print(f"文件位置: {os.path.abspath(output_path)}")
    print()
    print("现在你可以播放这个视频来测试！")
    
except Exception as e:
    print()
    print("❌ 出错了:")
    print(str(e))
    import traceback
    traceback.print_exc()
