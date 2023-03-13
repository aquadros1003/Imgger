from django.contrib.auth.models import User
from ..types import UserType
import graphene

class CreateUserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username, email, password):
        user = User.objects.create_user(username, email, password)
        user.save()
        return CreateUserMutation(user=user)
    

class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        username = graphene.String()
        email = graphene.String()
        password = graphene.String()

    user = graphene.Field(UserType)

    def mutate(self, info, user_id, username, email, password):
        user = User.objects.get(id=user_id)
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.set_password(password)
        user.save()
        return UpdateUserMutation(user=user)

class DeleteUserMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, user_id):
        user = User.objects.get(id=user_id)
        user.delete()
        return DeleteUserMutation(user=user)
    
