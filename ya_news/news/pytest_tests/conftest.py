from django.urls import reverse
from django.utils.timezone import now, timedelta

import pytest

from news.models import Comment, News
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.fixture
def news():
    return News.objects.create(title='Заголовок', text='Текст.')


@pytest.fixture
def news_id(news: News) -> tuple[int]:
    '''
    Фикстура возвращает кортеж из id новости,
    нужный для получения url-адреса.
    '''
    return news.id


@pytest.fixture
def detail_url(news_id):
    return reverse('news:detail', args=(news_id,))


@pytest.fixture
def bulk_news():
    today = now()
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
    return response.context['object_list']


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор комментария')


@pytest.fixture
def author_client(client, author):
    client.force_login(author)
    return client


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def zero_count():
    return Comment.objects.count()


@pytest.fixture
def initial_count(comment):
    return Comment.objects.count()


@pytest.fixture
def text():
    return 'Текст комментария'


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def two_comments(author, news):
    today = now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст комментария {index}'
        )
        comment.created = today + timedelta(days=index)
        comment.save()


@pytest.fixture
def form_data():
    return {'text': 'Текст комментария'}


@pytest.fixture
def new_form_data():
    return {'text': 'Новый текст комментария'}
