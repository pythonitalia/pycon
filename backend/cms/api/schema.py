from cms.api.page.queries.page_preview import page_preview
from strawberry.tools import create_type

from cms.api.page.queries.cms_page import cms_page
from cms.api.page.queries.cms_pages import cms_pages
from cms.api.news.queries.news_articles import news_articles
from cms.api.news.queries.news_article import news_article

CMSQuery = create_type(
    "CMSQuery", fields=[cms_page, cms_pages, news_articles, news_article, page_preview]
)
