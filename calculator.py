import streamlit as st

# 设置页面标题
st.title("🧮 简易计算器")

# 1. 输入两个数字
num1 = st.number_input("请输入第一个数字", value=0.0)
num2 = st.number_input("请输入第二个数字", value=0.0)

# 2. 选择运算方式
operation = st.selectbox("选择运算类型", ("加法 +", "减法 -", "乘法 ×", "除法 ÷"))

# 3. 计算按钮
if st.button("开始计算"):
    # 根据选择执行运算
    if operation == "加法 +":
        result = num1 + num2
        st.success(f"✅ 计算结果：{num1} + {num2} = {result}")

    elif operation == "减法 -":
        result = num1 - num2
        st.success(f"✅ 计算结果：{num1} - {num2} = {result}")

    elif operation == "乘法 ×":
        result = num1 * num2
        st.success(f"✅ 计算结果：{num1} × {num2} = {result}")

    elif operation == "除法 ÷":
        # 判断除零错误
        if num2 == 0:
            st.error("❌ 错误：除数不能为 0！")
        else:
            result = num1 / num2
            st.success(f"✅ 计算结果：{num1} ÷ {num2} = {result}")