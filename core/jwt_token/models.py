from django.db import models
from jose import jwt, jwe
from jose.exceptions import JWEError, JWEParseError, JWTError
from django.utils import timezone
from datetime import datetime, timedelta
from django.conf import settings
from account.models import User


class Token(models.Model):
    token = models.CharField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jwt_tokens")
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
    _is_active = models.BooleanField(default=True)

    @classmethod
    def _encrypt(cls, token: str) -> str:
        return jwe.encrypt(
            token,
            settings.SECRET_KEY[:32],
            algorithm="dir",
            encryption="A256GCM",
        ).decode("utf-8")

    @classmethod
    def _decrypt(cls, token: str) -> str:
        try:
            dec = jwe.decrypt(token, settings.SECRET_KEY[:32])
        except (JWEError, JWEParseError):
            raise ValueError("Invalid token")
        return dec.decode("utf-8")

    @classmethod
    def make_token(cls, user: User, encrypted: bool = True):
        now = datetime.now()
        user_id = user.id
        exp = now + timedelta(hours=1)

        payload = {"token_type": "verify", "iat": now, "exp": exp, "user_id": user_id}
        _token = jwt.encode(
            payload,
            settings.SECRET_KEY[:32],
            algorithm="HS256",
        )

        if encrypted:
            _token = cls._encrypt(_token)

        return Token.objects.create(user=user, token=_token, expired_at=exp).get()

    @classmethod
    def validate(cls, token: str, deactivate: bool = True) -> User:
        try:
            obj = Token.objects.get(token=token)
        except Token.DoesNotExist:
            raise ValueError("Invalid Token")

        if not obj.is_active:
            raise ValueError("Invalid Token")

        try:
            if token.startswith("eyJ"):
                token = cls._decrypt(token)
            payload = jwt.decode(
                token,
                settings.SECRET_KEY[:32],
                algorithms=["HS256"],
            )
        except (JWTError, ValueError):
            raise ValueError("Invalid token")

        if payload.get("token_type") != "verify":
            raise ValueError("Invalid token type")

        user_id = payload.get("user_id")
        if not user_id:
            raise ValueError("User ID not found in token")

        if user_id != obj.user.id:
            raise ValueError("Invalid Token")

        exp = payload.get("exp")

        if exp and (datetime.fromtimestamp(exp) < datetime.now()):
            raise ValueError("Token has expired")

        user = obj.user
        if deactivate:
            obj._is_active = False
            obj.save()

        return user

    @property
    def is_active(self):
        if self.expired_at < timezone.now():
            self._is_active = False
            self.save()
        return self._is_active

    def get(self) -> str:
        return self.token

    def __str__(self):
        return self.token
