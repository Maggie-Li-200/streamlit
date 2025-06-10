# 陈列图像分析助手 - 网页版本（带图像识别逻辑）

import streamlit as st
from PIL import Image
import numpy as np
import cv2

st.set_page_config(page_title="陈列图像分析助手", layout="centered")

# 页面标题
st.title("👜 陈列图像分析助手")
st.markdown("请上传一张服装陈列照片，我将为你自动生成完整的专业分析报告。")

# 上传图片
uploaded_file = st.file_uploader("上传陈列图片", type=["jpg", "jpeg", "png"])

# 简易图像特征提取函数
def extract_image_features(image: Image.Image) -> dict:
    img = np.array(image.convert("RGB"))
    resized = cv2.resize(img, (200, 200))
    avg_color = np.mean(resized.reshape(-1, 3), axis=0)
    brightness = np.mean(cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY))

    # 粗略判断主色调
    if avg_color[2] > avg_color[0] and avg_color[2] > avg_color[1]:
        color_tag = "偏紫/粉色系"
    elif avg_color[0] > avg_color[1]:
        color_tag = "偏蓝色系"
    else:
        color_tag = "浅米/灰白系"

    return {
        "main_color": color_tag,
        "brightness_level": "偏亮" if brightness > 160 else "中性/偏暗"
    }

# 自动话术生成器
def generate_dynamic_report(features: dict) -> dict:
    color = features['main_color']
    light = features['brightness_level']

    return {
        "headline": f"以{color}为主色调，整体{light}视觉氛围，构建轻盈明亮的春夏主题陈列。",
        "highlights": [
            f"整组色调以{color}为主，配合{light}打光，视觉舒适度高",
            "中段C位如有留白，便于聚焦主推款形成视觉断点",
            "两侧风格建议分区展开，避免商品视觉干扰",
            "色块与结构节奏需拉开，增强空间呼吸感",
            "适合打造清爽、梦感、婚礼相关场景主题"
        ],
        "execution": [
            "中间单挂主推款增强焦点感，建议不密挂",
            "左右风格如偏差大，建议以颜色做过渡区域",
            "每组间适当留空，控制节奏避免视觉疲劳",
            "利用面料差异增加视觉层次：如蕾丝 vs 棉质",
            "禁用深色/厚重面料影响清爽氛围"
        ],
        "application": [
            "C位焦点式挂法",
            "风格配色双重分区法",
            f"{color}色调统一控制法",
            "节奏错落分组法",
            "氛围导向风格设定法"
        ],
        "upload_guidelines": [
            "主挂C位区域高清照",
            "左右分区结构与配色分布图",
            "节奏与结构错落局部图"
        ]
    }

# 展示结果
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="已上传图片", use_column_width=True)

    features = extract_image_features(image)
    result = generate_dynamic_report(features)

    st.markdown("---")
    st.subheader("📌 一句话重点导读")
    st.write(result['headline'])

    st.subheader("✨ 亮点分析")
    for i, point in enumerate(result['highlights'], 1):
        st.markdown(f"**{i}.** {point}")

    st.subheader("🛠️ 执行要点")
    for i, point in enumerate(result['execution'], 1):
        st.markdown(f"**{i}.** {point}")

    st.subheader("📌 复制应用建议")
    for i, point in enumerate(result['application'], 1):
        st.markdown(f"**{i}.** {point}")

    st.subheader("📷 建议上传打卡图区域")
    for i, point in enumerate(result['upload_guidelines'], 1):
        st.markdown(f"**{i}.** {point}")
