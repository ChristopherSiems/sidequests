import numpy as np
from sklearn.neighbors import NearestNeighbors
from backend.database import get_global_interactions

def dynamic_user_weight(n_user_entries, base_weight=1.0, max_weight=4.0, growth_rate=0.1):

    return base_weight + (max_weight - base_weight) * (1 - np.exp(-growth_rate * n_user_entries))


def score_entry(new_embedding, interactions,user_embeddings, 
                user_weight=2.0, other_weight=1.0, k=5):
    user_accepted_embeddings = [e for e in user_embeddings if e.score > 0]
    user_rejected_embeddings = [e for e in user_embeddings if e.score < 0]
    other_accepted_embeddings = [embedding for embedding in interactions if embedding["score"] > 0 and embedding["embedding"] != new_embedding]
    other_rejected_embeddings = [embedding for embedding in interactions if embedding["score"] < 0 and embedding["embedding"] != new_embedding]
    
    def get_avg_distance(new_emb, reference_embeddings, k):
        if reference_embeddings is None or len(reference_embeddings) == 0:
            return 0.0
        if not new_emb or len(new_emb) == 0:
            return 0.0
        d = len(new_emb)
        vecs = [
            v for v in reference_embeddings
            if v is not None and len(v) == d
        ]
        if len(vecs) == 0:
            return 0.0
        X = np.asarray(vecs, dtype=np.float64)
        if X.ndim != 2 or X.shape[0] == 0 or X.shape[1] == 0:
            return 0.0
        k_actual = min(k, X.shape[0])
        knn = NearestNeighbors(n_neighbors=k_actual, metric='cosine')
        knn.fit(X)
        distances, _ = knn.kneighbors(np.asarray(new_emb, dtype=np.float64).reshape(1, -1))
        avg_similarity = 1 - np.mean(distances)
        return avg_similarity
    
    user_weight = dynamic_user_weight(len(user_accepted_embeddings))
    user_accept_score  = get_avg_distance(new_embedding, [e.embedding for e in user_accepted_embeddings], k) * user_weight
    user_reject_score  = get_avg_distance(new_embedding, [e.embedding for e in user_rejected_embeddings], k) * user_weight

    other_accept_score = get_avg_distance(new_embedding, [e["embedding"] for e in other_accepted_embeddings], k) 
    other_reject_score = get_avg_distance(new_embedding, [e["embedding"] for e in other_rejected_embeddings], k) 
    
    score = (user_accept_score + other_accept_score) - (user_reject_score + other_reject_score) * 0.5
    
    return score

def get_best_quest(quests, embedding_history):
    interactions = get_global_interactions()
    seen = [e.embedding for e in embedding_history]
    best_quest = None
    best_score = 0
    print("quests", len(quests))
    for quest in quests:
        if quest["embedding"] in seen or quest["embedding"] == []:
            continue

        score = score_entry(quest["embedding"], interactions, embedding_history)
        if score >= best_score:
            best_score = score
            best_quest = quest

    if best_quest is None and quests:
        for q in quests:
            emb = q["embedding"]
            if emb and emb not in seen:
                return q
        for q in quests:
            if q["embedding"] not in seen:
                return q
        return quests[0]
    return best_quest

