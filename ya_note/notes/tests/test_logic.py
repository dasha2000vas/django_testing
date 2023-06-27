from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import WARNING
from notes.models import Note

User = get_user_model()


class TestNoteCreation(TestCase):
    TITLE = 'Заметка'
    TEXT = 'Текст.'
    SLUG = 'zametka'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.url = reverse('notes:add')
        cls.initial_count = Note.objects.count()
        cls.form_data = {
            'title': cls.TITLE,
            'text': cls.TEXT,
        }

    def test_anonymous_user_cant_create_note(self):
        response = self.client.post(self.url, data=self.form_data)
        login_url = reverse('users:login')
        expected_url = f'{login_url}?next={self.url}'
        self.assertRedirects(response, expected_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.initial_count)

    def test_authorized_user_can_create_note(self):
        response = self.author_client.post(self.url, data=self.form_data)
        redirect_url = reverse('notes:success')
        self.assertRedirects(response, redirect_url)
        notes_count = Note.objects.count()
        self.assertGreater(notes_count, self.initial_count)
        note = Note.objects.get()
        self.assertEqual(note.title, self.TITLE)
        self.assertEqual(note.text, self.TEXT)
        self.assertEqual(note.author, self.author)
        self.assertEqual(note.slug, self.SLUG)

    def test_user_cant_post_notes_with_same_slug(self):
        self.author_client.post(self.url, data=self.form_data)
        initial_count = Note.objects.count()
        response = self.author_client.post(self.url, data=self.form_data)
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=self.SLUG + WARNING
        )
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, initial_count)


class TestNoteDeleteEdit(TestCase):
    TITLE = 'Заголовок'
    NEW_TITLE = 'Новый заголовок'
    TEXT = 'Текст.'
    NEW_TEXT = 'Новый текст.'
    SLUG = 'slug'
    NEW_SLUG = 'new-slug'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.another_user = User.objects.create(username='Другой автор')
        cls.another_user_client = Client()
        cls.another_user_client.force_login(cls.another_user)
        cls.note = Note.objects.create(
            title=cls.TITLE,
            text=cls.TEXT,
            slug=cls.SLUG,
            author=cls.author,
        )
        cls.initial_count = Note.objects.count()
        cls.url_delete = reverse('notes:delete', args=(cls.note.slug,))
        cls.url_edit = reverse('notes:edit', args=(cls.note.slug,))
        cls.url_redirect = reverse('notes:success')
        cls.form_data = {
            'title': cls.NEW_TITLE,
            'text': cls.NEW_TEXT,
            'slug': cls.NEW_SLUG,
        }

    def test_author_can_delete_note(self):
        response = self.author_client.delete(self.url_delete)
        self.assertRedirects(response, self.url_redirect)
        notes_count = Note.objects.count()
        self.assertLess(notes_count, self.initial_count)

    def test_user_cant_delete_note_of_another_user(self):
        response = self.another_user_client.delete(self.url_delete)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.initial_count)

    def test_author_can_edit_note(self):
        response = self.author_client.post(self.url_edit, data=self.form_data)
        self.assertRedirects(response, self.url_redirect)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.NEW_TITLE)
        self.assertEqual(self.note.text, self.NEW_TEXT)
        self.assertEqual(self.note.slug, self.NEW_SLUG)

    def test_user_cant_edit_note_of_another_user(self):
        response = self.another_user_client.post(
            self.url_edit,
            data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.TITLE)
        self.assertEqual(self.note.text, self.TEXT)
        self.assertEqual(self.note.slug, self.SLUG)
