from jose import jwt, jwe
from jose.exceptions import JWEError, JWEParseError, JWTError
from django.utils import timezone
from datetime import datetime, timedelta
from django.conf import settings
from account.models import User


class VerifyToken:
    def __init__(self, user: User, encrypted: bool = True):
        now = datetime.now(tz=timezone.get_current_timezone())
        payload = {
            "token_type": "verify",
            "iat": now,
            "exp": now + timedelta(hours=1),
            "user_id": user.id,
        }
        self._token = jwt.encode(
            payload,
            settings.SECRET_KEY[:32],
            algorithm="HS256",
        )
        if encrypted:
            self._token = VerifyToken._encrypt(self._token)

    def get(self) -> str:
        return self._token

    @classmethod
    def _encrypt(cls, token) -> str:
        return jwe.encrypt(
            token,
            settings.SECRET_KEY[:32],
            algorithm="dir",
            encryption="A256GCM",
        ).decode("utf-8")

    @classmethod
    def _decrypt(cls, token: str):
        try:
            dec = jwe.decrypt(token, settings.SECRET_KEY[:32])
        except (JWEError, JWEParseError):
            raise ValueError("Invalid token")
        return dec.decode("utf-8")

    @classmethod
    def validate(cls, token: str) -> User:
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

        exp = payload.get("exp")
        if exp and (datetime.fromtimestamp(exp, tz=timezone.get_current_timezone()) < timezone.now()):
            raise ValueError("Token has expired")

        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValueError("User does not exist")

    @classmethod
    def make_token(cls, user: User):
        return VerifyToken(user).get()
