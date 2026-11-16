from strawberry.tools import create_type

from api.reviews.mutations.vote_proposal import vote_proposal
from api.reviews.queries.next_proposal_to_review import next_proposal_to_review
from api.reviews.queries.review_proposal import review_proposal
from api.reviews.queries.review_session import review_session

ReviewsQuery = create_type(
    "ReviewsQuery",
    [review_session, review_proposal, next_proposal_to_review],
)

ReviewsMutations = create_type("ReviewsMutations", [vote_proposal])
