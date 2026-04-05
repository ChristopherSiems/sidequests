import json
import os
import requests
from datetime import datetime

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"

_ENGAGE_PROMPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "questgiver_prompt.md")
with open(_ENGAGE_PROMPT_PATH, "r") as _f:
    _ENGAGE_SYSTEM_PROMPT = _f.read()

def test_connection():
    now = int(datetime.now().timestamp())
    test_event = json.dumps({
        "title": "International Coffee Hour",
        "description": "Join students from around the world for an informal gathering over coffee and light refreshments. All are welcome to attend and connect with the Clark community.",
        "host": "Clark University International Students Association",
        "start_time": now + 3600,
        "end_time": now + 7200,
    })
    payload = {
        "model": "qwen/qwen3-4b-2507",
        "messages": [
            {"role": "system", "content": _ENGAGE_SYSTEM_PROMPT},
            {"role": "user", "content": test_event},
        ],
        "max_tokens": 128,
    }
    try:
        resp = requests.post(LM_STUDIO_URL, json=payload, timeout=30)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"].strip()
        result_json = json.loads(content)
    except Exception as e:
        print(f"[llm_client] Warning: could not reach LM Studio model {e}")
        return False

    return True


def questify_post(post: dict, system_prompt: str = None) -> dict:
    """
    Send a post to the LM Studio questgiver prompt.
    Returns a copy of the post with 'title' replaced by quest_title
    and 'min_time' set to min_time_minutes.
    Falls back to original values on failure.
    """
    user_message = json.dumps({
        "title": post.get("title", ""),
        "description": post.get("description", ""),
        "host": post.get("host", ""),
        "start_time": post.get("start"),
        "end_time": post.get("end"),
    })

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_message})

    payload = {
        "model": "qwen/qwen3-4b-2507",
        "messages": messages,
        "max_tokens": 128,
    }

    print(f"[Questifier] Processing: {post.get('title', '')}")
    try:
        resp = requests.post(LM_STUDIO_URL, json=payload, timeout=30)
        if not resp.ok:
            print(f"[Questifier] {resp.status_code} error: {resp.text}")
            resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"].strip()
        result_json = json.loads(content)
    except Exception as e:
        print(f"[Questifier] Warning: could not questify '{post.get('title')}': {e}")
        return post

    result = dict(post)
    if result_json.get("quest_title"):
        result["title"] = result_json["quest_title"]
        print(f"[Questifier] -> {result['title']}")
    if result_json.get("time_category") is not None:
        result["time_category"] = result_json["time_category"]
    return result


def questify_posts(posts: list[dict], system_prompt: str = None) -> list[dict]:
    """Run questify_post on each post in the list."""
    return [questify_post(post, system_prompt=system_prompt) for post in posts]
