import os
import re
import base64
import json
from openai import OpenAI
from utils.prompts import object_cost_generation_prompt_v0

os.environ['OPENAI_API_KEY'] = 'xxx'
client = OpenAI()

# 文件路径
input_file = "data/preprocessed_data/ride_17822_20240203052746/prompt_image_pairs.txt"
output_file = "data/preprocessed_data/ride_17822_20240203052746/prompt_image_pairs_object_costs.json"

def encode_image(image_path):
    # 检查文件是否存在
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# 打开输出文件并开始写入 JSON 数组的开始符
with open(output_file, "a") as json_file:
    json_file.write("[")

    # 读取文件并输出每行的三项内容
    with open(input_file, "r") as f:
        for idx, line in enumerate(f):
            # 移除换行符并按逗号分割
            parts = line.strip().split(",", 2)  # 限制为最多分割成三部分
            if len(parts) == 3:
                prompt, half_second_image_path, five_second_image_path = parts
                half_second_base64 = encode_image(half_second_image_path)

                # 如果图像文件不存在，跳过当前循环
                if half_second_base64 is None:
                    print(f"File not found: {half_second_image_path}. Skipping...")
                    continue
                
                # 调用 GPT 接口生成 prompt
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": object_cost_generation_prompt_v0 + 'User instructions: ' + prompt,
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
                
                # 解析响应并将结果存储到字典中
                pattern = r'"([^"]+)":\s*(-?\d+)'
                result = {match[0]: int(match[1]) for match in re.findall(pattern, response.choices[0].message.content)}
                
                # 构建当前数据的字典
                entry = {
                    half_second_image_path: {
                        "user_instruction": prompt,
                        "object_costs": result,
                        "five_second_image_path": five_second_image_path,
                    }
                }
                print(entry)
                
                # 写入 JSON 文件并处理逗号
                json.dump(entry, json_file, indent=4)
                if idx < sum(1 for _ in open(input_file)) - 1:  # 不是最后一行时加逗号
                    json_file.write(",\n")

    # 写入 JSON 数组的结束符
    json_file.write("]")
