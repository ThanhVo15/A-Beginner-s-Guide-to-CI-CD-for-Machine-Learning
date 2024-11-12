
import gradio as gr
from skops.io import get_untrusted_types
import skops.io as sio

# Xác định các kiểu không tin cậy từ tệp cụ thể
untrusted_types = get_untrusted_types(file="Model/drug_pipeline.skops")

# Tải mô hình, sử dụng các kiểu không tin cậy đã xác định như các kiểu tin cậy
pipeline = sio.load("Model/drug_pipeline.skops", trusted=untrusted_types)

def predict_drug(age, sex, blood_pressure, cholesterol, na_to_k_ratio):
    """
    Dự đoán loại thuốc dựa trên các đặc điểm của bệnh nhân.

    Args:
        age (int): Tuổi của bệnh nhân
        sex (str): Giới tính của bệnh nhân 
        blood_pressure (str): Mức độ huyết áp
        cholesterol (str): Mức cholesterol
        na_to_k_ratio (float): Tỉ lệ natri trên kali trong máu

    Returns:
        str: Nhãn loại thuốc dự đoán
    """
    features = [age, sex, blood_pressure, cholesterol, na_to_k_ratio]
    predicted_drug = pipeline.predict([features])[0]

    label = f"Predicted Drug: {predicted_drug}"
    return label

# Định nghĩa các đầu vào và đầu ra của giao diện Gradio
inputs = [
    gr.Slider(15, 74, step=1, label="Age"),
    gr.Radio(["M", "F"], label="Sex"),
    gr.Radio(["HIGH", "LOW", "NORMAL"], label="Blood Pressure"),
    gr.Radio(["HIGH", "NORMAL"], label="Cholesterol"),
    gr.Slider(6.2, 38.2, step=0.1, label="Na_to_K"),
]
outputs = gr.Label(num_top_classes=5)

examples = [
    [30, "M", "HIGH", "NORMAL", 15.4],
    [35, "F", "LOW", "NORMAL", 8],
    [50, "M", "HIGH", "HIGH", 34],
]

title = "Drug Classification"
description = "Nhập thông tin để xác định chính xác loại thuốc phù hợp."
article = (
    "Ứng dụng này là một phần của Beginner's Guide to CI/CD for Machine Learning. "
    "Hướng dẫn cách tự động hóa quá trình huấn luyện, đánh giá và triển khai mô hình tới Hugging Face bằng GitHub Actions."
)

# Khởi chạy giao diện Gradio
gr.Interface(
    fn=predict_drug,
    inputs=inputs,
    outputs=outputs,
    examples=examples,
    title=title,
    description=description,
    article=article,
    theme=gr.themes.Soft(),
).launch()
