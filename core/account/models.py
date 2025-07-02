from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserManager(BaseUserManager):
    """
    Custom manager for the User model that handles user creation and superuser creation.
    """

    def create_user(self, email, username, password=None, **extra_fields):
        """
        Creates and returns a user with an email, username, and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")

        email = self.normalize_email(email)
        user: User = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Creates and returns a superuser with an email, username, and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)

    def get_by_natural_key(self, username):
        try:
            user = self.get(**{"username": username})
        except User.DoesNotExist:
            user = super().get_by_natural_key(username)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that uses email as the unique identifier.
    This model extends Django's AbstractBaseUser and PermissionsMixin to provide
    authentication and permission functionalities.
    """

    email = models.EmailField(unique=True, verbose_name="Email Address")
    username = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Username",
        help_text="Username must be unique and is used to show to other users.",
    )
    image = models.ImageField(
        upload_to="users", null=True, blank=True, verbose_name="Profile Image"
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    is_staff = models.BooleanField(default=False, verbose_name="Is Staff")
    is_verified = models.BooleanField(default=False, verbose_name="Is Verified")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Date Joined")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email
