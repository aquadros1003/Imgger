from django.contrib.auth import get_user_model
from ..types import PostType
import graphene
from ..models import Post, Category, Image, ExtendUser
from graphql_jwt.decorators import login_required
import base64


class CreatePostMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
        user_id = graphene.ID(required=True)
        image_id = graphene.String(required=True)
        category_id = graphene.ID(required=True)
        likes = graphene.Int()
        dislikes = graphene.Int()

    success = graphene.Boolean()
    errors = graphene.String()
    post = graphene.Field(PostType)

    @login_required
    def mutate(self, info, title, description, user_id, image_id, category_id):
        try:
            user = ExtendUser.objects.get(id=user_id)
            category_id = Category.objects.get(id=base64.b64decode(category_id)
                                        .decode("utf-8").split(':')[1])
            if image_id:
                image = Image.objects.get(id=image_id)
                post = Post(title=title, description=description, user=user,
                            image=image, category=category_id, likes=0,
                            dislikes=0)
            else:
                post = Post(title=title, description=description, user=user,
                            category=category_id, likes=0,
                            dislikes=0)
            post.save()
            return CreatePostMutation(success=True, post=post)
        except Exception as e:
            return CreatePostMutation(success=False, errors=str(e))

class UpdatePostMutation(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()
        user_id = graphene.ID()
        image_id = graphene.ID()
        category_id = graphene.ID()

    post = graphene.Field(PostType)

    @login_required
    def mutate(self, info, post_id, title, description, user_id, image_id,
               category_id):
        post = Post.objects.get(id=post_id)
        if title:
            post.title = title
        if description:
            post.description = description
        if user_id:
            user = get_user_model().objects.get(id=user_id)
            post.user = user
        if image_id:
            image = Image.objects.get(id=image_id)
            post.image = image
        if category_id:
            category = Category.objects.get(id=category_id)
            post.category = category
        post.save()
        return UpdatePostMutation(post=post)


class DeletePostMutation(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)

    post = graphene.Field(PostType)

    @login_required
    def mutate(self, info, post_id):
        post = Post.objects.get(id=post_id)
        post.delete()
        return DeletePostMutation(post=post)


class like(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)
    post = graphene.Field(PostType)

    @login_required
    def mutate(self, info, post_id):
        post = Post.objects.get(id=post_id)
        post.likes += 1
        post.save()
        return like(post=post)


class dislike(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)
    post = graphene.Field(PostType)

    @login_required
    def mutate(self, info, post_id):
        post = Post.objects.get(id=post_id)
        post.dislikes += 1
        post.save()
        return dislike(post=post)
