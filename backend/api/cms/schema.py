from strawberry.tools import create_type

from api.cms.page.queries.cms_page import cms_page
from api.cms.page.queries.cms_pages import cms_pages
from api.cms.news.queries.news_articles import news_articles
from api.cms.news.queries.news_article import news_article

CMSQuery = create_type(
    "CMSQuery", fields=[cms_page, cms_pages, news_articles, news_article]
)
