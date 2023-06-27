from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRouts(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.another_author = User.objects.create(username='Другой автор')
        cls.note = Note.objects.create(
            title='Заметка',
            text='Текст',
            author=cls.author
        )
        cls.urls_for_notes = (
            ('notes:add', None),
            ('notes:detail', (cls.note.slug,)),
            ('notes:edit', (cls.note.slug,)),
            ('notes:delete', (cls.note.slug,)),
            ('notes:list', None),
            ('notes:success', None)
        )

    def test_pages_availability(self):
        urls = ('notes:home', 'users:signup', 'users:login', 'users:logout')
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_notes(self):
        for name, args in self.urls_for_notes:
            self.client.force_login(self.author)
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unavailability_notes_for_other_users(self):
        urls = self.urls_for_notes[1:4]
        for name, args in urls:
            self.client.force_login(self.another_author)
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        for name, args in self.urls_for_notes:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertEqual(response.url, redirect_url)
