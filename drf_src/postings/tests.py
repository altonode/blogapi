from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from rest_framework_jwt.settings import api_settings

from django.contrib.auth import get_user_model

from postings.models import BlogPost

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()


class BlogPostAPITestCase(APITestCase):
	def setUp(self):
		user_obj = User(username='testcfeuser', email='test@trdt.com')
		user_obj.set_password("somerandompassword")
		user_obj.save()
		blog_post = BlogPost.objects.create(
				user=user_obj, 
				title='New title',
				content='Some Random Content')
	
	def test_single_user(self):
		user_count = User.objects.count()
		self.assertEqual(user_count, 1)
	
	def test_single_post(self):
		post_count = BlogPost.objects.count()
		self.assertEqual(post_count, 1)
		
	def test_get_item(self):
		blog_post = BlogPost.objects.first()
		data = {}
		url = blog_post.get_api_url()
		response = self.client.get(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		print(response.data)
		
	def test_post_item(self):
		data = {"title": "Some other title", "content": "Some other content"}
		url = api_reverse('api-postings:post-listcreate')
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
	
	def test_update_item_with_user(self):
		blog_post = BlogPost.objects.first()
		url = blog_post.get_api_url()
		data = {"title": "Some other title", "content": "Some other content"}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
		user_obj = User.objects.first()
		payload = payload_handler(user_obj)
		token_response = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)
		response = self.client.put(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		
	def test_user_ownership(self):
		owner = User.objects.create(username='TestUserX')
		blog_post = BlogPost.objects.create(
				user=owner, 
				title='New title',
				content='Some Random Content')
		user_obj = User.objects.first()
		self.assertNotEqual(user_obj.username, owner.username)
		payload = payload_handler(user_obj)
		token_response = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)
		url = blog_post.get_api_url()
		data = {"title": "Some title I cant remember", "content": "The related content"}
		response = self.client.put(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
		
	def test_user_login_and_update(self):
		data = {
			"username": 'testcfeuser',
			"password": 'somerandompassword',
		}
		url = api_reverse("api-login")
		response = self.client.post(url, data)
		print(response.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		token = response.data.get("token")
		if token is not None:
			blog_post = BlogPost.objects.first()
			url = blog_post.get_api_url()
			data = {"title": "Some other title", "content": "Some other content"}
			self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
			response = self.client.put(url, data, format='json')
			self.assertEqual(response.status_code, status.HTTP_200_OK)

			
		