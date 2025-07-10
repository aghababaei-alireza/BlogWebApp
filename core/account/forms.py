from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django_recaptcha.fields import ReCaptchaField, ReCaptchaV2Checkbox
from django.core.files.base import ContentFile
from django.conf import settings
import base64
from account.models import User


class CaptchaForm(forms.Form):
    """
    Base form to add reCAPTCHA to the forms.
    """

    if settings.USE_CAPTCHA:
        captcha = ReCaptchaField(required=True, widget=ReCaptchaV2Checkbox)

    def clean(self):
        cleaned_data = super().clean()
        if settings.USE_CAPTCHA:
            captcha = cleaned_data.get("captcha", None)

            if captcha is None:
                raise forms.ValidationError(
                    ReCaptchaField.default_error_messages["captcha_invalid"],
                    code="captcha_invalid",
                )
        return cleaned_data


class CustomSignupForm(CaptchaForm, forms.Form):
    """
    Custom form for user signup that includes email, password, username, and profile image.
    This form validates the uniqueness of email and username, checks password confirmation,
    and allows for an optional profile image upload.
    """

    email = forms.EmailField(label="Email", required=True)
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", required=True, widget=forms.PasswordInput)
    username = forms.CharField(label="Username", required=True)

    def clean(self):
        """
        Custom clean method to validate the form data.
        """
        cleaned_data = super().clean()
        # cleaned_data = super(forms.Form, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        username = cleaned_data.get("username")
        # if settings.USE_CAPTCHA:
        #     captcha = cleaned_data.get("captcha", None)

        #     if captcha is None:
        #         raise forms.ValidationError(
        #             ReCaptchaField.default_error_messages["captcha_invalid"],
        #             code="captcha_invalid",
        #         )
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already in use.")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        validate_password(password)

        return cleaned_data

    def save(self, commit=True):
        """
        Save the user instance created from the form data.
        """

        email = self.cleaned_data["email"]
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]

        user = User(email=email, username=username)
        user.set_password(password)
        if commit:
            user.save()
        return user


class CustomLoginForm(CaptchaForm, forms.Form):
    email = forms.CharField(label="Email or Username", required=True)
    password = forms.CharField(label="Password", required=True)
    # if settings.USE_CAPTCHA:
    #     captcha = ReCaptchaField(required=True, widget=ReCaptchaV2Checkbox)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(forms.Form, self).__init__(*args, **kwargs)

    def clean(self):
        self.cleaned_data = super().clean()
        # self.cleaned_data = super(forms.Form, self).clean()

        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        # captcha = self.cleaned_data.get("captcha", None)

        # if settings.USE_CAPTCHA and captcha is None:
        #     raise forms.ValidationError(
        #         ReCaptchaField.default_error_messages["captcha_invalid"],
        #         code="captcha_invalid",
        #     )
        if not email or not password:
            raise forms.ValidationError("Please enter a correct email and password. Note that both fields may be case-sensitive.")

        self.user_cache = authenticate(self.request, email=email, password=password)

        if self.user_cache is None:
            raise forms.ValidationError("Please enter a correct email and password. Note that both fields may be case-sensitive.")

        if not self.user_cache.is_active:
            raise forms.ValidationError("This account is inactive.")
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class CustomPasswordChangeForm(PasswordChangeForm):
    if settings.USE_CAPTCHA:
        captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, required=True)

    def clean(self):
        self.cleaned_data = super().clean()
        if settings.USE_CAPTCHA:
            captcha = self.cleaned_data.get("captcha", None)
            if captcha is None:
                raise forms.ValidationError(
                    ReCaptchaField.default_error_messages["captcha_invalid"],
                    code="captcha_invalid",
                )
        return self.cleaned_data


class CustomPasswordResetForm(SetPasswordForm):
    if settings.USE_CAPTCHA:
        captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(None, *args, **kwargs)

    def clean(self):
        self.cleaned_data = super().clean()
        if settings.USE_CAPTCHA:
            captcha = self.cleaned_data.get("captcha", None)
            if captcha is None:
                raise forms.ValidationError(
                    ReCaptchaField.default_error_messages["captcha_invalid"],
                    code="captcha_invalid",
                )
        return self.cleaned_data


class UserInfoForm(forms.ModelForm):
    cropped_image_data = forms.CharField(widget=forms.HiddenInput(), required=False)
    delete_image = forms.BooleanField(required=False, label="Remove current profile image")

    class Meta:
        model = User
        fields = ["email", "username"]
        readonly_fields = ["email"]

    def save(self, commit=True):
        instance: User = super().save(commit=False)

        # Handle deleting the current image
        if self.cleaned_data.get("delete_image") and instance.image:
            instance.image.delete(save=False)
            instance.image = None

        cropped_data = self.cleaned_data.get("cropped_image_data")
        if cropped_data:
            try:
                format, imgstr = cropped_data.split(";base64,")
                ext = format.split("/")[-1]
                image_file = ContentFile(base64.b64decode(imgstr), name=f"user_{instance.pk}.{ext}")
                instance.image = image_file
            except ValueError:
                pass

        if commit:
            instance.save()

        return instance
