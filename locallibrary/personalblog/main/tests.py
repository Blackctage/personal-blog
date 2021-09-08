from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post, Comment, ArticlesType, ArticleTypeHeader


class BlogTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='samuel',
            email='user@email.com',
            password='secret',
        )

        self.articles_type_header = ArticleTypeHeader.objects.create(
            title='12',
            link='12',
        )

        self.articles_type = ArticlesType.objects.create(
            name='1',
            article_type_header=self.articles_type_header,

        )

        self.post = Post.objects.create(

            title='11',
            photo_or_video='post_file/Screenshot_24_9Un3zDz.png',

            summary='none',
            isbn='95744',
            imprint='something',
            articles_type=self.articles_type,
            publish_date='2020-01-12',

            status='a',
        )

        self.comment = Comment.objects.create(
            post=self.post,
            name="John Doe",
            profile_photo='static/main/assets/images/default_avatar.jpg',
            body="A comment on this post",
        )

    def test_post_list(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First post')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First post')
        self.assertContains(response, 'Some text about travelling the world')
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'A comment on this post')
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_submit_comment_logged_in(self):
        self.client.login(username='samuel', password='secret')
        url = reverse('post_detail', args=[1])
        response = self.client.post(url, {
            'name': 'Samuel',
            'comment': 'Thanks for your feedback'
        })
        self.assertEqual(response.status_code, 302)  # Found redirect
        self.assertEqual(Comment.objects.last().name, 'Samuel')
        self.assertEqual(Comment.objects.last().comment, 'Thanks for your feedback')


    def test_submit_comment_logged_out_fail(self):
        self.client.logout()
        last_comment = Comment.objects.last()
        url = reverse('post_detail', args=[1])
        response = self.client.post(url, {
            'name': 'Samuel',
            'comment': 'I am not the real author',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry, you cannot use this name.")
        self.assertEqual(last_comment, Comment.objects.last())

    def test_submit_comment_logged_out_success(self):
        self.client.logout()
        url = reverse('post_detail', args=[1])
        response = self.client.post(url, {
            'name': 'Peter',
            'comment': "I definitely have to try this!"
        })
        self.assertEqual(response.status_code, 302)  # Found redirect
        self.assertEqual(Comment.objects.last().name, 'Peter')
        self.assertEqual(Comment.objects.last().comment, "I definitely have to try this!")