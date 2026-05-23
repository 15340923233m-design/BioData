# 删掉了错误的 email.mime 导入
import streamlit as st
from PIL import Image

st.title("Wang")

# 用正确的 Image 类打开图片（大写 I）
image = Image.open("OIP.png")
st.image(image, caption="", width=500)