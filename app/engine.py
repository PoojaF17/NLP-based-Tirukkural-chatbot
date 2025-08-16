\
from typing import List, Dict, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .indexer import load_index
from .utils import clean_tamil_text, starts_with_words

vectorizer, matrix, df = load_index()

def _format_kural_row(row) -> Dict:
    return {
        "kural_number": int(row["KuralNumber"]),
        "tamil": row["Verse"],
        "translation": row["Translation"],
        "explanation": row.get("Explanation", ""),
        "chapter": row.get("Chapter Name", ""),
        "section": row.get("Section Name", ""),
    }

def lookup_by_number(num: int) -> Dict:
    if num < 1 or num > len(df):
        raise ValueError(f"Kural number must be between 1 and {len(df)}")
    row = df.iloc[num - 1]
    return _format_kural_row(row)

def lookup_by_prefix(prefix: str, top_k: int = 5) -> List[Dict]:
    prefix = clean_tamil_text(prefix)
    matches = []
    for _, row in df.iterrows():
        if starts_with_words(row["Verse"], prefix):
            matches.append(_format_kural_row(row))
        if len(matches) >= top_k:
            break
    return matches

def search_semantic(query: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
    q_vec = vectorizer.transform([query])
    sims = cosine_similarity(q_vec, matrix)[0]
    top_idx = np.argsort(-sims)[:top_k]
    results = []
    for i in top_idx:
        row = df.iloc[i]
        results.append((_format_kural_row(row), float(sims[i])))
    return results

def lookup_by_theme(theme: str, top_k: int = 5) -> List[Dict]:
    hits = search_semantic(theme, top_k=top_k)
    return [h[0] for h in hits]

def top_k_for_query(query: str, top_k: int = 5) -> List[Dict]:
    hits = search_semantic(query, top_k=top_k)
    return [h[0] for h in hits]
