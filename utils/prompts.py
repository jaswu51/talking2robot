
user_instruction_generation_prompt_v0 = """
If a person on an autonomous wheelchair is about to move forward and observes the current scene, \n
what kind of oral instructions might they give to the wheelchair? 
List 4 possible user intention variations and format the output as a list, such as:
[
'I want to go to a place to rest for 10 minutes.',
'Turn left and proceed slowly.',
'Circle around the curb.'
]
Use your imaginations to think about user needs for current image frame and generate the instructions. 
Only output in this standard list format, so it is easy to apply RE to split them. 
"""

user_instruction_generation_prompt_v1 = """
If a person on an autonomous wheelchair is about to move forward and observes the current scene, 
what kind of oral instructions might they give to the wheelchair? 
List 4 possible user intention variations and format the output as a dictionary, where keys are the variation type numbers 
and values are the user instruction sentences. Output only in this standard format so it can be easily parsed with regular expressions.

Example format:
{
  "1": "I want to go to a place to rest for 10 minutes.",
  "2": "Turn left and proceed slowly.",
  "3": "Circle around the curb."
}

Use your imagination to consider the user's possible needs based on the current scene and generate instructions accordingly. 
Consider using variations in the type of command and in the tone, and select randomly to describe objects and express personalized preferences. 
You may choose from the following variations:

1. **Direct Commands vs. Indirect Commands**: 
   - *Direct*: Explicit instructions, e.g., “Turn right at the end of the sidewalk.”
   - *Indirect*: Polite or softer tone, e.g., “Could you please avoid the bumps on the left side?”

2. **Navigational Guidance with Prepositional Phrases**: 
   - Uses spatial relationships, e.g., “Head towards the building on your right, then turn at the corner.”

3. **Ambiguous References**:
   - Vague references requiring context, e.g., “Move a little bit more to the right.”

4. **Comparative or Relative Instructions**:
   - Commands based on comparison or relative position, e.g., “Go further right than where you are now.”

5. **Goal-Oriented Commands**:
   - Reaching a specific destination, e.g., “Reach the end of the block and then cross the street.”

6. **Step-by-Step Instructions**:
   - Commands with multiple steps, e.g., “First, turn slightly left to avoid the cracks. Then, move forward until you reach the lamp post.”

7. **High-Level Instructions**:
   - General commands, e.g., “Navigate this area safely and avoid any obstacles.”

8. **Emotion-based Commands**:
   - Expresses urgency, encouragement, etc., e.g., “Carefully avoid the bumpy area, no need to rush.”

9. **Conditional Instructions**:
   - Commands based on conditions, e.g., “If you see a bump, navigate around it.”

10. **Range-Based Instructions (Proximity and Distance)**:
    - Focuses on maintaining distance, e.g., “Stay at least a foot away from the edge of the sidewalk.”

Please use the above variations to create a diverse and realistic set of user instructions. Format output only as shown in the example.
"""

object_cost_generation_prompt_v0="""
Based on the user instructions and the current robot's ego-view image, 
generate intger costs ranging from negative 10 to positive 10,
for any objects that are semantically and logically related to the user instructions. 
If a user wanan avoid some objects, assign the costs as negative values.
If a user wanna approach near to some objects, assign the costs as positive values. 
Otherwise neutrally zero.
Respond with only a dictionary, where object names are keys and costs are values. 
Ensure that object descriptions are specific enough 
for a segmentation model to generate accurate pixel-wise masks. 
Only output the dictionary, staring with { and end with }.
"""
