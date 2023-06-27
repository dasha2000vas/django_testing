from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.another_user = User.objects.create(username='Другой автор')
        cls.another_user_client = Client()
        cls.another_user_client.force_login(cls.another_user)
        cls.note = Note.objects.create(
            title='Заметка',
            text='Текст.',
            author=cls.author,
        )

    def test_pages_contain_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.author_client.get(url)
                self.assertIn('form', response.context)

    def test_notes_list_for_different_users(self):
        url = reverse('notes:list')
        test_info = (
            (self.author_client, True),
            (self.another_user_client, False),
        )
        for client, note_in_list in test_info:
            with self.subTest(client=client):
                response = client.get(url)
                self.assertEqual(
                    (self.note in response.context['object_list']),
                    note_in_list
                )
