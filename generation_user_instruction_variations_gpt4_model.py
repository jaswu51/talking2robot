import os
import re
import base64
from openai import OpenAI
from utils.prompts import user_instruction_generation_prompt_v0

# 环境变量中设置 OpenAI API Key
os.environ['OPENAI_API_KEY'] = 'xxx'

# 初始化 OpenAI 客户端
client = OpenAI()


# 定义数据和输出文件夹
input_folder = "data/preprocessed_data/ride_17822_20240203052746/image_pairs"
output_file = "data/preprocessed_data/ride_17822_20240203052746/prompt_image_pairs.txt"

# 编码图片为 base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
# 遍历输入文件夹的所有子文件夹
for root, dirs, files in os.walk(input_folder):
    # 检查文件夹是否包含指定的两张图片
    if "image_pair_half_second.jpg" in files and "image_pair_five_second.jpg" in files:
        # 获取图片路径并规范路径格式
        half_second_image_path = os.path.normpath(os.path.join(root, "image_pair_half_second.jpg"))
        five_second_image_path = os.path.normpath(os.path.join(root, "image_pair_five_second.jpg"))
        
        # 编码图片为 base64
        half_second_base64 = encode_image(half_second_image_path)
        five_second_base64 = encode_image(five_second_image_path)
        
        # 调用 GPT 接口生成 prompt
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_instruction_generation_prompt_v0,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{half_second_base64}"
                            },
                        },
                    ],
                }
            ],
        )
        
        # 从响应中提取 prompt 列表
        extracted_list = re.findall(r"'(.*?)'", response.choices[0].message.content)
        
        # 实时写入文件
        with open(output_file, "a") as f_out:  # 使用 "a" 模式进行追加写入
            for prompt in extracted_list:
                f_out.write(f"{prompt},{half_second_image_path},{five_second_image_path}\n")
            print("Text-image pairs have been saved.")
