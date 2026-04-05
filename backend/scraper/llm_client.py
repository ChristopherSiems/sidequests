import json
import requests
from datetime import datetime

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"

def _build_user_message(post: dict) -> str:
    start = datetime.fromtimestamp(post["start"]).strftime("%A, %B %d at %I:%M %p") if post.get("start") else "unknown"
    end   = datetime.fromtimestamp(post["end"]).strftime("%I:%M %p") if post.get("end") else "unknown"

    lines = [
        f'Title: {post.get("title", "")}',
        f'Time: {start} – {end}',
        f'Location: {post.get("location") or "unspecified"}',
    ]
    if post.get("description"):
        lines.append(f'Existing description: {post["description"]}')
    if post.get("categories"):
        lines.append(f'Existing categories: {post["categories"]}')

    return "\n".join(lines)


def enrich_post(post: dict, model: str = None) -> dict:
    """
    Send a post dict to LM Studio and return a copy with 'description'
    and 'categories' filled in (or improved) by the LLM.

    Falls back to the original values if the request fails or the
    response can't be parsed.
    """
    payload = {
        "messages": [
            {"role": "user", "content": _build_user_message(post)},
        ],
        "temperature": 0.4,
        "max_tokens": 256,
    }
    if model:
        payload["model"] = model

    try:
        resp = requests.post(LM_STUDIO_URL, json=payload, timeout=30)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"].strip()
        enriched = json.loads(content)
    except Exception as e:
        print(f"[llm_client] Warning: could not enrich '{post.get('title')}': {e}")
        return post

    result = dict(post)
    if enriched.get("description"):
        result["description"] = enriched["description"]
    if enriched.get("categories"):
        result["categories"] = enriched["categories"]
    return result


def enrich_posts(posts: list[dict], model: str = None) -> list[dict]:
    """Enrich a list of posts, skipping any that already have both fields."""
    enriched = []
    for post in posts:
        needs_description = not post.get("description")
        needs_categories  = not post.get("categories")
        if needs_description or needs_categories:
            post = enrich_post(post, model=model)
        enriched.append(post)
    return enriched
