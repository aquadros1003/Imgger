import base64
from datetime import datetime, timedelta

import graphene
from django.core.cache import cache
from django.db.models import Count, F, Q
from graphene_django.filter import DjangoFilterConnectionField
from graphql_auth import mutations
from graphql_auth.schema import MeQuery, UserQuery
from graphql_jwt.decorators import login_required, staff_member_required

from .models import Category, Comment, ExtendUser, Image, Post, Subcomment
from .mutations.categories import (
    CreateCategoryMutation,
    DeleteCategoryMutation,
    UpdateCategoryMutation,
)
from .mutations.comments import (
    CreateCommentMutation,
    DeleteCommentMutation,
    DislikeCommentMutation,
    LikeCommentMutation,
    UpdateCommentMutation,
)
from .mutations.images import (
    CreateImageMutation,
    DeleteImageMutation,
    UpdateImageMutation,
)
from .mutations.posts import (
    CreatePostMutation,
    DeletePostMutation,
    UpdatePostMutation,
    dislike,
    like,
)
from .mutations.subcomments import (
    CreateSubCommentMutation,
    DeleteSubCommentMutation,
    UpdateSubCommentMutation,
)
from .mutations.users import (
    DeleteMeMutation,
    DeleteUserMutation,
    LoginMutation,
    UpdateUserMutation,
)
from .types import (
    CategoryType,
    CommentType,
    ImageType,
    PostType,
    SubcommentType,
    UserType,
)


def can_increase_views():
    last_increase_time = cache.get("last_increase_time")
    if last_increase_time:
        elapsed_time = datetime.now() - last_increase_time
        if elapsed_time < timedelta(minutes=1):
            return False
    return True


