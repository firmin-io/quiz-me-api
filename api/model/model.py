import logging

from api.common import errors


class Model:

    def __init__(self):
        pass

    def to_dict(self):
        pass

    def to_dynamo_dict(self):
        pass

    @classmethod
    def from_request(cls, json):
        pass

    @classmethod
    def from_update_request(cls, json):
        pass

    @classmethod
    def from_dynamo(cls, json):
        pass


class LoginRequestModel(Model):

    def __init__(self, email, password):
        Model.__init__(self)
        self.email = email
        self.password = password

    @classmethod
    def from_request(cls, json):
        try:
            return LoginRequestModel(json['email'], json['password'])
        except KeyError as e:
            raise_bad_request_error(e)

    @classmethod
    def from_dynamo(cls, json):
        pass


class FlashcardDeckModel(Model):

    def __init__(self, name, description, _id=None, flashcards=None, user_id=None):
        Model.__init__(self)
        self.id = _id
        self.user_id = user_id
        self.name = name
        self.description = description
        self.flashcards = flashcards

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'flashcards': [flashcard.to_dict() for flashcard in self.flashcards if self.flashcards]
        }

    @classmethod
    def from_update_request(cls, json):
        try:
            desc = json['description']
            logging.debug('desc update ***')
            logging.debug(json)
            logging.debug(desc)
            return FlashcardDeckModel(
                _id=json['id'],
                name=json['name'],
                description=str(desc)
            )
        except KeyError as e:
            raise_bad_request_error(e)

    @classmethod
    def from_request(cls, json):
        try:
            return FlashcardDeckModel(
                user_id=json['user_id'],
                name=json['name'],
                description=json['description']
            )
        except KeyError as e:
            raise_bad_request_error(e)

    @classmethod
    def from_dynamo(cls, json):
        return FlashcardDeckModel(
            _id=json['id'],
            user_id=json['user_id'],
            name=json['name'],
            description=json['description']
        )

    def to_dynamo_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description
        }


class FlashcardModel(Model):

    def __init__(self, question, answer, _id=None, flashcard_deck_id=None):
        Model.__init__(self)
        self.id = _id
        self.flashcard_deck_id = flashcard_deck_id
        self.question = question
        self.answer = answer

    def to_dynamo_dict(self):
        return self.to_dict()

    def to_dict(self):
        return {
            'id': self.id,
            'flashcard_deck_id': self.flashcard_deck_id,
            'question': self.question,
            'answer': self.answer
        }

    @classmethod
    def from_update_request(cls, json):
        try:
            return FlashcardModel(
                _id=json['id'],
                question=json['question'],
                answer=json['answer']
            )
        except KeyError as e:
            raise_bad_request_error(e)

    @classmethod
    def from_request(cls, json):
        try:
            return FlashcardModel(
                flashcard_deck_id=json['flashcard_deck_id'],
                question=json['question'],
                answer=json['answer']
            )
        except KeyError as e:
            raise_bad_request_error(e)

    @classmethod
    def from_dynamo(cls, json):
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

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password': self.password
        }

    def to_dynamo_dict(self):
        return self.to_dict()

    @classmethod
    def from_request(cls, json):
        print('building model')
        print(json)
        try:
            return UserModel(
                email=json['email'],
                first_name=json['first_name'],
                last_name=json['last_name'],
                password=json['password']
            )
        except KeyError as e:
            print('key error {}'.format(str(e)))
            raise_bad_request_error(e)

    @classmethod
    def from_dynamo(cls, json):
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


class AnswerModel(Model):

    def __init__(self, value, is_correct=False):
        Model.__init__(self)
        self.value = value
        self.is_correct = is_correct

    def to_dict(self):
        return {
            'value': self.value,
            'is_correct': self.is_correct
        }

    def to_dynamo_dict(self):
        return self.to_dict()

    @classmethod
    def from_request(cls, json):
        try:
            return AnswerModel(
                value=json['value'],
                is_correct=json['is_correct']
            )
        except KeyError as e:
            raise_bad_request_error(e)

    @classmethod
    def from_dynamo(cls, json):
        try:
            return AnswerModel(
                value=json['value'],
                is_correct=json['is_correct']
            )
        except KeyError as e:
            raise_dynamo_error(e)


class QuestionModel(Model):

    def __init__(self, question_type, question, answers, _id=None, quiz_id=None):
        Model.__init__(self)
        self.id = _id
        self.quiz_id = quiz_id
        self.question_type = question_type
        self.question = question
        self.answers = answers

    def to_dict(self):
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'question_type': self.question_type,
            'question': self.question,
            'answers': [answer.to_dict() for answer in self.answers]
        }

    def to_dynamo_dict(self):
        return self.to_dict()

    @classmethod
    def from_update_request(cls, json):
        try:
            return QuestionModel(
                _id=json['id'],
                question_type=json['question_type'],
                question=json['question'],
                answers=[AnswerModel.from_request(answer) for answer in json['answers']]
            )
        except KeyError as e:
            raise_bad_request_error(e)

    @classmethod
    def from_request(cls, json):
        logging.debug(json)
        try:
            return QuestionModel(
                quiz_id=json['quiz_id'],
                question_type=json['question_type'],
                question=json['question'],
                answers=[AnswerModel.from_request(answer) for answer in json['answers']]
            )
        except KeyError as e:
            raise_bad_request_error(e)

    @classmethod
    def from_dynamo(cls, json):
        print('###', json)
        try:
            return QuestionModel(
                _id=json['id'],
                quiz_id=json['quiz_id'],
                question_type=json['question_type'],
                question=json['question'],
                answers=[AnswerModel.from_dynamo(answer) for answer in json['answers']]
            )
        except KeyError as e:
            raise_dynamo_error(e)


class QuizModel(Model):

    def __init__(self, name, description, _id=None, views=None, questions=None, user_id=None):
        Model.__init__(self)
        self.id = _id
        self.user_id = user_id
        self.name = name
        self.description = description
        self.views = views
        self.questions = questions

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'questions': [question.to_dict() for question in self.questions if self.questions]
        }

    def to_dynamo_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description
        }

    @classmethod
    def from_request(cls, json):
        print(json)
        try:
            return QuizModel(
                user_id=json['user_id'],
                name=json['name'],
                description=json['description']
            )
        except KeyError as e:
            raise_bad_request_error(e)

    @classmethod
    def from_update_request(cls, json):
        try:
            return QuizModel(
                _id=json['id'],
                name=json['name'],
                description=json['description']
            )
        except KeyError as e:
            raise_bad_request_error(e)

    @classmethod
    def from_dynamo(cls, json):
        try:
            return QuizModel(
                _id=json['id'],
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
        errors.Error('MISSING_EXPECTED_ATTRIBUTE', str(e), 422)
    )
