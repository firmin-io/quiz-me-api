from flask import Flask
from flask_restful import Api

from app.main.api.login_resource import LoginResource
from app.main.api.quiz_resource import UserQuizzesResource, QuizzesResource
from app.main.api.register_resource import RegisterResource

app = Flask(__name__)
api = Api(app)

def endpoint(path):
    return 'v1/qm{}'.format(path)


api.add_resource(LoginResource, endpoint('/login'))
api.add_resource(RegisterResource, endpoint('/register'))
api.add_resource(UserQuizzesResource, endpoint('/users/<string:user_id>/quizzes'))
api.add_resource(QuizzesResource, endpoint('/quizzes'))


if __name__ == '__main__':
    app.run(debug=True)
