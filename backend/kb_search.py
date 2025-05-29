import json
from sentence_transformers import SentenceTransformer, util
'''
def search_kb(query: str):
    with open("knowledge_base.json") as f:
        kb = json.load(f)
    for topic, answer in kb.items():
        if topic.lower() in query.lower():
            return answer
    return "not found"
'''
model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_search(query: str, threshold: float = 0.7):
    with open("knowledge_base.json") as f:
        kb = json.load(f)

    combined_entries = [f"{k}" for k, v in kb.items()]
    entry_embeddings = model.encode(combined_entries, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)

    # Compute cosine similarity scores
    scores = util.pytorch_cos_sim(query_embedding, entry_embeddings)[0]
    best_score = scores.max().item()
    best_match_idx = scores.argmax().item()

    if best_score >= threshold:
        best_topic = list(kb.keys())[best_match_idx]
        return {
            "escalate": False,
            "topic": best_topic,
            "response": kb[best_topic],
            "match_score": best_score
        }
    else:
        return {
            "escalate": True,
            "response": "We're escalating your query to a human agent for further assistance.",
            "match_score": best_score
        }