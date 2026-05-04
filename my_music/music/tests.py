from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from my_music.music.models import Album, Profile


class AuthOwnershipTests(TestCase):
	def _create_user_with_profile(self, username='user1', email='u1@example.com'):
		user = User.objects.create_user(username=username, password='pass12345', email=email)
		Profile.objects.create(user=user, username=username, email=email)
		return user

	def test_index_redirects_guest_to_login(self):
		response = self.client.get(reverse('index'))
		self.assertRedirects(response, reverse('login'))

	def test_index_redirects_authenticated_user_without_profile(self):
		user = User.objects.create_user(username='no_profile', password='pass12345')
		self.client.force_login(user)

		response = self.client.get(reverse('index'))
		self.assertRedirects(response, reverse('add profile'))

	def test_index_shows_only_current_user_albums(self):
		user1 = self._create_user_with_profile('alice', 'alice@example.com')
		user2 = self._create_user_with_profile('bob', 'bob@example.com')

		own_album = Album.objects.create(
			owner=user1,
			album_name='A1',
			artist='Artist 1',
			genre='Pop Music',
			image_url='https://example.com/a1.jpg',
			price=10,
		)
		Album.objects.create(
			owner=user2,
			album_name='B1',
			artist='Artist 2',
			genre='Rock Music',
			image_url='https://example.com/b1.jpg',
			price=12,
		)

		self.client.force_login(user1)
		response = self.client.get(reverse('index'))

		self.assertEqual(response.status_code, 200)
		albums = list(response.context['albums'])
		self.assertEqual(albums, [own_album])

	def test_user_cannot_open_other_user_album_details(self):
		user1 = self._create_user_with_profile('owner', 'owner@example.com')
		user2 = self._create_user_with_profile('viewer', 'viewer@example.com')
		album = Album.objects.create(
			owner=user1,
			album_name='Private',
			artist='Owner Artist',
			genre='Jazz Music',
			image_url='https://example.com/private.jpg',
			price=15,
		)

		self.client.force_login(user2)
		response = self.client.get(reverse('details album', kwargs={'pk': album.pk}))

		self.assertEqual(response.status_code, 404)

	def test_no_cache_headers_for_authenticated_users(self):
		user = self._create_user_with_profile('cachetest', 'cache@example.com')
		self.client.force_login(user)

		response = self.client.get(reverse('index'))

		self.assertEqual(response['Cache-Control'], 'no-cache, no-store, must-revalidate')
		self.assertEqual(response['Pragma'], 'no-cache')
		self.assertEqual(response['Expires'], '0')

	def test_no_cache_headers_not_for_guests(self):
		response = self.client.get(reverse('login'))

		self.assertNotIn('Cache-Control', response)
	def test_register_creates_user_and_logs_in(self):
		before = User.objects.count()
		response = self.client.post(
			reverse('register'),
			{
				'username': 'new_user',
				'email': 'new@example.com',
				'password1': 'Strongpass123',
				'password2': 'Strongpass123',
			},
		)

		self.assertEqual(User.objects.count(), before + 1)
		self.assertRedirects(response, reverse('add profile'))
		self.assertIn('_auth_user_id', self.client.session)

	def test_register_invalid_data_does_not_create_user(self):
		before = User.objects.count()
		response = self.client.post(
			reverse('register'),
			{
				'username': 'bad_user',
				'email': 'bad@example.com',
				'password1': 'Strongpass123',
				'password2': 'Wrongpass123',
			},
		)

		self.assertEqual(User.objects.count(), before)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'errorlist')

