from strawberry.tools import create_type

import strawberry
from api.page.queries.cms_page import cms_page
from api.page.queries.cms_pages import cms_pages
from api.news.queries.news_articles import news_articles
from api.news.queries.news_article import news_article

Query = create_type("Query", fields=[cms_page, cms_pages, news_articles, news_article])
schema = strawberry.federation.Schema(query=Query)
