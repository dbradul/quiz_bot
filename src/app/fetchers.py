from app.api import ApiClient, BASE_API_URL
from app.models import Test


class BaseApiFetcher:
    entity_name = ''
    model = None

    def __init__(self):
        self.client = self.get_client()

    def get_client(self):
        return ApiClient(BASE_API_URL)

    def get_list_url(self, **kwargs):
        return f'{self.client.base_url}/{self.entity_name}/'

    def get_object_url(self, pk):
        return f'{self.client.base_url}/{self.entity_name}/{pk}'

    def get_list(self):
        url = self.get_list_url()
        return self.client.get(url)

    # @classmethod
    # def get_list(cls):
    #     url = cls.get_list_url()
    #     return cls.get_client().get(url)

    def get_object(self, id):
        url = self.get_object_url(id)
        return self.client.get(url)

    def create_object(self, data, **kwargs):
        url = self.get_list_url()
        return self.client.post(url, data)

    def update_object(self, pk, data, **kwargs):
        url = self.get_object_url(pk)
        return self.client.patch(url, data)


class RelatedApiFetcher(BaseApiFetcher):
    parent_entity_name = ''
    entity_name = ''

    def get_list_url(self, **kwargs):
        parent_id = kwargs.get('parent_id')
        return f'{self.client.base_url}/{self.parent_entity_name}/{parent_id}/{self.entity_name}/'

    def create_object(self, data, **kwargs):
        parent_id = kwargs.get('parent_id')
        url = self.get_list_url(parent_id=parent_id)
        return self.client.post(url, data)


class TestFetcher(BaseApiFetcher):
    entity_name = 'tests'
    model = Test


class TestResultFetcher(RelatedApiFetcher):
    parent_entity_name = 'tests'
    entity_name = 'results'


class QuestionFetcher(BaseApiFetcher):
    entity_name = 'questions'


class ChoiceFetcher(BaseApiFetcher):
    entity_name = 'choices'


class UserFetcher(BaseApiFetcher):
    entity_name = 'users'
