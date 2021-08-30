from app.api import ApiClient, BASE_API_URL, JWTApiClient
from app.models import Test, TestResult, Question, Choice, User


class BaseApiFetcher:
    client = ApiClient(BASE_API_URL)


class BaseApiModelFetcher(BaseApiFetcher):
    entity_name = ''
    model = None

    def __init__(self, user):
        # TODO: DI client
        type(self).client = JWTApiClient(base_url=BASE_API_URL, jwt_token=user.jwt_token)

    @classmethod
    def get_list_url(cls, **kwargs):
        return f'{cls.client.base_url}/{cls.entity_name}/'

    @classmethod
    def get_object_url(cls, pk):
        return f'{cls.client.base_url}/{cls.entity_name}/{pk}/'

    @classmethod
    def get_list(cls):
        url = cls.get_list_url()
        values = cls.client.get(url)
        return [cls.model(**value) for value in values]

    @classmethod
    def get_object(cls, id):
        url = cls.get_object_url(id)
        value = cls.client.get(url)
        return cls.model(**value)

    @classmethod
    def post_object(cls, obj, **kwargs):
        url = cls.get_list_url(**kwargs)
        value = cls.client.post(url, obj.dict(exclude_unset=True))
        return cls.model(**value)

    @classmethod
    def update_object(cls, obj, **kwargs):
        url = cls.get_object_url(obj.id)
        value = cls.client.patch(url, obj.dict())
        return cls.model(**value)


class RelatedApiModelFetcher(BaseApiModelFetcher):
    parent_entity_name = ''
    entity_name = ''

    @classmethod
    def get_list_url(cls, **kwargs):
        parent_id = kwargs.get('parent_id')
        return f'{cls.client.base_url}/{cls.parent_entity_name}/{parent_id}/{cls.entity_name}/'


class TestModelFetcher(BaseApiModelFetcher):
    entity_name = 'tests'
    model = Test


class TestResultFetcher(RelatedApiModelFetcher):
    parent_entity_name = 'tests'
    entity_name = 'results'
    model = TestResult


class QuestionModelFetcher(BaseApiModelFetcher):
    entity_name = 'questions'
    model = Question


class ChoiceModelFetcher(BaseApiModelFetcher):
    entity_name = 'choices'
    model = Choice


class UserModelFetcher(BaseApiModelFetcher):
    entity_name = 'users'
    model = User
