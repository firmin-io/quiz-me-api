from app.main.common import errors


class Model:

    def __init__(self):
        pass

    def to_json(self, ignore_empty=False):
        pass

    @classmethod
    def from_request_json(cls, json, logger=None):
        pass

    @classmethod
    def from_dynamo_json(cls, json, logger=None):
        pass


class LoginRequestModel(Model):

    def __init__(self, email, password):
        Model.__init__(self)
        self.email = email
        self.password = password

    @classmethod
    def from_request_json(cls, json, logger=None):
        try:
            return LoginRequestModel(json['email'], json['password'])
        except KeyError as e:
            raise_bad_request_error(e)

    @classmethod
    def from_dynamo_json(cls, json, logger=None):
        pass


class FlashcardDeckModel(Model):

    def __init__(self, user_id, name, description, _id=None, flashcards=None):
        Model.__init__(self)
        self._id = _id
        self.user_id = user_id
        self.name = name
        self.description = description,
        self.flashcards = flashcards

    def to_json(self, ignore_empty=False):
        return {
            'id': self._id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'flashcards': self.flashcards
        }

    @classmethod
    def from_request_json(cls, json, logger=None):
        return FlashcardDeckModel(
            user_id=json['user_id'],
            name=json['name'],
            description=json['description']
        )

    @classmethod
    def from_dynamo_json(cls, json, logger=None):
        return FlashcardDeckModel(
            _id=json['id'],
            user_id=json['user_id'],
            name=json['name'],
            description=json['description']
        )


class FlashcardModel(Model):

    def __init__(self, flashcard_deck_id, question, answer, _id):
        Model.__init__(self)
        self.id = _id
        self.flashcard_deck_id = flashcard_deck_id
        self.question = question
        self.answer = answer

    def to_json(self, ignore_empty=False):
        return {
            'id': self.id,
            'flashcard_deck_id': self.flashcard_deck_id,
            'question': self.question,
            'answer': self.answer
        }

    @classmethod
    def from_request_json(cls, json, logger=None):
        try:
            return FlashcardModel(
                flashcard_deck_id=json['flashcard_deck_id'],
                question=json['question'],
                answer=json['answer']
            )
        except KeyError as e:
            raise_bad_request_error(e)

    @classmethod
    def from_dynamo_json(cls, json, logger=None):
        try:
            return FlashcardModel(
                _id=json['id'],
                flashcard_deck_id=json['flashcard_deck_id'],
                question=json['question'],
                answer=json['answer']
            )
        except KeyError as e:
            raise_dynamo_error(e)


class UserModel(Model):

    def __init__(self, email, first_name, last_name, password, _id=None):
        Model.__init__(self)
        self.id = _id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

    def to_json(self, ignore_empty=False):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password': self.password
        }

    @classmethod
    def from_request_json(cls, json, logger=None):
        try:
            return UserModel(
                email=json['email'],
                first_name=json['first_name'],
                last_name=json['last_name'],
                password=json['password']
            )
        except KeyError as e:
            raise_bad_request_error(e)

    @classmethod
    def from_dynamo_json(cls, json, logger=None):
        try:
            return UserModel(
                _id=json['id'],
                email=json['email'],
                first_name=json['first_name'],
                last_name=json['last_name'],
                password=json['password']
            )
        except KeyError as e:
            raise_dynamo_error(e)


class QuestionModel(Model):

    def __init__(self, quiz_id, question_type, questions, answers, _id=None):
        Model.__init__(self)
        self.id = _id
        self.quiz_id = quiz_id
        self.question_type = question_type
        self.questions = questions
        self.answers = answers

    def to_json(self, ignore_empty=False):
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'question_type': self.question_type,
            'questions': self.questions,
            'answers': self.answers
        }

    @classmethod
    def from_request_json(cls, json, logger=None):
        try:
            return QuestionModel(
                quiz_id=json['quiz_id'],
                question_type=json['question_type'],
                questions=json['questions'],
                answers=json['answers']
            )
        except KeyError as e:
            raise_bad_request_error(e)

    @classmethod
    def from_dynamo_json(cls, json, logger=None):
        try:
            return QuestionModel(
                _id=json['id'],
                quiz_id=json['quiz_id'],
                question_type=json['question_type'],
                questions=json['questions'],
                answers=json['answers']
            )
        except KeyError as e:
            raise_dynamo_error(e)


class QuizModel(Model):

    def __init__(self, user_id, name, description, _id=None, views=None, questions=None):
        Model.__init__(self)
        self.id = _id
        self.user_id = user_id
        self.name = name
        self.description = description
        self.views = views
        self.questions = questions

    def to_json(self, ignore_empty=False):
        if ignore_empty:
            return {
                'id': self.id,
                'user_id': self.user_id,
                'name': self.name,
                'description': self.description
            }

        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'views': self.views,
            'questions': self.questions
        }

    @classmethod
    def from_request_json(cls, json, logger=None):
        try:
            return QuizModel(
                user_id=json['user_id'],
                name=json['name'],
                description=json['description']
            )
        except KeyError as e:
            raise_bad_request_error(e)

    @classmethod
    def from_dynamo_json(cls, json, logger=None):
        try:
            return QuizModel(
                _id=json['json'],
                user_id=json['user_id'],
                name=json['name'],
                description=json['description']
            )
        except KeyError as e:
            raise_dynamo_error(e)


def raise_bad_request_error(e):
    raise errors.ApiError(errors.Error('MISSING_REQUIRED_PARAMETER', str(e), 400))


def raise_dynamo_error(e):
    raise errors.ApiError(
        errors.Error('MISSING_EXPECTED_ATTRIBUTE', 'An expected attribute [{}] is missing'.format(str(e)), 422)
    )
