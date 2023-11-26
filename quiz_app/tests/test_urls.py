from django.test import SimpleTestCase
from quiz_app import views
from django.urls import reverse, resolve


class TestUrl(SimpleTestCase):
    def test_quiz(self):
        url = reverse('quiz:quiz_page')
        self.assertEqual(resolve(url).func.view_class, views.Quiz)

    def test_result(self):
        url = reverse('quiz:result_page')
        self.assertEqual(resolve(url).func.view_class, views.Result)

    def test_send_email(self):
        url = reverse('quiz:send_email')
        self.assertEqual(resolve(url).func, views.send_email)

    def test_question_list(self):
        url = reverse('quiz:questionList_api')
        self.assertEqual(resolve(url).func.view_class, views.QuestionListView)

    def test_question_add(self):
        url = reverse('quiz:QuestionAdd_api')
        self.assertEqual(resolve(url).func.view_class, views.QuestionAddView)

    def test_question_update(self):
        url = reverse('quiz:QuestionUpdate_api', args=(2,))
        self.assertEqual(resolve(url).func.view_class, views.QuestionUpdateView)

    def test_question_delete(self):
        url = reverse('quiz:QuestionDelete_api', args=(2,))
        self.assertEqual(resolve(url).func.view_class, views.QuestionDeleteView)

    def test_user_result_api(self):
        url = reverse('quiz:UserResult_api')
        self.assertEqual(resolve(url).func.view_class, views.ResultView)

