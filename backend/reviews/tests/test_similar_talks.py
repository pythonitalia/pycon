from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from reviews.similar_talks import (
    compute_similar_talks,
    compute_topic_clusters,
)


def _make_submission(id, title="Test Talk", elevator_pitch="A pitch", abstract="Abstract"):
    """Create a mock submission object."""
    sub = MagicMock()
    sub.id = id
    sub.title = title
    sub.elevator_pitch = elevator_pitch
    sub.abstract = abstract
    sub.languages.all.return_value = []
    return sub


@patch("reviews.similar_talks.get_embedding_model")
@patch("reviews.similar_talks.cache")
class TestComputeSimilarTalks:
    def test_empty_submissions(self, mock_cache, mock_model):
        result = compute_similar_talks([], top_n=5)
        assert result == {}
        mock_model.assert_not_called()

    def test_single_submission(self, mock_cache, mock_model):
        sub = _make_submission(1)
        result = compute_similar_talks([sub], top_n=5)
        assert result == {}
        mock_model.assert_not_called()

    def test_returns_similar_talks(self, mock_cache, mock_model):
        mock_cache.get.return_value = None

        embeddings = np.array([
            [1.0, 0.0, 0.0],
            [0.9, 0.1, 0.0],
            [0.0, 0.0, 1.0],
        ])
        mock_model.return_value.encode.return_value = embeddings

        subs = [
            _make_submission(1, title="Talk A"),
            _make_submission(2, title="Talk B"),
            _make_submission(3, title="Talk C"),
        ]

        result = compute_similar_talks(subs, top_n=2, conference_id=1)

        assert 1 in result
        assert 2 in result
        assert 3 in result

        # Talk A and Talk B should be most similar to each other
        similar_to_a = result[1]
        assert similar_to_a[0]["id"] == 2

    def test_uses_cache(self, mock_cache, mock_model):
        cached = {1: [{"id": 2, "title": "Cached", "similarity": 80.0}]}
        mock_cache.get.return_value = cached

        subs = [_make_submission(1), _make_submission(2)]
        result = compute_similar_talks(subs, top_n=5, conference_id=1)

        assert result == cached
        mock_model.return_value.encode.assert_not_called()

    def test_force_recompute_skips_cache(self, mock_cache, mock_model):
        mock_cache.get.return_value = None

        embeddings = np.array([[1.0, 0.0], [0.0, 1.0]])
        mock_model.return_value.encode.return_value = embeddings

        subs = [_make_submission(1), _make_submission(2)]
        compute_similar_talks(subs, top_n=5, conference_id=1, force_recompute=True)

        mock_cache.get.assert_not_called()
        mock_model.return_value.encode.assert_called_once()
        mock_cache.set.assert_called_once()


@patch("reviews.similar_talks.get_embedding_model")
@patch("reviews.similar_talks.cache")
class TestComputeTopicClusters:
    def test_empty_submissions(self, mock_cache, mock_model):
        result = compute_topic_clusters([])
        assert result == {"topics": [], "submission_topics": {}, "outliers": []}
        mock_model.assert_not_called()

    def test_too_few_submissions(self, mock_cache, mock_model):
        subs = [_make_submission(1), _make_submission(2)]
        result = compute_topic_clusters(subs, min_topic_size=3)
        assert result == {"topics": [], "submission_topics": {}, "outliers": []}
        mock_model.assert_not_called()

    def test_uses_cache(self, mock_cache, mock_model):
        cached = {"topics": [{"name": "Cached"}], "outliers": [], "submission_topics": {}}
        mock_cache.get.return_value = cached

        subs = [_make_submission(i) for i in range(5)]
        result = compute_topic_clusters(subs, min_topic_size=3, conference_id=1)

        assert result == cached
        mock_model.return_value.encode.assert_not_called()

    def test_force_recompute_skips_cache(self, mock_cache, mock_model):
        mock_cache.get.return_value = None

        embeddings = np.random.rand(5, 10)
        mock_model.return_value.encode.return_value = embeddings

        subs = [_make_submission(i, title=f"Talk {i}") for i in range(5)]

        with patch("reviews.similar_talks.BERTopic") as mock_bertopic:
            mock_topic_model = MagicMock()
            mock_bertopic.return_value = mock_topic_model
            mock_topic_model.fit_transform.return_value = ([0, 0, 1, 1, -1], None)
            mock_topic_model.get_topic_info.return_value = MagicMock(
                iterrows=lambda: iter([])
            )
            mock_topic_model.get_topic.return_value = []

            compute_topic_clusters(
                subs, min_topic_size=3, conference_id=1, force_recompute=True
            )

        mock_cache.get.assert_not_called()
        mock_model.return_value.encode.assert_called_once()
        mock_cache.set.assert_called_once()
