import ollama

DEFAULT_EMBEDDING_MODEL = "nomic-embed-text"

def get_embedding(text: str, model: str = DEFAULT_EMBEDDING_MODEL) -> list[float]:
    if not text.strip():
        return []
        
    try:
        response = ollama.embeddings(model=model, prompt=text)
        return response.get('embedding', [])
    except Exception as e:
        print(f"[Embedder] Error generating embedding: {e}")
        return []

def attach_embeddings_to_quests(quests: list[dict], model: str = DEFAULT_EMBEDDING_MODEL) -> list[dict]:
    for quest in quests:
        title = quest.get("title", "")
        desc = quest.get("description", "")
        
        raw_cats = quest.get("categories", [])
        cats = ", ".join(raw_cats) if isinstance(raw_cats, list) else raw_cats
        
        text_to_embed = f"Title: {title}\nCategories: {cats}\nDescription: {desc}"
        
        print(f"[Embedder] Generating embedding for: {title}")
        quest["embedding"] = get_embedding(text_to_embed, model)
        
    return quests
