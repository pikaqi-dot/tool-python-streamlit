import streamlit as st
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
import tempfile
import os
from datetime import datetime
import time

def format_time(seconds):
    """将秒数转换为 HH:MM:SS 格式"""
    return str(datetime.fromtimestamp(seconds).strftime('%H:%M:%S'))

def parse_time(time_str):
    """将 HH:MM:SS 格式转换为秒数"""
    try:
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s
    except:
        return 0

def process_video():
    st.header("视频剪辑")
    with st.expander("视频剪辑工具", expanded=True):
        st.markdown("""
        ---
        该功能可以帮助你：
        - 剪切视频片段
        - 合并多个视频
        - 提取/替换音频
        - 调整视频速度
        """)

        # 上传视频文件
        uploaded_file = st.file_uploader("上传视频文件", type=['mp4', 'avi', 'mov', 'mkv'], key="video_uploader")
        
        if uploaded_file is not None:
            # 保存上传的视频到临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_video:
                tmp_video.write(uploaded_file.read())
                video_path = tmp_video.name

            try:
                # 加载视频
                video = VideoFileClip(video_path)
                
                # 显示视频信息
                st.info(f"""
                视频信息：
                - 时长：{format_time(video.duration)}
                - 尺寸：{video.size}
                - FPS：{video.fps}
                """)

                # 选择操作类型
                operation = st.selectbox(
                    "选择操作",
                    ["剪切片段", "调整速度", "提取音频", "替换音频"]
                )

                if operation == "剪切片段":
                    col1, col2 = st.columns(2)
                    with col1:
                        start_time = st.text_input("开始时间 (HH:MM:SS)", "00:00:00")
                    with col2:
                        end_time = st.text_input("结束时间 (HH:MM:SS)", format_time(video.duration))

                    if st.button("预览片段", use_container_width=True):
                        start_seconds = parse_time(start_time)
                        end_seconds = parse_time(end_time)
                        
                        if start_seconds >= end_seconds:
                            st.error("开始时间必须小于结束时间")
                        else:
                            # 创建预览
                            clip = video.subclip(start_seconds, end_seconds)
                            
                            # 保存预览视频
                            preview_path = f"preview_{int(time.time())}.mp4"
                            clip.write_videofile(preview_path, 
                                              codec='libx264', 
                                              audio_codec='aac')
                            
                            # 显示预览
                            st.video(preview_path)
                            
                            # 清理预览文件
                            os.unlink(preview_path)
                            clip.close()

                    if st.button("导出片段", use_container_width=True):
                        start_seconds = parse_time(start_time)
                        end_seconds = parse_time(end_time)
                        
                        if start_seconds >= end_seconds:
                            st.error("开始时间必须小于结束时间")
                        else:
                            with st.spinner("正在处理视频..."):
                                # 剪切视频
                                clip = video.subclip(start_seconds, end_seconds)
                                
                                # 保存处理后的视频
                                output_path = f"output_{int(time.time())}.mp4"
                                clip.write_videofile(output_path, 
                                                   codec='libx264',
                                                   audio_codec='aac')
                                
                                # 提供下载
                                with open(output_path, 'rb') as f:
                                    st.download_button(
                                        label="下载处理后的视频",
                                        data=f,
                                        file_name=f"edited_{uploaded_file.name}",
                                        mime="video/mp4",
                                        use_container_width=True
                                    )
                                
                                # 清理临时文件
                                os.unlink(output_path)
                                clip.close()

                elif operation == "调整速度":
                    speed = st.slider("速度倍率", 0.25, 4.0, 1.0, 0.25)
                    
                    if st.button("预览效果", use_container_width=True):
                        # 调整速度
                        clip = video.speedx(speed)
                        
                        # 保存预览视频
                        preview_path = f"preview_{int(time.time())}.mp4"
                        clip.write_videofile(preview_path, 
                                          codec='libx264',
                                          audio_codec='aac')
                        
                        # 显示预览
                        st.video(preview_path)
                        
                        # 清理预览文件
                        os.unlink(preview_path)
                        clip.close()

                    if st.button("导出视频", use_container_width=True):
                        with st.spinner("正在处理视频..."):
                            # 调整速度
                            clip = video.speedx(speed)
                            
                            # 保存处理后的视频
                            output_path = f"output_{int(time.time())}.mp4"
                            clip.write_videofile(output_path,
                                              codec='libx264',
                                              audio_codec='aac')
                            
                            # 提供下载
                            with open(output_path, 'rb') as f:
                                st.download_button(
                                    label="下载处理后的视频",
                                    data=f,
                                    file_name=f"speed_{speed}x_{uploaded_file.name}",
                                    mime="video/mp4",
                                    use_container_width=True
                                )
                            
                            # 清理临时文件
                            os.unlink(output_path)
                            clip.close()

                elif operation == "提取音频":
                    if st.button("提取音频", use_container_width=True):
                        with st.spinner("正在提取音频..."):
                            # 提取音频
                            audio = video.audio
                            
                            # 保存音频文件
                            output_path = f"audio_{int(time.time())}.mp3"
                            audio.write_audiofile(output_path)
                            
                            # 提供下载
                            with open(output_path, 'rb') as f:
                                st.download_button(
                                    label="下载音频文件",
                                    data=f,
                                    file_name=f"{uploaded_file.name}.mp3",
                                    mime="audio/mp3",
                                    use_container_width=True
                                )
                            
                            # 清理临时文件
                            os.unlink(output_path)
                            audio.close()

                elif operation == "替换音频":
                    uploaded_audio = st.file_uploader("上传音频文件", type=['mp3', 'wav'], key="audio_uploader")
                    
                    if uploaded_audio is not None:
                        # 保存上传的音频到临时文件
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_audio:
                            tmp_audio.write(uploaded_audio.read())
                            audio_path = tmp_audio.name

                        try:
                            # 加载音频
                            new_audio = AudioFileClip(audio_path)
                            
                            if st.button("替换音频", use_container_width=True):
                                with st.spinner("正在处理视频..."):
                                    # 替换音频
                                    clip = video.set_audio(new_audio)
                                    
                                    # 保存处理后的视频
                                    output_path = f"output_{int(time.time())}.mp4"
                                    clip.write_videofile(output_path,
                                                       codec='libx264',
                                                       audio_codec='aac')
                                    
                                    # 提供下载
                                    with open(output_path, 'rb') as f:
                                        st.download_button(
                                            label="下载处理后的视频",
                                            data=f,
                                            file_name=f"new_audio_{uploaded_file.name}",
                                            mime="video/mp4",
                                            use_container_width=True
                                        )
                                    
                                    # 清理临时文件
                                    os.unlink(output_path)
                                    clip.close()
                                    new_audio.close()
                                    os.unlink(audio_path)

                        except Exception as e:
                            st.error(f"处理音频时出错：{str(e)}")
                            if os.path.exists(audio_path):
                                os.unlink(audio_path)

            except Exception as e:
                st.error(f"处理视频时出错：{str(e)}")
            
            finally:
                # 关闭视频
                if 'video' in locals():
                    video.close()
                # 清理临时文件
                if os.path.exists(video_path):
                    os.unlink(video_path)
