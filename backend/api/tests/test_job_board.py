from conferences.tests.factories import ConferenceFactory
from job_board.tests.factories import JobListingFactory
from pytest import mark

from helpers.tests import get_image_url_from_request
from i18n.strings import LazyI18nString


def _query_job_board(client, conference):
    return client.query(
        """
        query($conference: String!) {
            jobListings(conference: $conference) {
                id
                title
                slug
                description
                company
                companyLogo
                applyUrl
            }
        }
    """,
        variables={"conference": conference},
    )


@mark.django_db
def test_query_job_board(rf, graphql_client):
    listing = JobListingFactory()
    JobListingFactory(conference=ConferenceFactory())

    request = rf.get("/")

    resp = _query_job_board(graphql_client, conference=listing.conference.code)

    assert len(resp["data"]["jobListings"]) == 1

    assert {
        "id": str(listing.id),
        "title": str(listing.title),
        "slug": str(listing.slug),
        "description": str(listing.description),
        "company": str(listing.company),
        "companyLogo": get_image_url_from_request(request, listing.company_logo),
        "applyUrl": str(listing.apply_url),
    } == resp["data"]["jobListings"][0]


@mark.django_db
def test_query_single_job_listing(rf, graphql_client):
    listing = JobListingFactory(
        slug=LazyI18nString({"en": "demo", "it": "esempio"}),
        company_logo=None,
    )

    resp = graphql_client.query(
        """query {
            jobListing(slug: "demo") {
                id
                title
                slug
                description
                company
                companyLogo
                applyUrl
            }
        } """
    )

    assert {
        "id": str(listing.id),
        "title": str(listing.title),
        "slug": str(listing.slug),
        "description": str(listing.description),
        "company": str(listing.company),
        "companyLogo": None,
        "applyUrl": str(listing.apply_url),
    } == resp["data"]["jobListing"]

    resp = graphql_client.query(
        """query {
            jobListing(slug: "donut") {
                id
            }
        } """
    )

    assert resp["data"]["jobListing"] is None


@mark.django_db
def test_passing_language(graphql_client):
    JobListingFactory(
        title=LazyI18nString({"en": "this is a test", "it": "diventa una lumaca"}),
        slug=LazyI18nString({"en": "slug", "it": "lumaca"}),
    )

    resp = graphql_client.query(
        """query {
            jobListing(slug: "slug") {
                title(language: "it")
                slug(language: "it")
            }
        } """
    )

    assert not resp.get("errors")
    assert resp["data"]["jobListing"] == {
        "title": "diventa una lumaca",
        "slug": "lumaca",
    }
