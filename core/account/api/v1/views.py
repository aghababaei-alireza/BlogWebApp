from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.settings import api_settings
from .serializers import (
    SignupSerializer,
    UserWithTokenSerializer,
    MessageSerializer,
    LoginSerializer,
    VerificationResendSerializer,
    PasswordChangeSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    ProfileSerializer,
)
from .permissions import IsVerified, IsVerifiedOrReadOnly

from jwt_token.models import Token
from account.tasks import send_email


class SignupAPIView(GenericAPIView):
    """
    API view for user signup.
    """

    permission_classes = []

    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST request for user signup.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # Send verification email
        current_site = get_current_site(request)
        domain = current_site.domain
        protocol = "https" if request.is_secure() else "http"
        token = Token.make_token(user)

        send_email.delay(
            email=user.email,
            domain=domain,
            protocol=protocol,
            using_api=True,
            token=token,
            subject="Blogosphere: Email Verification",
            html_template_name="account/email/verification_resend_email.html",
            txt_template_name="account/email/verification_resend_email.txt",
        )

        response_serializer = UserWithTokenSerializer(instance=user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    """
    API view for user login.
    """

    permission_classes = []

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST request for user login.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        response_serializer = UserWithTokenSerializer(instance=user)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    """
    API view for user logout.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST request for user logout.
        """
        request.user.auth_token.delete()
        return Response(
            MessageSerializer({"detail": "Successfully logged out."}).data,
            status=status.HTTP_200_OK,
        )


class VerificationResendAPIView(GenericAPIView):
    """
    API view for resending verification email.
    """

    permission_classes = []
    serializer_class = VerificationResendSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST request for resending verification email.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(
                MessageSerializer({"detail": "User is already verified."}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.validated_data.get("user", None)
        if not user:
            return Response(
                MessageSerializer({"detail": "Verification Email sent."}).data,
                status=status.HTTP_200_OK,
            )
        if not user.is_verified:
            current_site = get_current_site(request)
            domain = current_site.domain
            protocol = "https" if request.is_secure() else "http"
            token = Token.make_token(user)

            send_email.delay(
                email=user.email,
                domain=domain,
                protocol=protocol,
                using_api=True,
                token=token,
                subject="Blogosphere: Email Verification",
                html_template_name="account/email/verification_resend_email.html",
                txt_template_name="account/email/verification_resend_email.txt",
            )
            return Response(
                MessageSerializer({"detail": "Verification email sent."}).data,
                status=status.HTTP_200_OK,
            )
        return Response(
            MessageSerializer({"detail": "User is already verified."}).data,
            status=status.HTTP_400_BAD_REQUEST,
        )


class VerificationConfirmAPIView(APIView):
    """
    API view for confirming user verification.
    """

    permission_classes = []

    def get(self, request, token, *args, **kwargs):
        """
        Handle GET request for confirming user verification.
        """
        try:
            user = Token.validate(token)
            if user.is_verified:
                return Response(
                    MessageSerializer({"detail": "User is already verified."}).data,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.is_verified = True
            user.save()
            return Response(
                MessageSerializer({"detail": "User verified successfully."}).data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                MessageSerializer({"detail": str(e)}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )


class PasswordChangeAPIView(GenericAPIView):
    """
    API view for changing user password.
    """

    permission_classes = [*api_settings.DEFAULT_PERMISSION_CLASSES, IsVerified]
    serializer_class = PasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST request for changing user password.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        new_password = serializer.validated_data["new_password"]
        user.set_password(new_password)
        user.save()
        return Response(
            MessageSerializer({"detail": "Password changed successfully."}).data,
            status=status.HTTP_200_OK,
        )


class PasswordResetAPIView(GenericAPIView):
    """
    API view for resetting user password.
    """

    permission_classes = []
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST request for resetting user password.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user", None)

        if not user:
            return Response(
                MessageSerializer({"detail": "Password reset email sent."}).data,
                status=status.HTTP_200_OK,
            )

        current_site = get_current_site(request)
        domain = current_site.domain
        protocol = "https" if request.is_secure() else "http"
        token = Token.make_token(user)

        send_email.delay(
            email=user.email,
            domain=domain,
            protocol=protocol,
            using_api=True,
            token=token,
            subject="Blogosphere: Email Verification",
            html_template_name="account/email/verification_resend_email.html",
            txt_template_name="account/email/verification_resend_email.txt",
        )

        return Response(
            MessageSerializer({"detail": "Password reset email sent."}).data,
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmAPIView(GenericAPIView):
    """
    API view for confirming password reset.
    """

    permission_classes = []
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, token, *args, **kwargs):
        """
        Handle POST request for confirming password reset.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = Token.validate(token)
        except ValueError as e:
            return Response(
                MessageSerializer({"detail": str(e)}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not user:
            return Response(
                MessageSerializer({"detail": "Invalid token."}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        new_password = serializer.validated_data["new_password"]
        user.set_password(new_password)
        user.save()
        return Response(
            MessageSerializer({"detail": "Password reset successfully."}).data,
            status=status.HTTP_200_OK,
        )


class ProfileAPIView(GenericAPIView):
    """
    API view for retrieving and updating user profile.
    """

    permission_classes = [
        *api_settings.DEFAULT_PERMISSION_CLASSES,
        IsVerifiedOrReadOnly,
    ]
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        """
        Handle GET request to retrieve user profile.
        """
        user = request.user
        serializer = self.get_serializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """
        Handle PUT request to update user profile.
        """
        user = request.user
        serializer = self.get_serializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
