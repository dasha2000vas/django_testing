import pytest
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_count(home_page_object_list):
    news_count = len(home_page_object_list)
    assert news_count == NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(home_page_object_list):
    all_dates = [news.date for news in home_page_object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, two_comments, detail_url):
    response = client.get(detail_url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, detail_url):
    response = client.get(detail_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(admin_client, detail_url):
    response = admin_client.get(detail_url)
    assert 'form' in response.context
