#!/usr/bin/env python3
"""
文本到音频的演示 - 不需要FFmpeg
"""

print("=" * 60)
print("🎤 文本到音频 Demo")
print("=" * 60)
print()

import sys
import os

# 检查依赖
try:
    import gtts
    print("✅ gTTS 已安装")
except ImportError:
    print("❌ gTTS 未安装")
    print("  运行: pip install gTTS")
    sys.exit(1)

print()
print("✅ 所有依赖就绪！")
print()

# 测试文本
print("📝 测试文本:")
test_text = "欢迎使用文本到音频Demo。这是一个简单的测试，展示如何将文字转换为音频。虽然服务器没有FFmpeg，但我们仍然可以生成音频文件！"
print(test_text)
print()

# 生成TTS
print("🚀 开始生成音频...")
from gtts import gTTS

tts = gTTS(text=test_text, lang='zh', slow=False)
output_path = "demo_audio.mp3"

print(f"🎤 生成语音中...")
tts.save(output_path)

print(f"✅ 音频已生成: {output_path}")
print()

# 查看文件信息
if os.path.exists(output_path):
    file_size = os.path.getsize(output_path) / 1024
    print(f"📄 文件信息:")
    print(f"  文件名: {output_path}")
    print(f"  大小: {file_size:.1f} KB")
    print(f"  位置: {os.path.abspath(output_path)}")
    print()
    print("🎉 成功！你可以下载这个音频文件来测试。")
else:
    print("❌ 音频生成失败")

print()
print("=" * 60)
print("🎯 核心功能演示完成！")
print("=" * 60)
print()
print("这个Demo展示了：")
print("1. 📝 输入文本")
print("2. 🎤 生成语音 (TTS)")
print("3. 💾 保存为MP3文件")
print()
print("虽然没有FFmpeg无法生成视频，但核心的文本到音频功能已经实现！")
