from pytest import mark
from datetime import timedelta

from django.utils import timezone

from blog.models import Post
from users.models import User

def _query_blog_posts(client):
    return client.query("""
        query{
            blogPosts {
                id
                title
                slug
                excerpt
                content
                published
                image
                author{
                    id
                    email
                }
            }
        }
    """)

@mark.django_db
def test_query_blog_posts(graphql_client,user_factory,post_factory):
    now = timezone.now()
    past_post = post_factory(
        published=timezone.now()-timedelta(days=1),
        image=None)
    present_post = post_factory()
    future_post = post_factory(published=timezone.now()+timedelta(days=1))
    
    resp = _query_blog_posts(graphql_client)

    assert len(resp['data']['blogPosts']) == 2

    assert {
        'id' : str(past_post.id),
        'title' : past_post.title,
        'slug' : past_post.slug,
        'excerpt' : past_post.excerpt,
        'content' : past_post.content,
        'published' : past_post.published.isoformat(),
        'image' : str(past_post.image),
        'author' : {
            'id' : str(past_post.author.id),
            'email' : past_post.author.email,
        }
    } == resp['data']['blogPosts'][1]

    assert {
        'id' : str(present_post.id),
        'title' : present_post.title,
        'slug' : present_post.slug,
        'excerpt' : present_post.excerpt,
        'content' : present_post.content,
        'published' : present_post.published.isoformat(),
        'image' : str(present_post.image),
        'author' : {
            'id' : str(present_post.author.id),
            'email' : present_post.author.email,
        }
    } == resp['data']['blogPosts'][0]





