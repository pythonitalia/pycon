import logging

from pycon.celery import app

logger = logging.getLogger(__name__)


@app.task
def compute_recap_analysis(conference_id, force_recompute=False):
    from django.core.cache import cache
    from django.db.models import Q

    from reviews.similar_talks import (
        _get_cache_key,
        compute_similar_talks,
        compute_topic_clusters,
    )
    from submissions.models import Submission

    accepted_submissions = list(
        Submission.objects.filter(conference_id=conference_id)
        .filter(
            Q(pending_status=Submission.STATUS.accepted)
            | Q(pending_status__isnull=True, status=Submission.STATUS.accepted)
            | Q(pending_status="", status=Submission.STATUS.accepted)
        )
        .select_related("speaker", "type", "audience_level")
        .prefetch_related("languages")
    )

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

    combined_cache_key = _get_cache_key(
        "recap_analysis", conference_id, accepted_submissions
    )
    cache.set(combined_cache_key, result, 60 * 60 * 24)

    return result
