import requests

LM_STUDIO_EMBEDDINGS_URL = "http://127.0.0.1:1234/v1/embeddings"

def get_embedding(text: str) -> list[float]:
    if not text.strip():
        return []
    try:
        resp = requests.post(
            LM_STUDIO_EMBEDDINGS_URL,
            json={"model": "text-embedding-nomic-embed-text-v1.5@q8_0", "input": text},
            timeout=30,
        )
        if not resp.ok:
            print(f"[Embedder] {resp.status_code} error: {resp.text}")
            resp.raise_for_status()
        return resp.json()["data"][0]["embedding"]
    except Exception as e:
        print(f"[Embedder] Error generating embedding: {e}")
        return []

def attach_embeddings_to_quests(quests: list[dict]) -> list[dict]:
    for quest in quests:
        title = quest.get("title", "")
        if title == "N/A":
            continue
        desc = quest.get("description", "")
        raw_cats = quest.get("categories", [])
        cats = ", ".join(raw_cats) if isinstance(raw_cats, list) else raw_cats
        text_to_embed = f"Title: {title}\nCategories: {cats}\nDescription: {desc}"
        print(f"[Embedder] Generating embedding for: {title}")
        quest["embedding"] = get_embedding(text_to_embed)
    return quests
