import streamlit as st
import os
import time
from video_generator import generate_video, generate_video_with_scenes

st.set_page_config(
    page_title="🎬 文本到视频 Demo",
    page_icon="🎬",
    layout="wide"
)

# 页面标题
st.title("🎬 文本到视频 Demo")
st.markdown("将你的文本转换为精美的视频！")

# 侧边栏设置
st.sidebar.title("⚙️ 设置")

# 视频分辨率设置
resolution = st.sidebar.selectbox(
    "视频分辨率",
    ["720p (1280x720)", "1080p (1920x1080)", "480p (854x480)"],
    index=1
)

# 解析分辨率
resolution_map = {
    "480p (854x480)": (854, 480),
    "720p (1280x720)": (1280, 720),
    "1080p (1920x1080)": (1920, 1080)
}
width, height = resolution_map[resolution]

# 主题选择
theme = st.sidebar.selectbox(
    "主题颜色",
    ["随机", "蓝色", "绿色", "紫色", "橙色", "粉色"],
    index=0
)

theme_map = {
    "随机": None,
    "蓝色": "blue",
    "绿色": "green",
    "紫色": "purple",
    "橙色": "orange",
    "粉色": "pink"
}
selected_theme = theme_map[theme]

# 模式选择
mode = st.sidebar.radio(
    "生成模式",
    ["单场景", "多场景"],
    index=0
)

# 多场景设置
num_scenes = 3
if mode == "多场景":
    num_scenes = st.sidebar.slider("场景数量", 2, 5, 3)

# 主界面
col1, col2 = st.columns([3, 1])

with col1:
    # 用户输入区域
    st.subheader("📝 输入文本")
    
    # 示例文本
    examples = {
        "人工智能介绍": "人工智能正在改变我们的生活，从自动驾驶到医疗诊断，AI的应用越来越广泛。未来，AI将成为我们生活中不可或缺的一部分，帮助我们解决更多复杂的问题。",
        "自然风光": "大自然是美丽的画卷，从雄伟的山川到宁静的湖泊，从茂密的森林到广阔的海洋。每一处风景都让人心旷神怡，流连忘返。",
        "科技改变生活": "科技的发展让我们的生活变得更加便捷，智能手机、互联网、智能家居，这些创新让我们的世界变得更加美好。"
    }
    
    selected_example = st.selectbox("选择示例文本（可选）", ["自定义"] + list(examples.keys()))
    
    if selected_example != "自定义":
        user_input = st.text_area("或者输入你自己的文本", value=examples[selected_example], height=150)
    else:
        user_input = st.text_area("输入你想转换为视频的文本", 
                                  placeholder="例如：人工智能正在改变我们的生活，从自动驾驶到医疗诊断...",
                                  height=150)
    
    # 生成按钮
    generate_btn = st.button("🎬 生成视频", type="primary", use_container_width=True)

with col2:
    st.subheader("📊 说明")
    st.info("""
    **功能特点：**
    - 🎤 自动TTS语音合成
    - 🎨 渐变彩色背景
    - 📝 文字自动换行显示
    - 🎬 导出MP4格式视频
    
    **免费使用：**
    - 无需API Key
    - 完全本地处理
    """)

# 历史记录
if "history" not in st.session_state:
    st.session_state.history = []

# 视频生成逻辑
if generate_btn and user_input:
    with st.spinner("🎬 正在生成视频，请稍候..."):
        try:
            # 创建进度条
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # 状态更新
            status_text.text("准备生成...")
            time.sleep(0.5)
            progress_bar.progress(10)
            
            # 生成视频
            timestamp = int(time.time())
            output_filename = f"generated_video_{timestamp}.mp4"
            
            status_text.text("🎤 生成语音中...")
            progress_bar.progress(30)
            
            # 根据模式选择生成方法
            if mode == "多场景":
                video_path = generate_video_with_scenes(user_input, output_filename, num_scenes)
            else:
                video_path = generate_video(user_input, output_filename, width=width, height=height, theme=selected_theme)
            
            status_text.text("✅ 视频生成完成！")
            progress_bar.progress(100)
            
            # 显示成功信息
            st.success("🎉 视频生成成功！")
            
            # 显示视频
            st.subheader("🎥 预览视频")
            st.video(video_path)
            
            # 下载按钮
            with open(video_path, "rb") as f:
                st.download_button(
                    label="📥 下载视频",
                    data=f,
                    file_name="generated_video.mp4",
                    mime="video/mp4",
                    use_container_width=True
                )
            
            # 保存到历史记录
            st.session_state.history.append({
                "text": user_input[:100] + "..." if len(user_input) > 100 else user_input,
                "path": video_path,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
        except Exception as e:
            st.error(f"❌ 生成失败: {str(e)}")
            st.info("💡 请确保已安装FFmpeg：`sudo apt-get install ffmpeg`")
else:
    if not user_input:
        st.info("👆 请在上方输入文本或选择示例")

# 历史记录
if st.session_state.history:
    st.divider()
    st.subheader("📜 历史记录")
    for i, item in enumerate(reversed(st.session_state.history[-5:])):  # 显示最近5条
        with st.expander(f"🎬 {item['timestamp']} - {item['text']}"):
            if os.path.exists(item['path']):
                st.video(item['path'])
                with open(item['path'], "rb") as f:
                    st.download_button(
                        label="📥 下载",
                        data=f,
                        file_name=f"history_video_{i}.mp4",
                        mime="video/mp4"
                    )

# 底部信息
st.divider()
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🎬 文本到视频 Demo | 基于Streamlit和MoviePy</p>
</div>
""", unsafe_allow_html=True)
