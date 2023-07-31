import graphene
from quiz_app.schema import QuestionQuery, UserResultQuery, Mutate


class Query(UserResultQuery, QuestionQuery, graphene.ObjectType):
    pass


class Mutation(Mutate, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
