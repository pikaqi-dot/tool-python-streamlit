import streamlit as st
import pandas as pd
import random
import os
import fitz  # PyMuPDF
from docx import Document
from docx.shared import Inches
import tempfile

st.set_page_config(
    page_title="多功能数据处理工具",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 侧边栏：功能选择
st.sidebar.title("功能选择")
selected_function = st.sidebar.radio(
    "选择要使用的功能：",
    ["Excel关键字检索", "PDF转Word", "功能3"]
)

# 主标题
st.title("多功能数据处理工具")

# Excel关键字检索功能
if selected_function == "Excel关键字检索":
    with st.container():
        st.header("Excel关键字检索")
        st.markdown("""
        ---
        该功能可以帮助你：
        - 上传Excel文件并选择工作表
        - 根据指定列名和关键字进行筛选
        - 支持关键字包含和排除两种模式
        - 将结果保存为新的Excel文件
        """)
        
        with st.expander("Excel文件处理", expanded=True):
            uploaded_file = st.file_uploader("上传文件", type=['xlsx', 'xls'], key="excel_uploader")

            if uploaded_file is not None:
                xls = pd.ExcelFile(uploaded_file)
                sheet_names = xls.sheet_names
                
                selected_sheets = st.multiselect("选择工作表", options=sheet_names)
                
                col1, col2 = st.columns(2)
                with col1:
                    col_key = st.text_input("列名：")
                with col2:
                    filter_key = st.text_input("检索关键字：")
                
                exclude = st.checkbox("排除模式（不包含关键字的结果）")
                
                if st.button("开始查询", use_container_width=True):
                    if col_key and filter_key and selected_sheets:
                        with st.spinner('处理中...'):
                            output_path = f'{random.randint(10000, 99999)}.xlsx'
                            
                            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                                found_data = False
                                for sheet_name in selected_sheets:
                                    df = pd.read_excel(xls, sheet_name=sheet_name)
                                    if col_key in df.columns:
                                        if not exclude:
                                            filtered_df = df[df[col_key].astype(str).str.contains(filter_key, na=False)]
                                        else:
                                            filtered_df = df[~df[col_key].astype(str).str.contains(filter_key, na=False)]
                                        if not filtered_df.empty:
                                            filtered_df.to_excel(writer, sheet_name=sheet_name, index=False)
                                            found_data = True
                            
                            if found_data:
                                st.success("处理完成！")
                                
                                with open(output_path, 'rb') as f:
                                    st.download_button(
                                        label="下载处理后的文件",
                                        data=f,
                                        file_name=output_path,
                                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                        use_container_width=True
                                    )
                                
                                if os.path.exists(output_path):
                                    os.remove(output_path)
                            else:
                                st.warning("未找到符合条件的数据！")
                    else:
                        st.warning("请填写所有必要信息（列名、关键字）并选择至少一个工作表！")

# PDF转Word功能
elif selected_function == "PDF转Word":
    st.header("PDF转Word")
    with st.expander("PDF转换器", expanded=True):
        st.markdown("""
        ---
        该功能可以帮助你：
        - 将PDF文件转换为Word文档
        - 保留文本内容和基本格式
        - 支持多页PDF文档
        """)
        
        uploaded_file = st.file_uploader("上传PDF文件", type=['pdf'], key="pdf_uploader")
        
        if uploaded_file is not None:
            # 创建临时文件来保存上传的PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_pdf:
                tmp_pdf.write(uploaded_file.getvalue())
                pdf_path = tmp_pdf.name

            try:
                # 创建Word文档
                doc = Document()
                
                # 打开PDF文件
                pdf_document = fitz.open(pdf_path)
                total_pages = len(pdf_document)
                
                # 显示进度条
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 逐页处理PDF
                for page_num in range(total_pages):
                    # 更新进度
                    progress = (page_num + 1) / total_pages
                    progress_bar.progress(progress)
                    status_text.text(f"正在处理第 {page_num + 1} 页，共 {total_pages} 页...")
                    
                    # 获取当前页面
                    page = pdf_document[page_num]
                    
                    # 提取文本
                    text = page.get_text()
                    
                    # 添加到Word文档
                    doc.add_paragraph(text)
                    
                    # 添加分页符（除了最后一页）
                    if page_num < total_pages - 1:
                        doc.add_page_break()
                
                # 保存Word文档到临时文件
                with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_docx:
                    doc.save(tmp_docx.name)
                    
                    # 创建下载按钮
                    with open(tmp_docx.name, 'rb') as f:
                        st.success("转换完成！")
                        st.download_button(
                            label="下载Word文档",
                            data=f,
                            file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )
                    
                    # 清理临时文件
                    os.unlink(tmp_docx.name)
                
                # 关闭PDF文档
                pdf_document.close()
                
            except Exception as e:
                st.error(f"转换过程中出现错误：{str(e)}")
            
            finally:
                # 清理临时PDF文件
                if os.path.exists(pdf_path):
                    os.unlink(pdf_path)

# 功能3
elif selected_function == "功能3":
    st.header("功能3")
    with st.expander("功能3说明", expanded=True):
        st.write("这里是功能3的内容，待开发...")
