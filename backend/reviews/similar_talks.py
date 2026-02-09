import functools
import hashlib
import logging

import nltk
import numpy as np
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired, MaximalMarginalRelevance
from django.core.cache import cache
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

CACHE_TIMEOUT = 60 * 60 * 24  # 24 hours


# Map language codes to NLTK stopword language names
LANGUAGE_CODE_MAP = {
    "en": "english",
    "it": "italian",
}

# Conference-specific stopwords (language-agnostic technical terms)
CONFERENCE_STOPWORDS = {
    # Generic talk terms
    "talk",
    "talks",
    "session",
    "presentation",
    "workshop",
    "tutorial",
    "introduction",
    "intro",
    "advanced",
    "beginner",
    "intermediate",
    "guide",
    "overview",
    "deep",
    "dive",
    "hands",
    "practical",
    "real",
    "world",
    "quick",
    "lightning",
    # Common verbs
    "using",
    "use",
    "uses",
    "build",
    "building",
    "create",
    "creating",
    "make",
    "making",
    "learn",
    "learning",
    "get",
    "getting",
    "started",
    "start",
    "work",
    "working",
    "write",
    "writing",
    "run",
    "running",
    "develop",
    "developing",
    "development",
    "implement",
    "implementing",
    "implementation",
    # Common adjectives
    "new",
    "modern",
    "better",
    "best",
    "simple",
    "easy",
    "fast",
    "faster",
    "efficient",
    "effective",
    "powerful",
    "complex",
    "basic",
    "basics",
    # Generic terms
    "practices",
    "way",
    "ways",
    "approach",
    "approaches",
    "pattern",
    "patterns",
    "example",
    "examples",
    "case",
    "cases",
    "study",
    "code",
    "codes",
    "coding",
    "project",
    "projects",
    "application",
    "applications",
    "app",
    "apps",
    "system",
    "systems",
    "tool",
    "tools",
    "solution",
    "solutions",
    "feature",
    "features",
    "technique",
    "techniques",
    "method",
    "methods",
    "trick",
    "tricks",
    "tip",
    "tips",
    "lesson",
    "lessons",
    "learned",
    "experience",
    "experiences",
    "journey",
    "story",
    "stories",
    # Python-specific (since this is a Python conference)
    "python",
    "python's",
    "py",
    "pythonic",
    "cpython",
    "pypi",
    # Generic programming terms
    "library",
    "libraries",
    "package",
    "packages",
    "module",
    "modules",
    "framework",
    "frameworks",
    "function",
    "functions",
    "class",
    "classes",
    "object",
    "objects",
    "variable",
    "variables",
    "data",
    "file",
    "files",
    "script",
    "scripts",
    "program",
    "programs",
    "programming",
    "developer",
    "developers",
    "software",
    "hardware",
    "user",
    "users",
}


@functools.cache
def _ensure_nltk_data():
    """Download NLTK stopwords if not already present."""
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        logger.info("Downloading NLTK stopwords...")
        nltk.download("stopwords", quiet=True)


def get_stopwords_for_languages(language_codes: set[str]) -> set[str]:
    """
    Get combined stopwords for the given language codes using NLTK.

    Args:
        language_codes: Set of 2-letter language codes (e.g., {"en", "it"})

    Returns:
        Set of stopwords for all specified languages
    """
    _ensure_nltk_data()

    stopwords = set()

    for code in language_codes:
        lang_name = LANGUAGE_CODE_MAP.get(code.lower())
        if lang_name:
            try:
                lang_stopwords = set(nltk.corpus.stopwords.words(lang_name))
                stopwords.update(lang_stopwords)
            except OSError:
                logger.warning(f"Stopwords not available for language: {lang_name}")

    # Always add conference-specific stopwords
    stopwords.update(CONFERENCE_STOPWORDS)

    return stopwords


@functools.cache
def get_embedding_model():
    """Get or create the shared embedding model instance."""
    return SentenceTransformer("all-MiniLM-L6-v2")


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


def _get_submission_languages(submissions) -> set[str]:
    """Extract all unique language codes from submissions."""
    language_codes = set()

    for submission in submissions:
        for lang in submission.languages.all():
            language_codes.add(lang.code.lower())

    return language_codes or {"en"}


def _get_cache_key(prefix: str, conference_id: int, submissions) -> str:
    """Generate a cache key based on conference and submission content."""
    content_hash = hashlib.md5()
    for s in sorted(submissions, key=lambda x: x.id):
        content_hash.update(f"{s.id}:{get_embedding_text(s)}".encode())
    return f"{prefix}:conf_{conference_id}:{content_hash.hexdigest()}"


