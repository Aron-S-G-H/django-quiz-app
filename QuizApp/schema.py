import graphene
from quiz_app.schema import QuestionQuery, UserResultQuery, QuestionMutate
from account_app.schema import UserMutate


class Query(UserResultQuery, QuestionQuery, graphene.ObjectType):
    pass


class Mutation(UserMutate, QuestionMutate, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
