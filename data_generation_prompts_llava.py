from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration
import torch
from PIL import Image
import requests

processor = LlavaNextProcessor.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")

model = LlavaNextForConditionalGeneration.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf", torch_dtype=torch.float16, low_cpu_mem_usage=True)
model.to("cuda:0")

# prepare image and text prompt, using the appropriate prompt template
image = Image.open('data/preprocessed_data/ride_17822_20240203052746/image_pairs/972b2f73e8408e687e2819a2d9e70693_ride_17822__uid_s_1000__uid_e_video_20240203052751685/image_pair_five_second.jpg')

conversation = [
    {
        "role": "user",
        "content": [
            {"type": "image"},
            {"type": "text", "text": "If a person on an autonomous wheelchair is about to move forward and looks at the current scene, what kind of oral instructions might they give to the wheelchair? List 10 possible variations, and output in the format of a list like ['I wanan to go to a place to rest for 10 minutes.',...,'Circle around the curb.']"},
        ],
    },
]
prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
inputs = processor(image, prompt, return_tensors="pt").to("cuda:0")

# autoregressively complete prompt
output = model.generate(**inputs, max_new_tokens=100)

print(processor.decode(output[0], skip_special_tokens=True))