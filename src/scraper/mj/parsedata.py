import json
import os
from collections import defaultdict
import glob
import json


filepaths = []
for dirname, _, filenames in os.walk('datasets/mj/midjourney-texttoimage-new'):
    for filename in filenames:
        filepaths.append(os.path.join(dirname, filename))

COMPONENTS_FOR_INITIAL_AND_VARIATION = set(
    ['U1', 'U2', 'U3', 'U4', '⟳', 'V1', 'V2', 'V3', 'V4'])
COMPONENTS_FOR_UPSCALE = set(
    ['Make Variations', 'Upscale to Max', 'Light Upscale Redo'])


def get_message_type(message):
    """Figures out the message type based on the UI components displayed."""
    for components in message["components"]:
        for component in components["components"]:
            if component["label"] in COMPONENTS_FOR_INITIAL_AND_VARIATION:
                # For (very few) messages that are supposedly initial or variation requests, the content indicates
                # that they are actually upscale requests. We will just put these aside.
                if "Upscaled" in message["content"]:
                    return "INCONCLUSIVE"
                return "INITIAL_OR_VARIATION"
            elif component["label"] in COMPONENTS_FOR_UPSCALE:
                return "UPSCALE"
    return "TEXT_MESSAGE"


messages_by_type = defaultdict(list)
for filepath in filepaths:
    if os.path.splitext(filepath)[1] == '.json':
        with open(filepath, "r") as f:
            content = json.load(f)
            for single_message_list in content["messages"]:
                assert len(single_message_list) == 1
                message = single_message_list[0]
                message_type = get_message_type(message)
                messages_by_type[message_type].append(message)

print("Message counts:")
for mtype, messages in messages_by_type.items():
    print("\t", mtype, len(messages))

import re

def get_prompt(message):
    """Extracts the prompt from the message content, which is located between double stars."""
    content = message["content"]
    # Replace newlines with spaces; makes the regex below work.
    content = content.replace("\n", " ")
    # Find the text enclosed by two consecutive stars.
    BETWEEN_STARS = "\\*\\*(.*?)\\*\\*"
    match = re.search(BETWEEN_STARS, content)
    if match:
        return match.group()[2:-2]  # Exclude the stars.


def remove_urls(prompt):
    """Prompts can include both text and images; this method removes the prompt image URLs."""
    URL = "<https[^<]*>?\s"
    matches = re.findall(URL, prompt)
    for match in matches:
        prompt = prompt.replace(match, "")
    return prompt


def get_generated_image_url(message):
    """Extracts the URL of the generated image from the message."""
    attachments = message["attachments"]
    if len(attachments) == 1:
        return attachments[0]["url"]


from dataclasses import dataclass

@dataclass
class UserRequest:
    prompt: str
    generated_url: str


user_requests = []
for m in messages_by_type["UPSCALE"]:
    prompt = get_prompt(m)
    generated_url = get_generated_image_url(m)
    # In *very* rare cases, messages are malformed and these fields cannot be extracted.
    if prompt and generated_url:
        user_requests.append(UserRequest(prompt, generated_url))

num_messages = len(messages_by_type["UPSCALE"])
print(f"Parsed {len(user_requests)} user requests from {num_messages} messages.")



mj_data = {}
for num, ii in enumerate(user_requests):
    num_str = 'dalle/dalle{:07d}.jpg'.format(num)
    mj_data[num_str] = {'Prompt': ii.prompt,
                        'url': ii.generated_url}



with open("mj_up.json", "w") as f:
    json.dump(mj_data, f)
























