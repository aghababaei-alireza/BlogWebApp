import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from blog.models import Category
from account.models import User


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user() -> User:
    return User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword")


@pytest.fixture
def superuser() -> User:
    return User.objects.create_superuser(username="admin", email="admin@example.com", password="adminpassword")


@pytest.fixture
def category() -> Category:
    return Category.objects.create(name="Test Category", color="#FFFFFF")


@pytest.mark.django_db
class TestCategoryAPI:
    def get_list_url(self):
        return reverse("category:api-v1:categories-list")

    def get_detail_url(self, pk):
        return reverse("category:api-v1:categories-detail", args=[pk])

    # LIST
    def test_list_categories_unauthenticated(self, api_client: APIClient, category: Category):
        response = api_client.get(self.get_list_url())
        print(response.data)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_list_categories_authenticated_user(self, api_client: APIClient, user: User, category: Category):
        api_client.force_authenticate(user=user)
        response = api_client.get(self.get_list_url())
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_list_categories_authenticated_superuser(self, api_client: APIClient, superuser: User, category: Category):
        api_client.force_authenticate(user=superuser)
        response = api_client.get(self.get_list_url())
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    # CREATE
    def test_create_category_unauthenticated(self, api_client: APIClient):
        data = {"name": "New Category", "color": "#123456"}
        response = api_client.post(self.get_list_url(), data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_category_authenticated_user(self, api_client: APIClient, user: User):
        api_client.force_authenticate(user=user)
        data = {"name": "New Category", "color": "#123456"}
        response = api_client.post(self.get_list_url(), data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_category_authenticated_superuser(self, api_client: APIClient, superuser: User):
        api_client.force_authenticate(user=superuser)
        data = {"name": "New Category", "color": "#123456"}
        response = api_client.post(self.get_list_url(), data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "New Category"
        assert response.data["color"] == "#123456"

    # UPDATE
    def test_update_category_unauthenticated(self, api_client: APIClient, category: Category):
        url = self.get_detail_url(category.pk)
        data = {"name": "Updated Category", "color": "#654321"}
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_category_authenticated_user(self, api_client: APIClient, user: User, category: Category):
        api_client.force_authenticate(user=user)
        url = self.get_detail_url(category.pk)
        data = {"name": "Updated Category", "color": "#654321"}
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_category_authenticated_superuser(self, api_client: APIClient, superuser: User, category: Category):
        api_client.force_authenticate(user=superuser)
        url = self.get_detail_url(category.pk)
        data = {"name": "Updated Category", "color": "#654321"}
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated Category"
        assert response.data["color"] == "#654321"

    # DELETE
    def test_delete_category_unauthenticated(self, api_client: APIClient, category: Category):
        url = self.get_detail_url(category.pk)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_category_authenticated_user(self, api_client: APIClient, user: User, category: Category):
        api_client.force_authenticate(user=user)
        url = self.get_detail_url(category.pk)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_category_authenticated_superuser(self, api_client: APIClient, superuser: User, category: Category):
        api_client.force_authenticate(user=superuser)
        url = self.get_detail_url(category.pk)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Category.objects.filter(pk=category.pk).exists()
