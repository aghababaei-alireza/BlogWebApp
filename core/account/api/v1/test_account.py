import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from captcha.models import CaptchaStore
from captcha.conf import settings as captcha_settings
from account.models import User

from jwt_token.models import Token as JWTTOKEN


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def captcha() -> CaptchaStore:
    challenge, response = captcha_settings.get_challenge()()
    return CaptchaStore.objects.create(challenge=challenge, response=response)


@pytest.fixture
def user() -> User:
    return User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpassword",
        is_verified=True,
    )


@pytest.fixture
def unverified_user() -> User:
    return User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpassword",
        is_verified=False,
    )


@pytest.mark.django_db
class TestAccountAPI:
    # def test_account_signup(self, api_client: APIClient, captcha: CaptchaStore) -> None:
    #     url = reverse("account:api-v1:token-signup")
    #     data = {
    #         "username": "testuser",
    #         "email": "testuser@example.com",
    #         "password": "testpassword",
    #         "password_confirm": "testpassword",
    #         "captcha_code": captcha.response,
    #         "captcha_hashkey": captcha.hashkey,
    #     }
    #     response = api_client.post(url, data)

    #     assert response.status_code == status.HTTP_201_CREATED
    #     assert ["id", "email", "username", "token"] == list(response.data.keys())
    #     assert response.data["email"] == "testuser@example.com"
    #     assert response.data["username"] == "testuser"

    def test_account_login_with_username(self, api_client: APIClient, user: User) -> None:
        url = reverse("account:api-v1:token-login")
        data = {
            "email": "testuser",
            "password": "testpassword",
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert ["id", "email", "username", "token"] == list(response.data.keys())
        assert response.data["email"] == user.email
        assert response.data["username"] == user.username

    def test_account_login_with_email(self, api_client: APIClient, user: User) -> None:
        url = reverse("account:api-v1:token-login")
        data = {
            "email": "testuser@example.com",
            "password": "testpassword",
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert ["id", "email", "username", "token"] == list(response.data.keys())
        assert response.data["email"] == user.email
        assert response.data["username"] == user.username

    def test_account_login_with_invalid_credentials(self, api_client: APIClient) -> None:
        url = reverse("account:api-v1:token-login")
        data = {
            "email": "testuser",
            "password": "wrongpassword",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "non_field_errors" in response.data

    def test_account_logout(self, api_client: APIClient, user: User) -> None:
        api_client.force_authenticate(user=user)
        Token.objects.get_or_create(user=user)
        url = reverse("account:api-v1:token-logout")
        response = api_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "Successfully logged out."
        assert not Token.objects.filter(user=user).exists()

    def test_account_logout_without_authentication(self, api_client: APIClient) -> None:
        url = reverse("account:api-v1:token-logout")
        response = api_client.post(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == "Authentication credentials were not provided."

    def test_account_jwt_create(self, api_client: APIClient, user: User) -> None:
        url = reverse("account:api-v1:jwt-create")
        data = {
            "email": user.email,
            "password": "testpassword",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["access"] is not None

    def test_account_jwt_create_with_invalid_credentials(self, api_client: APIClient, user: User) -> None:
        url = reverse("account:api-v1:jwt-create")
        data = {
            "email": "wrongemail@example.com",
            "password": "wrongpassword",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == "No active account found with the given credentials"

    def test_account_jwt_refresh(self, api_client: APIClient, user: User) -> None:
        url = reverse("account:api-v1:jwt-refresh")
        data = {
            "refresh": str(RefreshToken.for_user(user)),
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert response.data["access"] is not None

    def test_account_jwt_verify(self, api_client: APIClient, user: User) -> None:
        url = reverse("account:api-v1:jwt-verify")
        data = {
            "token": str(RefreshToken.for_user(user).access_token),
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_account_jwt_verify_with_invalid_token(self, api_client: APIClient) -> None:
        url = reverse("account:api-v1:jwt-verify")
        data = {
            "token": "invalidtoken",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == "Token is invalid"
        assert response.data["code"] == "token_not_valid"

    # def test_account_verify_resend(self, api_client: APIClient, unverified_user: User) -> None:
    #     url = reverse("account:api-v1:verify-resend")
    #     data = {
    #         "email": unverified_user.email,
    #     }
    #     response = api_client.post(url, data)

    #     assert response.status_code == status.HTTP_200_OK
    #     assert response.data["detail"] == "Verification email sent."

    def test_account_verify_resend_with_verified_user(self, api_client: APIClient, user: User) -> None:
        url = reverse("account:api-v1:verify-resend")
        data = {
            "email": user.email,
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        print(response.data)
        assert response.data["detail"] == "User is already verified."

    def test_account_verify_confirm(self, api_client: APIClient, unverified_user: User) -> None:
        url = reverse("account:api-v1:verify-confirm", kwargs={"token": JWTTOKEN.make_token(unverified_user)})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "User verified successfully."
        assert User.objects.get(id=unverified_user.id).is_verified is True

    def test_account_verify_confirm_with_invalid_token(self, api_client: APIClient) -> None:
        url = reverse("account:api-v1:verify-confirm", kwargs={"token": "invalidtoken"})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_account_get_profile(self, api_client: APIClient, user: User) -> None:
        api_client.force_authenticate(user=user)
        url = reverse("account:api-v1:profile")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == user.id
        assert response.data["email"] == user.email
        assert response.data["username"] == user.username
        if user.image:
            assert response.data["image"] == user.image.url
        else:
            assert response.data["image"] is None
        assert response.data["is_verified"] == user.is_verified
        assert response.data["is_active"] == user.is_active

    def test_account_get_profile_without_authentication(self, api_client: APIClient) -> None:
        url = reverse("account:api-v1:profile")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == "Authentication credentials were not provided."

    def test_account_update_profile(self, api_client: APIClient, user: User) -> None:
        api_client.force_authenticate(user=user)
        url = reverse("account:api-v1:profile")
        data = {
            "username": "updateduser",
        }
        response = api_client.put(url, data)
        user.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == "updateduser"
        assert user.username == "updateduser"

    def test_account_update_profile_without_authentication(self, api_client: APIClient) -> None:
        url = reverse("account:api-v1:profile")
        data = {
            "username": "updateduser",
        }
        response = api_client.put(url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == "Authentication credentials were not provided."

    def test_account_update_profile_with_unverified_user(self, api_client: APIClient, unverified_user: User) -> None:
        api_client.force_authenticate(user=unverified_user)
        url = reverse("account:api-v1:profile")
        data = {
            "username": "updateduser",
        }
        response = api_client.put(url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_account_password_change(self, api_client: APIClient, user: User) -> None:
        api_client.force_authenticate(user=user)
        url = reverse("account:api-v1:password-change")
        data = {
            "old_password": "testpassword",
            "new_password": "pass123word*@",
            "new_password_confirm": "pass123word*@",
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "Password changed successfully."
        user.refresh_from_db()
        assert user.check_password("pass123word*@")

    def test_account_password_change_with_invalid_old_password(self, api_client: APIClient, user: User) -> None:
        api_client.force_authenticate(user=user)
        url = reverse("account:api-v1:password-change")
        data = {
            "old_password": "wrongpassword",
            "new_password": "pass123word*@",
            "new_password_confirm": "pass123word*@",
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_account_password_change_with_mismatched_new_passwords(self, api_client: APIClient, user: User) -> None:
        api_client.force_authenticate(user=user)
        url = reverse("account:api-v1:password-change")
        data = {
            "old_password": "testpassword",
            "new_password": "pass123word*@",
            "new_password_confirm": "differentpassword",
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["new_password"] == ["New password and confirmation do not match."]

    def test_account_password_change_unverified_user(self, api_client: APIClient, unverified_user: User) -> None:
        api_client.force_authenticate(user=unverified_user)
        url = reverse("account:api-v1:password-change")
        data = {
            "old_password": "testpassword",
            "new_password": "pass123word*@",
            "new_password_confirm": "pass123word*@",
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    # def test_account_password_reset(self, api_client: APIClient, user: User):
    #     url = reverse("account:api-v1:password-reset")
    #     data = {
    #         "email": user.email,
    #     }
    #     response = api_client.post(url, data)

    #     assert response.status_code == status.HTTP_200_OK
    #     assert response.data["detail"] == "Password reset email sent."

    def test_account_password_reset_with_wrong_email(self, api_client: APIClient):
        url = reverse("account:api-v1:password-reset")
        data = {
            "email": "testuser@example.com",
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "Password reset email sent."

    def test_account_password_reset_unverified_user(self, api_client: APIClient, unverified_user: User):
        url = reverse("account:api-v1:password-reset")
        data = {
            "email": unverified_user.email,
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_account_password_reset_confirm(self, api_client: APIClient, user: User):
        token = JWTTOKEN.make_token(user)
        url = reverse("account:api-v1:password-reset-confirm", kwargs={"token": token})
        data = {
            "new_password": "newpassword123",
            "new_password_confirm": "newpassword123",
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "Password reset successfully."
        user.refresh_from_db()
        assert user.check_password("newpassword123") is True

    def test_account_password_reset_confirm_invalid_token(self, api_client: APIClient, user: User):
        url = reverse("account:api-v1:password-reset-confirm", kwargs={"token": "token"})
        data = {
            "new_password": "newpassword123",
            "new_password_confirm": "newpassword123",
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
