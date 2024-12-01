import streamlit as st
from modules.excel_processor import process_excel
from modules.pdf_converter import convert_pdf_to_word
from modules.translator import translate_text
from modules.video_editor import process_video

st.set_page_config(
    page_title="多功能数据处理工具",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 创建侧边栏
st.sidebar.title("功能选择")
selected_function = st.sidebar.radio(
    "请选择要使用的功能：",
    ["Excel处理", "PDF转Word", "文本翻译", "视频剪辑"]
)

# 根据选择显示不同的功能
if selected_function == "Excel处理":
    process_excel()
elif selected_function == "PDF转Word":
    convert_pdf_to_word()
elif selected_function == "文本翻译":
    translate_text()
elif selected_function == "视频剪辑":
    process_video()
