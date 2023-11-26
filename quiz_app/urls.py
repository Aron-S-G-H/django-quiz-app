from rest_framework.authtoken import views
from django.urls import path
from.views import Quiz, Result, send_email, QuestionListView, QuestionAddView, QuestionUpdateView, QuestionDeleteView, ResultView

app_name = 'quiz'
urlpatterns = [
    path('', Quiz.as_view(), name='quiz_page'),
    path('result', Result.as_view(), name='result_page'),
    path('receive-result', send_email, name='send_email'),
    path('api/authentication', views.obtain_auth_token, name='Api_Auth'),
    path('api/questions', QuestionListView.as_view(), name='questionList_api'),
    path('api/question/add', QuestionAddView.as_view(), name='QuestionAdd_api'),
    path('api/question/update/<int:pk>', QuestionUpdateView.as_view(), name='QuestionUpdate_api'),
    path('api/question/delete/<int:pk>', QuestionDeleteView.as_view(), name='QuestionDelete_api'),
    path('api/userresult', ResultView.as_view(), name='UserResult_api')
]
