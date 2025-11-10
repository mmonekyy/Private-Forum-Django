from django.test import TestCase
from forum_users.models import CustomUser
from forum_post.models import ForumPost, Category

class ForumPostsSellTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser1', password='testpass1')
        self.client.login(username='testuser1', password='testpass1')

    def test_create_post_authenticated(self):
        category = Category.objects.create(Name='General')
        post_data = {
            'title': 'Test Post',
            'content': 'This is a test post content.',
            'category': 'General',
            'tags': 'test,post'
        }
        response = self.client.post('/Posts/Create/', post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ForumPost.objects.filter(Title='Test Post').exists())
    
    def test_category_not_exist(self):
        post_data = {
            'title': 'Test Post',
            'content': 'This is a test post content.',
            'category': 'NonExistentCategory',
            'tags': 'test,post'
        }
        response = self.client.post('/Posts/Create/', post_data)
        self.assertEqual(response.status_code, 200)  
        self.assertIn('error', response.context)

    def test_edit_post_authenticated(self):
        category = Category.objects.create(Name='General')
        post = ForumPost.objects.create(
            Title='Test Post',
            Content='This is a test post content.',
            Category=category,
            Author=self.user
        )
        post.tags.add('test', 'post')

        response = self.client.post(f'/Posts/ViewOwnPosts/Edit/{post.id}/', {
            'title': 'Updated Test Post',
            'content': 'This is updated test post content.',
            'category': 'General',
            'tags': 'updated,test,post'
        })
        self.assertEqual(response.status_code, 302)
        
        updated_post = ForumPost.objects.get(id=post.id)
        self.assertEqual(updated_post.Title, 'Updated Test Post')
        self.assertEqual(updated_post.Content, 'This is updated test post content.')
    
    def test_post_delete(self):
        category = Category.objects.create(Name='General')
        post = ForumPost.objects.create(
            Title='Test Post',
            Content='This is a test post content.',
            Category=category,
            Author=self.user
        )
        post.tags.add('test', 'post')
        
        response = self.client.post(f'/Posts/Delete/{post.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ForumPost.objects.filter(id=post.id).exists())
        
    def test_add_comment(self):
        category = Category.objects.create(Name='General')
        post = ForumPost.objects.create(
            Title='Test Post',
            Content='This is a test post content.',
            Category=category,
            Author=self.user
        )
        post.tags.add('test', 'post')
                             
        response = self.client.post(f'/Posts/Post/{post.id}/comment/', {
            'comment': 'This is a test comment.'
        })
        self.assertEqual(response.status_code, 302)

    def test_unauthorized_access(self):
        self.client.logout()
        response = self.client.get('/Posts/Create/')
        self.assertRedirects(response, '/register/')
        response = self.client.get('/Posts/ViewOwnPosts/Edit/1/')
        self.assertRedirects(response, '/register/')

    def test_edit_post_unauthorized(self):
        other_user = CustomUser.objects.create_user(username='other_user', password='testpass2')
        category = Category.objects.create(Name='General')
        post = ForumPost.objects.create(
            Title='Other User Post',
            Content='This is another user\'s post.',
            Category=category,
            Author=other_user
        )
        
        response = self.client.post(f'/Posts/ViewOwnPosts/Edit/{post.id}/', {
            'title': 'Trying to Update',
            'content': 'Trying to modify other\'s post',
            'category': 'General',
            'tags': 'test'
        })
        self.assertRedirects(response, '/Posts/ViewOwnPosts/')
        
        unchanged_post = ForumPost.objects.get(id=post.id)
        self.assertEqual(unchanged_post.Title, 'Other User Post')
        self.assertEqual(unchanged_post.Content, 'This is another user\'s post.')