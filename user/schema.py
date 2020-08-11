import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from django.contrib.auth.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(graphene.ObjectType):
    user = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, **kwargs):
        user =  info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not logged in!")
        return user


class Mutation(graphene.ObjectType):
    # TODO: Add Create, Update and Delete features for user
    pass