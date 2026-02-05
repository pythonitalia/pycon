import hashlib

import numpy as np
from django.core.cache import cache
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

CACHE_TIMEOUT = 60 * 60 * 24  # 24 hours


def get_embedding_text(submission) -> str:
    """Combine title and elevator_pitch into a single string for embedding."""
    title = str(submission.title) if submission.title else ""
    elevator_pitch = str(submission.elevator_pitch) if submission.elevator_pitch else ""
    return f"{title}. {elevator_pitch}"


def _get_cache_key(conference_id: int, submissions) -> str:
    """Generate a cache key based on conference and submission content."""
    content_hash = hashlib.md5()
    for s in sorted(submissions, key=lambda x: x.id):
        content_hash.update(f"{s.id}:{get_embedding_text(s)}".encode())
    return f"similar_talks:conf_{conference_id}:{content_hash.hexdigest()}"


def compute_similar_talks(submissions, top_n=5, conference_id=None):
    """
    Compute similar talks for each submission based on embeddings.

    Args:
        submissions: A list of Submission objects
        top_n: Number of similar talks to return for each submission
        conference_id: Optional conference ID for cache key

    Returns:
        A dictionary mapping submission IDs to lists of similar submission IDs
    """
    if not submissions:
        return {}

    submissions_list = list(submissions)
    if len(submissions_list) < 2:
        return {}

    # Try to get from cache
    cache_key = None
    if conference_id:
        cache_key = _get_cache_key(conference_id, submissions_list)
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result

    model = SentenceTransformer("all-MiniLM-L6-v2")

    texts = [get_embedding_text(s) for s in submissions_list]
    embeddings = model.encode(texts)

    similarity_matrix = cosine_similarity(embeddings)

    similar_talks = {}
    for i, submission in enumerate(submissions_list):
        sims = similarity_matrix[i]
        top_indices = np.argsort(sims)[::-1][1 : top_n + 1]  # skip self (index 0)

        similar_talks[submission.id] = [
            {
                "id": submissions_list[idx].id,
                "title": str(submissions_list[idx].title),
                "similarity": round(float(sims[idx]) * 100, 1),
            }
            for idx in top_indices
            if sims[idx] > 0.3  # Only include if similarity > 30%
        ]

    # Cache the result
    if cache_key:
        cache.set(cache_key, similar_talks, CACHE_TIMEOUT)

    return similar_talks