def compute_similar_talks(
    submissions, top_n=5, conference_id=None, force_recompute=False
):
    """
    Compute similar talks for each submission based on embeddings.

    Args:
        submissions: A list of Submission objects
        top_n: Number of similar talks to return for each submission
        conference_id: Optional conference ID for cache key
        force_recompute: Skip cache and recompute fresh results

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
        cache_key = _get_cache_key("similar_talks", conference_id, submissions_list)
        if not force_recompute:
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

    model = get_embedding_model()

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


def compute_topic_clusters(
    submissions, min_topic_size=3, conference_id=None, force_recompute=False
):
    """
    Compute topic clusters for submissions using BERTopic.

    Args:
        submissions: A list of Submission objects
        min_topic_size: Minimum number of talks per cluster
        conference_id: Optional conference ID for cache key
        force_recompute: Skip cache and recompute fresh results

    Returns:
        A dictionary with:
        - 'topics': list of topic info dicts with id, name, count, keywords
        - 'submission_topics': dict mapping submission ID to topic ID
    """
    if not submissions:
        return {"topics": [], "submission_topics": {}, "outliers": []}

    submissions_list = list(submissions)
    if len(submissions_list) < min_topic_size:
        return {"topics": [], "submission_topics": {}, "outliers": []}

    # Try to get from cache
    cache_key = None
    if conference_id:
        cache_key = _get_cache_key("topic_clusters_v4", conference_id, submissions_list)
        if not force_recompute:
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

    model = get_embedding_model()
    texts = [get_embedding_text(s) for s in submissions_list]
    embeddings = model.encode(texts)

    # Get stopwords based on submission languages
    language_codes = _get_submission_languages(submissions_list)
    stopwords = get_stopwords_for_languages(language_codes)
    stopwords_list = list(stopwords)

    # Calculate number of clusters based on submission count
    # Aim for ~5-8 talks per cluster on average
    n_clusters = max(2, min(15, len(submissions_list) // 6))

    # Use Agglomerative Clustering for more predictable results
    cluster_model = AgglomerativeClustering(n_clusters=n_clusters)

    # Custom vectorizer with language-aware stopwords
    vectorizer_model = CountVectorizer(
        stop_words=stopwords_list,
        min_df=1,
        ngram_range=(1, 2),
    )

    # Use KeyBERT-inspired representation for better keywords
    representation_model = [
        KeyBERTInspired(),
        MaximalMarginalRelevance(diversity=0.3),
    ]

    # Create and fit BERTopic model
    topic_model = BERTopic(
        embedding_model=model,
        hdbscan_model=cluster_model,
        vectorizer_model=vectorizer_model,
        representation_model=representation_model,
        verbose=False,
        calculate_probabilities=False,
    )

    topics, _probs = topic_model.fit_transform(texts, embeddings)

    # Get topic info
    topic_info = topic_model.get_topic_info()

    # Build topics list
    topics_list = []
    for _, row in topic_info.iterrows():
        topic_id = row["Topic"]
        if topic_id == -1:
            continue  # Skip outliers

        # Get top keywords for this topic (from KeyBERT representation)
        topic_words = topic_model.get_topic(topic_id)
        keywords = []
        if topic_words:
            for word, _ in topic_words[:10]:  # Check more words to find unique ones
                # Clean up the keyword
                word = word.strip().lower()

                # Skip if in stopwords or too short
                if not word or word in stopwords or len(word) < 3:
                    continue

                # Skip if this word is a substring of an existing keyword or vice versa
                # e.g., "interpreter" and "interpreter explore" → keep only "interpreter"
                is_duplicate = False
                for existing in keywords:
                    if word in existing or existing in word:
                        is_duplicate = True
                        break
                    # Also check for very similar words (same stem)
                    if len(word) > 4 and len(existing) > 4:
                        if word[:4] == existing[:4]:
                            is_duplicate = True
                            break

                if not is_duplicate:
                    keywords.append(word)

                if len(keywords) >= 5:
                    break

        # Generate a better topic name from top keywords
        if keywords:
            # Use only the most distinctive keywords for the name
            topic_name = " / ".join(keywords[:3]).title()
        else:
            topic_name = f"Topic {topic_id + 1}"

        topics_list.append(
            {
                "id": topic_id,
                "name": topic_name,
                "count": row["Count"],
                "keywords": keywords,
            }
        )

    # Map submission IDs to topics
    submission_topics = {}
    for i, submission in enumerate(submissions_list):
        topic_id = topics[i]
        submission_topics[submission.id] = topic_id

    # Group submissions by topic
    topics_with_submissions = []
    for topic in sorted(topics_list, key=lambda t: t["count"], reverse=True):
        topic_submissions = [
            {"id": s.id, "title": str(s.title)}
            for s in submissions_list
            if submission_topics.get(s.id) == topic["id"]
        ]
        topics_with_submissions.append({**topic, "submissions": topic_submissions})

    # Handle outliers (topic -1)
    outlier_submissions = [
        {"id": s.id, "title": str(s.title)}
        for s in submissions_list
        if submission_topics.get(s.id) == -1
    ]

    result = {
        "topics": topics_with_submissions,
        "outliers": outlier_submissions,
        "submission_topics": submission_topics,
    }

    # Cache the result
    if cache_key:
        cache.set(cache_key, result, CACHE_TIMEOUT)

    return result