class Query(UserQuery, MeQuery, graphene.ObjectType):
    users = DjangoFilterConnectionField(UserType)
    users_count = graphene.Int()
    me = graphene.Field(UserType)
    users_by_id = graphene.Field(UserType, id=graphene.ID(required=True))
    posts = DjangoFilterConnectionField(PostType)
    posts_count = graphene.Int()
    posts_by_id = graphene.Field(PostType, id=graphene.String(required=True))
    posts_by_short_url = graphene.Field(
        PostType, short_url=graphene.String(required=True)
    )
    posts_by_user = DjangoFilterConnectionField(PostType)
    posts_by_user_count = graphene.Int()
    posts_by_popularity = DjangoFilterConnectionField(PostType)
    posts_by_views = DjangoFilterConnectionField(PostType)
    search = DjangoFilterConnectionField(
        PostType, keyword=graphene.String(required=True)
    )
    categories = DjangoFilterConnectionField(CategoryType)
    images = graphene.List(ImageType)
    comments = DjangoFilterConnectionField(CommentType)
    comments_by_post = DjangoFilterConnectionField(
        CommentType, post_id=graphene.String(required=True)
    )
    subcomments = DjangoFilterConnectionField(SubcommentType)
    subcomments_by_comment = DjangoFilterConnectionField(
        SubcommentType, comment_id=graphene.String(required=True)
    )

    @staff_member_required
    def resolve_users(self, info, **kwargs):
        return ExtendUser.objects.all().order_by("id")

    @staff_member_required
    def resolve_users_count(self, info, **kwargs):
        return ExtendUser.objects.all().count()

    def resolve_me(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        return user

    def resolve_users_by_id(self, info, id):
        id = base64.b64decode(id).decode("utf-8").split(":")[1]
        id = int(id)
        return ExtendUser.objects.get(pk=id)

    def resolve_posts(self, info, **kwargs):
        return Post.objects.filter(is_private=False).order_by("-create_time")

    def resolve_posts_count(self, info, **kwargs):
        return Post.objects.filter(is_private=False).count()

    def resolve_posts_by_category(self, info, **kwargs):
        return Post.objects.filter(category=kwargs["category"])

    @login_required
    def resolve_posts_by_user(self, info, **kwargs):
        try:
            user = info.context.user
            return Post.objects.filter(user=user).order_by("-create_time")
        except:
            raise Exception("Not logged in!")

    def resolve_posts_by_user_count(self, info, **kwargs):
        try:
            user = info.context.user
            return Post.objects.filter(user=user).count()
        except:
            raise Exception("Not logged in!")

    def resolve_posts_by_popularity(self, info, **kwargs):
        likes_count = Count("likes", distinct=True)
        dislikes_count = Count("dislikes", distinct=True)
        rank = likes_count - dislikes_count
        return (
            Post.objects.filter(is_private=False)
            .annotate(rank=rank, likes_count=likes_count)
            .order_by("-rank", "-likes_count")
        )

    def resolve_posts_by_views(self, info, **kwargs):
        return Post.objects.filter(is_private=False).order_by("-views")

    def resolve_search(self, info, keyword, **kwargs):
        return (
            Post.objects.filter(
                Q(title__icontains=keyword)
                | Q(description__icontains=keyword)
                | Q(category__name__icontains=keyword)
                | Q(user__username__icontains=keyword)
            )
            .filter(is_private=False)
            .order_by("-create_time")
        )

    def resolve_categories_by_id(self, info, id):
        return Category.objects.get(pk=id)

    def resolve_categories(self, info, **kwargs):
        return Category.objects.annotate(num_posts=Count("post")).order_by("-num_posts")

    def resolve_posts_by_id(self, info, id, **kwargs):
        post_id = base64.b64decode(id).decode("utf-8").split(":")[1]
        post_id = int(post_id)
        if can_increase_views():
            Post.objects.filter(pk=post_id).update(views=F("views") + 1)
            cache.set("last_increase_time", datetime.now())
        return Post.objects.get(pk=post_id)

    def resolve_posts_by_short_url(self, info, short_url, **kwargs):
        return Post.objects.get(short_url=short_url)

    def resolve_comments(self, info, **kwargs):
        return Comment.objects.all()

    def resolve_comments_by_post(self, info, post_id, **kwargs):
        post_id = base64.b64decode(post_id).decode("utf-8").split(":")[1]
        post_id = int(post_id)
        return Comment.objects.filter(post=post_id).order_by("create_time")

    def resolve_subcomments(self, info, **kwargs):
        return Subcomment.objects.all()

    def resolve_subcomments_by_comment(self, info, comment_id, **kwargs):
        comment_id = base64.b64decode(comment_id).decode("utf-8").split(":")[1]
        comment_id = int(comment_id)
        return Subcomment.objects.filter(comment=comment_id).order_by("create_time")

    def resolve_images(self, info, **kwargs):
        return Image.objects.all()


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    update_account = mutations.UpdateAccount.Field()
    verify_account = mutations.VerifyAccount.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()


class Mutation(AuthMutation, graphene.ObjectType):
    login = LoginMutation.Field()

    update_user = UpdateUserMutation.Field()
    delete_user = DeleteUserMutation.Field()
    delete_me = DeleteMeMutation.Field()

    create_post = CreatePostMutation.Field()
    update_post = UpdatePostMutation.Field()
    delete_post = DeletePostMutation.Field()

    like = like.Field()
    dislike = dislike.Field()

    create_category = CreateCategoryMutation.Field()
    update_category = UpdateCategoryMutation.Field()
    delete_category = DeleteCategoryMutation.Field()

    create_comment = CreateCommentMutation.Field()
    update_comment = UpdateCommentMutation.Field()
    delete_comment = DeleteCommentMutation.Field()
    like_comment = LikeCommentMutation.Field()
    dislike_comment = DislikeCommentMutation.Field()

    create_subcomment = CreateSubCommentMutation.Field()
    update_subcomment = UpdateSubCommentMutation.Field()
    delete_subcomment = DeleteSubCommentMutation.Field()

    create_image = CreateImageMutation.Field()
    update_imaage = UpdateImageMutation.Field()
    delete_image = DeleteImageMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
