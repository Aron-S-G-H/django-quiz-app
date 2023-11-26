import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required, staff_member_required
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
    @staff_member_required
    @login_required
    def mutate(parent, info, inputs):
        user_instance = User.objects.create_user(username=inputs.username, email=inputs.email, password=inputs.password)
        is_created = True
        return CreateUser(is_created=is_created, user=user_instance)


class UserMutate(ObjectType):
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
