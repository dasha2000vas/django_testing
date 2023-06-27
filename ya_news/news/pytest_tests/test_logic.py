from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, form_data, detail_url):
    client.post(detail_url, data=form_data)
    comment_count = Comment.objects.count()
    assert comment_count == 0


def test_user_can_create_comment(
    admin_client, form_data, detail_url, admin_user, news
):
    admin_client.post(detail_url, data=form_data)
    comment_count = Comment.objects.count()
    assert comment_count == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == admin_user


def test_user_cant_use_bad_words(admin_client, detail_url):
    bad_words_data = {'text': f'Текст, {BAD_WORDS[0]}, еще текст'}
    response = admin_client.post(detail_url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING,
    )
    comment_count = Comment.objects.count()
    assert comment_count == 0


def test_author_can_delete_comment(author_client, delete_url, detail_url):
    url_to_comments = detail_url + '#comments'
    response = author_client.post(delete_url)
    assertRedirects(response, url_to_comments)
    comment_count = Comment.objects.count()
    assert comment_count == 0


def test_user_cant_delete_comment_of_another_user(admin_client, delete_url):
    response = admin_client.post(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_count = Comment.objects.count()
    assert comment_count == 1


def test_author_can_edit_comment(
    author_client, edit_url, new_form_data, detail_url, comment
):
    response = author_client.post(edit_url, data=new_form_data)
    url_to_comments = detail_url + '#comments'
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == new_form_data['text']


def test_user_cant_edit_comment_of_another_user(
    admin_client, edit_url, new_form_data, comment, text
):
    response = admin_client.post(edit_url, data=new_form_data,)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == text
