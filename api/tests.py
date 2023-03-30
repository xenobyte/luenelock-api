from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Lock
from .serializers import LockSerializer


class LockTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.lock = Lock.objects.create(
            name='Test Lock', user=self.user, is_locked=True)

    def test_lock_str(self):
        self.assertEqual(str(self.lock), self.lock.uuid.__str__())

    def test_lock_defaults(self):
        self.assertEqual(self.lock.is_locked, True)

    def test_lock_create(self):
        new_lock = Lock.objects.create(
            name='New Lock', user=self.user, is_locked=False)
        self.assertEqual(new_lock.name, 'New Lock')
        self.assertEqual(new_lock.user, self.user)
        self.assertEqual(new_lock.is_locked, False)

    def test_lock_update(self):
        self.lock.name = 'Updated Lock'
        self.lock.is_locked = False
        self.lock.save()
        self.lock.refresh_from_db()
        self.assertEqual(self.lock.name, 'Updated Lock')
        self.assertEqual(self.lock.is_locked, False)

    def test_lock_delete(self):
        lock_id = self.lock.id
        self.lock.delete()
        self.assertFalse(Lock.objects.filter(id=lock_id).exists())


class LockListTestCase(APITestCase):
    url = reverse('lock-list')

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.lock = Lock.objects.create(
            name='Test Lock', user=self.user, is_locked=True)

    def test_lock_list_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.lock.name)

    def test_lock_list_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LockDetailTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.lock = Lock.objects.create(
            name='Test Lock', user=self.user, is_locked=True)
        self.url = reverse('lock-detail', kwargs={'uuid': self.lock.uuid})

    def test_lock_detail_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = LockSerializer(self.lock).data
        self.assertEqual(response.data, serializer_data)

    def test_lock_detail_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('api.views.LockDetail.get_queryset')
    def test_lock_detail_filter_by_user(self, mock_get_queryset):
        mock_queryset = mock_get_queryset.return_value
        mock_queryset.filter.return_value = [self.lock]
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lock_detail_update(self):
        self.client.force_login(self.user)
        response = self.client.patch(self.url, {'is_locked': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lock.refresh_from_db()
        self.assertEqual(self.lock.is_locked, False)

    def test_lock_detail_delete(self):
        self.client.force_login(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lock.objects.filter(uuid=self.lock.uuid).exists())
