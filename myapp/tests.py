from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import User


class UserDirectoryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            name='Alex Morgan',
            photo='a.png',
            email='alex@example.com',
            password='private-value',
            mobile_number='+1 555 010 2040',
            date_of_birth=date(1992, 4, 12),
        )

    def test_directory_shows_profiles_without_password_values(self):
        response = self.client.get(reverse('myapp:user_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alex Morgan')
        self.assertNotContains(response, 'private-value')
        self.assertContains(response, 'Total profiles')

    def test_search_filters_by_name_and_email(self):
        response = self.client.get(reverse('myapp:user_list'), {'q': 'example.com'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].paginator.count, 1)
        self.assertContains(response, 'Alex Morgan')

    def test_profile_detail_does_not_expose_password(self):
        response = self.client.get(reverse('myapp:user_detail', args=[self.user.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alex Morgan')
        self.assertNotContains(response, 'private-value')

    def test_edit_with_blank_password_keeps_existing_value(self):
        response = self.client.post(
            reverse('myapp:user_edit', args=[self.user.pk]),
            {
                'name': 'Alex Morgan Updated',
                'email': 'alex@example.com',
                'password': '',
                'mobile_number': '+1 555 010 2040',
                'date_of_birth': '1992-04-12',
            },
        )

        self.assertRedirects(response, reverse('myapp:user_detail', args=[self.user.pk]))
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'Alex Morgan Updated')
        self.assertEqual(self.user.password, 'private-value')

    def test_delete_requires_post_and_removes_profile(self):
        delete_url = reverse('myapp:user_delete', args=[self.user.pk])

        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse('myapp:user_list'))
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_missing_profile_returns_404(self):
        response = self.client.get(reverse('myapp:user_detail', args=[999]))

        self.assertEqual(response.status_code, 404)
