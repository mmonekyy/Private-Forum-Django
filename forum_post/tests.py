from django.test import TestCase
from forum_users.models import CustomUser
from forum_post.models import ForumPost, Category
# Create your tests here.
class ForumPostsSellTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser1', password='testpass1')
        self.client.login(username='testuser1', password='testpass1')

    def test_create_post_authenticated(self):
        category = Category.objects.create(Name='General')
        post_data = {
            'title': 'Test Post',
            'content': 'This is a test post content.',
            'category': category,
            'tags': 'test,post'
        }
        response = self.client.post('/Posts/Create/', post_data)
        self.assertEqual(response.status_code, 200)
    
    def test_category_not_exist(self):
        post_data = {
            'title': 'Test Post',
            'content': 'This is a test post content.',
            'category': 'General',
            'tags': 'test,post'
        }
        response = self.client.post('/Posts/Create/', post_data)
        self.assertEqual(response.status_code, 400)

    def test_edit_post_authenticated(self):
        category = Category.objects.create(Name='General')
        post = ForumPost.objects.create(
            Title='Test Post',
            Content='This is a test post content.',
            Category=category,
            tags='test,post',
            Author=self.user
        )
        response = self.client.post(f'/Posts/ViewOwnPosts/Edit/{post.id}/', {
            'title': 'Updated Test Post',
            'content': 'This is updated test post content.',
            'tags': 'updated,test,post'
        })
        self.assertEqual(response.status_code, 302)
    
    def test_post_delete(self):
        category = Category.objects.create(Name='General')
        post_data = {
            'title': 'Test Post',
            'content': 'This is a test post content.',
            'category': category,
            'tags': 'test,post'
        }
        self.client.post('/Posts/Create/', post_data)
        post = ForumPost.objects.get(Title='Test Post')
        post_del = self.client.post(f'Delete/{post.id}/')
        self.assertEqual(post_del.status_code, 404)
        
    def test_add_comment(self):
        category = Category.objects.create(Name='General')
        post = ForumPost.objects.create(
            Title='Test Post',
            Content='This is a test post content.',
            Category=category,
            tags='test,post',
            Author=self.user
        )                             
        response = self.client.post(f'/Posts/Post/{post.id}/comment/', {
        'comment': 'This is a test comment.'
        })
        self.assertEqual(response.status_code, 302)