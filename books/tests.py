# books/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import CustomUser, Book

class BookListTestCase(APITestCase):
    def setUp(self):
        self.super_admin = CustomUser.objects.create_superuser(email='admin@test.com', password='adminpass', role='SuperAdmin')
        self.user = CustomUser.objects.create_user(email='user@test.com', password='userpass', role='User')
        self.book = Book.objects.create(title="Test Book", author="Author", description="Test Description")
        self.book.permitted_users.add(self.user)

    def test_superadmin_can_view_all_books(self):
        self.client.force_authenticate(user=self.super_admin)
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_can_only_view_permitted_books(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
