from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
import uuid
from django.utils.text import slugify
from account.models import User


class MessageSerializer(serializers.Serializer):
    detail = serializers.CharField()


class UserWithTokenSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "username", "token"]

    def get_token(self, obj):
        return Token.objects.get_or_create(user=obj)[0].key


class SignupSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True, label="Password Confirmation")

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "password_confirm"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password_confirm"):
            raise serializers.ValidationError(
                {"password": "Password and confirmation do not match."}
            )

        try:
            validate_password(attrs["password"])
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password_confirm", None)
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid email or password.!")

        attrs["user"] = user
        return attrs


class VerificationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return attrs

        if user.is_verified:
            raise serializers.ValidationError("This account is already verified.")

        attrs["user"] = user
        return attrs


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True, label="Old Password")
    new_password = serializers.CharField(write_only=True, required=True, label="New Password")
    new_password_confirm = serializers.CharField(
        write_only=True, required=True, label="Confirm New Password"
    )

    def validate(self, attrs):
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
        new_password_confirm = attrs.get("new_password_confirm")

        if new_password != new_password_confirm:
            raise serializers.ValidationError(
                {"new_password": "New password and confirmation do not match."}
            )

        user: User = self.context["request"].user
        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect.")

        try:
            validate_password(new_password, user=user)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        attrs["user"] = user
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return attrs

        if not user.is_verified:
            raise serializers.ValidationError("User is not verified.")

        attrs["user"] = user
        return attrs


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True, label="New Password")
    new_password_confirm = serializers.CharField(
        write_only=True, required=True, label="Confirm New Password"
    )

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        new_password_confirm = attrs.get("new_password_confirm")

        if new_password != new_password_confirm:
            raise serializers.ValidationError(
                {"new_password": "New password and confirmation do not match."}
            )

        try:
            validate_password(new_password)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "image", "is_verified", "is_active"]
        read_only_fields = ["id", "email", "is_verified", "is_active"]

    def validate(self, attrs):
        if "username" in attrs:
            username = attrs["username"]
            if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({"username": "Username is already in use."})

        # Change the name of the uploaded image if present
        image = attrs.get("image")
        if image:
            ext = image.name.split(".")[-1]
            username = self.instance.username if self.instance else "user"
            new_filename = f"{slugify(username)}-{uuid.uuid4().hex[:8]}.{ext}"
            image.name = new_filename

        return super().validate(attrs)
