import streamlit as st
from modules.excel_processor import process_excel

st.set_page_config(
    page_title="多功能数据处理工具",
    page_icon="📊",
    layout="wide"
)

st.sidebar.title("功能选择")
selected_function = st.sidebar.radio(
    "请选择要使用的功能：",
    ["Excel处理"]
)

# 根据选择显示不同的功能
if selected_function == "Excel处理":
    process_excel()
