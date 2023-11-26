import graphene
from graphql import GraphQLError
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Question, UserResult


# its like serializers in django rest framework
class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        exclude = ('status',)


class UserResultType(DjangoObjectType):
    class Meta:
        model = UserResult
        exclude = ('id',)


# a subclass of ObjectType representing the GraphQL queries related to questions
class QuestionQuery(ObjectType):
    questions = graphene.List(QuestionType)
    question = graphene.Field(QuestionType, id=graphene.ID(required=True))

    @staticmethod
    def resolve_questions(parent, info, **kwargs):
        return Question.objects.filter(status=True).defer('status')

    @staticmethod
    def resolve_question(parent, info, **kwargs):
        pk = kwargs.get('id')
        return Question.objects.get(id=pk)


class UserResultQuery(ObjectType):
    user_result = graphene.Field(UserResultType, name=graphene.String(required=True))

    @staticmethod
    def resolve_user_result(parent, info, **kwargs):
        name = kwargs.get('name')
        return UserResult.objects.get(fullname=name)


class QuestionInputs(graphene.InputObjectType):
    question = graphene.String()
    option1 = graphene.String()
    option2 = graphene.String()
    option3 = graphene.String()
    option4 = graphene.String()
    answer = graphene.String()


class CreateQuestion(graphene.Mutation):
    class Arguments:
        inputs = QuestionInputs(required=True)

    is_created = graphene.Boolean(default_value=False)

    @classmethod
    def mutate(cls, parent, info, inputs):
        if not inputs.answer in ['option1', 'option2', 'option3', 'option4']:
            raise GraphQLError('choose one of the options as answer!')
        elif not info.context.user.is_authenticated:
            raise GraphQLError('you are not authenticated')
        Question.objects.create(
            question=inputs.question, option1=inputs.option1,
            option2=inputs.option2, option3=inputs.option3,
            option4=inputs.option4, answer=inputs.answer,
        )
        is_created = True
        return CreateQuestion(is_created=is_created)


class UpdateQuestion(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        inputs = QuestionInputs()

    is_updated = graphene.Boolean(default_value=False)

    @classmethod
    def mutate(cls, parent, info, id, inputs=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('you are not authenticated!')
        elif not inputs:
            raise GraphQLError('there is no parameter to update!')
        elif inputs.answer and inputs.answer not in ['option1', 'option2', 'option3', 'option4']:
            raise GraphQLError('choose one of the options as answer!')
        else:
            question_instance = Question.objects.get(id=id)
            question_instance.question = inputs.question if inputs.question is not None else question_instance.question
            question_instance.option1 = inputs.option1 if inputs.option1 is not None else question_instance.option1
            question_instance.option2 = inputs.option2 if inputs.option2 is not None else question_instance.option2
            question_instance.option3 = inputs.option3 if inputs.option3 is not None else question_instance.option3
            question_instance.option4 = inputs.option4 if inputs.option4 is not None else question_instance.option4
            question_instance.answer = inputs.answer if inputs.answer is not None else question_instance.answer
            question_instance.save()
            is_updated = True
            return UpdateQuestion(is_updated=is_updated)


class DeleteQuestion(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    is_deleted = graphene.Boolean(default_value=False)

    @classmethod
    def mutate(cls, parent, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('you are not authenticated!')
        question = Question.objects.get(id=id)
        question.delete()
        is_deleted = True
        return DeleteQuestion(is_deleted=is_deleted)


# a subclass of graphene.ObjectType representing the GraphQL mutation operations
class QuestionMutate(graphene.ObjectType):
    create_question = CreateQuestion.Field()
    update_question = UpdateQuestion.Field()
    delete_question = DeleteQuestion.Field()
