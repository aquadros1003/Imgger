import base64
import random
import string

import graphene
from django.contrib.auth import get_user_model
from django.utils import timezone
from firebase_admin import storage
from graphql_jwt.decorators import login_required, staff_member_required

from ..models import Category, Image, Post
from ..types import PostType


class CreatePostMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
        image_id = graphene.String(required=True)
        category_id = graphene.ID()
        is_private = graphene.Boolean()
        expiration_date = graphene.Int()

    success = graphene.Boolean()
    errors = graphene.String()
    post = graphene.Field(PostType)

    def mutate(
        self,
        info,
        title,
        description,
        image_id,
        category_id,
        is_private,
        expiration_date=None,
    ):
        try:
            user = info.context.user
            exp_date = None
            if is_private:
                exp_date = timezone.now() + timezone.timedelta(days=1)
                if expiration_date:
                    match (expiration_date):
                        case 1:
                            exp_date = timezone.now() + timezone.timedelta(days=1)
                        case 2:
                            exp_date = timezone.now() + timezone.timedelta(days=3)
                        case 3:
                            exp_date = timezone.now() + timezone.timedelta(days=7)
                        case other:
                            exp_date = timezone.now() + timezone.timedelta(days=1)

            image = Image.objects.get(id=image_id)
            category_id = base64.b64decode(category_id).decode("utf-8").split(":")[1]
            category = Category.objects.get(id=category_id)

            if user.is_authenticated:
                post = Post.objects.create(
                    title=title,
                    description=description,
                    image=image,
                    category=category,
                    user=user,
                    is_private=is_private,
                    short_url=f"{''.join(random.choices(string.ascii_uppercase + string.digits, k=7))}",
                    expiration_date=exp_date,
                )
            else:
                post = Post.objects.create(
                    title=title,
                    description=description,
                    image=image,
                    category=category,
                    is_private=True,
                    short_url=f"{''.join(random.choices(string.ascii_uppercase + string.digits, k=7))}",
                    expiration_date=exp_date,
                )
            post.save()
            return CreatePostMutation(success=True, post=post)
        except Exception as e:
            return CreatePostMutation(success=False, errors=str(e))


class UpdatePostMutation(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()
        category_id = graphene.ID()

    post = graphene.Field(PostType)
    success = graphene.Boolean()
    errors = graphene.String()

    @login_required
    def mutate(self, info, post_id, title, description, category_id):
        try:
            user = info.context.user
            id = base64.b64decode(post_id).decode("utf-8").split(":")[1]
            post = Post.objects.get(id=id)
            if not (user.is_staff or post.user == user):
                return DeletePostMutation(
                    success=False,
                    errors="Only admins and the author can update this post",
                )
            if title:
                post.title = title

            if category_id:
                category_id = Category.objects.get(
                    id=base64.b64decode(category_id).decode("utf-8").split(":")[1]
                )
                post.category = category_id
            post.description = description
            post.save()
            return UpdatePostMutation(success=True, post=post)
        except Exception as e:
            return UpdatePostMutation(success=False, errors=str(e))


class DeletePostMutation(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)

    success = graphene.Boolean()
    errors = graphene.String()

    @login_required
    def mutate(self, info, post_id):
        try:
            user = info.context.user
            id = base64.b64decode(post_id).decode("utf-8").split(":")[1]
            post = Post.objects.get(id=id)
            if not (user.is_staff or post.user == user):
                return DeletePostMutation(
                    success=False,
                    errors="Only admins and the author can delete this post",
                )
            if post.image:
                image = post.image
            post.delete()
            if image:
                bucket = storage.bucket()
                url = image.url.split("/")[-1]
                blob = bucket.blob("images/" + url)
                blob.delete()
                image.delete()
            return DeletePostMutation(success=True)
        except Exception as e:
            return DeletePostMutation(success=False, errors=str(e))


class like(graphene.Mutation):
    class Arguments:
        post_id = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.String()

    @login_required
    def mutate(self, info, post_id):
        user = info.context.user

        if not user.is_authenticated:
            return like(success=False, errors="User not logged in")

        post = Post.objects.get(
            id=base64.b64decode(post_id).decode("utf-8").split(":")[1]
        )

        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        if user in post.dislikes.all():
            post.dislikes.remove(user)
        post.save()
        return like(success=True)


class dislike(graphene.Mutation):
    class Arguments:
        post_id = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.String()

    @login_required
    def mutate(self, info, post_id):
        user = info.context.user

        if not user.is_authenticated:
            return dislike(success=False, errors="User not logged in")

        post = Post.objects.get(
            id=base64.b64decode(post_id).decode("utf-8").split(":")[1]
        )

        if user in post.dislikes.all():
            post.dislikes.remove(user)
        else:
            post.dislikes.add(user)
        if user in post.likes.all():
            post.likes.remove(user)
        post.save()
        return dislike(success=True)
