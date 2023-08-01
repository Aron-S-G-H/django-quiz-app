import graphene
from graphql import GraphQLError
from graphene_django.types import DjangoObjectType, ObjectType
from django.contrib.auth.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password',)


class UserInput(graphene.InputObjectType):
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()


class CreateUser(graphene.Mutation):
    class Arguments:
        inputs = UserInput(required=True)

    is_created = graphene.Boolean(default_value=False)
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(parent, info, inputs):
        if not info.context.user.is_authenticated:
            GraphQLError('you are not authenticated!')
        elif not info.context.user.is_staff:
            GraphQLError('you dont have permission!')
        user_instance = User.objects.create_user(username=inputs.username, email=inputs.email, password=inputs.password)
        is_created = True
        return CreateUser(is_created=is_created, user=user_instance)


class UserMutate(ObjectType):
    create_user = CreateUser.Field()
