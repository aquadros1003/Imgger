from django.test import Client, TestCase
from graphql_jwt.shortcuts import get_token

from core.models import Category, Comment, ExtendUser, Image, Post, Subcomment


class ExtendUserModelTestCase(TestCase):
    def setUp(self):
        self.user = ExtendUser.objects.create_user(
            username="testuser", password="testpassword", email="test123@test.pl"
        )
        self.user.save()

        self.client = Client()
        self.client.login(username="testuser", password="testpassword")

    def test_string_representation(self):
        # self.assertEqual(str(self.user), self.user.username)
        self.assertEqual(str(self.user), "testuser")


class CategoryModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="TestCategory")
        self.category.save()

    def test_string_representation(self):
        self.assertEqual(str(self.category), "TestCategory")


class ImageModelTestCase(TestCase):
    def setUp(self):
        self.image = Image.objects.create(name="TestImage", url="sum.jpg")
        self.image.save()

    def test_string_representation(self):
        self.assertEqual(str(self.image), "TestImage")


class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = ExtendUser.objects.create_user(
            username="testuser", password="testpassword", email="test123@test.pl"
        )
        self.user.save()

        self.image = Image.objects.create(name="TestImage", url="sum.jpg")
        self.image.save()

        self.category = Category.objects.create(name="TestCategory")
        self.category.save()

        self.post = Post.objects.create(
            title="TestPost",
            description="TestDescription",
            user=self.user,
            image=self.image,
            category=self.category,
        )
        self.post.save()

    def test_string_representation(self):
        self.assertEqual(str(self.post), "TestPost")


class CommentModelTestCase(TestCase):
    def setUp(self):
        self.user = ExtendUser.objects.create_user(
            username="testuser", password="testpassword", email="test123@test.pl"
        )
        self.user.save()

        self.image = Image.objects.create(name="TestImage", url="sum.jpg")
        self.image.save()

        self.category = Category.objects.create(name="TestCategory")
        self.category.save()

        self.post = Post.objects.create(
            title="TestPost",
            description="TestDescription",
            user=self.user,
            image=self.image,
            category=self.category,
        )
        self.post.save()

        self.comment = Comment.objects.create(
            user=self.user, comment="TestComment", post=self.post
        )
        self.comment.save()

    def test_string_representation(self):
        self.assertEqual(str(self.comment), "TestComment")


class SubcommentModelTestCase(TestCase):
    def setUp(self):
        self.user = ExtendUser.objects.create_user(
            username="testuser", password="testpassword", email="test123@test.pl"
        )
        self.user.save()

        self.image = Image.objects.create(name="TestImage", url="sum.jpg")
        self.image.save()

        self.category = Category.objects.create(name="TestCategory")
        self.category.save()

        self.post = Post.objects.create(
            title="TestPost",
            description="TestDescription",
            user=self.user,
            image=self.image,
            category=self.category,
        )
        self.post.save()

        self.comment = Comment.objects.create(
            user=self.user, comment="TestComment", post=self.post
        )
        self.comment.save()

        self.subcomment = Subcomment.objects.create(
            user=self.user, comment=self.comment, content="TestSubComment"
        )
        self.subcomment.save()

    def test_string_representation(self):
        self.assertEqual(str(self.subcomment), "TestSubComment")
