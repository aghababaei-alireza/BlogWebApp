import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from comment.models import Comment
from account.models import User
from blog.models import Post


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
        username="unverifiedtestuser",
        email="unverifiedtestuser@example.com",
        password="testpassword",
        is_verified=False,
    )


@pytest.fixture
def post(user: User) -> Post:
    return Post.objects.create(title="Test Post", content="This is a test post.", author=user)


@pytest.fixture
def comment(user: User, post: Post) -> Comment:
    return Comment.objects.create(content="This is a test comment.", author=user, post=post)


@pytest.mark.django_db
class TestCommentAPI:
    def test_create_comment_unauthenticated(self, api_client: APIClient, post: Post) -> None:
        url = reverse("post:api-v1:post-comments-list", kwargs={"post_pk": post.id})
        data = {
            "content": "New comment",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_comment_authenticated(self, api_client: APIClient, user: User, post: Post) -> None:
        api_client.force_authenticate(user=user)
        url = reverse("post:api-v1:post-comments-list", kwargs={"post_pk": post.id})
        data = {
            "content": "New comment",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["content"] == "New comment"

    def test_create_comment_unverified_user(self, api_client: APIClient, unverified_user: User, post: Post) -> None:
        api_client.force_authenticate(user=unverified_user)
        url = reverse("post:api-v1:post-comments-list", kwargs={"post_pk": post.id})
        data = {
            "content": "New comment",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_comments_unauthenticated(self, api_client: APIClient, comment: Comment) -> None:
        url = reverse("post:api-v1:post-comments-list", kwargs={"post_pk": comment.post.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data and isinstance(response.data["results"], list)

    def test_list_comments_authenticated(self, api_client: APIClient, user: User, comment: Comment) -> None:
        api_client.force_authenticate(user=user)
        url = reverse("post:api-v1:post-comments-list", kwargs={"post_pk": comment.post.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_comments_unverified_user(
        self, api_client: APIClient, unverified_user: User, comment: Comment
    ) -> None:
        api_client.force_authenticate(user=unverified_user)
        url = reverse("post:api-v1:post-comments-list", kwargs={"post_pk": comment.post.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_update_comment_unauthenticated(self, api_client: APIClient, comment: Comment) -> None:
        url = reverse("comment:api-v1:comments-detail", args=[comment.id])
        data = {
            "content": "Updated content",
        }
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_comment_authenticated(self, api_client: APIClient, user: User, comment: Comment) -> None:
        api_client.force_authenticate(user=user)
        url = reverse("comment:api-v1:comments-detail", args=[comment.id])
        data = {
            "content": "Updated content",
        }
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["content"] == "Updated content"

    def test_update_comment_unverified_user(
        self, api_client: APIClient, unverified_user: User, comment: Comment
    ) -> None:
        api_client.force_authenticate(user=unverified_user)
        url = reverse("comment:api-v1:comments-detail", args=[comment.id])
        data = {"content": "Updated content"}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_comment_unauthenticated(self, api_client: APIClient, comment: Comment) -> None:
        url = reverse("comment:api-v1:comments-detail", args=[comment.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_comment_authenticated(self, api_client: APIClient, user: User, comment: Comment) -> None:
        api_client.force_authenticate(user=user)
        url = reverse("comment:api-v1:comments-detail", args=[comment.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Comment.objects.filter(id=comment.id).exists()

    def test_delete_comment_unverified_user(
        self, api_client: APIClient, unverified_user: User, comment: Comment
    ) -> None:
        api_client.force_authenticate(user=unverified_user)
        url = reverse("comment:api-v1:comments-detail", args=[comment.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
