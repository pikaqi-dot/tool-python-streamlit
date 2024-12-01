import streamlit as st
import pandas as pd
import random
import os

st.set_page_config(page_title="国考职位表关键字检索", layout="wide")
st.title("国考职位表关键字检索")

# File uploader
uploaded_file = st.file_uploader("上传文件", type=['xlsx', 'xls'])

if uploaded_file is not None:
    # Read Excel file
    xls = pd.ExcelFile(uploaded_file)
    sheet_names = xls.sheet_names
    
    # Sheet selection
    selected_sheets = st.multiselect("选择工作表", options=sheet_names)
    
    # Input fields
    col1, col2 = st.columns(2)
    with col1:
        col_key = st.text_input("列名：")
    with col2:
        filter_key = st.text_input("检索关键字：")
    
    # Exclude checkbox
    exclude = st.checkbox("排除")
    
    # Process button
    if st.button("开始查询"):
        if col_key and filter_key and selected_sheets:
            # Create random output filename
            output_path = f'{random.randint(10000, 99999)}.xlsx'
            
            # Process each selected sheet
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                for sheet_name in selected_sheets:
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                    if col_key in df.columns:
                        if not exclude:
                            filtered_df = df[df[col_key].astype(str).str.contains(filter_key, na=False)]
                        else:
                            filtered_df = df[~df[col_key].astype(str).str.contains(filter_key, na=False)]
                        if not filtered_df.empty:
                            filtered_df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Show success message and download button
            st.success(f"处理完成！文件已保存为: {output_path}")
            
            # Read the generated file and create a download button
            with open(output_path, 'rb') as f:
                st.download_button(
                    label="下载处理后的文件",
                    data=f,
                    file_name=output_path,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            # Clean up the file after download
            if os.path.exists(output_path):
                os.remove(output_path)
                
        else:
            st.warning("请填写所有必要信息（列名、关键字）并选择至少一个工作表！")
