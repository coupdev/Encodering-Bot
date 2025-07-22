import base64
import json
import os
from typing import Union

def encode_base64(text: str) -> str:
    return base64.b64encode(text.encode()).decode()

def decode_base64(b64: str) -> str:
    return base64.b64decode(b64.encode()).decode()

def store_access(encoded: str, user: Union[str, int]):
    if not os.path.exists("access.json"):
        with open("access.json", "w") as f:
            json.dump({}, f)
    with open("access.json", "r") as f:
        data = json.load(f)
    user = str(user)
    if encoded not in data:
        data[encoded] = [user]
    elif user not in data[encoded]:
        data[encoded].append(user)
    with open("access.json", "w") as f:
        json.dump(data, f, indent=2)

def get_user_lang(code: str) -> str:
    return "ru" if code.startswith("ru") else "en"
