import hashlib


def get_embedding_text(submission) -> str:
    """Combine title, elevator_pitch, and abstract into a single string for embedding."""
    title = str(submission.title) if submission.title else ""
    elevator_pitch = str(submission.elevator_pitch) if submission.elevator_pitch else ""
    abstract = (
        str(submission.abstract)
        if hasattr(submission, "abstract") and submission.abstract
        else ""
    )
    return f"{title}. {elevator_pitch}. {abstract}"


def get_cache_key(prefix: str, conference_id: int, submissions) -> str:
    """Generate a cache key based on conference and submission content."""
    content_hash = hashlib.md5()
    for s in sorted(submissions, key=lambda x: x.id):
        content_hash.update(f"{s.id}:{get_embedding_text(s)}".encode())
    return f"{prefix}:conf_{conference_id}:{content_hash.hexdigest()}"
