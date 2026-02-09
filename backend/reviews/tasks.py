import logging

from pycon.celery import app

logger = logging.getLogger(__name__)


@app.task
def compute_recap_analysis(conference_id, force_recompute=False):
    from django.core.cache import cache

    from reviews.admin import get_accepted_submissions
    from reviews.similar_talks import (
        _get_cache_key,
        compute_similar_talks,
        compute_topic_clusters,
    )

    from conferences.models import Conference

    conference = Conference.objects.get(id=conference_id)
    accepted_submissions = list(get_accepted_submissions(conference))

    combined_cache_key = _get_cache_key(
        "recap_analysis", conference_id, accepted_submissions
    )

    try:
        similar_talks = compute_similar_talks(
            accepted_submissions,
            top_n=5,
            conference_id=conference_id,
            force_recompute=force_recompute,
        )

        topic_clusters = compute_topic_clusters(
            accepted_submissions,
            min_topic_size=3,
            conference_id=conference_id,
            force_recompute=force_recompute,
        )

        submissions_list = sorted(
            [
                {
                    "id": s.id,
                    "title": str(s.title),
                    "type": s.type.name,
                    "speaker": s.speaker.display_name if s.speaker else "Unknown",
                    "similar": similar_talks.get(s.id, []),
                }
                for s in accepted_submissions
            ],
            key=lambda x: max(
                (item["similarity"] for item in x["similar"]), default=0
            ),
            reverse=True,
        )

        result = {
            "submissions_list": submissions_list,
            "topic_clusters": topic_clusters,
        }

        cache.set(combined_cache_key, result, 60 * 60 * 24)

        return result
    except Exception:
        logger.exception(
            "Failed to compute recap analysis for conference %s", conference_id
        )
        cache.set(
            combined_cache_key,
            {"status": "error", "message": "Analysis failed. Please try again."},
            60 * 5,
        )
        raise
