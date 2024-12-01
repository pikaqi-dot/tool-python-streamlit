import streamlit as st
import requests
import random
import json
import hashlib
import time

def translate_text():
    st.header("文本翻译")
    with st.expander("翻译工具", expanded=True):
        st.markdown("""
        ---
        该功能可以帮助你：
        - 支持多种语言之间的翻译
        - 支持批量文本翻译
        - 使用百度翻译API
        """)
        
        # 从环境变量或Streamlit Secrets获取API密钥
        BAIDU_APP_ID = st.text_input("百度翻译APP ID", type="password")
        BAIDU_SECRET_KEY = st.text_input("百度翻译密钥", type="password")
        
        if not BAIDU_APP_ID or not BAIDU_SECRET_KEY:
            st.warning("请输入百度翻译API的APP ID和密钥")
            st.markdown("""
            如何获取百度翻译API密钥：
            1. 访问[百度翻译开放平台](http://api.fanyi.baidu.com/api/trans/product/desktop)
            2. 注册并创建应用
            3. 获取APP ID和密钥
            """)
            return

        # 语言选项
        LANGUAGES = {
            "中文": "zh",
            "英语": "en",
            "日语": "jp",
            "韩语": "kor",
            "法语": "fra",
            "德语": "de",
            "俄语": "ru",
            "西班牙语": "spa",
            "意大利语": "it",
            "葡萄牙语": "pt"
        }

        col1, col2 = st.columns(2)
        with col1:
            from_lang = st.selectbox("源语言", list(LANGUAGES.keys()))
        with col2:
            to_lang = st.selectbox("目标语言", list(LANGUAGES.keys()), index=1)

        # 输入文本区域
        text_to_translate = st.text_area("输入要翻译的文本", height=150)

        def translate_baidu(text, from_lang, to_lang):
            url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
            salt = str(random.randint(32768, 65536))
            sign = hashlib.md5((BAIDU_APP_ID + text + salt + BAIDU_SECRET_KEY).encode()).hexdigest()
            
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            payload = {
                'appid': BAIDU_APP_ID,
                'q': text,
                'from': LANGUAGES[from_lang],
                'to': LANGUAGES[to_lang],
                'salt': salt,
                'sign': sign
            }

            try:
                response = requests.post(url, params=payload, headers=headers)
                result = response.json()
                
                if 'error_code' in result:
                    st.error(f"翻译错误 (错误码: {result['error_code']}): {result.get('error_msg', '未知错误')}")
                    return None
                    
                return result['trans_result'][0]['dst']
                
            except Exception as e:
                st.error(f"翻译请求失败: {str(e)}")
                return None

        if st.button("翻译", use_container_width=True):
            if text_to_translate:
                with st.spinner("正在翻译..."):
                    # 添加延时以遵守API限制
                    time.sleep(1)
                    translation = translate_baidu(text_to_translate, from_lang, to_lang)
                    
                    if translation:
                        st.success("翻译完成！")
                        st.markdown("### 翻译结果")
                        st.markdown(translation)
                        
                        # 提供复制按钮
                        st.markdown("""
                        <textarea id="translation" style="position: absolute; left: -9999px;">{}</textarea>
                        <button onclick="
                            var copyText = document.getElementById('translation');
                            copyText.select();
                            document.execCommand('copy');
                        ">复制翻译结果</button>
                        """.format(translation), unsafe_allow_html=True)
            else:
                st.warning("请输入要翻译的文本")
