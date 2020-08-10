import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from .models import Question, Choice


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question


class ChoiceType(DjangoObjectType):
    class Meta:
        model = Choice


class CreateQuestion(graphene.Mutation):
    question = graphene.Field(QuestionType)

    class Arguments:
        question_text = graphene.String(required=True)
        pub_date = graphene.DateTime(required=True)

    def mutate(self, info, question_text, pub_date):
        question = Question(question_text=question_text, pub_date=pub_date)
        question.save()
        return CreateQuestion(question=question)


class UpdateQuestion(graphene.Mutation):
    question = graphene.Field(QuestionType)

    class Arguments:
        id = graphene.Int(required=True)
        question_text = graphene.String()
        pub_date = graphene.DateTime()

    def mutate(self, info, id, question_text=None, pub_date=None, **kwargs):
        question = Question.objects.filter(id=id).first()
        if question is None:
            raise GraphQLError(f"Couldn't find record with id={id}")
        if question_text:
            question.question_text = question_text
        if pub_date:
            question.pub_date = pub_date
        question.save()
        return UpdateQuestion(question=question)

class DeleteQuestion(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id, **kwargs):
        question = Question.objects.filter(id=id).first()
        if question:
            question.delete()
            return DeleteQuestion(message=f"Record with id={id} deleted successfully")
        return DeleteQuestion(message=f"Couldn't find record with id={id}")


class CreateChoice(graphene.Mutation):
    question = graphene.Field(QuestionType)

    class Arguments:
        question_id = graphene.Int(required=True)
        choice_text = graphene.String(required=True)

    def mutate(self, info, question_id, choice_text, **kwargs):
        question = Question.objects.filter(id=question_id).first()
        if question is None:
            raise GraphQLError(f"Couldn't find record with question_id={question_id}")
        question.choices.create(choice_text=choice_text)
        return CreateChoice(question=question)


class Query(graphene.ObjectType):
    questions = graphene.List(QuestionType)
    question = graphene.Field(QuestionType, id=graphene.Int())
    # Nested field
    choices = graphene.List(ChoiceType)

    def resolve_questions(self, info, **kwargs):
        return Question.objects.all()

    def resolve_question(self, info, id, **kwargs):
        try:
            return Question.objects.get(id=id)
        except Question.DoesNotExist:
            raise GraphQLError("No question exists with this ID")

    def resolve_choices(self, question, info):
        return question.choices.all()


class Mutation(graphene.ObjectType):
    # Question
    create_question = CreateQuestion.Field()
    delete_question = DeleteQuestion.Field()
    update_question = UpdateQuestion.Field()

    # Choice
    create_choice = CreateChoice.Field()