import json
import requests
from datetime import datetime

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"

def test_connection():
    payload = {
        "messages": [
            {"role": "user", "content": "{\n  \"title\": \"Are you online?\",\n  \"description\": \"Respond\",\n \"start_time\": 3000\n, \n  \"end_time\": 3000\n}"},
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


def questify_post(post: dict) -> dict:
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

    payload = {
        "messages": [
            {"role": "user", "content": user_message},
        ],
        "max_tokens": 128,
    }

    try:
        resp = requests.post(LM_STUDIO_URL, json=payload, timeout=30)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"].strip()
        result_json = json.loads(content)
    except Exception as e:
        print(f"[llm_client] Warning: could not questify '{post.get('title')}': {e}")
        return post

    result = dict(post)
    if result_json.get("quest_title"):
        result["title"] = result_json["quest_title"]
    if result_json.get("time_category") is not None:
        result["time_category"] = result_json["time_category"]
    return result


def questify_posts(posts: list[dict], model: str = None) -> list[dict]:
    """Run questify_post on each post in the list."""
    return [questify_post(post) for post in posts]
