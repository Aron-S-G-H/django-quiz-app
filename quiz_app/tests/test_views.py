from django.test import TestCase, Client
from django.contrib.auth.models import User
from quiz_app.models import Question, UserResult
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker


class TestQuizView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='root', email='root@example.com', password='root1234')

    def test_quiz_GET_notAuthenticated(self):
        response = self.client.get(reverse('quiz:quiz_page'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account:login_page'))

    def test_quiz_GET_authenticated(self):
        self.client.login(username='root', email='root@example.com', password='root1234')
        response = self.client.get(reverse('quiz:quiz_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertTrue(response.context['flag'])

    def test_quiz_POST_correct_answer(self):
        self.client.login(username='root', email='root@example.com', password='root1234')
        question1 = Question.objects.create(
            question='What is the capital of France?',
            answer='Paris',
            status=True,
        )
        question2 = Question.objects.create(
            question='What is the largest ocean in the world?',
            answer='Pacific Ocean',
            status=True,
        )
        response = self.client.post(reverse('quiz:quiz_page'), data={
            question1.question: question1.answer,
            question2.question: question2.answer,
        })
        user_result = UserResult.objects.get(fullname=self.user.username)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('quiz:result_page') + '?fullname=root')
        self.assertEqual(user_result.score, 20)
        self.assertEqual(user_result.percent, 100)

    def test_quiz_POST_wrong_answer(self):
        self.client.login(username='root', email='root@example.com', password='root1234')
        question1 = Question.objects.create(
            question='What is the capital of France?',
            answer='Paris',
            status=True,
        )
        question2 = Question.objects.create(
            question='What is the largest ocean in the world?',
            answer='Pacific Ocean',
            status=True,
        )
        response = self.client.post(reverse('quiz:quiz_page'), data={
            question1.question: question1.answer,
            question2.question: 'Atlantic Ocean',
        })
        user_result = UserResult.objects.get(fullname=self.user.username)
        self.assertRedirects(response, reverse('quiz:result_page') + '?fullname=root')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user_result.score, 10)
        self.assertEqual(user_result.percent, 50)
        self.assertEqual(user_result.wrong, 1)


class TestResultView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='root', email='root@example.com', password='root1234')

    def test_result_GET_notAuthenticated(self):
        response = self.client.get(reverse('quiz:result_page'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account:login_page'))

    def test_result_GET_authenticated_sendFullname(self):
        self.client.login(username='root', email='root@example.com', password='root1234')
        UserResult.objects.create(fullname=self.user.username, percent=80)
        response = self.client.get(reverse('quiz:result_page'), data={'fullname': self.user.username})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_app/result.html')
        self.assertTrue(response.context['user'])

    def test_result_GET_authenticated_withoutFullname(self):
        self.client.login(username='root', email='root@example.com', password='root1234')
        response = self.client.get(reverse('quiz:result_page'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('quiz:quiz_page'))


class TestSendEmail(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='root', email='root@example.com', password='root1234')

    def test_sendEmail_unAuthenticated(self):
        response = self.client.get(reverse('quiz:send_email'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account:login_page'))

    def test_sendEmail_authenticated_withoutResult(self):
        self.client.login(username='root', email='root@example.com', password='root1234')
        response = self.client.get(reverse('quiz:send_email'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('quiz:quiz_page'))

    def test_sendEmail_authenticated_withResult(self):
        self.client.login(username='root', email='root@example.com', password='root1234')
        UserResult.objects.create(fullname=self.user.username, percent=80)
        response = self.client.get(reverse('quiz:send_email'))
        self.assertTrue(UserResult.objects.filter(fullname=self.user.username).exists())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('quiz:result_page'))


class TestApiResultView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='root2', email='root2@example.com', password='root21234')

    def test_apiResult_GET_unAuthenticated(self):
        response = self.client.get(reverse('quiz:UserResult_api'), data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_apiResult_GET_authenticated_withoutUserResult(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('quiz:UserResult_api'), data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, {'Error': 'There is no result'})

    def test_apiResult_everythingOK(self):
        self.client.force_authenticate(user=self.user)
        UserResult.objects.create(fullname=self.user.username, percent=80)
        response = self.client.get(reverse('quiz:UserResult_api'), data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestApiDeleteQuestion(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='root', email='root@example.com', password='root1234')
        self.question = baker.make(Question)

    def test_delete_question_unAuthenticated(self):
        response = self.client.delete(reverse('quiz:QuestionDelete_api', kwargs={'pk': self.question.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_question_withoutStaffPermission(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('quiz:QuestionDelete_api', kwargs={'pk': self.question.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_question_valid_data(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('quiz:QuestionDelete_api', kwargs={'pk': self.question.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'response': 'question deleted'})


class TestApiAddQuestion(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='root', email='root@example.com', password='root1234')
        self.data = {
            'question': 'language ?',
            'option1': 'python',
            'option2': 'js',
            'option3': 'java',
            'option4': 'rust',
            'answer': 'option1',
        }

    def test_add_question_unAuthenticated(self):
        response = self.client.post(reverse('quiz:QuestionAdd_api'), format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_question_withoutStaffPermission(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('quiz:QuestionAdd_api'), format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_question_valid_data(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('quiz:QuestionAdd_api'), format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'response': 'data saved successfully'})
        self.assertEqual(Question.objects.count(), 1)

    def test_add_question_invalid_data(self):
        self.data['option2'] = ''
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('quiz:QuestionAdd_api'), format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Question.objects.count(), 0)


class TestApiUpdateQuestion(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='root', email='root@example.com', password='root1234')
        self.question = baker.make(Question)
        self.data = {'question': 'why python ?'}

    def test_update_question_unAuthenticated(self):
        response = self.client.post(reverse('quiz:QuestionUpdate_api', kwargs={'pk': self.question.id}), format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_question_withoutStaffPermission(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('quiz:QuestionUpdate_api', kwargs={'pk': self.question.id}), format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_question_valid_data(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('quiz:QuestionUpdate_api', kwargs={'pk': self.question.id}), format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'response': 'Updated'})
        question = Question.objects.get(id=self.question.id)
        self.assertEqual(question.question, self.data['question'])

    def test_update_question_invalid_data(self):
        data = {'question': ''}
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('quiz:QuestionUpdate_api', kwargs={'pk': self.question.id}), format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        question = Question.objects.get(id=self.question.id)
        self.assertTrue(question.question)


class TestApiQuestionList(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='root', email='root@example.com', password='root1234')
        self.client.force_authenticate(user=self.user)

    def test_question_list_unAuthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('quiz:questionList_api'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_questions_list_without_data(self):
        response = self.client.get(reverse('quiz:questionList_api'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, 'No Data')

    def test_question_list_with_data(self):
        Question.objects.create(question='lan?', option1='py', option2='js', option3='c', option4='c++', answer='option1', status=True)
        response = self.client.get(reverse('quiz:questionList_api'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

