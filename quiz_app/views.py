from django.shortcuts import render, redirect, reverse
from .models import Question, UserResult
from django.views.generic import View
from .email_module import send_email_result
from .serializers import QuestionsSerializer, ResultSerializer
from .permissions import IsStaff
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class Quiz(View):
    def get(self, request):
        if request.user.is_authenticated:
            user_flag = True

            if UserResult.objects.filter(fullname=request.user.username).exists():
                user_flag = False

            questions = Question.objects.all()

            return render(request, 'index.html', {'questions': questions, 'flag': user_flag})
        else:
            return redirect('account:login_page')

    def post(self, request):
        questions = Question.objects.filter(status=True)
        fullname = request.user.username
        totall = 0
        score = 0
        correct = 0
        wrong = 0
        for q in questions:
            totall += 1
            if q.answer == request.POST.get(q.question):
                score += 10
                correct += 1
            else:
                wrong += 1
        percent = score / (totall * 10) * 100

        UserResult.objects.create(
            fullname=fullname,
            totall=totall,
            score=score,
            percent=percent,
            correct=correct,
            wrong=wrong,
        )

        return redirect(reverse('quiz:result_page') + f'?fullname={fullname}')


class Result(View):
    def get(self, request):
        if request.user.is_authenticated:
            try:
                fullname = request.GET['fullname']
                user_object = UserResult.objects.get(fullname=fullname)
                return render(request, 'quiz_app/result.html', {'user': user_object})
            except:
                return redirect('quiz:quiz_page')
        else:
            return redirect('account:login_page')


def send_email(request):
    if request.user.is_authenticated and request.method == 'GET':
        if UserResult.objects.filter(fullname=request.user.username).exists():
            name = request.user.username
            user_result = UserResult.objects.get(fullname=name)

            send_email_result.delay(
                name=user_result.fullname,
                total=user_result.totall,
                score=user_result.score,
                percent=user_result.percent,
                correct=user_result.correct,
                wrong=user_result.wrong,
                created_at=user_result.created_at,
                email=request.user.email,
            )
            return redirect('quiz:result_page')
        else:
            return redirect('quiz:quiz_page')
    else:
        return redirect('account:login_page')


# ----------------- API VIEWS--------------------


class QuestionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        questions_list = Question.objects.filter(status=True)
        if len(questions_list) == 0:
            return Response('No Data', status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = QuestionsSerializer(instance=questions_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionAddView(APIView):
    permission_classes = [IsAuthenticated, IsStaff]

    def post(self, request):
        serializer = QuestionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"response": "data saved successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsStaff]

    def post(self, request, pk):
        instance = Question.objects.get(id=pk)
        serializer = QuestionsSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(instance=instance, validated_data=serializer.validated_data)
            return Response({"response": "Updated"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsStaff]

    def delete(self, request, pk):
        instance = Question.objects.get(id=pk)
        instance.delete()
        return Response({"response": "question deleted"}, status=status.HTTP_200_OK)


class ResultView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            instance = UserResult.objects.get(fullname=request.user)
        except:
            return Response({'Error': 'There is no result'}, status=status.HTTP_204_NO_CONTENT)
        serializer = ResultSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
