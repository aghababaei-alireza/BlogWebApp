from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


@shared_task
def send_email(
    email: str,
    domain: str,
    protocol: str,
    using_api: bool,
    token: str,
    subject: str,
    html_template_name: str,
    txt_template_name: str,
):
    """
    Sends an email with the given parameters.
    Args:
        email (str): The recipient's email address.
        domain (str): The domain of the site.
        protocol (str): The protocol to use (http or https).
        using_api (bool): Whether the email is being sent via API.
        token (str): The verification token.
        subject (str): The subject of the email.
        html_template_name (str): The name of the HTML template to render.
        txt_template_name (str): The name of the plain text template to render.
    """
    email_context = {
        "domain": domain,
        "protocol": protocol,
        "using_api": using_api,
        "token": token,
    }
    body_html = render_to_string(html_template_name, email_context)
    body_txt = render_to_string(txt_template_name, email_context)
    email_obj = EmailMultiAlternatives(subject, body_txt, to=[email])
    email_obj.attach_alternative(body_html, "text/html")
    email_obj.send()
