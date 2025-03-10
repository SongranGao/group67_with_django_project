from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Category, Tag, Post, Sidebar
from datetime import datetime

class BlogModelsTestCase(TestCase):

    def setUp(self):
        """ Setup test data """
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        self.category = Category.objects.create(name="Test Category", desc="Category Description")
        self.tag = Tag.objects.create(name="Test Tag")
        self.post = Post.objects.create(
            title="Test Post",
            desc="This is a test post.",
            category=self.category,
            content="This is the content of the test post.",
            tags=self.tag,
            owner=self.user,
            is_hot=True,
            pv=10
        )
        self.sidebar = Sidebar.objects.create(
            title="Test Sidebar",
            display_type=3,
            content="Sidebar Content",
            status=2
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(self.category.desc, "Category Description")

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, "Test Tag")

    def test_post_creation(self):
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.desc, "This is a test post.")
        self.assertEqual(self.post.content, "This is the content of the test post.")
        self.assertEqual(self.post.category, self.category)
        self.assertEqual(self.post.tags, self.tag)
        self.assertEqual(self.post.owner, self.user)
        self.assertEqual(self.post.is_hot, True)
        self.assertEqual(self.post.pv, 10)

    def test_sidebar_creation(self):
        self.assertEqual(self.sidebar.title, "Test Sidebar")
        self.assertEqual(self.sidebar.display_type, 3)
        self.assertEqual(self.sidebar.content, "Sidebar Content")
        self.assertEqual(self.sidebar.status, 2)


class BlogViewsTestCase(TestCase):

    def setUp(self):
        """ Setup test data """
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        self.category = Category.objects.create(name="Test Category", desc="Category Description")
        self.tag = Tag.objects.create(name="Test Tag")
        self.post = Post.objects.create(
            title="Test Post",
            desc="This is a test post.",
            category=self.category,
            content="This is the content of the test post.",
            tags=self.tag,
            owner=self.user,
            is_hot=True,
            pv=10
        )

    def test_index_view(self):
        response = self.client.get(reverse("blog:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")
        self.assertTemplateUsed(response, "blog/index.html")

    def test_category_list_view(self):
        response = self.client.get(reverse("blog:category_list", args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")
        self.assertTemplateUsed(response, "blog/list.html")

    def test_post_detail_view(self):
        response = self.client.get(reverse("blog:post_detail", args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")
        self.assertTemplateUsed(response, "blog/detail.html")

    def test_search_view(self):
        response = self.client.get(reverse("blog:search"), {"keyword": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")
        self.assertTemplateUsed(response, "blog/index.html")

    def test_archives_view(self):
        response = self.client.get(reverse("blog:archives", args=[datetime.now().year, datetime.now().month]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")
        self.assertTemplateUsed(response, "blog/archives_list.html")


class AddPostViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        self.category = Category.objects.create(name="Test Category")
        self.tag = Tag.objects.create(name="Test Tag")

    def test_get_add_post_page(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse('blog:add_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/add_post.html')
        self.assertContains(response, '<form')

    def test_post_creation(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse('blog:add_post'), {
            'title': 'Test Post',
            'desc': 'Test description',
            'category': self.category.id,
            'content': 'This is a test post.',
            'tags': [self.tag.id],
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.owner, self.user)
