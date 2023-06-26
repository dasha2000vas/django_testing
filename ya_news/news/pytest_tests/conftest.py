from datetime import datetime, timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.fixture
def news():
    news = News.objects.create(title='Заголовок', text='Текст.')
    return news


@pytest.fixture
def news_id(news):
    return news.id,


@pytest.fixture
def detail_url(news_id):
    url = reverse('news:detail', args=news_id)
    return url


@pytest.fixture
def bulk_news():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Текст.',
            date=today - timedelta(days=index)
        )
        for index in range(NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    return News.objects.bulk_create(all_news)


@pytest.fixture
def home_page_object_list(client, bulk_news):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    return object_list


@pytest.fixture
def author(django_user_model):
    author = django_user_model.objects.create(username='Автор комментария')
    return author


@pytest.fixture
def author_client(client, author):
    client.force_login(author)
    return client


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def text():
    return 'Текст комментария'


@pytest.fixture
def delete_url(comment):
    url = reverse('news:delete', args=(comment.id,))
    return url


@pytest.fixture
def edit_url(comment):
    url = reverse('news:edit', args=(comment.id,))
    return url


@pytest.fixture
def two_comments(author, news):
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст комментария {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def form_data():
    return {'text': 'Текст комментария'}


@pytest.fixture
def new_form_data():
    return {'text': 'Новый текст комментария'}
