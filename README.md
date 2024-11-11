# talking2robot

## Generate image pairs
We extract a pair of images from each video clip, choosing the 0.5 second frame and the 5 second frame as image pairs, and naming them as 'image_pair_half_second.jpg' and 'image_pair_five_second.jpg' respectively. 

### Run:
```
python generate_image_pairs_from_video.py
```
### Paths:

Video source (Path('data/raw_data/ride_17822_20240203052746/recordings')) 

Output image pair path (Path('data/preprocessed_data/ride_17822_20240203052746/image_pairs')) 

### Results:

'2024-11-11 07:32:15,868 - INFO - Processing complete: 162/261 videos processed successfully'.


## Generate user prompt variations from image

We only use the first image ('image_pair_half_second.jpg') in the image pairs to generate user prompts. 

For each 'image_pair_half_second.jpg', we generate 4 variations of user images. 

We tried both LLaVA 1.6 and GPT4 models to generate user instructions, and GPT4 mdoel wins. Thus we use GPT4 as the VLM. 
### GPT4 Prompt:
The prompt used to generate user instructions (user_instruction_generation_prompt_v0) can be found at utils/prompts.py

Alternatively, we have a more complext version (user_instruction_generation_prompt_v1) for future references. 
### Run:
```
python generation_user_instruction_variations_gpt4_model.py
```
### Results:
Resutls are saved at data/preprocessed_data/ride_17822_20240203052746/prompt_image_pairs.txt

## Generate object costs from image + user instruction

The GPT4 read the user instruction and the 'image_pair_half_second.jpg', and generate a dictionary of objects costs ranging from [-10, 10] as integers.
### GPT4 Prompt:
The prompt used to generate user instructions (object_cost_generation_prompt_v0) can be found at utils/prompts.py

### Run:
```
python generate_object_costs_gpt4_model.py
```
### Results:
Resutls are saved at data/preprocessed_data/ride_17822_20240203052746/prompt_image_pairs_object_costs.json

Each json block has the following fomat:
```
entry = {
    half_second_image_path: {
        "user_instruction": prompt,
        "object_costs": result,
        "five_second_image_path": five_second_image_path,
    }
}
```
examplified by:
```
{
    "data/preprocessed_data/ride_17822_20240203052746/image_pairs/972b2f73e8408e687e2819a2d9e70693_ride_17822__uid_s_1000__uid_e_video_20240203053802185/image_pair_half_second.jpg": {
        "user_prompt": "I want to move forward and find a quiet spot to relax.",
        "object_costs": {
            "trees": 5,
            "park bench": 7,
            "playground equipment": -3,
            "walking path": 8,
            "building": -2,
            "grass": 6,
            "people": -4,
            "light pole": 0
        },
        "five_second_image_path": "data/preprocessed_data/ride_17822_20240203052746/image_pairs/972b2f73e8408e687e2819a2d9e70693_ride_17822__uid_s_1000__uid_e_video_20240203053802185/image_pair_five_second.jpg"
    }
}
```