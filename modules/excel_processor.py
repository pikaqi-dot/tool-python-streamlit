import streamlit as st
import pandas as pd

def process_excel():
    st.header("Excel处理")
    with st.expander("Excel处理器", expanded=True):
        st.markdown("""
        ---
        该功能可以帮助你：
        - 读取Excel文件
        - 选择要处理的工作表
        - 指定要处理的列
        - 根据关键字筛选数据
        """)
        
        uploaded_file = st.file_uploader("上传Excel文件", type=['xlsx', 'xls'], key="excel_uploader")
        
        if uploaded_file is not None:
            # 读取Excel文件中的所有工作表
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            
            # 创建多选框让用户选择要处理的工作表
            selected_sheets = st.multiselect(
                "选择要处理的工作表",
                options=sheet_names,
                default=sheet_names[0] if sheet_names else None
            )
            
            if selected_sheets:
                # 为每个选中的工作表创建一个部分
                for sheet_name in selected_sheets:
                    st.subheader(f"工作表: {sheet_name}")
                    
                    # 读取工作表数据
                    df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                    
                    # 显示列选择和关键字输入
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # 选择要处理的列
                        selected_column = st.selectbox(
                            f"选择要处理的列 ({sheet_name})",
                            options=df.columns,
                            key=f"column_{sheet_name}"
                        )
                    
                    with col2:
                        # 输入关键字
                        keyword = st.text_input(
                            f"输入筛选关键字 ({sheet_name})",
                            key=f"keyword_{sheet_name}"
                        )
                    
                    if selected_column and keyword:
                        # 根据关键字筛选数据
                        filtered_df = df[df[selected_column].astype(str).str.contains(keyword, na=False)]
                        
                        # 显示筛选结果
                        st.write(f"找到 {len(filtered_df)} 条匹配记录:")
                        st.dataframe(filtered_df)
                        
                        # 提供下载按钮
                        if not filtered_df.empty:
                            # 将筛选结果转换为Excel
                            output = pd.ExcelWriter(f'filtered_{sheet_name}.xlsx', engine='xlsxwriter')
                            filtered_df.to_excel(output, index=False, sheet_name=sheet_name)
                            output.close()
                            
                            # 创建下载按钮
                            with open(f'filtered_{sheet_name}.xlsx', 'rb') as f:
                                st.download_button(
                                    label=f"下载筛选结果 ({sheet_name})",
                                    data=f,
                                    file_name=f"filtered_{sheet_name}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                    else:
                        st.warning("请填写所有必要信息（列名、关键字）并选择至少一个工作表！")
