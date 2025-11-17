# app/core/llm/prompt_to_messages.py
from typing import Dict


def convert_prompt_to_messages(prompt_dict: Dict) -> list:
    messages = []

    # system 메시지
    if "system" in prompt_dict:
        messages.append(("system", prompt_dict["system"]))

    # instruction 메시지
    if "instruction" in prompt_dict:
        if "{input}" in prompt_dict["instruction"]:
            messages.append(("user", prompt_dict["instruction"]))
        else:
            messages.append(("user", prompt_dict["instruction"] + "\n\n{input}"))

    # input 메시지
    if "input" in prompt_dict:
        messages.append(("user", prompt_dict["input"]))

    return messages
