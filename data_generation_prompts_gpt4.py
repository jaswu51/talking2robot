import os
os.environ['OPENAI_API_KEY'] = 'xxx'

import re
import base64
from openai import OpenAI

client = OpenAI()
prompt = """
If a person on an autonomous wheelchair is about to move forward and observes the current scene, \n
what kind of oral instructions might they give to the wheelchair? 
List 10 possible user intention variations and format the output as a list, such as:
[
'I want to go to a place to rest for 10 minutes.',
'Turn left and proceed slowly.',
'Circle around the curb.'
]
Use your imaginations to think about user needs for current image frame and generate the instructions. 
Only output in this standard list format, so it is easy to apply RE to split them. 
"""

   
# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "image_pair_five_second.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": prompt,
        },
        {
          "type": "image_url",
          "image_url": {
            "url":  f"data:image/jpeg;base64,{base64_image}"
          },
        },
      ],
    }
  ],
)

extracted_list = re.findall(r"'(.*?)'", response.choices[0].message.content)

print(extracted_list)