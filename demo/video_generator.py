import os
import tempfile
import textwrap
from gtts import gTTS
from moviepy.editor import (
    VideoFileClip, 
    AudioFileClip, 
    TextClip, 
    CompositeVideoClip, 
    ColorClip, 
    ImageClip
)
import random


def create_gradient_background(width, height, start_color=None, end_color=None):
    """创建渐变背景"""
    if start_color is None:
        start_color = (random.randint(0, 100), random.randint(100, 200), random.randint(150, 255))
    if end_color is None:
        end_color = (random.randint(100, 200), random.randint(50, 150), random.randint(200, 255))
    
    import numpy as np
    
    # 创建渐变效果
    gradient = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        ratio = y / height
        for c in range(3):
            gradient[y, :, c] = int(start_color[c] * (1 - ratio) + end_color[c] * ratio)
    
    return gradient


def generate_video(
    text, 
    output_path="output.mp4",
    width=1920, 
    height=1080,
    duration=None,
    theme=None
):
    """
    生成视频的核心函数
    
    Args:
        text: 要转换为视频的文本
        output_path: 输出文件路径
        width: 视频宽度
        height: 视频高度
        duration: 视频持续时间（秒），如果不指定则根据文本长度自动计算
        theme: 主题颜色
    
    Returns:
        生成的视频文件路径
    """
    # 计算合适的视频时长
    if duration is None:
        # 根据文本长度计算大概的时长
        duration = max(10, min(len(text) / 10, 60))
    
    # 1. 生成TTS语音
    print("🎤 生成语音中...")
    tts = gTTS(text=text, lang='zh', slow=False)
    audio_path = tempfile.mktemp(suffix='.mp3')
    tts.save(audio_path)
    
    # 获取音频时长，确保视频和音频时长匹配
    audio_clip = AudioFileClip(audio_path)
    audio_duration = audio_clip.duration
    if audio_duration > 0:
        duration = audio_duration  # 使用实际音频时长
    print(f"⏱️ 音频时长: {audio_duration:.1f}秒")
    
    # 2. 创建背景
    print("🎨 创建背景...")
    theme_colors = {
        "blue": ((30, 144, 255), (0, 71, 171)),
        "green": ((34, 197, 94), (21, 128, 61)),
        "purple": ((168, 85, 247), (109, 40, 217)),
        "orange": ((251, 146, 60), (217, 119, 6)),
        "pink": ((244, 114, 182), (192, 38, 114)),
    }
    
    if theme and theme in theme_colors:
        start_color, end_color = theme_colors[theme]
        gradient = create_gradient_background(width, height, start_color, end_color)
    else:
        gradient = create_gradient_background(width, height)
    
    # 将numpy数组转换为临时图片用于视频
    from PIL import Image
    temp_img_path = tempfile.mktemp(suffix='.png')
    img = Image.fromarray(gradient)
    img.save(temp_img_path)
    
    # 创建背景视频
    background_clip = ImageClip(temp_img_path).set_duration(duration)
    
    # 3. 添加文字
    print("📝 添加文字...")
    # 自动换行
    wrapped_text = textwrap.fill(text, width=35)
    
    # 创建文字clip
    text_clip = TextClip(
        wrapped_text,
        fontsize=55,
        color='white',
        font='SimHei',  # 中文字体
        size=(width - 200, height - 200),
        method='caption',
        align='center'
    ).set_duration(duration)
    
    text_clip = text_clip.set_position('center')
    
    # 4. 添加标题
    # 提取前几个词作为标题
    title_text = text.split('，')[0].split('。')[0][:30]
    if title_text:
        title_clip = TextClip(
            title_text,
            fontsize=70,
            color='white',
            font='SimHei',
            method='label'
        ).set_duration(4)  # 标题显示4秒
        
        title_clip = title_clip.set_position(('center', height//4))
    
    # 5. 合成视频
    print("🎬 合成视频中...")
    layers = [background_clip, text_clip]
    if title_text:
        layers.append(title_clip)
    
    final_clip = CompositeVideoClip(layers, size=(width, height))
    
    # 6. 添加音频
    final_clip = final_clip.set_audio(audio_clip)
    
    # 7. 导出视频
    print("📤 导出视频中...")
    final_clip.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        logger='bar'
    )
    
    # 清理临时文件
    audio_clip.close()
    os.remove(audio_path)
    os.remove(temp_img_path)
    
    print(f"✅ 视频生成完成: {output_path}")
    return output_path


def generate_video_with_scenes(text, output_path="output.mp4", num_scenes=3):
    """
    生成多场景视频（增强版）
    """
    sentences = [s.strip() for s in text.split('。') if s.strip()]
    scenes = sentences[:num_scenes]
    
    print(f"🎬 生成{len(scenes)}个场景的视频")
    
    # 为每个场景生成视频片段
    clips = []
    themes = ["blue", "green", "purple", "orange", "pink"]
    
    for i, scene_text in enumerate(scenes):
        theme = themes[i % len(themes)]
        scene_output = f"temp_scene_{i}.mp4"
        generate_video(scene_text + "。", scene_output, theme=theme, duration=5)
        clips.append(VideoFileClip(scene_output))
    
    # 连接所有场景
    from moviepy.editor import concatenate_videoclips
    final_clip = concatenate_videoclips(clips, method="compose")
    
    # 导出
    final_clip.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
    
    # 清理临时文件
    for i in range(len(scenes)):
        os.remove(f"temp_scene_{i}.mp4")
    
    return output_path


if __name__ == "__main__":
    # 测试
    test_text = "人工智能正在改变我们的生活，从自动驾驶到医疗诊断，AI的应用越来越广泛。未来，AI将成为我们生活中不可或缺的一部分，帮助我们解决更多复杂的问题。"
    print("🚀 开始测试视频生成...")
    generate_video(test_text, "demo_output.mp4")
