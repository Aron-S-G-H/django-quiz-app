# Quiz App
Simple dummy project with Django , Django Rest framework , JS and GraphQ
## Features
- Authentication
  - Login
  - Register
- Questions
  - Each question has four options
  - Each question has 10 seconds to answer
- Quiz result at the end
- Send result to user with email
- Documented API
- Rest API
  - Add user
  - CRUD operations on questions
  - Token authentication
  - Get user result
- GraphQL API
  - Add user
  - JWT authentication
  - CRUD operations on questions
  - Get user result
- Celery & Flower(for monitoring celery)
- Dockerized

## Documentation
- localhost/swagger (Rest API)
- localhost/graphql (GraphQL API)
- localhost:5555 (Celery)

## Usage
```bash
git clone https://github.com/Aron-S-G-H/quizApp.git
pip install -r requirements.txt
python manage.py migrate
python manage.py test # to make sure everything is ok
python manage.py runserver # and see in localhost:8000
# In another terminal, enter the following command to run celery
celery -A QuizApp worker -l info
# again in another terminal, enter the following command to run flower
celery -A QuizApp flower
```
## Run with Docker
make sure that you have docker and docker compose
```bash
git clone https://github.com/Aron-S-G-H/quizApp.git
cd QuizApp (where docker-compose.yaml is)
# open a terminal
docker compose up -d
# now go to the localhost:80
```

---
#### any contributions are welcome
