import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from blog.models import Post, Category
from account.models import User


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user() -> User:
    return User.objects.create_user(
        username="testuser", email="testuser@example.com", password="testpassword", is_verified=True
    )


@pytest.fixture
def unverified_user() -> User:
    return User.objects.create_user(
        username="admin", email="admin@example.com", password="adminpassword", is_verified=False
    )


@pytest.fixture
def category() -> Category:
    return Category.objects.create(name="Test Category", color="#FFFFFF")


@pytest.fixture
def post(user: User, category: Category) -> Post:
    return Post.objects.create(
        title="Test Post", content="This is a test post.", author=user, category=category, published=True
    )


@pytest.mark.django_db
class TestPostAPI:
    def test_post_list_unauthenticated(self, api_client: APIClient, post: Post):
        url = reverse("post:api-v1:posts-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data and isinstance(response.data["results"], list)

    def test_post_list_authenticated(self, api_client: APIClient, user: User, post: Post):
        api_client.force_authenticate(user=user)
        url = reverse("post:api-v1:posts-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data and isinstance(response.data["results"], list)

    def test_post_create_unauthenticated(self, api_client: APIClient, category: Category):
        url = reverse("post:api-v1:posts-list")
        data = {
            "title": "New Post",
            "content": "Content",
            "category": category.id,
            "published": True,
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_create_authenticated_verified(self, api_client: APIClient, user: User, category: Category):
        api_client.force_authenticate(user=user)
        url = reverse("post:api-v1:posts-list")
        data = {
            "title": "New Post",
            "content": "Content",
            "category": category.id,
            "published": True,
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "New Post"
        assert response.data["content"] == "Content"
        assert response.data["category"]["id"] == category.id
        assert response.data["author"]["id"] == user.id

    def test_post_create_authenticated_unverified(
        self, api_client: APIClient, unverified_user: User, category: Category
    ):
        api_client.force_authenticate(user=unverified_user)
        url = reverse("post:api-v1:posts-list")
        data = {
            "title": "New Post",
            "content": "Content",
            "category": category.id,
            "published": True,
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_create_invalid_data(self, api_client: APIClient, user: User):
        api_client.force_authenticate(user=user)
        url = reverse("post:api-v1:posts-list")
        data = {
            "title": "",  # Invalid: title required
            "content": "Content",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_update_unauthenticated(self, api_client: APIClient, post: Post, category: Category):
        url = reverse("post:api-v1:posts-detail", args=[post.pk])
        data = {
            "title": "Updated Title",
            "category": category.id,
        }
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_update_authenticated_verified(
        self, api_client: APIClient, user: User, post: Post, category: Category
    ):
        api_client.force_authenticate(user=user)
        url = reverse("post:api-v1:posts-detail", args=[post.pk])
        data = {
            "title": "Updated Title",
            "content": post.content,
            "category": category.id,
            "published": post.published,
        }
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Updated Title"

    def test_post_update_authenticated_unverified(
        self, api_client: APIClient, unverified_user: User, post: Post, category: Category
    ):
        api_client.force_authenticate(user=unverified_user)
        url = reverse("post:api-v1:posts-detail", args=[post.pk])
        data = {
            "title": "Updated Title",
            "content": post.content,
            "category": category.id,
            "published": post.published,
        }
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_update_invalid_data(self, api_client: APIClient, user: User, post: Post):
        api_client.force_authenticate(user=user)
        url = reverse("post:api-v1:posts-detail", args=[post.pk])
        data = {
            "title": "",  # Invalid
            "content": post.content,
        }
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_partial_update_authenticated(self, api_client: APIClient, user: User, post: Post):
        api_client.force_authenticate(user=user)
        url = reverse("post:api-v1:posts-detail", args=[post.pk])
        data = {"title": "Partially Updated"}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Partially Updated"

    def test_post_partial_update_unauthenticated(self, api_client: APIClient, post: Post):
        url = reverse("post:api-v1:posts-detail", args=[post.pk])
        data = {"title": "Partially Updated"}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_delete_unauthenticated(self, api_client: APIClient, post: Post):
        url = reverse("post:api-v1:posts-detail", args=[post.pk])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_delete_authenticated_verified(self, api_client: APIClient, user: User, post: Post):
        api_client.force_authenticate(user=user)
        url = reverse("post:api-v1:posts-detail", args=[post.pk])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Post.objects.filter(pk=post.pk).exists()

    def test_post_delete_authenticated_unverified(self, api_client: APIClient, unverified_user: User, post: Post):
        api_client.force_authenticate(user=unverified_user)
        url = reverse("post:api-v1:posts-detail", args=[post.pk])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
